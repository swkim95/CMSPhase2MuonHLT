
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
process = cms.Process("MYHLT", eras.Phase2C9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


process.maxEvents = cms.untracked.PSet(
    input  = cms.untracked.int32(100),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/relval/CMSSW_11_1_0_pre4_GEANT4/RelValZMM_14/GEN-SIM-DIGI-RAW/110X_mcRun4_realistic_v3_2026D49noPU-v1/10000/FEB6F9C7-9090-5949-9877-4FA2EFD8CDD8.root'),
    secondaryFileNames = cms.untracked.vstring()
)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T15', '')

# -- L1 emulation -- #
doL1Emulation = 1  # 0: no emulation, 1: directly from SimL1Emulator_cff, 2: previous version

if doL1Emulation == 1:
    process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
    process.load('Configuration.StandardSequences.SimL1Emulator_cff')
    process.load('Configuration.StandardSequences.EndOfProcess_cff')
    process.L1TrackTrigger_step = cms.Path(process.L1TrackTrigger)
    process.L1simulation_step = cms.Path(process.SimL1Emulator)
    process.L1TkMuons.L1TrackInputTag = cms.InputTag("TTTracksFromTrackletEmulation", "Level1TTTracks", "RECO")

elif doL1Emulation == 2:
    process.load('Configuration.StandardSequences.SimL1Emulator_cff')
    process.load('Configuration.StandardSequences.EndOfProcess_cff')

    process.load('L1Trigger.TrackTrigger.TrackTrigger_cff')
    from L1Trigger.TrackTrigger.TTStubAlgorithmRegister_cfi import *
    process.load("SimTracker.TrackTriggerAssociation.TrackTriggerAssociator_cff")

    from SimTracker.TrackTriggerAssociation.TTClusterAssociation_cfi import *
    TTClusterAssociatorFromPixelDigis.digiSimLinks = cms.InputTag("simSiPixelDigis","Tracker")

    process.TTClusterStub = cms.Path(process.TrackTriggerClustersStubs)
    process.TTClusterStubTruth = cms.Path(process.TrackTriggerAssociatorClustersStubs)

    # L1TRKALGO == 'HYBRID'
    process.load("L1Trigger.TrackFindingTracklet.Tracklet_cfi")
    L1TRK_PROC  =  process.TTTracksFromTrackletEmulation
    L1TRK_NAME  = "TTTracksFromTrackletEmulation"
    L1TRK_LABEL = "Level1TTTracks"

    process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")  # defined above
    process.load("SimTracker.TrackTriggerAssociation.TrackTriggerAssociator_cff")
    process.TTTrackAssociatorFromPixelDigis.TTTracks = cms.VInputTag( cms.InputTag(L1TRK_NAME, L1TRK_LABEL) )

    process.TTTracksEmulation = cms.Path(process.offlineBeamSpot*L1TRK_PROC)
    process.TTTracksEmulationWithTruth = cms.Path(process.offlineBeamSpot*process.TTTracksFromTrackletEmulation*process.TrackTriggerAssociatorTracks)

    process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
    process.load('CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi')

    process.L1simulation_step = cms.Path(process.SimL1Emulator)
# -- #

# -- Timing -- #
# configure the FastTimerService
process.load( "HLTrigger.Timer.FastTimerService_cfi" )
# print a text summary at the end of the job
process.FastTimerService.printEventSummary         = False
process.FastTimerService.printRunSummary           = False
process.FastTimerService.printJobSummary           = True

# enable DQM plots
process.FastTimerService.enableDQM                 = True

# enable per-path DQM plots (starting with CMSSW 9.2.3-patch2)
process.FastTimerService.enableDQMbyPath           = True

# enable per-module DQM plots
process.FastTimerService.enableDQMbyModule         = True

# enable per-event DQM plots vs lumisection
process.FastTimerService.enableDQMbyLumiSection    = False
process.FastTimerService.dqmLumiSectionsRange      = 2500

# set the time resolution of the DQM plots
process.FastTimerService.dqmTimeRange              = 10000.
process.FastTimerService.dqmTimeResolution         =    10.
process.FastTimerService.dqmPathTimeRange          = 10000.
process.FastTimerService.dqmPathTimeResolution     =     5.
process.FastTimerService.dqmModuleTimeRange        =  5000.
process.FastTimerService.dqmModuleTimeResolution   =     1.

# set the base DQM folder for the plots
process.FastTimerService.dqmPath                   = 'HLT/TimerService'
process.FastTimerService.enableDQMbyProcesses      = False
# -- #

# -- ESProducers -- #
process.hltESPFastSteppingHelixPropagatorAny = cms.ESProducer("SteppingHelixPropagatorESProducer",
    ApplyRadX0Correction = cms.bool(True),
    AssumeNoMaterial = cms.bool(False),
    ComponentName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('anyDirection'),
    SetVBFPointer = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    debug = cms.bool(False),
    endcapShiftInZNeg = cms.double(0.0),
    endcapShiftInZPos = cms.double(0.0),
    returnTangentPlane = cms.bool(True),
    sendLogWarning = cms.bool(False),
    useEndcapShiftsInZ = cms.bool(False),
    useInTeslaFromMagField = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    useMagVolumes = cms.bool(True),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(True)
)

process.hltESPFastSteppingHelixPropagatorOpposite = cms.ESProducer("SteppingHelixPropagatorESProducer",
    ApplyRadX0Correction = cms.bool(True),
    AssumeNoMaterial = cms.bool(False),
    ComponentName = cms.string('hltESPFastSteppingHelixPropagatorOpposite'),
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('oppositeToMomentum'),
    SetVBFPointer = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    debug = cms.bool(False),
    endcapShiftInZNeg = cms.double(0.0),
    endcapShiftInZPos = cms.double(0.0),
    returnTangentPlane = cms.bool(True),
    sendLogWarning = cms.bool(False),
    useEndcapShiftsInZ = cms.bool(False),
    useInTeslaFromMagField = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    useMagVolumes = cms.bool(True),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(True)
)

process.hltESPMuonTransientTrackingRecHitBuilder = cms.ESProducer("MuonTransientTrackingRecHitBuilderESProducer",
    ComponentName = cms.string('hltESPMuonTransientTrackingRecHitBuilder')
)

process.hltESPKFUpdator = cms.ESProducer("KFUpdatorESProducer",
    ComponentName = cms.string('hltESPKFUpdator')
)

process.hltESPDummyDetLayerGeometry = cms.ESProducer("DetLayerGeometryESProducer",
    ComponentName = cms.string('hltESPDummyDetLayerGeometry')
)

process.hltESPChi2MeasurementEstimator30 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2MeasurementEstimator30'),
    MaxChi2 = cms.double(30.0),
    MaxDisplacement = cms.double(100.0),
    MaxSagitta = cms.double(-1.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(10.0),
    appendToDataLabel = cms.string(''),
    nSigma = cms.double(3.0)
)

process.hltESPKFTrajectorySmootherForMuonTrackLoader = cms.ESProducer("KFTrajectorySmootherESProducer",
    ComponentName = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPSmartPropagatorAnyOpposite'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    errorRescaling = cms.double(10.0),
    minHits = cms.int32(3)
)

process.hltESPSteppingHelixPropagatorOpposite = cms.ESProducer("SteppingHelixPropagatorESProducer",
    ApplyRadX0Correction = cms.bool(True),
    AssumeNoMaterial = cms.bool(False),
    ComponentName = cms.string('hltESPSteppingHelixPropagatorOpposite'),
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('oppositeToMomentum'),
    SetVBFPointer = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    debug = cms.bool(False),
    endcapShiftInZNeg = cms.double(0.0),
    endcapShiftInZPos = cms.double(0.0),
    returnTangentPlane = cms.bool(True),
    sendLogWarning = cms.bool(False),
    useEndcapShiftsInZ = cms.bool(False),
    useInTeslaFromMagField = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    useMagVolumes = cms.bool(True),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False)
)

process.hltESPChi2MeasurementEstimator100 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2MeasurementEstimator100'),
    MaxChi2 = cms.double(40.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1e+12),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    nSigma = cms.double(4.0)
)

process.hltESPChi2ChargeMeasurementEstimator30 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    MaxChi2 = cms.double(30.0),
    MaxDisplacement = cms.double(100.0),
    MaxSagitta = cms.double(-1.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(10.0),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(-1.0)
)

process.hltESPMeasurementTracker = cms.ESProducer("MeasurementTrackerESProducer",
    ComponentName = cms.string('hltESPMeasurementTracker'),
    DebugPixelModuleQualityDB = cms.untracked.bool(False),
    DebugPixelROCQualityDB = cms.untracked.bool(False),
    DebugStripAPVFiberQualityDB = cms.untracked.bool(False),
    DebugStripModuleQualityDB = cms.untracked.bool(False),
    DebugStripStripQualityDB = cms.untracked.bool(False),
    HitMatcher = cms.string('StandardMatcher'),
    MaskBadAPVFibers = cms.bool(True),
    #PixelCPE = cms.string('hltESPPixelCPEGeneric'),
    PixelCPE = cms.string('PixelCPEGeneric'),
    SiStripQualityLabel = cms.string(''),
    StripCPE = cms.string('hltESPStripCPEfromTrackAngle'),
    UsePixelModuleQualityDB = cms.bool(True),
    UsePixelROCQualityDB = cms.bool(True),
    UseStripAPVFiberQualityDB = cms.bool(True),
    UseStripModuleQualityDB = cms.bool(True),
    UseStripStripQualityDB = cms.bool(True),
    badStripCuts = cms.PSet(
        TEC = cms.PSet(
            maxBad = cms.uint32(4),
            maxConsecutiveBad = cms.uint32(2)
        ),
        TIB = cms.PSet(
            maxBad = cms.uint32(4),
            maxConsecutiveBad = cms.uint32(2)
        ),
        TID = cms.PSet(
            maxBad = cms.uint32(4),
            maxConsecutiveBad = cms.uint32(2)
        ),
        TOB = cms.PSet(
            maxBad = cms.uint32(4),
            maxConsecutiveBad = cms.uint32(2)
        )
    )
)

process.hltESPRKTrajectorySmoother = cms.ESProducer("KFTrajectorySmootherESProducer",
    ComponentName = cms.string('hltESPRKTrajectorySmoother'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3)
)

process.hltESPGlobalDetLayerGeometry = cms.ESProducer("GlobalDetLayerGeometryESProducer",
    ComponentName = cms.string('hltESPGlobalDetLayerGeometry')
)

process.hltESPRKTrajectoryFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('hltESPRKTrajectoryFitter'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    minHits = cms.int32(3)
)

process.hltESPRungeKuttaTrackerPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('hltESPRungeKuttaTrackerPropagator'),
    Mass = cms.double(0.105),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('alongMomentum'),
    SimpleMagneticField = cms.string(''),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(True)
)

process.hltESPKFFittingSmootherWithOutliersRejectionAndRK = cms.ESProducer("KFFittingSmootherESProducer",
    BreakTrajWith2ConsecutiveMissing = cms.bool(True),
    ComponentName = cms.string('hltESPKFFittingSmootherWithOutliersRejectionAndRK'),
    EstimateCut = cms.double(20.0),
    Fitter = cms.string('hltESPRKTrajectoryFitter'),
    LogPixelProbabilityCut = cms.double(-14.0),
    MaxFractionOutliers = cms.double(0.3),
    MaxNumberOfOutliers = cms.int32(3),
    MinDof = cms.int32(2),
    MinNumberOfHits = cms.int32(3),
    NoInvalidHitsBeginEnd = cms.bool(True),
    NoOutliersBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True),
    Smoother = cms.string('hltESPRKTrajectorySmoother'),
    appendToDataLabel = cms.string('')
)

process.hltESPSmartPropagatorAnyOpposite = cms.ESProducer("SmartPropagatorESProducer",
    ComponentName = cms.string('hltESPSmartPropagatorAnyOpposite'),
    Epsilon = cms.double(5.0),
    MuonPropagator = cms.string('SteppingHelixPropagatorAny'),
    PropagationDirection = cms.string('oppositeToMomentum'),
    TrackerPropagator = cms.string('PropagatorWithMaterialOpposite')
)

process.hltESPSmartPropagatorAny = cms.ESProducer("SmartPropagatorESProducer",
    ComponentName = cms.string('hltESPSmartPropagatorAny'),
    Epsilon = cms.double(5.0),
    MuonPropagator = cms.string('SteppingHelixPropagatorAny'),
    PropagationDirection = cms.string('alongMomentum'),
    TrackerPropagator = cms.string('PropagatorWithMaterial')
)

process.hltESPSmartPropagator = cms.ESProducer("SmartPropagatorESProducer",
    ComponentName = cms.string('hltESPSmartPropagator'),
    Epsilon = cms.double(5.0),
    MuonPropagator = cms.string('hltESPSteppingHelixPropagatorAlong'),
    PropagationDirection = cms.string('alongMomentum'),
    TrackerPropagator = cms.string('PropagatorWithMaterial')
)

process.hltESPL3MuKFTrajectoryFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('hltESPL3MuKFTrajectoryFitter'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPSmartPropagatorAny'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    minHits = cms.int32(3)
)

process.hltESPSteppingHelixPropagatorAlong = cms.ESProducer("SteppingHelixPropagatorESProducer",
    ApplyRadX0Correction = cms.bool(True),
    AssumeNoMaterial = cms.bool(False),
    ComponentName = cms.string('hltESPSteppingHelixPropagatorAlong'),
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('alongMomentum'),
    SetVBFPointer = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    debug = cms.bool(False),
    endcapShiftInZNeg = cms.double(0.0),
    endcapShiftInZPos = cms.double(0.0),
    returnTangentPlane = cms.bool(True),
    sendLogWarning = cms.bool(False),
    useEndcapShiftsInZ = cms.bool(False),
    useInTeslaFromMagField = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    useMagVolumes = cms.bool(True),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False)
)

process.hltESPTTRHBuilderPixelOnly = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    ComponentName = cms.string('hltESPTTRHBuilderPixelOnly'),
    ComputeCoarseLocalPositionFromDisk = cms.bool(False),
    Matcher = cms.string('StandardMatcher'),
    #Phase2StripCPE = cms.string('Phase2StripCPE'),
    Phase2StripCPE = cms.string(''),
    PixelCPE = cms.string('PixelCPEGeneric'),
    StripCPE = cms.string('Fake')
)

process.hltPixelTracksCleanerBySharedHits = cms.ESProducer("PixelTrackCleanerBySharedHitsESProducer",
    ComponentName = cms.string('hltPixelTracksCleanerBySharedHits'),
    appendToDataLabel = cms.string(''),
    useQuadrupletAlgo = cms.bool(False)
)

process.hltESPTrackAlgoPriorityOrder = cms.ESProducer("TrackAlgoPriorityOrderESProducer",
    ComponentName = cms.string('hltESPTrackAlgoPriorityOrder'),
    algoOrder = cms.vstring(),
    appendToDataLabel = cms.string('')
)

process.hltESPTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(0.0),
    ValidHitBonus = cms.double(100.0),
    allowSharedFirstHit = cms.bool(False),
    fractionShared = cms.double(0.5)
)

process.hltESPChi2ChargeMeasurementEstimator9 = cms.ESProducer( "Chi2ChargeMeasurementEstimatorESProducer",
    appendToDataLabel = cms.string( "" ),
    clusterChargeCut = cms.PSet(  refToPSet_ = cms.string( "HLTSiStripClusterChargeCutLoose" ) ),
    MinimalTolerance = cms.double( 0.5 ),
    MaxDisplacement = cms.double( 0.5 ),
    ComponentName = cms.string( "hltESPChi2ChargeMeasurementEstimator9" ),
    pTChargeCutThreshold = cms.double( 15.0 ),
    nSigma = cms.double( 3.0 ),
    MaxSagitta = cms.double( 2.0 ),
    MaxChi2 = cms.double( 9.0 ),
    MinPtForHitRecoveryInGluedDet = cms.double( 1000000.0 )
)

process.hltESPChi2ChargeMeasurementEstimator16 = cms.ESProducer( "Chi2ChargeMeasurementEstimatorESProducer",
    appendToDataLabel = cms.string( "" ),
    clusterChargeCut = cms.PSet(  refToPSet_ = cms.string( "HLTSiStripClusterChargeCutLoose" ) ),
    MinimalTolerance = cms.double( 0.5 ),
    MaxDisplacement = cms.double( 0.5 ),
    ComponentName = cms.string( "hltESPChi2ChargeMeasurementEstimator16" ),
    pTChargeCutThreshold = cms.double( -1.0 ),
    nSigma = cms.double( 3.0 ),
    MaxSagitta = cms.double( 2.0 ),
    MaxChi2 = cms.double( 16.0 ),
    MinPtForHitRecoveryInGluedDet = cms.double( 1000000.0 )
)

# -- PSet -- #
process.HLTPSetPvClusterComparerForIT = cms.PSet(
    track_chi2_max = cms.double(20.0),
    track_prob_min = cms.double(-1.0),
    track_pt_max = cms.double(20.0),
    track_pt_min = cms.double(1.0)
)

process.hltPhase2PSetPvClusterComparerForIT = cms.PSet(
    track_chi2_max = cms.double( 20.0 ),
    track_pt_max = cms.double( 20.0 ),
    track_prob_min = cms.double( -1.0 ),
    track_pt_min = cms.double( 1.0 )
)

process.HLTSiStripClusterChargeCutNone = cms.PSet(
    value = cms.double(-1.0)
)

process.HLTPSetMuonCkfTrajectoryFilter = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(1),
    maxLostHitsFraction = cms.double(999.0),
    maxNumberOfHits = cms.int32(-1),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.9),
    minimumNumberOfHits = cms.int32(5),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetMuonCkfTrajectoryBuilder = cms.PSet(
    ComponentType = cms.string('MuonCkfTrajectoryBuilder'),
    MeasurementTrackerName = cms.string('hltESPMeasurementTracker'),
    #TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TTRHBuilder = cms.string('WithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    deltaEta = cms.double(-1.0),
    deltaPhi = cms.double(-1.0),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    intermediateCleaning = cms.bool(False),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    propagatorProximity = cms.string('SteppingHelixPropagatorAny'),
    rescaleErrorIfFail = cms.double(1.0),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetMuonCkfTrajectoryFilter')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSeedLayer = cms.bool(False),
    seedAs5DHit = cms.bool(False),
)

process.HLTIter2TrkL3MuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    MeasurementTrackerName = cms.string('hltIter2HighPtTkMuESPMeasurementTracker'),
    #TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TTRHBuilder = cms.string('WithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(False),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(1000.0),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(2),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter2TrkL3MuonPSetTrajectoryFilterIT')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True),
    seedAs5DHit = cms.bool(False),
)

process.HLTIter2TrkL3MuonPSetTrajectoryFilterIT = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(3),
    maxLostHits = cms.int32(1),
    maxLostHitsFraction = cms.double(999.0),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.3),
    minimumNumberOfHits = cms.int32(5),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTIter0TrkL3FromL1TkMuonGroupedCkfTrajectoryFilterIT = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(10.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.9),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTIter0TrkL3FromL1TkMuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    MeasurementTrackerName = cms.string(''),
    #TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TTRHBuilder = cms.string('WithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(1000.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0TrkL3FromL1TkMuonGroupedCkfTrajectoryFilterIT')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(True),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(1.0),
    maxCand = cms.int32(5),
    minNrOfHitsForRebuild = cms.int32(2),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0TrkL3FromL1TkMuonGroupedCkfTrajectoryFilterIT')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True),
    seedAs5DHit = cms.bool(False),
)

process.HLTIter2TrkL3FromL1TkMuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    MeasurementTrackerName = cms.string('hltIter2HighPtTkMuESPMeasurementTracker'),
    TTRHBuilder = cms.string('WithTrackAngle'),
    #TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(False),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(1000.0),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(2),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter2TrkL3FromL1TkMuonPSetTrajectoryFilterIT')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True),
    seedAs5DHit = cms.bool(False),
)

process.HLTIter2TrkL3FromL1TkMuonPSetTrajectoryFilterIT = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(3),
    maxLostHits = cms.int32(1),
    maxLostHitsFraction = cms.double(999.0),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.3),
    minimumNumberOfHits = cms.int32(5),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTSeedFromProtoTracks = cms.PSet(
    ComponentName = cms.string('SeedFromConsecutiveHitsCreator'),
    MinOneOverPtError = cms.double(1.0),
    OriginTransverseErrorMultiplier = cms.double(1.0),
    SeedMomentumForBOFF = cms.double(5.0),
    TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
    forceKinematicWithRegionDirection = cms.bool(False),
    magneticField = cms.string('ParabolicMf'),
    propagator = cms.string('PropagatorWithMaterialParabolicMf')
)

