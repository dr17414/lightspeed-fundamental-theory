"""Reviewed container path for deterministic resource development only.

plan/preflight do not call the campaign or its receipt gate. start additionally
requires a new external exact-commit/image receipt and an operator window flag.
"""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT/'docs/stage5c_e4_v02_resource_measurement_manifest.json'
THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
              'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True); stream.write('\n')
        stream.flush(); os.fsync(stream.fileno())


def call(command):
    return subprocess.check_output(command, text=True, timeout=60).strip()


def git(*args):
    return call(['git', '-C', str(ROOT), *args])


def boot():
    return Path('/proc/sys/kernel/random/boot_id').read_text().strip()


def reviewed(commit, tree):
    require((ROOT/'.git').is_dir() and not (ROOT/'.git').is_symlink(), 'complete .git directory required')
    require(git('rev-parse', 'HEAD') == commit and git('rev-parse', 'HEAD^{tree}') == tree,
            'reviewed commit/tree mismatch')
    require(not git('status', '--porcelain'), 'clean reviewed checkout required')
    manifest = read(MANIFEST)
    require(manifest['authorization'] == 'NONE', 'manifest must retain authorization NONE')
    runtime = manifest['container_runtime']
    for name, value in {**manifest['input_sha256'], **runtime['implementation_sha256']}.items():
        require(sha(ROOT/name) == value, 'source/input pin mismatch: '+name)
    return manifest


def external(path):
    result = Path(path).resolve()
    require(not result.is_relative_to(ROOT), 'external path required')
    require(',' not in str(result) and '\n' not in str(result), 'unsupported mount path')
    return result


def validate_receipt(receipt, manifest, commit, tree, output_parent, current_boot):
    runtime = manifest['container_runtime']
    expected = {'authorization': 'DETERMINISTIC-RESOURCE-DEVELOPMENT-ONLY',
                'reviewed_commit': commit, 'reviewed_tree': tree,
                'manifest_sha256': sha(MANIFEST),
                'container_image_config_digest': runtime['image_config_digest'],
                'host_boot_id': current_boot, 'host_output_parent': str(Path(output_parent).resolve()),
                'output_directory': runtime['output_directory']}
    require(all(receipt.get(k) == v for k, v in expected.items()), 'new exact receipt mismatch')


def flags(runtime, repo, custody, output):
    repo, custody, output = map(lambda p: Path(p).resolve(), (repo, custody, output))
    require(len({repo, custody, output}) == 3 and not custody.is_relative_to(repo)
            and not output.is_relative_to(repo) and not custody.is_relative_to(output)
            and not output.is_relative_to(custody), 'distinct external custody/output mounts required')
    require(all(',' not in str(p) and '\n' not in str(p) for p in (repo, custody, output)), 'invalid mount path')
    result = ['--cpus', '2', '--cpuset-cpus', '0,1', '--memory', str(runtime['memory_bytes']),
              '--memory-swap', str(runtime['memory_bytes']), '--shm-size', str(runtime['shm_bytes']),
              '--cgroupns', 'private', '--network', 'none', '--read-only', '--restart', 'no',
              '--init', '--user', '0:0', '--stop-timeout', '15', '--cap-drop', 'ALL',
              '--security-opt', 'no-new-privileges', '--workdir', '/repo',
              '--tmpfs', '/tmp:rw,nosuid,nodev,noexec,size='+str(runtime['tmpfs_bytes'])+',mode=1777',
              '--mount', f'type=bind,src={repo},dst=/repo,readonly',
              '--mount', f'type=bind,src={custody},dst=/custody,readonly',
              '--mount', f'type=bind,src={output},dst=/output']
    for name in THREAD_ENV:
        result += ['-e', name+'=1']
    for key, value in {'PYTHONDONTWRITEBYTECODE':'1', 'PYTHONUNBUFFERED':'1',
                       'PYTHONNOUSERSITE':'1', 'PYTHONPATH':'/opt/deps:/repo',
                       'GIT_OPTIONAL_LOCKS':'0', 'GIT_CONFIG_COUNT':'1',
                       'GIT_CONFIG_KEY_0':'safe.directory', 'GIT_CONFIG_VALUE_0':'/repo'}.items():
        result += ['-e', key+'='+value]
    return result


