# CMS Phase-2 Muon HLT

## Running L3 Muon reco (OI + IO) in CMSSW_11_1_4

### Setup
```shell
cmsrel CMSSW_11_1_4
cd CMSSW_11_1_4/src
cmsenv

git cms-init
git cms-merge-topic cms-l1t-offline:l1t-phase2-v3.1.9
git cms-merge-topic trtomei:Phase2-L1T-HLT-Interface
git cms-merge-topic khaosmos93:dev_1114_L2L3FromL1TkMu

git clone https://github.com/khaosmos93/CMSPhase2MuonHLT.git HLTrigger/PhaseII/python/Muon

# for full tracking (temporary)
git clone https://github.com/AdrianoDee/CMS_HLT_Phase2_Tracking.git HLTrigger/PhaseII/CMS_HLT_Phase2_Tracking
mkdir -p HLTrigger/PhaseII/python/Tracking
mv HLTrigger/PhaseII/CMS_HLT_Phase2_Tracking/wfs HLTrigger/PhaseII/python/Tracking

scram b -j 10
```

### Testing
```shell
cd your-working-directory
cp /afs/cern.ch/user/t/tomei/public/L1TObjScaling.db your-working-directory
cp $CMSSW_BASE/src/HLTrigger/PhaseII/python/Muon/example_cfgs/HLT_Phase2_L3MuonFromL1TkMuon.py your-working-directory
cmsRun HLT_Phase2_L3MuonFromL1TkMuon.py
```

### Output L3 muon collections
 - hltPhase2L3Muons (reco::Muon)
 - hltPhase2L3MuonCandidates (reco::RecoChargedCandidate)




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