process.hltPhase2SeedFromProtoTracks = cms.PSet(
  ComponentName = cms.string("SeedFromConsecutiveHitsCreator" ),
  MinOneOverPtError = cms.double( 1.0 ),
  OriginTransverseErrorMultiplier = cms.double( 1.0 ),
  SeedMomentumForBOFF = cms.double( 5.0 ),
  TTRHBuilder = cms.string("WithTrackAngle"), 
  forceKinematicWithRegionDirection = cms.bool( False ),
  magneticField = cms.string(""),    
  propagator = cms.string("PropagatorWithMaterial")   
)

process.HLTIter0TrkL3MuonGroupedCkfTrajectoryFilterIT = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(10.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.9),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTIter0TrkL3MuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    MeasurementTrackerName = cms.string(''),
    #TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TTRHBuilder = cms.string('WithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(1000.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0TrkL3MuonGroupedCkfTrajectoryFilterIT')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(True),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(1.0),
    maxCand = cms.int32(5),
    minNrOfHitsForRebuild = cms.int32(2),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0TrkL3MuonGroupedCkfTrajectoryFilterIT')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True),
    seedAs5DHit = cms.bool(False),
)

process.HLTIter0TrkL3MuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
    useSameTrajFilter = cms.bool(True),    
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    MeasurementTrackerName = cms.string(''),
    keepOriginalIfRebuildFails = cms.bool(True),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(1.0),
    requireSeedHitsInRebuild = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0TrkL3MuonGroupedCkfTrajectoryFilterIT')
    ),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    minNrOfHitsForRebuild = cms.int32(2),
    maxCand = cms.int32(5),
    alwaysUseInvalidHits = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(1000.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0TrkL3MuonGroupedCkfTrajectoryFilterIT')
    ),
    intermediateCleaning = cms.bool(True),
    updator = cms.string('hltESPKFUpdator'),
    bestHitOnly = cms.bool(True),
    seedAs5DHit = cms.bool(False)
)

process.HLTIter0GroupedCkfTrajectoryBuilderIT = cms.PSet( 
    keepOriginalIfRebuildFails = cms.bool( False ),
    lockHits = cms.bool( True ),
    maxDPhiForLooperReconstruction = cms.double( 2.0 ),
    propagatorOpposite = cms.string( "PropagatorWithMaterialParabolicMfOpposite" ),
    trajectoryFilter = cms.PSet(  refToPSet_ = cms.string( "HLTIter0PSetTrajectoryFilterIT" ) ),
    doSeedingRegionRebuilding = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    maxCand = cms.int32( 2 ),
    estimator = cms.string( "hltESPChi2ChargeMeasurementEstimator9" ),
    intermediateCleaning = cms.bool( True ),
    bestHitOnly = cms.bool( True ),
    useSameTrajFilter = cms.bool( True ),
    MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
    ComponentType = cms.string( "GroupedCkfTrajectoryBuilder" ),
    lostHitPenalty = cms.double( 30.0 ),
    requireSeedHitsInRebuild = cms.bool( True ),
    TTRHBuilder = cms.string( "WithTrackAngle" ),
    maxPtForLooperReconstruction = cms.double( 0.7 ),
    cleanTrajectoryAfterInOut = cms.bool( False ),
    propagatorAlong = cms.string( "PropagatorWithMaterialParabolicMf" ),
    minNrOfHitsForRebuild = cms.int32( 5 ),
    alwaysUseInvalidHits = cms.bool( False ),
    inOutTrajectoryFilter = cms.PSet(  refToPSet_ = cms.string( "HLTIter0PSetTrajectoryFilterIT" ) ),
    foundHitBonus = cms.double( 5.0 ),
    updator = cms.string( "hltESPKFUpdator" ),
    seedAs5DHit = cms.bool(False)
)

