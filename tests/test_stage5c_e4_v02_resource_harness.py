"""Real Linux limits/signals/kill with test-only sleeping/busy stubs; no numeric producer."""
import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap

import pytest
from benchmarks import stage5c_e4_v02_resource_campaign as campaign

pytestmark = pytest.mark.skipif(sys.platform != 'linux', reason='Linux process contract')


def stub_campaign(tmp_path, mode):
    # Entire supervisor runs in a disposable interpreter: never lower pytest's hard limits.
    worker = tmp_path / 'stub_worker.py'
    worker.write_text(textwrap.dedent('''
        import json, os, resource, signal, sys, time
        from benchmarks import stage5c_e4_v02_resource_campaign as c
        mode, cap = sys.argv[1], int(sys.argv[2])
        c.parent_death_guard(os.getppid())
        c.announce_worker_identity()
        c.worker_limits({'cpu_cap': cap})
        assert resource.getrlimit(resource.RLIMIT_CORE) == (0, 0)
        print(json.dumps({'event': 'PHASE-STARTED', 'wall': time.monotonic(),
                          'cpu': time.process_time()}), file=sys.stderr, flush=True)
        if mode == 'cpu':
            while True: pass
        if mode in ('wall', 'plan', 'parent'):
            time.sleep(15)
        if mode == 'alarm':
            signal.signal(signal.SIGALRM, signal.SIG_DFL)
            signal.setitimer(signal.ITIMER_REAL, .03)
            time.sleep(15)
        if mode == 'scope':
            try:
                with c.e4_deadline(.03): time.sleep(15)
            except c.E4WallExpired:
                assert signal.getitimer(signal.ITIMER_REAL) == (0., 0.)
                outcome = 'PRODUCTION-E4-WALL-CENSORED'
            else: raise AssertionError('timer did not expire')
        else:
            time.sleep(.23 if mode == 'admission' else .08)
            outcome = 'FORCED-BUDGET-EXHAUSTED'
        print(json.dumps({'event': 'PHASE-FINISHED'}), file=sys.stderr, flush=True)
        assert 'numpy' not in sys.modules and not any(k.startswith('analysis.') for k in sys.modules)
        print(json.dumps({'outcome': outcome, 'phase_cpu_seconds': .001, 'phase_wall_seconds': .08}))
    '''))
    manifest = json.loads(campaign.MANIFEST.read_text())
    cap = 1 if mode == 'cpu' else 3
    wall = .4 if mode in ('wall', 'admission') else 12 if mode == 'parent' else 4
    manifest.update(supervisor_cpu_soft_cap=1, total_cpu_cap=50,
                    total_wall_cap=.6 if mode == 'admission' else 20,
                    wall_cleanup_margin=.01, wall_startup_margin=.01, poll_cadence_seconds=.01)
    manifest['jobs'] = [dict(id='stub-first', kind='stress', cpu_cap=cap, wall_cap=wall, role='held_out_cell'),
                        dict(id='stub-next', kind='stress', cpu_cap=3, wall_cap=wall, role='held_out_cell')]
    mf, output, receipt = tmp_path/'manifest.json', tmp_path/'output', tmp_path/'stub-receipt.json'
    mf.write_text(json.dumps(manifest)); receipt.write_text('{}')
    script = tmp_path/'supervisor.py'
    script.write_text(textwrap.dedent('''
        import json, pathlib, sys, time
        from benchmarks import stage5c_e4_v02_resource_campaign as c
        mf, output, receipt, worker, mode = sys.argv[1:]
        c.MANIFEST = pathlib.Path(mf)
        c.check_receipt = lambda *a: {'reviewed_commit': 'test-only'}
        c.check_runtime = lambda *a, **k: None
        c.memory_preflight = lambda: {'host_available_bytes': 4*1024**3, 'cgroup_remaining_bytes': 4*1024**3}
        c.methods.method_reference = lambda: {}
        c.methods.verify_reference = lambda *a: None
        real_popen = c.subprocess.Popen
        def launch(command, **kwargs):
            job = json.loads(pathlib.Path(mf).read_text())['jobs'][int(command[-1])]
            return real_popen([sys.executable, worker, mode, str(job['cpu_cap'])], **kwargs)
        c.subprocess.Popen = launch
        if mode == 'parent':
            def busy(seconds):
                end = time.process_time() + .04
                while time.process_time() < end: pass
            c.time.sleep = busy
        c.run_campaign(receipt, output)
        assert 'numpy' not in sys.modules
    '''))
    env = dict(os.environ, PYTHONPATH=str(campaign.ROOT))
    result = subprocess.run([sys.executable, str(script), str(mf), str(output), str(receipt),
                             str(worker), mode], cwd=tmp_path, env=env, capture_output=True, text=True, timeout=25)
    assert result.returncode == 0, result.stderr
    assert not list(tmp_path.glob('core*'))
    return [json.loads(x) for x in (output/'records.jsonl').read_text().splitlines()]


