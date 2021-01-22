# CMS Phase-2 Muon HLT

## Running L3 Muon reco (OI + IO) in CMSSW_11_1_7

### Setup
```shell
cmsrel CMSSW_11_1_7
cd CMSSW_11_1_7/src
cmsenv

git cms-init
git cms-addpkg HLTrigger/HLTfilters

git clone https://github.com/khaosmos93/CMSPhase2MuonHLT.git HLTrigger/PhaseII/python/Muon

scram b -j 10
```

### Testing
```shell
cd your-working-directory
cp $CMSSW_BASE/src/HLTrigger/PhaseII/python/Muon/example_cfgs/HLT_Phase2_example_menu.py your-working-directory
cmsRun HLT_Phase2_example_menu.py

# N.B. other cfg files in example_cfgs are obsolete
```

### Output L3 muon collections
 - hltPhase2L3Muons (reco::Muon)
 - hltPhase2L3MuonCandidates (reco::RecoChargedCandidate)



## (Outdated) Running L3 Muon reco (OI + IO) in CMSSW_11_1_6
<details><summary> show </summary>
<p>

```shell
cmsrel CMSSW_11_1_6
cd CMSSW_11_1_6/src
cmsenv

git cms-init
git cms-merge-topic -u cms-l1t-offline:l1t-phase2-v3.3.5.2-CMSSW_11_1_6
git cms-merge-topic 32517  # for HGcal isolation
git cms-merge-topic 32474  # Phase2-L1T-HLT
git cms-merge-topic khaosmos93:dev_1116_L2L3FromL1TkMu
git cms-merge-topic khaosmos93:dev_1116_L1TkMuFilters

git clone https://github.com/khaosmos93/CMSPhase2MuonHLT.git HLTrigger/PhaseII/python/Muon

scram b -j 10
```

</p>
</details>


## (Outdated) Running L3 Muon reco (OI + IO) in CMSSW_11_1_4
<details><summary> show </summary>
<p>

```shell
cmsrel CMSSW_11_1_4
cd CMSSW_11_1_4/src
cmsenv

git cms-init
git cms-merge-topic SohamBhattacharya:CMSSW_11_1_4_TICLv3  # TICLv3
git cms-merge-topic Sam-Harper:HGCalShowerShapes_1113      # 2D layer cluster based HGCal Isolation
git cms-merge-topic cms-l1t-offline:l1t-phase2-v3.1.9
git cms-merge-topic trtomei:Phase2-L1T-HLT-Interface
git cms-merge-topic khaosmos93:dev_1114_L2L3FromL1TkMu
git cms-merge-topic khaosmos93:dev_1114_HgcalLayerClusterIso_tmp

git clone https://github.com/khaosmos93/CMSPhase2MuonHLT.git HLTrigger/PhaseII/python/Muon

scram b -j 10
```

</p>
</details>


## (Outdated) Running L3 Trk Muon reco in CMSSW_11_1_4
<details><summary> show </summary>
<p>

```shell
cmsrel CMSSW_11_1_4
cd CMSSW_11_1_4/src
cmsenv
git cms-init

# L1T-HLT Interface from Thiago Tomei
# https://twiki.cern.ch/twiki/bin/view/CMS/PhaseIIL1THLTInterface
git cms-merge-topic trtomei:Phase2-L1T-HLT-Interface

scram b -j 10

cd your-working-directory
git clone https://github.com/khaosmos93/CMSPhase2MuonHLT.git
cp /afs/cern.ch/user/t/tomei/public/L1TObjScaling.db CMSPhase2MuonHLT/example_cfgs
cd CMSPhase2MuonHLT/example_cfgs
cmsRun HLT_Phase2D49_IOFromL1TkMuon.py
```

</p>
</details>


## (Outdated) Running L3 Trk Muon reco in CMSSW_11_1_3
<details><summary> show </summary>
<p>

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

cd your-working-directory
git clone https://github.com/khaosmos93/CMSPhase2MuonHLT.git
cd CMSPhase2MuonHLT/example_cfgs
cmsRun HLT_Phase2D49_IOFromL1TkMuon_CMSSW_11_1_3.py
```

</p>
</details>