process.HLTIter0PSetTrajectoryFilterIT = cms.PSet( 
    minimumNumberOfHits = cms.int32( 4 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    seedExtension = cms.int32( 0 ),
    chargeSignificance = cms.double( -1.0 ),
    pixelSeedExtension = cms.bool( False ),
    strictSeedExtension = cms.bool( False ),
    nSigmaMinPt = cms.double( 5.0 ),
    maxCCCLostHits = cms.int32( 0 ),
    minPt = cms.double( 0.3 ),
    maxConsecLostHits = cms.int32( 1 ),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32( 4 ),
    constantValueForLostHitsFractionFilter = cms.double( 1.0 ),
    seedPairPenalty = cms.int32( 0 ),
    maxNumberOfHits = cms.int32( 100 ),
    minNumberOfHitsForLoopers = cms.int32( 13 ),
    minGoodStripCharge = cms.PSet(  refToPSet_ = cms.string( "HLTSiStripClusterChargeCutNone" ) ),
    minNumberOfHitsPerLoop = cms.int32( 4 ),
    minHitsMinPt = cms.int32( 4 ),
    maxLostHitsFraction = cms.double( 999.0 ),
    maxLostHits = cms.int32( 1 )
)

process.HLTSiStripClusterChargeCutLoose = cms.PSet(
    value = cms.double( 1620.0 )
)

process.HLTIter1GroupedCkfTrajectoryBuilderIT = cms.PSet( 
    useSameTrajFilter = cms.bool( True ),
    ComponentType = cms.string( "GroupedCkfTrajectoryBuilder" ),
    MeasurementTrackerName = cms.string( "hltIter1ESPMeasurementTracker" ),
    keepOriginalIfRebuildFails = cms.bool( False ),
    lostHitPenalty = cms.double( 30.0 ),
    lockHits = cms.bool( True ),
    requireSeedHitsInRebuild = cms.bool( True ),
    TTRHBuilder = cms.string( "WithTrackAngle" ),
    propagatorOpposite = cms.string( "PropagatorWithMaterialParabolicMfOpposite" ),
    trajectoryFilter = cms.PSet(  refToPSet_ = cms.string( "HLTIter1PSetTrajectoryFilterIT" ) ),
    propagatorAlong = cms.string( "PropagatorWithMaterialParabolicMf" ),
    minNrOfHitsForRebuild = cms.int32( 5 ),
    maxCand = cms.int32( 2 ),
    alwaysUseInvalidHits = cms.bool( False ),
    estimator = cms.string( "hltESPChi2ChargeMeasurementEstimator16" ),
    intermediateCleaning = cms.bool( True ),
    foundHitBonus = cms.double( 5.0 ),
    updator = cms.string( "hltESPKFUpdator" ),
    bestHitOnly = cms.bool( True ),
    seedAs5DHit = cms.bool(False)
)

process.HLTIter1PSetTrajectoryFilterIT = cms.PSet( 
    minimumNumberOfHits = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    seedExtension = cms.int32( 0 ),
    chargeSignificance = cms.double( -1.0 ),
    pixelSeedExtension = cms.bool( False ),
    strictSeedExtension = cms.bool( False ),
    nSigmaMinPt = cms.double( 5.0 ),
    maxCCCLostHits = cms.int32( 0 ),
    minPt = cms.double( 0.2 ),
    maxConsecLostHits = cms.int32( 1 ),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32( 4 ),
    constantValueForLostHitsFractionFilter = cms.double( 1.0 ),
    seedPairPenalty = cms.int32( 0 ),
    maxNumberOfHits = cms.int32( 100 ),
    minNumberOfHitsForLoopers = cms.int32( 13 ),
    minGoodStripCharge = cms.PSet(  refToPSet_ = cms.string( "HLTSiStripClusterChargeCutNone" ) ),
    minNumberOfHitsPerLoop = cms.int32( 4 ),
    minHitsMinPt = cms.int32( 3 ),
    maxLostHitsFraction = cms.double( 999.0 ),
    maxLostHits = cms.int32( 1 )
)

process.HLTIter2GroupedCkfTrajectoryBuilderIT = cms.PSet( 
    keepOriginalIfRebuildFails = cms.bool( False ),
    lockHits = cms.bool( True ),
    maxDPhiForLooperReconstruction = cms.double( 2.0 ),
    propagatorOpposite = cms.string( "PropagatorWithMaterialParabolicMfOpposite" ),
    trajectoryFilter = cms.PSet(  refToPSet_ = cms.string( "HLTIter2PSetTrajectoryFilterIT" ) ),
    doSeedingRegionRebuilding = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    maxCand = cms.int32( 2 ),
    estimator = cms.string( "hltESPChi2ChargeMeasurementEstimator16" ),
    intermediateCleaning = cms.bool( True ),
    bestHitOnly = cms.bool( True ),
    useSameTrajFilter = cms.bool( True ),
    MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
    ComponentType = cms.string( "GroupedCkfTrajectoryBuilder" ),
    lostHitPenalty = cms.double( 30.0 ),
    requireSeedHitsInRebuild = cms.bool( True ),
    TTRHBuilder = cms.string( "WithTrackAngle" ),
    maxPtForLooperReconstruction = cms.double( 0.7 ),
    cleanTrajectoryAfterInOut = cms.bool( False ),
    propagatorAlong = cms.string( "PropagatorWithMaterialParabolicMf" ),
    minNrOfHitsForRebuild = cms.int32( 5 ),
    alwaysUseInvalidHits = cms.bool( False ),
    inOutTrajectoryFilter = cms.PSet(  refToPSet_ = cms.string( "HLTIter2PSetTrajectoryFilterIT" ) ),
    foundHitBonus = cms.double( 5.0 ),
    updator = cms.string( "hltESPKFUpdator" ),
    seedAs5DHit = cms.bool(False)
)

process.HLTIter2PSetTrajectoryFilterIT = cms.PSet( 
    minimumNumberOfHits = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    seedExtension = cms.int32( 1 ),
    chargeSignificance = cms.double( -1.0 ),
    pixelSeedExtension = cms.bool( False ),
    strictSeedExtension = cms.bool( False ),
    nSigmaMinPt = cms.double( 5.0 ),
    maxCCCLostHits = cms.int32( 0 ),
    minPt = cms.double( 0.3 ),
    maxConsecLostHits = cms.int32( 1 ),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32( 4 ),
    constantValueForLostHitsFractionFilter = cms.double( 1.0 ),
    seedPairPenalty = cms.int32( 0 ),
    maxNumberOfHits = cms.int32( 100 ),
    minNumberOfHitsForLoopers = cms.int32( 13 ),
    minGoodStripCharge = cms.PSet(  refToPSet_ = cms.string( "HLTSiStripClusterChargeCutNone" ) ),
    minNumberOfHitsPerLoop = cms.int32( 4 ),
    minHitsMinPt = cms.int32( 3 ),
    maxLostHitsFraction = cms.double( 999.0 ),
    maxLostHits = cms.int32( 1 )
)
# -- #

# -- Begin sequence -- #
process.hltTriggerType = cms.EDFilter("HLTTriggerTypeFilter",
    SelectedTriggerType = cms.int32(1)
)

process.hltScalersRawToDigi = cms.EDProducer("ScalersRawToDigi",
    scalersInputTag = cms.InputTag("rawDataCollector")
)

process.hltOnlineBeamSpot = cms.EDProducer("BeamSpotOnlineProducer",
    changeToCMSCoordinates = cms.bool(False),
    gtEvmLabel = cms.InputTag(""),
    maxRadius = cms.double(2.0),
    maxZ = cms.double(40.0),
    setSigmaZ = cms.double(0.0),
    src = cms.InputTag("hltScalersRawToDigi")
)

process.HLTBeamSpot = cms.Sequence(
    process.hltScalersRawToDigi+
    process.hltOnlineBeamSpot
)

process.HLTBeginSequence = cms.Sequence(
    process.hltTriggerType+
    process.HLTBeamSpot
)
# -- #


# -- Muon Local Reconstruction -- #
process.hltDt1DRecHits = process.dt1DRecHits.clone(
    dtDigiLabel = cms.InputTag("simMuonDTDigis")
)

process.hltDt4DSegments = process.dt4DSegments.clone(
    recHits1DLabel = cms.InputTag("hltDt1DRecHits")
)

process.hltCsc2DRecHits = process.csc2DRecHits.clone(
    stripDigiTag = cms.InputTag("simMuonCSCDigis","MuonCSCStripDigi"),
    wireDigiTag = cms.InputTag("simMuonCSCDigis","MuonCSCWireDigi")
)

process.hltCscSegments = process.cscSegments.clone(
    inputObjects = cms.InputTag("hltCsc2DRecHits")
)

process.hltRpcRecHits = process.rpcRecHits.clone(
    rpcDigiLabel = cms.InputTag("simMuonRPCDigis")
)

process.hltGemRecHits = process.gemRecHits.clone(
    gemDigiLabel = cms.InputTag("simMuonGEMDigis")
)

process.hltGemSegments = process.gemSegments.clone(
    gemRecHitLabel = cms.InputTag("hltGemRecHits")
)

process.hltMe0RecHits = process.me0RecHits.clone(
    me0DigiLabel = cms.InputTag("simMuonME0PseudoReDigis")
)

process.hltMe0Segments = process.me0Segments.clone(
    me0RecHitLabel = cms.InputTag("hltMe0RecHits")
)

process.HLTMuonGemLocalRecoSequence = cms.Sequence(
    process.hltGemRecHits+
    process.hltGemSegments+
    process.hltMe0RecHits+
    process.hltMe0Segments
)

process.HLTMuonLocalRecoSequence = cms.Sequence(
    process.hltDt1DRecHits+
    process.hltDt4DSegments+
    process.hltCsc2DRecHits+
    process.hltCscSegments+
    process.hltRpcRecHits+
    process.HLTMuonGemLocalRecoSequence
)
# -- #

# -- Tracker Local Reconstruction -- #
process.hltSiPixelClusters = process.siPixelClusters.clone(
    src = cms.InputTag("simSiPixelDigis","Pixel")
)

process.hltSiPixelClustersCache = cms.EDProducer("SiPixelClusterShapeCacheProducer",
    onDemand = cms.bool(False),
    src = cms.InputTag("hltSiPixelClusters")
)

process.hltSiPixelRecHits = process.siPixelRecHits.clone(
    src = cms.InputTag("hltSiPixelClusters")
)

process.HLTDoLocalPixelSequence = cms.Sequence(
    process.hltSiPixelClusters+
    process.hltSiPixelClustersCache+
    process.hltSiPixelRecHits
)

process.hltSiStripClusters = cms.EDProducer("MeasurementTrackerEventProducer",
    Phase2TrackerCluster1DProducer = cms.string('siPhase2Clusters'),
    badPixelFEDChannelCollectionLabels = cms.VInputTag("siPixelDigis"),
    inactivePixelDetectorLabels = cms.VInputTag(),
    inactiveStripDetectorLabels = cms.VInputTag("siStripDigis"),
    measurementTracker = cms.string(''),
    mightGet = cms.optional.untracked.vstring,
    pixelCablingMapLabel = cms.string(''),
    pixelClusterProducer = cms.string('hltSiPixelClusters'),
    skipClusters = cms.InputTag(""),
    stripClusterProducer = cms.string(''),
    switchOffPixelsIfEmpty = cms.bool(True)
)

process.HLTDoLocalStripSequence = cms.Sequence(
    process.siPhase2Clusters+
    process.hltSiStripClusters
)
# -- #

# -- Iter0 quadruplet -- #
process.hltTrkL3MuonPixelTracksFilter = cms.EDProducer("PixelTrackFilterByKinematicsProducer",
    chi2 = cms.double(1000.0),
    nSigmaInvPtTolerance = cms.double(0.0),
    nSigmaTipMaxTolerance = cms.double(0.0),
    ptMin = cms.double(0.9),  ## before was 0.1
    tipMax = cms.double(1.0)
)

process.hltTrkL3MuonPixelTracksFitter = cms.EDProducer("PixelFitterByHelixProjectionsProducer",
    scaleErrorsForBPix1 = cms.bool(False),
    scaleFactor = cms.double(0.65)
)

process.hltTrkL3FromL1TkMuonPixelTracksTrackingRegions = cms.EDProducer("CandidateSeededTrackingRegionsEDProducer",
    RegionPSet = cms.PSet(
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        deltaEta = cms.double(0.035),        # modified at the end
        deltaPhi = cms.double(0.02),         # modified at the end
        input = cms.InputTag("L1TkMuons", "", "MYHLT"),  # new L1 input HERE
        maxNRegions = cms.int32(10000),      # was 2
        maxNVertices = cms.int32(1),
        measurementTrackerName = cms.InputTag(""),
        mode = cms.string('BeamSpotSigma'),
        nSigmaZBeamSpot = cms.double(4.0),
        nSigmaZVertex = cms.double(3.0),
        originRadius = cms.double(0.2),
        precise = cms.bool(True),
        ptMin = cms.double(2.0),            # modified at the end
        searchOpt = cms.bool(False),
        vertexCollection = cms.InputTag("notUsed"),
        whereToUseMeasurementTracker = cms.string('Never'),
        zErrorBeamSpot = cms.double(24.2),
        zErrorVetex = cms.double(0.2)
    )
)

process.hltTrkL3FromL1TkMuonPixelLayerQuadruplets = cms.EDProducer("SeedingLayersEDProducer",
    BPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('WithTrackAngle'),
        #hitErrorRPhi = cms.double(0.0027),
        #hitErrorRZ = cms.double(0.006),
        #useErrorsFromParam = cms.bool(True)
    ),
    FPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('WithTrackAngle'),
        #hitErrorRPhi = cms.double(0.0051),
        #hitErrorRZ = cms.double(0.0036),
        #useErrorsFromParam = cms.bool(True)
    ),
    MTEC = cms.PSet(

    ),
    MTIB = cms.PSet(

    ),
    MTID = cms.PSet(

    ),
    MTOB = cms.PSet(

    ),
    TEC = cms.PSet(

    ),
    TIB = cms.PSet(

    ),
    TID = cms.PSet(

    ),
    TOB = cms.PSet(

    ),
    layerList = cms.vstring(
        'BPix1+BPix2+BPix3+BPix4', 
        'BPix1+BPix2+BPix3+FPix1_pos', 
        'BPix1+BPix2+BPix3+FPix1_neg', 
        'BPix1+BPix2+FPix1_pos+FPix2_pos', 
        'BPix1+BPix2+FPix1_neg+FPix2_neg', 
        'BPix1+FPix1_pos+FPix2_pos+FPix3_pos', 
        'BPix1+FPix1_neg+FPix2_neg+FPix3_neg'
    )
)

process.hltTrkL3FromL1TkMuonPixelTracksHitDoublets = cms.EDProducer("HitPairEDProducer",
    clusterCheck = cms.InputTag(""),
    layerPairs = cms.vuint32(0, 1, 2),
    maxElement = cms.uint32(0),
    produceIntermediateHitDoublets = cms.bool(True),
    produceSeedingHitSets = cms.bool(False),
    seedingLayers = cms.InputTag("hltTrkL3FromL1TkMuonPixelLayerQuadruplets"),
    trackingRegions = cms.InputTag("hltTrkL3FromL1TkMuonPixelTracksTrackingRegions"),
    trackingRegionsSeedingLayers = cms.InputTag("")
)

process.hltTrkL3FromL1TkMuonPixelTracksHitQuadruplets = cms.EDProducer("CAHitQuadrupletEDProducer",
    CAHardPtCut = cms.double(0.0),
    CAPhiCut = cms.double(0.2),
    CAThetaCut = cms.double(0.005),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('LowPtClusterShapeSeedComparitor'),
        clusterShapeCacheSrc = cms.InputTag("hltSiPixelClustersCache"),
        clusterShapeHitFilter = cms.string('ClusterShapeHitFilter')
    ),
    doublets = cms.InputTag("hltTrkL3FromL1TkMuonPixelTracksHitDoublets"),
    extraHitRPhitolerance = cms.double(0.032),
    fitFastCircle = cms.bool(True),
    fitFastCircleChi2Cut = cms.bool(True),
    maxChi2 = cms.PSet(
        enabled = cms.bool(True),
        pt1 = cms.double(0.7),
        pt2 = cms.double(2.0),
        value1 = cms.double(200.0),
        value2 = cms.double(50.0)
    ),
    useBendingCorrection = cms.bool(True)
)

process.hltTrkL3FromL1TkMuonPixelTracks = cms.EDProducer("PixelTrackProducer",
    Cleaner = cms.string('hltPixelTracksCleanerBySharedHits'),
    Filter = cms.InputTag("hltTrkL3MuonPixelTracksFilter"),
    Fitter = cms.InputTag("hltTrkL3MuonPixelTracksFitter"),
    SeedingHitSets = cms.InputTag("hltTrkL3FromL1TkMuonPixelTracksHitQuadruplets"),
    passLabel = cms.string('')
)

