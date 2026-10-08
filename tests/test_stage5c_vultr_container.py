"""Container contract negatives and fabricated metadata only; never launch Docker."""
import argparse
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import stage5c_vultr_container as launcher


class ContainerContract(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(launcher.MANIFEST.read_text())
        self.runtime = self.manifest['container_runtime']
        self.command = ['/repo/tools/stage5c_vultr_container.py','internal']

    def created(self):
        env = [k+'=1' for k in launcher.THREAD_ENV]
        env += ['PYTHONPATH=/opt/deps:/repo','PYTHONDONTWRITEBYTECODE=1','PYTHONNOUSERSITE=1',
                'GIT_OPTIONAL_LOCKS=0','GIT_CONFIG_COUNT=1','GIT_CONFIG_KEY_0=safe.directory','GIT_CONFIG_VALUE_0=/repo']
        return {'Image':self.runtime['image_config_digest'],'RestartCount':0,
                'State':{'Status':'created','Running':False},
                'Config':{'User':'0:0','WorkingDir':'/repo','Entrypoint':['/opt/python/bin/python3.12'],
                          'Cmd':self.command,'Env':env},
                'HostConfig':{'NanoCpus':2000000000,'CpusetCpus':'0,1','Memory':6442450944,'MemorySwap':6442450944,
                              'ReadonlyRootfs':True,'Init':True,'CgroupnsMode':'private','NetworkMode':'none',
                              'RestartPolicy':{'Name':'no'},'ShmSize':67108864,'CapDrop':['ALL'],
                              'SecurityOpt':['no-new-privileges'],
                              'Tmpfs':{'/tmp':'rw,nosuid,nodev,noexec,size=268435456,mode=1777'}},
                'Mounts':[{'Type':'bind','Destination':dst,'Source':str(src),'RW':rw}
                          for dst,src,rw in [('/repo',launcher.ROOT,False),('/custody','/fixture-custody',False),('/output','/fixture-output',True)]]}

    def check(self, info):
        launcher.verify_created(info,self.runtime,'/fixture-custody','/fixture-output',self.command)

    def test_inspect_allows_expected_created_container(self):
        self.check(self.created())

    def test_rejects_wrong_image_or_already_started_container(self):
        info=self.created();info['Image']='sha256:other'
        with self.assertRaises(RuntimeError):self.check(info)
        info=self.created();info['State']['Status']='running';info['State']['Running']=True
        with self.assertRaises(RuntimeError):self.check(info)

    def test_rejects_command_and_entrypoint_drift(self):
        for field,value in [('Cmd',['-m','unreviewed']),('Entrypoint',['/bin/bash'])]:
            info=self.created();info['Config'][field]=value
            with self.assertRaises(RuntimeError):self.check(info)

    def test_rejects_cpu_memory_swap_and_lifecycle_drift(self):
        for field,value in [('NanoCpus',1000000000),('Memory',8589934592),('MemorySwap',8589934592),
                            ('CpusetCpus','0'),('ReadonlyRootfs',False),('Init',False),
                            ('CgroupnsMode','host'),('NetworkMode','bridge'),('ShmSize',134217728),
                            ('RestartPolicy',{'Name':'always'}),('CapDrop',[]),('SecurityOpt',[]),
                            ('Tmpfs',{'/tmp':'rw,size=512m'})]:
            with self.subTest(field=field):
                info=self.created();info['HostConfig'][field]=value
                with self.assertRaises(RuntimeError):self.check(info)

    def test_rejects_missing_envs_or_rw_repo_receipt(self):
        for name in launcher.THREAD_ENV:
            info=self.created();info['Config']['Env'].remove(name+'=1')
            with self.assertRaises(RuntimeError):self.check(info)
        for index in range(3):
            info=self.created();info['Mounts'][index]['RW']=not info['Mounts'][index]['RW']
            with self.assertRaises(RuntimeError):self.check(info)

    def test_rejects_extra_mount_and_python_path_drift(self):
        info=self.created();info['Mounts'].append({'Type':'bind','Destination':'/extra','Source':'/fixture-extra','RW':True})
        with self.assertRaises(RuntimeError):self.check(info)
        info=self.created();info['Config']['Env'].remove('PYTHONPATH=/opt/deps:/repo')
        with self.assertRaises(RuntimeError):self.check(info)

    def test_flags_set_six_pins_and_reject_overlap(self):
        flags=launcher.flags(self.runtime,launcher.ROOT,'/fixture-custody','/fixture-output')
        for key in launcher.THREAD_ENV:self.assertIn(key+'=1',flags)
        for args in [(launcher.ROOT,launcher.ROOT/'custody','/fixture-output'),
                     (launcher.ROOT,'/fixture','/fixture/output'),
                     (launcher.ROOT,'/fixture,bad','/fixture-output')]:
            with self.assertRaises(RuntimeError):launcher.flags(self.runtime,*args)

    def test_fabricated_receipt_requires_every_exact_binding(self):
        receipt={'authorization':'DETERMINISTIC-RESOURCE-DEVELOPMENT-ONLY','reviewed_commit':'fixture-commit',
                 'reviewed_tree':'fixture-tree','manifest_sha256':launcher.sha(launcher.MANIFEST),
                 'container_image_config_digest':self.runtime['image_config_digest'],'host_boot_id':'fixture-boot',
                 'host_output_parent':'/fixture-output','output_directory':'/output/campaign'}
        launcher.validate_receipt(receipt,self.manifest,'fixture-commit','fixture-tree','/fixture-output','fixture-boot')
        for key in receipt:
            bad=copy.deepcopy(receipt);bad[key]='wrong'
            with self.assertRaises(RuntimeError):
                launcher.validate_receipt(bad,self.manifest,'fixture-commit','fixture-tree','/fixture-output','fixture-boot')

    def test_plan_never_creates_or_starts_container_or_reads_receipt(self):
        args=argparse.Namespace(mode='plan',expected_commit='fixture-commit',expected_tree='fixture-tree')
        with patch.object(launcher,'reviewed',return_value=self.manifest), \
             patch.object(launcher,'call',return_value=json.dumps([{'Id':self.runtime['image_config_digest'],'Architecture':'amd64'}])) as call, \
             patch.object(launcher,'validate_receipt',side_effect=AssertionError('no receipt validation in plan')):
            launcher.host(args)
        self.assertEqual(len(call.call_args_list),1)
        self.assertEqual(call.call_args.args[0][1:3],['image','inspect'])

    def test_missing_window_blocks_before_evidence_or_container(self):
        with tempfile.TemporaryDirectory() as d:
            evidence=Path(d)/'uncreated'
            args=argparse.Namespace(mode='start',expected_commit='fixture-commit',expected_tree='fixture-tree',
                                   evidence_directory=str(evidence),confirm_uninterrupted_60000_seconds=False)
            with patch.object(launcher,'reviewed',return_value=self.manifest), \
                 patch.object(launcher,'boot',return_value='fixture-boot'), \
                 patch.object(launcher,'call',side_effect=[json.dumps([{'Id':self.runtime['image_config_digest'],'Architecture':'amd64'}]),'']), \
                 patch.object(launcher,'validate_receipt',side_effect=AssertionError('window first')):
                with self.assertRaisesRegex(RuntimeError,'window'):launcher.host(args)
            self.assertFalse(evidence.exists())

    def test_manifest_preserves_existing_jobs_caps_and_34_pins(self):
        candidate=launcher.read(launcher.ROOT/'docs/stage5c_e4_v02_vultr_host_manifest_candidate.json')
        expected={k:v for k,v in candidate.items() if k not in ['host_amendment','state']}
        actual={k:v for k,v in self.manifest.items() if k not in ['container_runtime','state']}
        self.assertEqual(actual,expected)
        self.assertEqual(len(self.manifest['jobs']),139);self.assertEqual(len(self.manifest['input_sha256']),34)
        for path,value in self.runtime['implementation_sha256'].items():self.assertEqual(launcher.sha(launcher.ROOT/path),value)


if __name__=='__main__':
    unittest.main()