def verify_created(info, runtime, custody, output, command):
    host = info['HostConfig']; state = info['State']
    require(info['Image'] == runtime['image_config_digest'] and info['RestartCount'] == 0,
            'created image/restart mismatch')
    require(state['Status'] == 'created' and not state['Running'], 'container started before inspection')
    require(host['NanoCpus'] == 2000000000 and host['CpusetCpus'] == '0,1', 'created CPU mismatch')
    require(host['Memory'] == host['MemorySwap'] == runtime['memory_bytes'], 'created memory mismatch')
    require(host['ReadonlyRootfs'] and host['Init'] and host['CgroupnsMode'] == 'private'
            and host['NetworkMode'] == 'none' and host['RestartPolicy']['Name'] == 'no', 'created lifecycle mismatch')
    require(host['ShmSize'] == runtime['shm_bytes'] and 'ALL' in host['CapDrop']
            and any(x.startswith('no-new-privileges') for x in host['SecurityOpt']), 'created security/shm mismatch')
    require(host['Tmpfs'] == {'/tmp': 'rw,nosuid,nodev,noexec,size='+str(runtime['tmpfs_bytes'])+',mode=1777'},
            'created tmpfs mismatch')
    config = info['Config']
    require(config['User'] == '0:0' and config['WorkingDir'] == '/repo'
            and config['Entrypoint'] == ['/opt/python/bin/python3.12'] and config['Cmd'] == command,
            'created entrypoint/command mismatch')
    env = dict(x.split('=',1) for x in config['Env'])
    require(all(env.get(k) == '1' for k in THREAD_ENV), 'created thread env mismatch')
    require(env.get('PYTHONPATH') == '/opt/deps:/repo' and env.get('PYTHONDONTWRITEBYTECODE') == '1'
            and env.get('PYTHONNOUSERSITE') == '1' and env.get('GIT_OPTIONAL_LOCKS') == '0'
            and env.get('GIT_CONFIG_COUNT') == '1' and env.get('GIT_CONFIG_KEY_0') == 'safe.directory'
            and env.get('GIT_CONFIG_VALUE_0') == '/repo', 'created Python/Git env mismatch')
    binds = {x['Destination']:x for x in info['Mounts'] if x['Type']=='bind'}
    require(set(binds) == {'/repo','/custody','/output'}, 'unexpected bind mount')
    for destination, source, rw in [('/repo',ROOT,False),('/custody',custody,False),('/output',output,True)]:
        require(binds[destination]['Source'] == str(Path(source).resolve()) and binds[destination]['RW'] == rw,
                'created mount mismatch')


def mount(target):
    for row in Path('/proc/self/mountinfo').read_text().splitlines():
        fields = row.split()
        if fields[4] == target:
            return fields[5].split(','), fields[fields.index('-')+1]
    raise RuntimeError('missing mount: '+target)