process.hltTrkL3FromL1TkMuonPixelVertices = cms.EDProducer("PixelVertexProducer",
    Finder = cms.string('DivisiveVertexFinder'),
    Method2 = cms.bool(True),
    NTrkMin = cms.int32(2),
    PVcomparer = cms.PSet(
        refToPSet_ = cms.string('hltPhase2PSetPvClusterComparerForIT')
    ),
    PtMin = cms.double(1.0),
    TrackCollection = cms.InputTag("hltTrkL3FromL1TkMuonPixelTracks"),
    UseError = cms.bool(True),
    Verbosity = cms.int32(0),
    WtAverage = cms.bool(True),
    ZOffset = cms.double(5.0),
    ZSeparation = cms.double(0.05),
    beamSpot = cms.InputTag("hltOnlineBeamSpot")
)

process.hltTrkL3FromL1TkMuonTrimmedPixelVertices = cms.EDProducer("PixelVertexCollectionTrimmer",
    PVcomparer = cms.PSet(
        refToPSet_ = cms.string('hltPhase2PSetPvClusterComparerForIT')
    ),
    fractionSumPt2 = cms.double(0.3),
    maxVtx = cms.uint32(100),
    minSumPt2 = cms.double(0.0),
    src = cms.InputTag("hltTrkL3FromL1TkMuonPixelVertices")
)

process.hltIter0TrkL3FromL1TkMuonPixelSeedsFromPixelTracks = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
    InputCollection = cms.InputTag("hltTrkL3FromL1TkMuonPixelTracks"),
    InputVertexCollection = cms.InputTag("hltTrkL3FromL1TkMuonTrimmedPixelVertices"),
    SeedCreatorPSet = cms.PSet(
        refToPSet_ = cms.string('hltPhase2SeedFromProtoTracks')
    ),
    TTRHBuilder = cms.string('WithTrackAngle'),
    originHalfLength = cms.double(0.3),
    originRadius = cms.double(0.1),
    useEventsWithNoVertex = cms.bool(True),
    usePV = cms.bool(False),
    useProtoTrackKinematics = cms.bool(False)
)

process.hltIter0TrkL3FromL1TkMuonCkfTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltSiStripClusters"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('none'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    TrajectoryBuilder = cms.string('GroupedCkfTrajectoryBuilder'),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTIter0TrkL3FromL1TkMuonPSetGroupedCkfTrajectoryBuilderIT')
    ),
    TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(False),
    doSeedingRegionRebuilding = cms.bool(True),
    maxNSeeds = cms.uint32(100000),
    maxSeedsBeforeCleaning = cms.uint32(1000),
    src = cms.InputTag("hltIter0TrkL3FromL1TkMuonPixelSeedsFromPixelTracks"),
    useHitsSplitting = cms.bool(True)
)

process.hltIter0TrkL3FromL1TkMuonCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('hltIter0'),
    Fitter = cms.string('FlexibleKFFittingSmoother'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string(''),
    MeasurementTrackerEvent = cms.InputTag("hltSiStripClusters"),
    NavigationSchool = cms.string(''),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    SimpleMagneticField = cms.string(''),
    TTRHBuilder = cms.string('WithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    alias = cms.untracked.string('ctfWithMaterialTracks'),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    src = cms.InputTag("hltIter0TrkL3FromL1TkMuonCkfTrackCandidates"),
    useHitsSplitting = cms.bool(False),
    useSimpleMF = cms.bool(False)
)

process.hltIter0TrkL3FromL1TkMuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(False),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
            d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
            dr_exp = cms.vint32(4, 4, 2147483647),
            dr_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dr_par2 = cms.vdouble(0.3, 0.3, 3.40282346639e+38)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 2147483647),
            dz_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dz_par2 = cms.vdouble(0.35, 0.35, 3.40282346639e+38)
        ),
        maxChi2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
        maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
        maxLostLayers = cms.vint32(1, 1, 1),
        min3DLayers = cms.vint32(0, 3, 4),
        minLayers = cms.vint32(3, 3, 4),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 3, 4)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIter0TrkL3FromL1TkMuonCtfWithMaterialTracks"),
    vertices = cms.InputTag("hltTrkL3FromL1TkMuonTrimmedPixelVertices")
)

process.hltIter0TrkL3FromL1TkMuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIter0TrkL3FromL1TkMuonTrackCutClassifier","MVAValues"),
    originalQualVals = cms.InputTag("hltIter0TrkL3FromL1TkMuonTrackCutClassifier","QualityMasks"),
    originalSource = cms.InputTag("hltIter0TrkL3FromL1TkMuonCtfWithMaterialTracks")
)
# -- #

# -- Iter2 triplet -- #
process.hltIter2TrkL3FromL1TkMuonClustersRefRemoval = cms.EDProducer("TrackClusterRemoverPhase2",
    TrackQuality = cms.string('highPurity'),
    maxChi2 = cms.double(16.0),
    minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
    oldClusterRemovalInfo = cms.InputTag(""),
    overrideTrkQuals = cms.InputTag(""),
    phase2pixelClusters = cms.InputTag("hltSiPixelClusters"),
    phase2OTClusters = cms.InputTag("siPhase2Clusters"),
    trackClassifier = cms.InputTag("","QualityMasks"),
    trajectories = cms.InputTag("hltIter0TrkL3FromL1TkMuonTrackSelectionHighPurity")
)

process.hltIter2TrkL3FromL1TkMuonMaskedMeasurementTrackerEvent = cms.EDProducer("MaskedMeasurementTrackerEventProducer",
    OnDemand = cms.bool(False),
    phase2clustersToSkip = cms.InputTag("hltIter2TrkL3FromL1TkMuonClustersRefRemoval"),
    src = cms.InputTag("hltSiStripClusters")
)

process.hltIter2TrkL3FromL1TkMuonPixelLayerTriplets = cms.EDProducer("SeedingLayersEDProducer",
    BPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('WithTrackAngle'),
        #hitErrorRPhi = cms.double(0.0027),
        #hitErrorRZ = cms.double(0.006),
        skipClusters = cms.InputTag("hltIter2TrkL3FromL1TkMuonClustersRefRemoval"),
        #useErrorsFromParam = cms.bool(True)
    ),
    FPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('WithTrackAngle'),
        #hitErrorRPhi = cms.double(0.0051),
        #hitErrorRZ = cms.double(0.0036),
        skipClusters = cms.InputTag("hltIter2TrkL3FromL1TkMuonClustersRefRemoval"),
        #useErrorsFromParam = cms.bool(True)
    ),
    MTEC = cms.PSet(

    ),
    MTIB = cms.PSet(

    ),
    MTID = cms.PSet(

    ),
    MTOB = cms.PSet(

    ),
    TEC = cms.PSet(

    ),
    TIB = cms.PSet(

    ),
    TID = cms.PSet(

    ),
    TOB = cms.PSet(

    ),
    layerList = cms.vstring(
        'BPix1+BPix2+BPix3', 
        'BPix2+BPix3+BPix4', 
        'BPix1+BPix3+BPix4', 
        'BPix1+BPix2+BPix4', 
        'BPix2+BPix3+FPix1_pos', 
        'BPix2+BPix3+FPix1_neg', 
        'BPix1+BPix2+FPix1_pos', 
        'BPix1+BPix2+FPix1_neg', 
        'BPix2+FPix1_pos+FPix2_pos', 
        'BPix2+FPix1_neg+FPix2_neg', 
        'BPix1+FPix1_pos+FPix2_pos', 
        'BPix1+FPix1_neg+FPix2_neg', 
        'FPix1_pos+FPix2_pos+FPix3_pos', 
        'FPix1_neg+FPix2_neg+FPix3_neg', 
        'BPix1+BPix3+FPix1_pos', 
        'BPix1+BPix2+FPix2_pos', 
        'BPix1+BPix3+FPix1_neg', 
        'BPix1+BPix2+FPix2_neg', 
        'BPix1+FPix2_neg+FPix3_neg', 
        'BPix1+FPix1_neg+FPix3_neg', 
        'BPix1+FPix2_pos+FPix3_pos', 
        'BPix1+FPix1_pos+FPix3_pos'
    )
)

process.hltIter2TrkL3FromL1TkMuonPixelClusterCheck = cms.EDProducer("ClusterCheckerEDProducer",
    ClusterCollectionLabel = cms.InputTag("hltSiStripClusters"),
    MaxNumberOfCosmicClusters = cms.uint32(50000),
    MaxNumberOfPixelClusters = cms.uint32(10000),
    PixelClusterCollectionLabel = cms.InputTag("hltSiPixelClusters"),
    cut = cms.string(''),
    doClusterCheck = cms.bool(False),
    silentClusterCheck = cms.untracked.bool(False)
)

process.hltIter2TrkL3FromL1TkMuonPixelHitDoublets = cms.EDProducer("HitPairEDProducer",
    clusterCheck = cms.InputTag("hltIter2TrkL3FromL1TkMuonPixelClusterCheck"),
    layerPairs = cms.vuint32(0, 1),
    maxElement = cms.uint32(0),
    produceIntermediateHitDoublets = cms.bool(True),
    produceSeedingHitSets = cms.bool(False),
    seedingLayers = cms.InputTag("hltIter2TrkL3FromL1TkMuonPixelLayerTriplets"),
    trackingRegions = cms.InputTag("hltTrkL3FromL1TkMuonPixelTracksTrackingRegions"),
    trackingRegionsSeedingLayers = cms.InputTag("")
)

process.hltIter2TrkL3FromL1TkMuonPixelHitTriplets = cms.EDProducer("CAHitTripletEDProducer",
    CAHardPtCut = cms.double(0.3),
    CAPhiCut = cms.double(0.1),
    CAThetaCut = cms.double(0.015),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    ),
    doublets = cms.InputTag("hltIter2TrkL3FromL1TkMuonPixelHitDoublets"),
    extraHitRPhitolerance = cms.double(0.032),
    maxChi2 = cms.PSet(
        enabled = cms.bool(True),
        pt1 = cms.double(0.8),
        pt2 = cms.double(8.0),
        value1 = cms.double(100.0),
        value2 = cms.double(6.0)
    ),
    useBendingCorrection = cms.bool(True)
)

process.hltIter2TrkL3FromL1TkMuonPixelSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsTripletOnlyEDProducer",
    MinOneOverPtError = cms.double(1.0),
    OriginTransverseErrorMultiplier = cms.double(1.0),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    TTRHBuilder = cms.string('WithTrackAngle'),
    forceKinematicWithRegionDirection = cms.bool(False),
    magneticField = cms.string('ParabolicMf'),
    propagator = cms.string('PropagatorWithMaterialParabolicMf'),
    seedingHitSets = cms.InputTag("hltIter2TrkL3FromL1TkMuonPixelHitTriplets")
)