@pytest.mark.parametrize('mode,outcome', [('success','FORCED-BUDGET-EXHAUSTED'),
    ('cpu','CPU-CAP-CENSORED'), ('wall','WALL-CAP-CENSORED'),
    ('scope','PRODUCTION-E4-WALL-CENSORED'), ('alarm','IMPLEMENTATION-ABORT')])
def test_real_limits_scoped_alarm_and_child_kill(tmp_path, mode, outcome):
    records = stub_campaign(tmp_path, mode)
    first = next(r for r in records if r.get('job_id') == 'stub-first' and r.get('outcome') != 'ATTEMPT-STARTED')
    assert first['outcome'] == outcome
    assert first['worker_deadline_source'] == 'per-child'
    if mode in ('cpu', 'wall'):
        assert first['phase_wall_lower_bound_seconds'] > 0
        assert first['phase_cpu_lower_bound_seconds'] >= 0
        assert records[-1]['outcome'] == 'PLAN-COMPLETE'
    elif mode == 'alarm':
        assert records[-1]['outcome'] == 'IMPLEMENTATION-ABORT'
        assert records[-2]['not_run_ids'] == ['stub-next']
    else:
        assert records[-1]['outcome'] == 'PLAN-COMPLETE'


def test_full_next_wall_cap_is_reserved_before_spawning(tmp_path):
    records = stub_campaign(tmp_path, 'admission')
    assert records[-1]['outcome'] == 'PLAN-WALL-BUDGET-INCOMPLETE'
    assert records[-2]['not_run_ids'] == ['stub-next']
    assert not any(r.get('job_id') == 'stub-next' for r in records)
    assert not any(r.get('outcome') == 'IMPLEMENTATION-ABORT' for r in records)


def test_real_supervisor_sigxcpu_reaps_and_preserves_remaining_jobs(tmp_path):
    records = stub_campaign(tmp_path, 'parent')
    assert records[-1]['outcome'] == 'PLAN-PARENT-CPU-INCOMPLETE'
    assert records[-2]['not_run_ids'] == ['stub-next']


def test_monitor_plan_deadline_has_distinct_kill_reason(tmp_path):
    with (tmp_path/'out').open('w') as out, (tmp_path/'err').open('w') as err:
        p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(15)'], stdout=out, stderr=err)
        start = campaign.time.monotonic()
        reason, usage, _ = campaign.monitor_child(p, {}, child_deadline=start+5,
            plan_deadline=start+.1, cadence=.01, child_rss_cap=2**30, aggregate_rss_cap=2**40)
    assert reason == 'PLAN-WALL-BUDGET-INCOMPLETE'
    assert p.returncode == -campaign.signal.SIGKILL
    with pytest.raises(ChildProcessError): os.waitpid(p.pid, os.WNOHANG)


def test_finished_phase_never_acquires_a_censored_lower_bound(tmp_path):
    path = tmp_path/'stderr'
    path.write_text(json.dumps({'event':'PHASE-STARTED','wall':1.,'cpu':.5})+'\n'+
                    json.dumps({'event':'PHASE-FINISHED'})+'\n')
    assert campaign.phase_lower_bounds(path, {'wall':2.,'cpu':1.,'tick':.01}) == {}


def test_proc_samples_require_worker_pid_and_start_identity():
    fields = Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()
    identity = dict(namespace_pid=os.getpid(), proc_pid=int(os.readlink('/proc/self')),
                    start_ticks=int(fields[19]))
    sample = campaign.read_live_sample(os.getpid(), identity)
    assert sample is not None and sample['rss'] > 0
    assert campaign.read_live_sample(os.getpid()+1, identity) is None
    assert campaign.read_live_sample(os.getpid(), dict(identity, start_ticks=-1)) is None
    assert campaign.read_live_sample(os.getpid(), None) is None


def test_worker_kernel_parent_death_guard(tmp_path):
    child = tmp_path/'orphan_stub.py'
    child.write_text("import os,time\nfrom benchmarks import stage5c_e4_v02_resource_campaign as c\n"
                     "c.parent_death_guard(os.getppid())\nc.announce_worker_identity()\ntime.sleep(15)\n")
    parent = tmp_path/'parent.py'
    parent.write_text("import os,subprocess,sys\np=subprocess.Popen([sys.executable,sys.argv[1]],stderr=subprocess.PIPE,text=True)\n"
                      "print(p.stderr.readline(),end='',flush=True)\nos._exit(0)\n")
    env = dict(os.environ, PYTHONPATH=str(campaign.ROOT))
    result = subprocess.run([sys.executable,str(parent),str(child)],env=env,cwd=tmp_path,
                            capture_output=True,text=True,timeout=5)
    assert result.returncode == 0
    identity = json.loads(result.stdout)
    proc = Path(f"/proc/{identity['proc_pid']}/stat")
    # The kernel may leave a zombie for the outer subreaper, but it cannot keep running.
    deadline = campaign.time.monotonic()+2
    while proc.exists():
        fields = proc.read_text().rsplit(')',1)[1].split()
        if fields[0] == 'Z' or int(fields[19]) != identity['start_ticks']: break
        assert campaign.time.monotonic() < deadline
        campaign.time.sleep(.01)