def container_preflight(manifest):
    runtime = manifest['container_runtime']; profile = manifest['host']
    require(ROOT == Path('/repo') and sys.version == profile['sys_version'], 'container root/Python mismatch')
    require(sorted(os.sched_getaffinity(0)) == profile['allowed_affinity'], 'initial CPU affinity mismatch')
    model = next(x.split(':',1)[1].strip() for x in Path('/proc/cpuinfo').read_text().splitlines()
                 if x.startswith('model name'))
    require(model == profile['cpu_model'], 'CPU model mismatch')
    for field, file in [('cgroup_cpu_max','cpu.max'),('cgroup_memory_max','memory.max')]:
        require(Path('/sys/fs/cgroup',file).read_text().strip() == profile[field], 'cgroup limit mismatch')
    require(Path('/sys/fs/cgroup/memory.swap.max').read_text().strip() == '0'
            and len(Path('/proc/swaps').read_text().splitlines()) == 1, 'swap must be off')
    topology = []
    for cpu in (0,1):
        p = Path(f'/sys/devices/system/cpu/cpu{cpu}/topology')
        require((p/'thread_siblings_list').read_text().strip() == '0-1', 'SMT siblings mismatch')
        topology.append(((p/'core_id').read_text().strip(), (p/'physical_package_id').read_text().strip()))
    require(topology[0] == topology[1], 'one shared physical core required')
    require(all(os.environ.get(k) == '1' for k in THREAD_ENV), 'six thread env pins required')
    for target in ['/','/repo','/custody']:
        require('ro' in mount(target)[0], 'read-only mount required: '+target)
    require('rw' in mount('/output')[0], 'writable output mount required')
    options, filesystem = mount('/tmp')
    require(filesystem == 'tmpfs' and {'rw','nosuid','nodev','noexec'} <= set(options), 'tmpfs options mismatch')
    require(os.statvfs('/tmp').f_blocks*os.statvfs('/tmp').f_frsize == runtime['tmpfs_bytes'], 'tmpfs size mismatch')
    require(not Path(runtime['output_directory']).exists(), 'fresh campaign output leaf required')
    os.sched_setaffinity(0,set(profile['supervisor_affinity']))
    import numpy
    import scipy.linalg
    import scipy.optimize
    from threadpoolctl import threadpool_info
    versions = {p:importlib.metadata.version(p) for p in runtime['packages']}
    require(versions == runtime['packages'], 'pinned dependency mismatch')
    pools = threadpool_info()
    require(pools and all(x['num_threads'] == 1 for x in pools), 'single-thread pools required')
    current = int(Path('/sys/fs/cgroup/memory.current').read_text())
    available = int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines()
                         if x.startswith('MemAvailable:')))*1024
    remaining = min(runtime['memory_bytes']-current,available)
    require(remaining >= manifest['minimum_memory_headroom_bytes'], 'at least 3 GiB headroom required')
    return {'versions':versions, 'threadpools':pools, 'minimum_actual_headroom_bytes':remaining,
            'supervisor_affinity':sorted(os.sched_getaffinity(0)),
            'receipt_gate_called':False, 'numeric_producer_called':False}


def internal(args):
    require(sha(MANIFEST) == args.expected_manifest_sha256, 'container manifest mismatch')
    manifest = reviewed(args.expected_commit,args.expected_tree)
    require(boot() == args.expected_boot_id, 'host rebooted between inspection and start')
    result = container_preflight(manifest)
    require(Path('/custody/receipt.json').is_file() and not Path('/custody/receipt.json').is_symlink(),
            'regular external receipt file required')
    receipt = read('/custody/receipt.json')
    if args.operation == 'preflight':
        require(receipt.get('authorization') == 'NONE' and receipt.get('purpose') == 'ENVIRONMENT-PREFLIGHT-ONLY',
                'preflight accepts only dummy receipt')
        print(json.dumps({'event':'CONTAINER-PREFLIGHT-PASS', **result},sort_keys=True),flush=True)
        return
    validate_receipt(receipt,manifest,args.expected_commit,args.expected_tree,args.host_output_parent,boot())
    # The original campaign gate rechecks receipt/checkout; its source remains frozen.
    os.execv(sys.executable,[sys.executable,'-m','benchmarks.stage5c_e4_v02_resource_campaign',
             'run','--authorization','/custody/receipt.json','--output',manifest['container_runtime']['output_directory']])