process.hltIter2TrkL3FromL1TkMuonCkfTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltIter2TrkL3FromL1TkMuonMaskedMeasurementTrackerEvent"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    TrajectoryBuilder = cms.string(''),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTIter2TrkL3FromL1TkMuonPSetGroupedCkfTrajectoryBuilderIT')
    ),
    TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(False),
    doSeedingRegionRebuilding = cms.bool(False),
    maxNSeeds = cms.uint32(100000),
    maxSeedsBeforeCleaning = cms.uint32(1000),
    src = cms.InputTag("hltIter2TrkL3FromL1TkMuonPixelSeeds"),
    useHitsSplitting = cms.bool(False)
)

process.hltIter2TrkL3FromL1TkMuonCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('hltIter2'),
    Fitter = cms.string('FlexibleKFFittingSmoother'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string(''),
    MeasurementTrackerEvent = cms.InputTag("hltIter2TrkL3FromL1TkMuonMaskedMeasurementTrackerEvent"),
    NavigationSchool = cms.string(''),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    SimpleMagneticField = cms.string(''),
    TTRHBuilder = cms.string('WithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    alias = cms.untracked.string('ctfWithMaterialTracks'),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    src = cms.InputTag("hltIter2TrkL3FromL1TkMuonCkfTrackCandidates"),
    useHitsSplitting = cms.bool(False),
    useSimpleMF = cms.bool(False)
)

process.hltIter2TrkL3FromL1TkMuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(False),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
            d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
            dr_exp = cms.vint32(4, 4, 2147483647),
            dr_par1 = cms.vdouble(3.40282346639e+38, 0.4, 3.40282346639e+38),
            dr_par2 = cms.vdouble(3.40282346639e+38, 0.3, 3.40282346639e+38)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 2147483647),
            dz_par1 = cms.vdouble(3.40282346639e+38, 0.4, 3.40282346639e+38),
            dz_par2 = cms.vdouble(3.40282346639e+38, 0.35, 3.40282346639e+38)
        ),
        maxChi2 = cms.vdouble(9999.0, 25.0, 3.40282346639e+38),
        maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
        maxLostLayers = cms.vint32(1, 1, 1),
        min3DLayers = cms.vint32(0, 0, 0),
        minLayers = cms.vint32(3, 3, 3),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIter2TrkL3FromL1TkMuonCtfWithMaterialTracks"),
    vertices = cms.InputTag("hltTrkL3FromL1TkMuonTrimmedPixelVertices")
)

process.hltIter2TrkL3FromL1TkMuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIter2TrkL3FromL1TkMuonTrackCutClassifier","MVAValues"),
    originalQualVals = cms.InputTag("hltIter2TrkL3FromL1TkMuonTrackCutClassifier","QualityMasks"),
    originalSource = cms.InputTag("hltIter2TrkL3FromL1TkMuonCtfWithMaterialTracks")
)
# -- #

# -- Track merging and L3 Muon Reco -- #
process.hltIter2TrkL3FromL1TkMuonMerged = cms.EDProducer("TrackListMerger",
    Epsilon = cms.double(-0.001),
    FoundHitBonus = cms.double(5.0),
    LostHitPenalty = cms.double(20.0),
    MaxNormalizedChisq = cms.double(1000.0),
    MinFound = cms.int32(3),
    MinPT = cms.double(0.05),
    ShareFrac = cms.double(0.19),
    TrackProducers = cms.VInputTag("hltIter0TrkL3FromL1TkMuonTrackSelectionHighPurity", "hltIter2TrkL3FromL1TkMuonTrackSelectionHighPurity"),
    allowFirstHitShare = cms.bool(True),
    copyExtras = cms.untracked.bool(True),
    copyMVA = cms.bool(False),
    hasSelector = cms.vint32(0, 0),
    indivShareFrac = cms.vdouble(1.0, 1.0),
    newQuality = cms.string('confirmed'),
    selectedTrackQuals = cms.VInputTag("hltIter0TrkL3FromL1TkMuonTrackSelectionHighPurity", "hltIter2TrkL3FromL1TkMuonTrackSelectionHighPurity"),
    setsToMerge = cms.VPSet(cms.PSet(
        pQual = cms.bool(False),
        tLists = cms.vint32(0, 1)
    )),
    trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
    writeOnlyTrkQuals = cms.bool(False)
)

process.hltTrkL3MuonsNoID = cms.EDProducer("MuonIdProducer",
    CaloExtractorPSet = cms.PSet(
        CenterConeOnCalIntersection = cms.bool(False),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        DR_Max = cms.double(1.0),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_H = cms.double(0.1),
        DR_Veto_HO = cms.double(0.1),
        DepositInstanceLabels = cms.vstring(
            'ecal', 
            'hcal', 
            'ho'
        ),
        DepositLabel = cms.untracked.string('Cal'),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_EB = cms.double(0.025),
        Noise_EE = cms.double(0.1),
        Noise_HB = cms.double(0.2),
        Noise_HE = cms.double(0.2),
        Noise_HO = cms.double(0.2),
        PrintTimeReport = cms.untracked.bool(False),
        PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
            RPCLayers = cms.bool(False),
            UseMuonNavigation = cms.untracked.bool(False)
        ),
        Threshold_E = cms.double(0.2),
        Threshold_H = cms.double(0.5),
        Threshold_HO = cms.double(0.5),
        TrackAssociatorParameters = cms.PSet(
            CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
            CaloTowerCollectionLabel = cms.InputTag("Notused"),
            DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
            EBRecHitCollectionLabel = cms.InputTag("Notused"),
            EERecHitCollectionLabel = cms.InputTag("Notused"),
            HBHERecHitCollectionLabel = cms.InputTag("Notused"),
            HORecHitCollectionLabel = cms.InputTag("Notused"),
            accountForTrajectoryChangeCalo = cms.bool(False),
            dREcal = cms.double(1.0),
            dREcalPreselection = cms.double(1.0),
            dRHcal = cms.double(1.0),
            dRHcalPreselection = cms.double(1.0),
            dRMuon = cms.double(9999.0),
            dRMuonPreselection = cms.double(0.2),
            dRPreshowerPreselection = cms.double(0.2),
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            propagateAllDirections = cms.bool(True),
            trajectoryUncertaintyTolerance = cms.double(-1.0),
            truthMatch = cms.bool(False),
            useCalo = cms.bool(True),
            useEcal = cms.bool(False),
            useHO = cms.bool(False),
            useHcal = cms.bool(False),
            useMuon = cms.bool(False),
            usePreshower = cms.bool(False)
        ),
        UseRecHitsFlag = cms.bool(False)
    ),
    JetExtractorPSet = cms.PSet(
        ComponentName = cms.string('JetExtractor'),
        DR_Max = cms.double(1.0),
        DR_Veto = cms.double(0.1),
        ExcludeMuonVeto = cms.bool(True),
        JetCollectionLabel = cms.InputTag("Notused"),
        PrintTimeReport = cms.untracked.bool(False),
        PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
            RPCLayers = cms.bool(False),
            UseMuonNavigation = cms.untracked.bool(False)
        ),
        Threshold = cms.double(5.0),
        TrackAssociatorParameters = cms.PSet(
            CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
            CaloTowerCollectionLabel = cms.InputTag("Notused"),
            DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
            EBRecHitCollectionLabel = cms.InputTag("Notused"),
            EERecHitCollectionLabel = cms.InputTag("Notused"),
            HBHERecHitCollectionLabel = cms.InputTag("Notused"),
            HORecHitCollectionLabel = cms.InputTag("Notused"),
            accountForTrajectoryChangeCalo = cms.bool(False),
            dREcal = cms.double(0.5),
            dREcalPreselection = cms.double(0.5),
            dRHcal = cms.double(0.5),
            dRHcalPreselection = cms.double(0.5),
            dRMuon = cms.double(9999.0),
            dRMuonPreselection = cms.double(0.2),
            dRPreshowerPreselection = cms.double(0.2),
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            propagateAllDirections = cms.bool(True),
            trajectoryUncertaintyTolerance = cms.double(-1.0),
            truthMatch = cms.bool(False),
            useCalo = cms.bool(True),
            useEcal = cms.bool(False),
            useHO = cms.bool(False),
            useHcal = cms.bool(False),
            useMuon = cms.bool(False),
            usePreshower = cms.bool(False)
        )
    ),
    MuonCaloCompatibility = cms.PSet(
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_lowPt_3_1_norm.root'),
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_lowPt_3_1_norm.root'),
        allSiPMHO = cms.bool(False),
        delta_eta = cms.double(0.02),
        delta_phi = cms.double(0.02)
    ),
    TimingFillerParameters = cms.PSet(
        CSCTimingParameters = cms.PSet(
            CSCStripError = cms.double(7.0),
            CSCStripTimeOffset = cms.double(0.0),
            CSCTimeOffset = cms.double(0.0),
            CSCWireError = cms.double(8.6),
            CSCWireTimeOffset = cms.double(0.0),
            CSCsegments = cms.InputTag("hltCscSegments"),
            MatchParameters = cms.PSet(
                CSCsegments = cms.InputTag("hltCscSegments"),
                DTradius = cms.double(0.01),
                DTsegments = cms.InputTag("hltDt4DSegments"),
                TightMatchCSC = cms.bool(True),
                TightMatchDT = cms.bool(False)
            ),
            PruneCut = cms.double(100.0),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(True)
            ),
            UseStripTime = cms.bool(True),
            UseWireTime = cms.bool(True),
            debug = cms.bool(False)
        ),
        DTTimingParameters = cms.PSet(
            DTTimeOffset = cms.double(2.7),
            DTsegments = cms.InputTag("hltDt4DSegments"),
            DoWireCorr = cms.bool(False),
            DropTheta = cms.bool(True),
            HitError = cms.double(6.0),
            HitsMin = cms.int32(5),
            MatchParameters = cms.PSet(
                CSCsegments = cms.InputTag("hltCscSegments"),
                DTradius = cms.double(0.01),
                DTsegments = cms.InputTag("hltDt4DSegments"),
                TightMatchCSC = cms.bool(True),
                TightMatchDT = cms.bool(False)
            ),
            PruneCut = cms.double(10000.0),
            RequireBothProjections = cms.bool(False),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(True)
            ),
            UseSegmentT0 = cms.bool(False),
            debug = cms.bool(False)
        ),
        EcalEnergyCut = cms.double(0.4),
        ErrorCSC = cms.double(7.4),
        ErrorDT = cms.double(6.0),
        ErrorEB = cms.double(2.085),
        ErrorEE = cms.double(6.95),
        UseCSC = cms.bool(True),
        UseDT = cms.bool(True),
        UseECAL = cms.bool(True)
    ),
    TrackAssociatorParameters = cms.PSet(
        CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
        CaloTowerCollectionLabel = cms.InputTag("Notused"),
        DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
        EBRecHitCollectionLabel = cms.InputTag("Notused"),
        EERecHitCollectionLabel = cms.InputTag("Notused"),
        GEMSegmentCollectionLabel = cms.InputTag("hltGemSegments"),
        HBHERecHitCollectionLabel = cms.InputTag("Notused"),
        HORecHitCollectionLabel = cms.InputTag("Notused"),
        ME0SegmentCollectionLabel = cms.InputTag("hltMe0Segments"),
        accountForTrajectoryChangeCalo = cms.bool(False),
        dREcal = cms.double(9999.0),
        dREcalPreselection = cms.double(0.05),
        dRHcal = cms.double(9999.0),
        dRHcalPreselection = cms.double(0.2),
        dRMuon = cms.double(9999.0),
        dRMuonPreselection = cms.double(0.2),
        dRPreshowerPreselection = cms.double(0.2),
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        propagateAllDirections = cms.bool(True),
        trajectoryUncertaintyTolerance = cms.double(-1.0),
        truthMatch = cms.bool(False),
        useCalo = cms.bool(False),
        useEcal = cms.bool(False),
        useGEM = cms.bool(True),
        useHO = cms.bool(False),
        useHcal = cms.bool(False),
        useME0 = cms.bool(True),
        useMuon = cms.bool(True),
        usePreshower = cms.bool(False)
    ),
    TrackExtractorPSet = cms.PSet(
        BeamSpotLabel = cms.InputTag("hltOnlineBeamSpot"),
        BeamlineOption = cms.string('BeamSpotFromEvent'),
        Chi2Ndof_Max = cms.double(1e+64),
        Chi2Prob_Min = cms.double(-1.0),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        DR_Veto = cms.double(0.01),
        Diff_r = cms.double(0.1),
        Diff_z = cms.double(0.2),
        NHits_Min = cms.uint32(0),
        Pt_Min = cms.double(-1.0),
        inputTrackCollection = cms.InputTag("hltIter2TrkL3FromL1TkMuonMerged")
    ),
    TrackerKinkFinderParameters = cms.PSet(
        diagonalOnly = cms.bool(False),
        usePosition = cms.bool(False)
    ),
    addExtraSoftMuons = cms.bool(False),
    arbitrateTrackerMuons = cms.bool(True),
    arbitrationCleanerOptions = cms.PSet(
        ClusterDPhi = cms.double(0.6),
        ClusterDTheta = cms.double(0.02),
        Clustering = cms.bool(True),
        ME1a = cms.bool(True),
        Overlap = cms.bool(True),
        OverlapDPhi = cms.double(0.0786),
        OverlapDTheta = cms.double(0.02)
    ),
    debugWithTruthMatching = cms.bool(False),
    ecalDepositName = cms.string('ecal'),
    fillCaloCompatibility = cms.bool(False),
    fillEnergy = cms.bool(False),
    fillGlobalTrackQuality = cms.bool(False),
    fillGlobalTrackRefits = cms.bool(False),
    fillIsolation = cms.bool(False),
    fillMatching = cms.bool(True),
    fillTrackerKink = cms.bool(False),
    globalTrackQualityInputTag = cms.InputTag("glbTrackQual"),
    hcalDepositName = cms.string('hcal'),
    hoDepositName = cms.string('ho'),
    inputCollectionLabels = cms.VInputTag("hltIter2TrkL3FromL1TkMuonMerged"),
    inputCollectionTypes = cms.vstring(
        'inner tracks'
    ),
    # inputCollectionLabels = cms.VInputTag("hltTrkL3MuonAndMuonFromL1TkMerged", "hltTrkL3GlbMuon", "hltL2Muons:UpdatedAtVtx"),
    # inputCollectionTypes = cms.vstring(
    #     'inner tracks', 
    #     'links', 
    #     'outer tracks'
    # ),
    jetDepositName = cms.string('jets'),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    maxAbsEta = cms.double(3.0),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minCaloCompatibility = cms.double(0.6),
    minNumberOfMatches = cms.int32(1),
    minP = cms.double(0.0),
    minPCaloMuon = cms.double(1000000000.0),
    minPt = cms.double(2.0),
    ptThresholdToFillCandidateP4WithGlobalFit = cms.double(200.0),
    runArbitrationCleaner = cms.bool(False),
    sigmaThresholdToFillCandidateP4WithGlobalFit = cms.double(2.0),
    trackDepositName = cms.string('tracker'),
    writeIsoDeposits = cms.bool(False)
)

