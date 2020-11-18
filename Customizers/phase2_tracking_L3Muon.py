import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Reconstruction_cff import *
from RecoLuminosity.LumiProducer.bunchSpacingProducer_cfi import *

def customise_common_L3Muon(process):

    process.itLocalReco = cms.Sequence(
        process.siPhase2Clusters
      + process.siPixelClusters
      + process.siPixelClusterShapeCache
      + process.siPixelRecHits
    )

    process.otLocalReco = cms.Sequence(
        process.MeasurementTrackerEvent
        + process.bunchSpacingProducer
    )

    #Region Definitions
    process.hltPhase2L3MuonPixelTracksTrackingRegions = cms.EDProducer("CandidateSeededTrackingRegionsEDProducer",
        RegionPSet = cms.PSet(
            beamSpot = cms.InputTag("offlineBeamSpot"),
            deltaEta = cms.double(0.4),
            deltaPhi = cms.double(0.4),
            input = cms.InputTag("hltPhase2L3MuonCandidates"),
            maxNRegions = cms.int32(10000),
            maxNVertices = cms.int32(1),
            measurementTrackerName = cms.InputTag(""),
            mode = cms.string('BeamSpotSigma'),
            nSigmaZBeamSpot = cms.double(4.0),
            nSigmaZVertex = cms.double(3.0),
            originRadius = cms.double(0.2),
            precise = cms.bool(True),
            ptMin = cms.double(0.9),
            searchOpt = cms.bool(False),
            vertexCollection = cms.InputTag("notUsed"),
            whereToUseMeasurementTracker = cms.string('Never'),
            zErrorBeamSpot = cms.double(24.2),
            zErrorVetex = cms.double(0.2)
        )
    )
    process.hltPhase2L3MuonInitialStepTrackingRegions = process.hltPhase2L3MuonPixelTracksTrackingRegions.clone()
    process.hltPhase2L3MuonHighPtTripletStepTrackingRegions = process.hltPhase2L3MuonPixelTracksTrackingRegions.clone()

    #Seeding
    layerList = ['BPix1+BPix2+BPix3+BPix4',
            'BPix1+BPix2+BPix3+FPix1_pos',
            'BPix1+BPix2+BPix3+FPix1_neg',
            'BPix1+BPix2+FPix1_pos+FPix2_pos',
            'BPix1+BPix2+FPix1_neg+FPix2_neg',
            'BPix1+FPix1_pos+FPix2_pos+FPix3_pos',
            'BPix1+FPix1_neg+FPix2_neg+FPix3_neg',
            'FPix1_pos+FPix2_pos+FPix3_pos+FPix4_pos',
            'FPix1_neg+FPix2_neg+FPix3_neg+FPix4_neg',
            'FPix2_pos+FPix3_pos+FPix4_pos+FPix5_pos',
            'FPix2_neg+FPix3_neg+FPix4_neg+FPix5_neg',
            'FPix3_pos+FPix4_pos+FPix5_pos+FPix6_pos',
            'FPix3_neg+FPix4_neg+FPix5_neg+FPix6_neg',
            'FPix4_pos+FPix5_pos+FPix6_pos+FPix7_pos',
            'FPix4_neg+FPix5_neg+FPix6_neg+FPix7_neg',
            'FPix5_pos+FPix6_pos+FPix7_pos+FPix8_pos',
            'FPix5_neg+FPix6_neg+FPix7_neg+FPix8_neg']

    from RecoTracker.TkSeedingLayers.seedingLayersEDProducer_cfi import seedingLayersEDProducer

    #Seed Layers
    process.hittrack = cms.PSet(
        HitProducer = cms.string('siPixelRecHits'),
        TTRHBuilder = cms.string('WithTrackAngle')
    )

    process.hltPhase2L3MuonPixelTracksSeedLayers = seedingLayersEDProducer.clone(
        BPix = process.hittrack,
        FPix = process.hittrack,
        layerList = cms.vstring(layerList)
    )

    process.hltPhase2L3MuonInitialStepSeedLayers = process.hltPhase2L3MuonPixelTracksSeedLayers.clone()

    #Pixel Tracks
    from RecoTracker.TkHitPairs.hitPairEDProducerDefault_cfi import hitPairEDProducerDefault
    process.hltPhase2L3MuonPixelTracksHitDoublets = hitPairEDProducerDefault.clone(
        layerPairs = cms.vuint32(0, 1, 2),
        maxElement = cms.uint32(5000000),
        clusterCheck = cms.InputTag("trackerClusterCheck"), 
        produceIntermediateHitDoublets = cms.bool(True),
        seedingLayers = cms.InputTag('hltPhase2L3MuonPixelTracksSeedLayers'),
        trackingRegions = cms.InputTag('hltPhase2L3MuonPixelTracksTrackingRegions'),
        )

    from RecoPixelVertexing.PixelTriplets.caHitQuadrupletEDProducer_cfi import caHitQuadrupletEDProducer
    process.hltPhase2L3MuonPixelTracksHitQuadruplets = caHitQuadrupletEDProducer.clone(
        CAPhiCut = cms.double(0.2),
        CAThetaCut = cms.double(0.0012),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('LowPtClusterShapeSeedComparitor'),
            clusterShapeCacheSrc = cms.InputTag('siPixelClusterShapeCache'),
            clusterShapeHitFilter = cms.string('ClusterShapeHitFilter')
        ),
        doublets = cms.InputTag('hltPhase2L3MuonPixelTracksHitDoublets'),
        extraHitRPhitolerance = cms.double(0.032),
        fitFastCircle = cms.bool(True), ##TOD
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

    from RecoPixelVertexing.PixelTrackFitting.pixelTrackFilterByKinematics_cfi import pixelTrackFilterByKinematics
    process.hltPhase2L3MuonPixelTrackFilterByKinematics = pixelTrackFilterByKinematics.clone(
        ptMin = cms.double(0.9),
    ) 
    
  
    process.hltPhase2L3MuonPixelTrackCleanerBySharedHits = cms.ESProducer( "PixelTrackCleanerBySharedHitsESProducer",
     useQuadrupletAlgo = cms.bool( False ),
     ComponentName = cms.string( "hltPhase2L3MuonPixelTrackCleanerBySharedHits" ),
     appendToDataLabel = cms.string( "" )
    )
  
    process.hltPhase2L3MuonPixelTrackFilterByKinematics = cms.EDProducer( "PixelTrackFilterByKinematicsProducer",
            nSigmaTipMaxTolerance = cms.double( 0.0 ),
        chi2 = cms.double( 1000.0 ),
        nSigmaInvPtTolerance = cms.double( 0.0 ),
        ptMin = cms.double( 0.9 ), #previous 0.1
        tipMax = cms.double( 1.0 )
    )

    process.hltPhase2L3MuonPixelFitterByHelixProjections = cms.EDProducer( "PixelFitterByHelixProjectionsProducer",
        scaleErrorsForBPix1 = cms.bool( False ),
        scaleFactor = cms.double( 0.65 )
    )
 
    process.hltPhase2L3MuonPixelTracks = cms.EDProducer('PixelTrackProducer',
        Cleaner = cms.string('hltPhase2L3MuonPixelTrackCleanerBySharedHits'),
        Filter = cms.InputTag('hltPhase2L3MuonPixelTrackFilterByKinematics'),
        Fitter = cms.InputTag('hltPhase2L3MuonPixelFitterByHelixProjections'),
        SeedingHitSets = cms.InputTag('hltPhase2L3MuonPixelTracksHitQuadruplets'),
        passLabel = cms.string('hltPhase2L3MuonPixelTracks'),
        mightGet = cms.untracked.vstring('RegionsSeedingHitSets_hltPhase2L3MuonPixelTracksHitQuadruplets__RECO')
    )

    from RecoPixelVertexing.PixelVertexFinding.PixelVertexes_cfi import pixelVertices

    process.hltPhase2L3MuonPixelVertices = pixelVertices.clone(
        PVcomparer = cms.PSet(refToPSet_ = cms.string('hltPhase2L3MuonPSetPvClusterComparerForIT')),
        TrackCollection = cms.InputTag('hltPhase2L3MuonPixelTracks'),
        ZOffset = cms.double(5.0),
        ZSeparation = cms.double(0.005),
    )

    process.hltPhase2L3MuonPSetPvClusterComparerForIT = cms.PSet(
        track_chi2_max = cms.double( 20.0 ),
        track_pt_max = cms.double( 100.0 ),
        # track_pt_max = cms.double(100.0 ),
        track_prob_min = cms.double( -1.0 ),
        track_pt_min = cms.double( 1.0 )

    )

    process.hltPhase2L3MuonHighPtTripletStepTrajectoryCleanerBySharedHits = cms.ESProducer('TrajectoryCleanerESProducer',
            ComponentName = cms.string('hltPhase2L3MuonHighPtTripletStepTrajectoryCleanerBySharedHits'),
            ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
            MissingHitPenalty = cms.double(20.0),
            ValidHitBonus = cms.double(5.0),
            allowSharedFirstHit = cms.bool(True),
            fractionShared = cms.double(0.16)
        )

    #Initia Step
    from RecoTracker.CkfPattern.GroupedCkfTrajectoryBuilder_cfi import GroupedCkfTrajectoryBuilder

    process.hltPhase2L3MuonInitialStepTrajectoryBuilder = GroupedCkfTrajectoryBuilder.clone(
            ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
            alwaysUseInvalidHits = cms.bool(False),
            estimator = cms.string('hltPhase2L3MuonInitialStepChi2Est'),
            inOutTrajectoryFilter = cms.PSet(
                refToPSet_ = cms.string('hltPhase2L3MuonInitialStepTrajectoryFilter')
            ),
            keepOriginalIfRebuildFails = cms.bool(True),
            maxCand = cms.int32(2),
            maxDPhiForLooperReconstruction = cms.double(2.0),
            maxPtForLooperReconstruction = cms.double(0.7),
            minNrOfHitsForRebuild = cms.int32(1),
            propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
            propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),

            trajectoryFilter = cms.PSet(
                refToPSet_ = cms.string('hltPhase2L3MuonInitialStepTrajectoryFilter')
            ),
            seedPairPenalty = cms.int32(0),
            minPt = cms.double(0.9),
            maxLostHitsFraction = cms.double(999.0), # previous 0.1
            maxNumberOfHits = cms.int32(100)
        )


    process.hltPhase2L3MuonHighPtTripletStepTrajectoryBuilder = process.hltPhase2L3MuonInitialStepTrajectoryBuilder.clone(
            ComponentType = cms.string('GroupedCkfTrajectoryBuilder'), #needs to stay like this for now
            MeasurementTrackerName = cms.string(''), #??
            TTRHBuilder = cms.string('WithTrackAngle'),
            alwaysUseInvalidHits = cms.bool(False), # previous True
            bestHitOnly = cms.bool(True),
            estimator = cms.string('hltPhase2L3MuonHighPtTripletStepChi2Est'),
            foundHitBonus = cms.double(10.0),
            inOutTrajectoryFilter = cms.PSet(
                refToPSet_ = cms.string('hltPhase2L3MuonHighPtTripletStepTrajectoryFilterInOut') #??
            ),
            intermediateCleaning = cms.bool(True),
            keepOriginalIfRebuildFails = cms.bool(False),
            lockHits = cms.bool(True),
            lostHitPenalty = cms.double(30.0),
            maxCand = cms.int32(2), # previous 3
            maxDPhiForLooperReconstruction = cms.double(2.0),
            maxPtForLooperReconstruction = cms.double(0.7),
            minNrOfHitsForRebuild = cms.int32(5),
            propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'), # previous PropagatorWithMaterial
            propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'), # previous PropagatorWithMaterialOpposite
            requireSeedHitsInRebuild = cms.bool(True),
            seedAs5DHit = cms.bool(False), #cmssw_11_0
            trajectoryFilter = cms.PSet(
                refToPSet_ = cms.string('hltPhase2L3MuonHighPtTripletStepTrajectoryFilter')
            ),
            updator = cms.string('KFUpdator'),
            useSameTrajFilter = cms.bool(False)
        )


    from RecoTracker.MeasurementDet.Chi2ChargeMeasurementEstimator_cfi import Chi2ChargeMeasurementEstimator

    process.hltPhase2L3MuonInitialStepChi2Est = Chi2ChargeMeasurementEstimator.clone(
        ComponentName = cms.string('hltPhase2L3MuonInitialStepChi2Est'),
        MaxChi2 = cms.double(9.0),
        MaxDisplacement = cms.double(0.5),
        MaxSagitta = cms.double(2),
        MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
        MinimalTolerance = cms.double(0.5),
        appendToDataLabel = cms.string(''),
        clusterChargeCut = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutLoose')
        ),
        nSigma = cms.double(3.0),
        pTChargeCutThreshold = cms.double(15.0)
    )

    process.hltPhase2L3MuonHighPtTripletStepChi2Est = process.hltPhase2L3MuonInitialStepChi2Est.clone(
        ComponentName = cms.string('hltPhase2L3MuonHighPtTripletStepChi2Est'),
        MaxChi2 = cms.double(16.0),
        nSigma = cms.double(3),
        pTChargeCutThreshold = cms.double(-1),
    )

    from TrackingTools.TrajectoryFiltering.TrajectoryFilter_cff import CkfBaseTrajectoryFilter_block
    process.hltPhase2L3MuonInitialStepTrajectoryFilter = CkfBaseTrajectoryFilter_block.clone(
            maxLostHits = cms.int32(1),
        constantValueForLostHitsFractionFilter = cms.double(1.0),
            minHitsMinPt = cms.int32(4),
            minPt = cms.double(0.9),
            minimumNumberOfHits = cms.int32(4),
            maxNumberOfHits = cms.int32(100),
            maxCCCLostHits = cms.int32(0),
        maxLostHitsFraction = cms.double(999),
        )

    process.hltPhase2L3MuonHighPtTripletStepTrajectoryFilterInOut = CkfBaseTrajectoryFilter_block.clone(
            maxNumberOfHits = cms.int32(100),
            minimumNumberOfHits = cms.int32(4),
            nSigmaMinPt = cms.double(5.0),
            seedExtension = cms.int32(1),
            minPt = cms.double(0.9)
        )

    process.hltPhase2L3MuonHighPtTripletStepTrajectoryFilterBase = CkfBaseTrajectoryFilter_block.clone(
                ComponentType = cms.string('CkfBaseTrajectoryFilter'),
                chargeSignificance = cms.double(-1.0),
                constantValueForLostHitsFractionFilter = cms.double(1.0),
                extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
                maxCCCLostHits = cms.int32(0),
                maxConsecLostHits = cms.int32(1),
                maxLostHits = cms.int32(1),
                maxLostHitsFraction = cms.double(999.0),
        minPt = cms.double(0.9),
                minimumNumberOfHits = cms.int32(3),
        seedExtension = cms.int32(1)
            )

    process.hltPhase2L3MuonHighPtTripletStepTrajectoryFilter = cms.PSet(
        ComponentType = cms.string('CompositeTrajectoryFilter'),
        filters = cms.VPSet(
            cms.PSet(
                refToPSet_ = cms.string('hltPhase2L3MuonHighPtTripletStepTrajectoryFilterBase')
            ),
            cms.PSet(
                refToPSet_ = cms.string('ClusterShapeTrajectoryFilter')
            )
        )
    )


    from RecoTracker.CkfPattern.CkfTrackCandidates_cfi import ckfTrackCandidates


    process.hltPhase2L3MuonInitialStepTrackCandidates = ckfTrackCandidates.clone(
       
        propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
        SimpleMagneticField = cms.string('ParabolicMf'),
        TrajectoryBuilderPSet = cms.PSet(
            refToPSet_ = cms.string('hltPhase2L3MuonInitialStepTrajectoryBuilder')
        ),
        maxNSeeds = cms.uint32(100000),
        maxSeedsBeforeCleaning = cms.uint32(1000),
        numHitsForSeedCleaner = cms.int32(50),
        onlyPixelHitsForSeedCleaner = cms.bool(True),
        src = cms.InputTag('hltPhase2L3MuonInitialStepSeeds'),
        useHitsSplitting = cms.bool(False),


    )

    process.hltPhase2L3MuonHighPtTripletStepTrackCandidates = process.hltPhase2L3MuonInitialStepTrackCandidates.clone(
        propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
        TrajectoryBuilderPSet = cms.PSet(
            refToPSet_ = cms.string('hltPhase2L3MuonHighPtTripletStepTrajectoryBuilder')
        ),
        TrajectoryCleaner = cms.string('hltPhase2L3MuonHighPtTripletStepTrajectoryCleanerBySharedHits'),

        phase2clustersToSkip = cms.InputTag('hltPhase2L3MuonHighPtTripletStepClusters'),
        src = cms.InputTag('hltPhase2L3MuonHighPtTripletStepSeeds'),
    )


    process.hltPhase2L3MuonHighPtTripletStepSeeds = cms.EDProducer('SeedCreatorFromRegionConsecutiveHitsEDProducer',
        MinOneOverPtError = cms.double(1),
        OriginTransverseErrorMultiplier = cms.double(1),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('none')
        ),
        SeedMomentumForBOFF = cms.double(5),
        TTRHBuilder = cms.string('WithTrackAngle'),
        forceKinematicWithRegionDirection = cms.bool(False),
        magneticField = cms.string(''),
        propagator = cms.string('PropagatorWithMaterial'),
        seedingHitSets = cms.InputTag('hltPhase2L3MuonHighPtTripletStepHitTriplets')
    )

    from RecoTracker.TrackProducer.TrackProducer_cfi import TrackProducer

    process.hltPhase2L3MuonInitialStepTracks = TrackProducer.clone(
        AlgorithmName = cms.string('initialStep'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        TTRHBuilder = cms.string('WithTrackAngle'),
        src = cms.InputTag('hltPhase2L3MuonInitialStepTrackCandidates'),
        useHitsSplitting = cms.bool(False),
    )

    process.hltPhase2L3MuonHighPtTripletStepTracks = process.hltPhase2L3MuonInitialStepTracks.clone(
        AlgorithmName = cms.string('highPtTripletStep'),
        src = cms.InputTag("hltPhase2L3MuonHighPtTripletStepTrackCandidates"),
    )

    process.hltPhase2L3MuonInitialStepTrackCutClassifier = cms.EDProducer('TrackCutClassifier',
        beamspot = cms.InputTag('offlineBeamSpot'),
        ignoreVertices = cms.bool(False),
        mva = cms.PSet(
            dr_par = cms.PSet(
                d0err = cms.vdouble(0.003, 0.003, 0.003),
                d0err_par = cms.vdouble(0.001, 0.001, 0.001),
                dr_exp = cms.vint32(4, 4, 4),
                dr_par1 = cms.vdouble(0.8, 0.7, 0.6),
                dr_par2 = cms.vdouble(0.6, 0.5, 0.45)
            ),
            dz_par = cms.PSet(
                dz_exp = cms.vint32(4, 4, 4),
                dz_par1 = cms.vdouble(0.9, 0.8, 0.7),
                dz_par2 = cms.vdouble(0.8, 0.7, 0.55)
            ),
            maxChi2 = cms.vdouble(9999.0, 25.0, 16.0),
            maxChi2n = cms.vdouble(2.0, 1.4, 1.2),
            maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
            maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
            maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
            maxLostLayers = cms.vint32(3, 2, 2),
            min3DLayers = cms.vint32(3, 3, 3),
            minLayers = cms.vint32(3, 3, 3),
            minNVtxTrk = cms.int32(3),
            minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
            minPixelHits = cms.vint32(0, 0, 3)
        ),
        qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
        src = cms.InputTag('hltPhase2L3MuonInitialStepTracks'),
        vertices = cms.InputTag('hltPhase2L3MuonPixelVertices')
    )

    process.hltPhase2L3MuonInitialStepTracksSelectionHighPurity = cms.EDProducer('TrackCollectionFilterCloner',
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string("highPurity"),
        originalMVAVals = cms.InputTag('hltPhase2L3MuonInitialStepTrackCutClassifier','MVAValues'),
        originalQualVals = cms.InputTag('hltPhase2L3MuonInitialStepTrackCutClassifier','QualityMasks'),
        originalSource = cms.InputTag('hltPhase2L3MuonInitialStepTracks')
        # originalSource = cms.InputTag('hltPhase2L3MuonInitialStepTracks','','RECO2')
    )

    process.hltPhase2L3MuonHighPtTripletStepClusters = cms.EDProducer('TrackClusterRemoverPhase2',
        TrackQuality = cms.string('highPurity'),
        maxChi2 = cms.double(9.0),
        mightGet = cms.optional.untracked.vstring,
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
        oldClusterRemovalInfo = cms.InputTag(''),
        overrideTrkQuals = cms.InputTag(''),
        phase2OTClusters = cms.InputTag('siPhase2Clusters'),
        phase2pixelClusters = cms.InputTag('siPixelClusters'),
        trackClassifier = cms.InputTag('','QualityMasks'),
        trajectories = cms.InputTag('hltPhase2L3MuonInitialStepTracksSelectionHighPurity')
    )

    process.hltPhase2L3MuonHighPtTripletStepSeedLayers = cms.EDProducer('SeedingLayersEDProducer',
        BPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag('hltPhase2L3MuonHighPtTripletStepClusters')
        ),
        FPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag('hltPhase2L3MuonHighPtTripletStepClusters')
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
            'BPix1+FPix2_pos+FPix3_pos',
            'BPix1+FPix2_neg+FPix3_neg',
            'FPix2_pos+FPix3_pos+FPix4_pos',
            'FPix2_neg+FPix3_neg+FPix4_neg',
            'FPix3_pos+FPix4_pos+FPix5_pos',
            'FPix3_neg+FPix4_neg+FPix5_neg',
            'FPix4_pos+FPix5_pos+FPix6_pos',
            'FPix4_neg+FPix5_neg+FPix6_neg',
            'FPix5_pos+FPix6_pos+FPix7_pos',
            'FPix5_neg+FPix6_neg+FPix7_neg',
            'FPix6_pos+FPix7_pos+FPix8_pos',
            'FPix6_neg+FPix7_neg+FPix8_neg'
        ),
        mightGet = cms.optional.untracked.vstring
    )

    process.hltPhase2L3MuonHighPtTripletStepHitDoublets = cms.EDProducer('HitPairEDProducer',
        clusterCheck = cms.InputTag('trackerClusterCheck'),
        layerPairs = cms.vuint32(0, 1),
        maxElement = cms.uint32(50000000),
        maxElementTotal = cms.uint32(50000000),
        mightGet = cms.optional.untracked.vstring,
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag('hltPhase2L3MuonHighPtTripletStepSeedLayers'),
        trackingRegions = cms.InputTag('hltPhase2L3MuonHighPtTripletStepTrackingRegions'),
        trackingRegionsSeedingLayers = cms.InputTag('')
    )

    process.hltPhase2L3MuonHighPtTripletStepHitTriplets = cms.EDProducer('CAHitTripletEDProducer',
        CAHardPtCut = cms.double(0.5),
        CAPhiCut = cms.double(0.06),
        CAThetaCut = cms.double(0.003),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('LowPtClusterShapeSeedComparitor'),
            clusterShapeCacheSrc = cms.InputTag('siPixelClusterShapeCache'),
            clusterShapeHitFilter = cms.string('ClusterShapeHitFilter')
        ),
        doublets = cms.InputTag('hltPhase2L3MuonHighPtTripletStepHitDoublets'),
        extraHitRPhitolerance = cms.double(0.032),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.8),
            pt2 = cms.double(8),
            value1 = cms.double(100),
            value2 = cms.double(6)
        ),
        useBendingCorrection = cms.bool(True),
        mightGet = cms.untracked.vstring('IntermediateHitDoublets_highPtTripletStepHitDoublets__RECO'),
    )

    process.hltPhase2L3MuonHighPtTripletStepTrackCutClassifier = cms.EDProducer('TrackCutClassifier',
        beamspot = cms.InputTag('offlineBeamSpot'),
        ignoreVertices = cms.bool(False),
        mva = cms.PSet(
            dr_par = cms.PSet(
                d0err = cms.vdouble(0.003, 0.003, 0.003),
                d0err_par = cms.vdouble(0.002, 0.002, 0.001),
                dr_exp = cms.vint32(4, 4, 4),
                dr_par1 = cms.vdouble(0.7, 0.6, 0.6),
                dr_par2 = cms.vdouble(0.6, 0.5, 0.45)
            ),
            dz_par = cms.PSet(
                dz_exp = cms.vint32(4, 4, 4),
                dz_par1 = cms.vdouble(0.8, 0.7, 0.7),
                dz_par2 = cms.vdouble(0.6, 0.6, 0.55)
            ),
            maxChi2 = cms.vdouble(9999.0, 9999.0, 9999.0),
            maxChi2n = cms.vdouble(2.0, 1.0, 0.8),
            maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
            maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
            maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
            maxLostLayers = cms.vint32(3, 3, 2),
            min3DLayers = cms.vint32(3, 3, 4),
            minLayers = cms.vint32(3, 3, 4),
            minNVtxTrk = cms.int32(3),
            minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
            minPixelHits = cms.vint32(0, 0, 3)
        ),
        qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
        src = cms.InputTag('hltPhase2L3MuonHighPtTripletStepTracks'),
        vertices = cms.InputTag('hltPhase2L3MuonPixelVertices')
    )

    process.hltPhase2L3MuonHighPtTripletStepTracksSelectionHighPurity = cms.EDProducer('TrackCollectionFilterCloner',
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string('highPurity'),
        originalMVAVals = cms.InputTag('hltPhase2L3MuonHighPtTripletStepTrackCutClassifier','MVAValues'),
        originalQualVals = cms.InputTag('hltPhase2L3MuonHighPtTripletStepTrackCutClassifier','QualityMasks'),
        originalSource = cms.InputTag('hltPhase2L3MuonHighPtTripletStepTracks')
        # originalSource = cms.InputTag('hltPhase2L3MuonHighPtTripletStepTracks','','RECO2')
    )

    process.hltPhase2L3MuonTrackAlgoPriorityOrder = cms.ESProducer('TrackAlgoPriorityOrderESProducer',
        ComponentName = cms.string('hltPhase2L3MuonTrackAlgoPriorityOrder'),
        algoOrder = cms.vstring(
            'initialStep',
            'highPtTripletStep'
        ),
        appendToDataLabel = cms.string('')
    )

    process.hltPhase2L3MuonGeneralTracks = cms.EDProducer('TrackListMerger',
        Epsilon = cms.double(-0.001),
        FoundHitBonus = cms.double(5.0),
        LostHitPenalty = cms.double(5.0),
        MaxNormalizedChisq = cms.double(1000.0),
        MinFound = cms.int32(3),
        MinPT = cms.double(0.9),
        ShareFrac = cms.double(0.19),
        TrackProducers = cms.VInputTag('hltPhase2L3MuonInitialStepTracksSelectionHighPurity', 'hltPhase2L3MuonHighPtTripletStepTracksSelectionHighPurity'),
        allowFirstHitShare = cms.bool(True),
        copyExtras = cms.untracked.bool(True),
        copyMVA = cms.bool(False),
        hasSelector = cms.vint32(0, 0),
        indivShareFrac = cms.vdouble(1.0, 1.0),
        makeReKeyedSeeds = cms.untracked.bool(False),
        newQuality = cms.string('confirmed'),
        selectedTrackQuals = cms.VInputTag(cms.InputTag('hltPhase2L3MuonInitialStepTracksSelectionHighPurity'), cms.InputTag('hltPhase2L3MuonHighPtTripletStepTracksSelectionHighPurity')),
        setsToMerge = cms.VPSet(cms.PSet(
            pQual = cms.bool(True),
            tLists = cms.vint32(0, 1)
        )),
        trackAlgoPriorityOrder = cms.string('hltPhase2L3MuonTrackAlgoPriorityOrder'),
        writeOnlyTrkQuals = cms.bool(False)
    )

    return process