def host(args):
    manifest = reviewed(args.expected_commit,args.expected_tree); runtime = manifest['container_runtime']
    info = json.loads(call(['docker','image','inspect',runtime['image_config_digest']]))[0]
    require(info['Id'] == runtime['image_config_digest'] and info['Architecture'] == 'amd64', 'frozen image missing')
    if args.mode == 'plan':
        print(json.dumps({'event':'CONTAINER-PLAN','commit':args.expected_commit,'tree':args.expected_tree,
                         'manifest_sha256':sha(MANIFEST),'image_config_digest':info['Id'],
                         'authorization':'NONE','container_created':False},indent=2)); return
    evidence = external(args.evidence_directory)
    require(not evidence.exists(), 'fresh evidence directory required')
    current_boot = boot()
    require(not call(['docker','ps','--filter','name=lightspeed-','--format','{{.ID}}']), 'do not overlap lightspeed containers')
    if args.mode == 'start':
        require(args.confirm_uninterrupted_60000_seconds, 'operator must confirm uninterrupted 60000-second window')
        custody = external(args.receipt_directory); output = external(args.output_parent)
        require(custody.is_dir() and output.is_dir() and not any(output.iterdir()), 'existing custody and fresh empty output parent required')
        require((custody/'receipt.json').is_file() and not (custody/'receipt.json').is_symlink(),
                'regular receipt.json required')
        validate_receipt(read(custody/'receipt.json'),manifest,args.expected_commit,args.expected_tree,output,current_boot)
    else:
        custody = evidence/'dummy-custody'; output = evidence/'dummy-output'
    # Validate source relationships before allocating evidence or creating a container.
    runtime_flags = flags(runtime,ROOT,custody,output)
    require(not evidence.is_relative_to(custody) and not evidence.is_relative_to(output), 'evidence must be outside actual mount dirs')
    evidence.mkdir(parents=True)
    if args.mode == 'preflight':
        custody.mkdir(); output.mkdir()
        save(custody/'receipt.json',{'authorization':'NONE','purpose':'ENVIRONMENT-PREFLIGHT-ONLY',
                                   'output_directory':runtime['output_directory']})
    else:
        save(output/'.resource-attempt-reserved.json',{'commit':args.expected_commit,'manifest_sha256':sha(MANIFEST)})
    name = 'lightspeed-resource-'+uuid.uuid4().hex
    command = ['/repo/tools/stage5c_vultr_container.py','internal','--operation',
               'run' if args.mode == 'start' else 'preflight','--expected-commit',args.expected_commit,
               '--expected-tree',args.expected_tree,'--expected-manifest-sha256',sha(MANIFEST),
               '--expected-boot-id',current_boot,'--host-output-parent',str(output)]
    cid = call(['docker','create','--name',name,*runtime_flags,'--entrypoint','/opt/python/bin/python3.12',
                runtime['image_config_digest'],*command])
    save(evidence/'registration.json',{'container_id':cid,'command':command,'flags':runtime_flags,'operation':args.mode})
    created = json.loads(call(['docker','inspect',cid]))[0]; save(evidence/'created-inspect.json',created)
    verify_created(created,runtime,custody,output,command)
    reviewed(args.expected_commit,args.expected_tree)
    require(current_boot == boot(), 'host rebooted before start')
    call(['docker','start',cid])
    if args.mode == 'start':
        print(json.dumps({'event':'RESOURCE-CONTAINER-STARTED','container_id':cid,
                         'evidence_directory':str(evidence),'output_directory':runtime['output_directory']},indent=2)); return
    deadline = time.monotonic()+180
    while True:
        final = json.loads(call(['docker','inspect',cid]))[0]
        if not final['State']['Running']: break
        if time.monotonic() >= deadline:
            call(['docker','stop','--time','15',cid]); raise RuntimeError('preflight timeout; stopped only this container; retain evidence')
        time.sleep(.25)
    save(evidence/'final-inspect.json',final)
    logs = subprocess.check_output(['docker','logs',cid],stderr=subprocess.STDOUT,text=True,timeout=60)
    with (evidence/'container.log').open('x') as stream: stream.write(logs)
    require(final['State']['ExitCode'] == 0 and not final['State']['OOMKilled'] and final['RestartCount'] == 0,
            'preflight container failed; retained logs/inspect')
    result = json.loads(logs)
    require(result['event'] == 'CONTAINER-PREFLIGHT-PASS' and not result['receipt_gate_called']
            and not result['numeric_producer_called'], 'preflight result mismatch')
    save(evidence/'report.json',result); print(json.dumps(result,indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='mode',required=True)
    for mode in ['plan','preflight','start','internal']:
        s = sub.add_parser(mode)
        s.add_argument('--expected-commit',required=True); s.add_argument('--expected-tree',required=True)
        if mode in ['preflight','start']: s.add_argument('--evidence-directory',required=True)
        if mode == 'start':
            s.add_argument('--receipt-directory',required=True); s.add_argument('--output-parent',required=True)
            s.add_argument('--confirm-uninterrupted-60000-seconds',action='store_true')
        if mode == 'internal':
            s.add_argument('--operation',choices=['preflight','run'],required=True)
            s.add_argument('--expected-manifest-sha256',required=True); s.add_argument('--expected-boot-id',required=True)
            s.add_argument('--host-output-parent',required=True)
    args = p.parse_args()
    internal(args) if args.mode == 'internal' else host(args)


if __name__ == '__main__':
    main()