process.hltTrkL3Muons = cms.EDProducer("MuonIDFilterProducerForHLT",
    allowedTypeMask = cms.uint32(0),
    applyTriggerIdLoose = cms.bool(True),
    inputMuonCollection = cms.InputTag("hltTrkL3MuonsNoID"),
    maxNormalizedChi2 = cms.double(9999.0),
    minNMuonHits = cms.int32(0),
    minNMuonStations = cms.int32(0),
    minNTrkLayers = cms.int32(0),
    minPixHits = cms.int32(0),
    minPixLayer = cms.int32(0),
    minPt = cms.double(0.0),
    minTrkHits = cms.int32(0),
    requiredTypeMask = cms.uint32(0),
    typeMuon = cms.uint32(0)
)

process.hltL3MuonsTrkL3Links = cms.EDProducer("MuonLinksProducer",
    inputCollection = cms.InputTag("hltTrkL3Muons")
)

process.hltTrkL3MuonTracks = cms.EDProducer("HLTMuonTrackSelector",
    copyExtras = cms.untracked.bool(True),
    copyMVA = cms.bool(False),
    copyTrajectories = cms.untracked.bool(False),
    muon = cms.InputTag("hltTrkL3Muons"),
    originalMVAVals = cms.InputTag("none"),
    track = cms.InputTag("hltIter2TrkL3FromL1TkMuonMerged")
)

process.hltTrkL3MuonCandidates = cms.EDProducer( "L3MuonCandidateProducerFromMuons",
    InputObjects = cms.InputTag("hltTrkL3Muons")
)

process.HLTIOFromL1TkMuonTkCandidateSequence = cms.Sequence(
    process.hltTrkL3MuonPixelTracksFilter+
    process.hltTrkL3MuonPixelTracksFitter+
    process.hltTrkL3FromL1TkMuonPixelTracksTrackingRegions+
    process.hltTrkL3FromL1TkMuonPixelLayerQuadruplets+
    process.hltTrkL3FromL1TkMuonPixelTracksHitDoublets+
    process.hltTrkL3FromL1TkMuonPixelTracksHitQuadruplets+
    process.hltTrkL3FromL1TkMuonPixelTracks+
    process.hltTrkL3FromL1TkMuonPixelVertices+
    process.hltTrkL3FromL1TkMuonTrimmedPixelVertices+
    process.hltIter0TrkL3FromL1TkMuonPixelSeedsFromPixelTracks+
    process.hltIter0TrkL3FromL1TkMuonCkfTrackCandidates+
    process.hltIter0TrkL3FromL1TkMuonCtfWithMaterialTracks+
    process.hltIter0TrkL3FromL1TkMuonTrackCutClassifier+
    process.hltIter0TrkL3FromL1TkMuonTrackSelectionHighPurity+
    process.hltIter2TrkL3FromL1TkMuonClustersRefRemoval+
    process.hltIter2TrkL3FromL1TkMuonMaskedMeasurementTrackerEvent+
    process.hltIter2TrkL3FromL1TkMuonPixelLayerTriplets+
    process.hltIter2TrkL3FromL1TkMuonPixelClusterCheck+
    process.hltIter2TrkL3FromL1TkMuonPixelHitDoublets+
    process.hltIter2TrkL3FromL1TkMuonPixelHitTriplets+
    process.hltIter2TrkL3FromL1TkMuonPixelSeeds+
    process.hltIter2TrkL3FromL1TkMuonCkfTrackCandidates+
    process.hltIter2TrkL3FromL1TkMuonCtfWithMaterialTracks+
    process.hltIter2TrkL3FromL1TkMuonTrackCutClassifier+
    process.hltIter2TrkL3FromL1TkMuonTrackSelectionHighPurity+
    process.hltIter2TrkL3FromL1TkMuonMerged
)

process.HLTL3TrkMuonRecoNocandSequence = cms.Sequence(
    process.HLTIOFromL1TkMuonTkCandidateSequence+
    process.hltTrkL3MuonsNoID+
    process.hltTrkL3Muons+
    process.hltL3MuonsTrkL3Links+
    process.hltTrkL3MuonTracks
)

process.HLTL3TrkMuonRecoSequence = cms.Sequence(
    process.HLTL3TrkMuonRecoNocandSequence+
    process.hltTrkL3MuonCandidates
)

process.hltBoolEnd = cms.EDFilter("HLTBool",
    result = cms.bool(True)
)

process.HLTEndSequence = cms.Sequence(
    process.hltBoolEnd
)

process.hltTriggerSummaryAOD = cms.EDProducer( "TriggerSummaryProducerAOD",
    moduleLabelPatternsToSkip = cms.vstring(  ),
    processName = cms.string( "@" ),
    moduleLabelPatternsToMatch = cms.vstring( 'hlt*' ),
    throw = cms.bool( False )
)
process.hltTriggerSummaryRAW = cms.EDProducer( "TriggerSummaryProducerRAW",
    processName = cms.string( "@" )
)
process.hltBoolFalse = cms.EDFilter( "HLTBool",
    result = cms.bool( False )
)
process.HLTriggerFinalPath = cms.Path(
    process.hltTriggerSummaryAOD+
    process.hltTriggerSummaryRAW+
    process.hltBoolFalse
)
# -- #

for moduleType in [process.producers_(), process.filters_(), process.analyzers_()]:
    for name, module in moduleType.iteritems():
        if hasattr(module, "mightGet") and module.mightGet:
            module.mightGet = cms.optional.untracked.vstring

