# CMS Phase-2 Muon HLT

```shell
cmsrel CMSSW_11_1_3
cd CMSSW_11_1_3/src
cmsenv
git cms-init

# L1TkMuon Filter
git cms-addpkg DataFormats/HLTReco
git cms-addpkg HLTrigger/HLTcore
git cms-addpkg HLTrigger/HLTfilters
git remote add khaosmos93 https://github.com/khaosmos93/cmssw.git
git fetch khaosmos93
git cherry-pick c9f4616d164b7689e2f87eb6ffa33f844e41d910
git cherry-pick 4180226821c4e16ca6203efd38c3ca79936e1831

# Bug fix for L1TkMuon
git cms-merge-topic 31342
git cms-checkdeps -a

scram b -j 8
```

## Running L3 Trk Muon reco
cd cfgs\
cmsRun HLT_Phase2D49_IOFromL1TkMuon.py