def customise_hltPhase2_TRKv06_1_L3Muon(process):

    process = customise_common_L3Muon(process)

    process.hltPhase2L3MuonSeedFromProtoTracks = cms.PSet(
      TTRHBuilder = cms.string( "WithTrackAngle"), #hltESPTTRHBuilderPixelOnly" ),
      SeedMomentumForBOFF = cms.double( 5.0 ),
      propagator = cms.string( "PropagatorWithMaterial"),#" ), #
      forceKinematicWithRegionDirection = cms.bool( False ),
      magneticField = cms.string( ""), #" ),
      OriginTransverseErrorMultiplier = cms.double( 1.0 ),
      ComponentName = cms.string( "SeedFromConsecutiveHitsCreator" ),
      MinOneOverPtError = cms.double( 1.0 )
    )

    process.hltPhase2L3MuonInitialStepSeeds = cms.EDProducer( "SeedGeneratorFromProtoTracksEDProducer",
        useEventsWithNoVertex = cms.bool( True ),
        originHalfLength = cms.double(0.3),
        useProtoTrackKinematics = cms.bool( False ),
        usePV = cms.bool( True ),
        SeedCreatorPSet = cms.PSet(  refToPSet_ = cms.string( "hltPhase2L3MuonSeedFromProtoTracks" ) ),
        InputVertexCollection = cms.InputTag(""),
        TTRHBuilder = cms.string( "WithTrackAngle"), #hltESPTTRHBuilderPixelOnly" ),
        InputCollection = cms.InputTag( "hltPhase2L3MuonPixelTracks" ),
        originRadius = cms.double( 0.1 )
    )

    process.hltPhase2L3MuonPixelTracksSequence = cms.Sequence(
        process.hltPhase2L3MuonPixelTrackFilterByKinematics +
       # process.hltPhase2L3MuonPixelTrackCleanerBySharedHits +
        process.hltPhase2L3MuonPixelFitterByHelixProjections +
        process.hltPhase2L3MuonPixelTracksTrackingRegions +  # = hlt
        process.hltPhase2L3MuonPixelTracksSeedLayers +
        process.hltPhase2L3MuonPixelTracksHitDoublets +
        process.hltPhase2L3MuonPixelTracksHitQuadruplets +
        process.hltPhase2L3MuonPixelTracks
    )

    process.hltPhase2L3MuonPixelVerticesSequence = cms.Sequence(
        process.hltPhase2L3MuonPixelVertices
    )

    process.hltPhase2L3MuonInitialStepSequence = cms.Sequence(
        process.hltPhase2L3MuonInitialStepSeeds +
        process.hltPhase2L3MuonInitialStepTrackCandidates +
        process.hltPhase2L3MuonInitialStepTracks +
        process.hltPhase2L3MuonInitialStepTrackCutClassifier +
        process.hltPhase2L3MuonInitialStepTracksSelectionHighPurity
    )

    process.hltPhase2L3MuonHighPtTripletStepSequence = cms.Sequence(
        process.hltPhase2L3MuonHighPtTripletStepClusters +
        process.hltPhase2L3MuonHighPtTripletStepSeedLayers +
        process.hltPhase2L3MuonHighPtTripletStepTrackingRegions +
        process.hltPhase2L3MuonHighPtTripletStepHitDoublets +
        process.hltPhase2L3MuonHighPtTripletStepHitTriplets +
        process.hltPhase2L3MuonHighPtTripletStepSeeds +
        process.hltPhase2L3MuonHighPtTripletStepTrackCandidates +
        process.hltPhase2L3MuonHighPtTripletStepTracks +
        process.hltPhase2L3MuonHighPtTripletStepTrackCutClassifier +
        process.hltPhase2L3MuonHighPtTripletStepTracksSelectionHighPurity
    )

    if hasattr(process,"trackTimeValueMapProducer"):
        del process.trackTimeValueMapProducer
    if hasattr(process,"gsfTrackTimeValueMapProducer"):
        del process.gsfTrackTimeValueMapProducer
    if hasattr(process, 'globalreco_trackingTask'):
        del process.globalreco_trackingTask

    return process