# load the DQMStore and DQMRootOutputModule
process.load( "DQMServices.Core.DQMStore_cfi" )
process.DQMStore.enableMultiThread = True

# -- Validation -- #
from SimTracker.TrackAssociatorProducers.trackAssociatorByHits_cfi import *
process.LhcParametersDefinerForTP = cms.ESProducer("ParametersDefinerForTPESProducer",
   ComponentName = cms.string('LhcParametersDefinerForTP'),
   beamSpot      = cms.untracked.InputTag('hltOnlineBeamSpot', '', 'MYHLT')
)

from Validation.RecoMuon.associators_cff import *
from Validation.RecoMuon.muonValidationHLT_cff import *
from Validation.RecoMuon.selectors_cff import muonTPSet
muonTPSetPt22 = muonTPSet.clone()
muonTPSetPt22.ptMin = cms.double(22.0)
muonTPSetPt22.minRapidity = cms.double(-2.4)
muonTPSetPt22.maxRapidity = cms.double(2.4)

process.load("Validation.RecoMuon.muonValidationHLT_cff")
process.tpToL3FromL1TkMuonAssociation.tracksTag                = cms.InputTag("hltIter2TrkL3FromL1TkMuonMerged")
process.l3IOFromL1TkMuonMuTrackV.label                         = cms.VInputTag("hltIter2TrkL3FromL1TkMuonMerged:")
process.l3IOFromL1TkMuonMuTrackV.beamSpot                      = cms.InputTag('hltOnlineBeamSpot', '', 'MYHLT')
process.l3IOFromL1TkMuonMuTrackV.muonTPSelector                = muonTPSetPt22

process.hltIterL3MuonsNoIDTracks.muonsTag                      = cms.InputTag("hltTrkL3MuonsNoID")
process.hltIterL3MuonsNoIDTracks.inputCSCSegmentCollection     = cms.InputTag("hltCscSegments")
process.hltIterL3MuonsNoIDTracks.inputDTRecSegment4DCollection = cms.InputTag("hltDt4DSegments")
# process.tpToL3NoIDMuonAssociation
process.l3NoIDMuonMuTrackV.beamSpot                            = cms.InputTag('hltOnlineBeamSpot', '', 'MYHLT')
process.l3NoIDMuonMuTrackV.muonTPSelector                      = muonTPSetPt22

process.hltIterL3MuonsTracks.muonsTag                          = cms.InputTag("hltTrkL3Muons")
process.hltIterL3MuonsTracks.inputCSCSegmentCollection         = cms.InputTag("hltCscSegments")
process.hltIterL3MuonsTracks.inputDTRecSegment4DCollection     = cms.InputTag("hltDt4DSegments")
# process.tpToL3MuonAssociation
process.l3MuonMuTrackV.beamSpot                                = cms.InputTag('hltOnlineBeamSpot', '', 'MYHLT')
process.l3MuonMuTrackV.muonTPSelector                          = muonTPSetPt22

process.valpath = cms.Path(
    process.tpToL3FromL1TkMuonAssociation+
    process.l3IOFromL1TkMuonMuTrackV+

    process.hltIterL3MuonsNoIDTracks+
    process.tpToL3NoIDMuonAssociation+
    process.l3NoIDMuonMuTrackV+

    process.hltIterL3MuonsTracks+
    process.tpToL3MuonAssociation+
    process.l3MuonMuTrackV
)

process.dqmOutput = cms.OutputModule("DQMRootOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('DQMIO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string("DQMIO_IOFromL1TkMuon_L1TkMu22_dEta035_dPhi02.root"),
    outputCommands = process.DQMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)
process.DQMOutput = cms.EndPath( process.dqmOutput )
# -- #

# -- Test Setup -- #
process.GlobalTag.globaltag = "111X_mcRun4_realistic_T15_v2"

process.source.fileNames = cms.untracked.vstring(
    # "file:/eos/user/m/moh/TestSamples/DYToLL_M-50_TuneCP5_14TeV-pythia8__Phase2HLTTDRWinter20DIGI-PU200_pilot_110X_mcRun4_realistic_v3-v2__GEN-SIM-DIGI-RAW/4043F7D2-1BF4-FE40-82D9-10786D005454.root"

    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYJetsToLL_M-10to50_TuneCP5_14TeV-madgraphMLM-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_111X_mcRun4_realistic_T15_v1-v1/120000/5821E269-9E33-AE49-9133-67A03F2527EC.root",

    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F7512F92-AA6C-F642-BBA5-8BAED84CF4C9.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F786C6BD-D600-A845-B12B-D2A499B05D2B.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F7CBE904-DE8D-ED4D-A5C3-EACE571910BE.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F8C8FBAC-2360-E649-B7C9-A1F5C8F2A788.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F9371A50-AC2F-1649-9949-11D1C169E6A5.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FAB40CB7-0647-F344-8470-2E0BAB68C7AF.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FAF35BE0-D62E-9E41-AA4E-6EFA98032795.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FB635D0A-F1D3-5D4E-90AD-6C396681FC87.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FC9170CA-633F-EB4C-8CE5-4E2D29969EBB.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FCB6CEBD-0248-1C4E-9C95-D45A3F3F5902.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FDE7E62F-A277-B145-9FC7-8078B21C0913.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FE7B45F1-3D6D-7643-999E-CEA976B2CDC1.root",

    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FC1C5501-17FF-AD4E-B0C2-78B114D94AD6.root",
    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FD2DCC3C-9732-854B-AD23-A010899DB902.root",
    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FD35A9AA-051D-B94B-A971-901867BFED51.root",
    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FD8D88D6-E791-6B4F-B067-AAFEA3F852D3.root",
    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FDA9AEB8-5A1F-AF49-B919-5C7A64194B0A.root",
    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FDB296D7-F051-9645-BC27-9D222B962B3A.root",
    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FDBE16F6-13A5-FF48-A316-83D9B8FB3CB2.root",
    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FE0F2AF9-BDD9-AF4A-88F1-D426E89F788E.root",
    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FE352801-A32A-304E-8EF2-FEB62D8A4036.root",
    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FEA94BB5-2837-A14F-9F65-24D5103522D2.root",
    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FF3C16DF-5B11-8B4A-9B67-DF3CEF790F2F.root",
    "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FF7BF0E2-1380-2D48-BB19-F79E6907CD5D.root",

    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/87C80516-CB14-0346-9579-1CCCE4607148.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/0058F613-AE76-4840-82C3-7F6F3224BBF3.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/0064CF05-E335-5440-BDA1-4DDA696F3CBD.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/008A2993-1370-424A-ABA1-B2D163F8AEED.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/012D4B65-425E-8A49-B961-A289D0447E1E.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/014A3F26-43E6-AA41-B605-AA4861CE6351.root",
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( 100 )
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool( True ),
    numberOfThreads = cms.untracked.uint32( 1 ),
    numberOfStreams = cms.untracked.uint32( 0 ),
    sizeOfStackForThreadsInKB = cms.untracked.uint32( 10*1024 )
)

if 'MessageLogger' in process.__dict__:
    process.MessageLogger.categories.append('TriggerSummaryProducerAOD')
    process.MessageLogger.categories.append('L1GtTrigReport')
    process.MessageLogger.categories.append('L1TGlobalSummary')
    process.MessageLogger.categories.append('HLTrigReport')
    process.MessageLogger.categories.append('FastReport')
# -- #

# -- L1TkMuon Tracking Region -- #
process.hltTrkL3FromL1TkMuonPixelTracksTrackingRegions.RegionPSet.deltaEta = cms.double(0.035)
process.hltTrkL3FromL1TkMuonPixelTracksTrackingRegions.RegionPSet.deltaPhi = cms.double(0.02)
process.hltTrkL3FromL1TkMuonPixelTracksTrackingRegions.RegionPSet.ptMin = cms.double(2.0)
# -- #

# -- input db
# https://github.com/trtomei/cmssw/blob/Phase2-L1T-HLT-Interface/HLTrigger/HLTfilters/test/test_Phase2L1THLT.py
process.load("CondCore.CondDB.CondDB_cfi")
process.CondDB.connect = "sqlite_file:L1TObjScaling.db"

process.L1TScalingESSource = cms.ESSource(
    "PoolDBESSource",
    process.CondDB,
    DumpStat=cms.untracked.bool(True),
    toGet=cms.VPSet(
        cms.PSet(
            record=cms.string("L1TObjScalingRcd"),
            tag=cms.string("L1TkMuonScaling"),
            label=cms.untracked.string("L1TkMuonScaling"),
        ),
    ),
)
process.es_prefer_l1tscaling = cms.ESPrefer("PoolDBESSource", "L1TScalingESSource")
# -- #

# -- Filter, Path and Schedule -- #
process.hltL1TkSingleMuFiltered22 = cms.EDFilter("L1TkMuonFilter",
    MinPt = cms.double(22),
    inputTag = cms.InputTag("L1TkMuons", "", "MYHLT")
)

process.HLT_IOFromL1TkMuon = cms.Path(
    process.HLTBeginSequence+

    # L1TkMuon filter
    process.hltL1TkSingleMuFiltered22+

    process.HLTMuonLocalRecoSequence+
    process.HLTDoLocalPixelSequence+
    process.HLTDoLocalStripSequence+

    # L3 reco
    process.HLTL3TrkMuonRecoSequence+
    # cms.ignore(process.hltL1fForTrkL3L1fL1sMu22or25L1Filtered0)+
    # cms.ignore(process.hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q)+

    process.HLTEndSequence
)

process.schedule = cms.Schedule(
    process.L1simulation_step,
    process.HLT_IOFromL1TkMuon,
    process.HLTriggerFinalPath,
    process.valpath,
    process.DQMOutput
)
# -- #

from SLHCUpgradeSimulations.Configuration.aging import customise_aging_1000
process = customise_aging_1000(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customisePhase2TTNoMC
from L1Trigger.Configuration.customisePhase2TTNoMC import customisePhase2TTNoMC

#call to customisation function customisePhase2TTNoMC imported from L1Trigger.Configuration.customisePhase2TTNoMC
process = customisePhase2TTNoMC(process)


from HLTrigger.Configuration.Eras import modifyHLTforEras
modifyHLTforEras(process)


# print process.dumpPython()

# process.Timing = cms.Service("Timing",
#     summaryOnly = cms.untracked.bool(True),
#     useJobReport = cms.untracked.bool(True)
# )

# process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",
#     ignoreTotal = cms.untracked.int32(1)
# )
