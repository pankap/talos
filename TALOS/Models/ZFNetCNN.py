# =====================================================================================================================
#        
#        Tensor Abstraction Layer Objects 0.0.8-ALPHA
#        TALOS IMPLEMENTATION OF ZFNET [1]
#
#        Framework design/Model implementation by Pantelis I. Kaplanoglou
#        Licensed under the MIT License
#
# ---------------------------------------------------------------------------------------------------------------------
#
#  [1] M. D. Zeiler and R. Fergus, "Visualizing and Understanding Convolutional Networks,"
#      in Computer Vision � ECCV 2014, 2014, pp. 818�833.
#
# =====================================================================================================================
import TALOS.Constants as tcc
from TALOS.DeepCNN import DCNN,InputColorImageAndClass,ConvMaxPoolLRN,FullyConnectedWithDropout,SoftMax
from TALOS.HyperParams import NNLearnParams


#==================================================================================================
class ZFNet(DCNN):
    #------------------------------------------------------------------------------------
    def __init__(self, p_oSettings, p_oExperiment=None):
        #........ |  Instance Attributes | ..............................................
        #................................................................................
        super(ZFNet, self).__init__("ZFNetBase", None, p_oExperiment=p_oExperiment, p_oSettings=p_oSettings)
    #------------------------------------------------------------------------------------
    def CreateModules(self):
        oFeatures = [3, 96, 256, 384, 384, 256, 4096, 4096, self.Settings.ClassCount]
        self.InputModule=InputColorImageAndClass(self, self.Settings.ImageDimensions, self.Settings.BatchSize)
        ConvMaxPoolLRN(self, 1, oFeatures[1], (7,7)  , 2, (3,3), 2  , p_bIsLRN=True, p_nActivationType=tcc.NAF_RELU, p_bIsPaddingConv=False)
        ConvMaxPoolLRN(self, 2, oFeatures[2], (5,5)  , 2, (3,3), 2  , p_bIsLRN=True, p_nActivationType=tcc.NAF_RELU)
        
        ConvMaxPoolLRN(self, 3, oFeatures[3], (3,3)  , 1, None, None, p_bIsLRN=True, p_nActivationType=tcc.NAF_RELU)
        ConvMaxPoolLRN(self, 4, oFeatures[4], (3,3)  , 1, None, None, p_bIsLRN=True, p_nActivationType=tcc.NAF_RELU)
        ConvMaxPoolLRN(self, 5, oFeatures[5], (3,3)  , 1, (3,3), 2  , p_bIsLRN=True, p_nActivationType=tcc.NAF_RELU)
        FullyConnectedWithDropout(self, 6, oFeatures[6], p_nDropoutKeepProbability=0.5, p_nActivationType=tcc.NAF_TANH)
        FullyConnectedWithDropout(self, 7, oFeatures[7], p_nDropoutKeepProbability=0.5, p_nActivationType=tcc.NAF_TANH)
        self.OutputModule = SoftMax(self, 8, oFeatures[8])  
    #------------------------------------------------------------------------------------
    def OldSetupLearning(self):
        self.LearnParams=NNLearnParams()
        self.LearnParams.IsShuffling=True
        
        bLegacySetup=False
            
        #self.LearnParams.SetTrainingMethodType(tcc.TRN_MOMENTUM)
        self.LearnParams.SetTrainingMethodType(tcc.TRN_ADAM)
        
        #VACC: 41% TRERR < 0.5
        #self.LearnParams.LearningRate = 0.0001
        #self.LearnParams.Epsilon = 0.001
        
        if self.LearnParams.TrainingMethodType == tcc.TRN_ADAM:      
            #self.LearnParams.LearningRate = 0.00002
            self.LearnParams.LearningRate = 0.00006
            self.LearnParams.Epsilon = 0.001
            
            
            
            
            self.LearnParams.MinTrainingEpochs = 20
            self.LearnParams.MaxTrainingEpochs = 40
            
            if False:
                self.LearnParams.MarginRatioPositive = 1.3
                self.LearnParams.MarginRatioNegative = 1.8
            
            if False:
                # 35% with SGD #201712_42912
                # 47% with ADAM #201712_43139
                # 46% with ADAM filtering out strongly classified #201712_43242
                self.LearnParams
                
            self.LearnParams.IsMargin = True
            self.LearnParams.MarginType = 11
            self.LearnParams.MarginRatioPositive = 0.2
            self.LearnParams.MarginRatioNegative = 0.05
            self.LearnParams.Margin.MarginFullyClassified = 0.9
            
            if False:
                #
                self.LearnParams.Margin.MarginFullyClassified = 0.8
            
            # LITE100
            self.LearnParams.MaxTrainingEpochs = 30
            
            
            
            # ADAM Plain for DCROWD60
            if False:
                self.LearnParams.IsMargin = False      
                self.LearnParams.MaxTrainingEpochs = 50
            
            # ADAM 2 for DCROWD60
            if True:
                self.LearnParams.IsMargin = False      
                self.LearnParams.MaxTrainingEpochs = 50
                self.LearnParams.LearningRate = 0.001
                self.LearnParams.Epsilon = 0.001
                            
            # ADAM 2 for LITE20
            if True:
                self.LearnParams.IsMargin = False      
                self.LearnParams.MaxTrainingEpochs = 50
                self.LearnParams.LearningRate = 0.00006
                self.LearnParams.Epsilon = 0.001                            
                          
        
        elif self.LearnParams.TrainingMethodType == tcc.TRN_MOMENTUM:
            if bLegacySetup:
                self.LearnParams.Momentum=0.90
                self.LearnParams.LearningRate=0.0006 
        
                self.LearnParams.AcceptableAccuracy=0.39
                self.LearnParams.PseudoRandomSeed=EXPERIMENT_RANDOM_SEED
                
                self.LearnParams.IsAdaptiveLearning=False
                #ORIGINAL SETUP VALUE: self.LearnParams.AdaptMaxLearningRate=0.1
                
                self.LearnParams.StopConditionInc=[18,20,20]
                self.LearnParams.StopConditionDecDiv=[2,2,4]
                self.LearnParams.LimitUnchangedBestEpoch=12
            else:
                # Same as ZFNet
                #self.LearnParams.SetAdaptiveLearningParams(0.85, 0.0001, p_nMaxLearningRate=0.06)#0.008) #6000-RUN-2
                            
                #self.LearnParams.SetAdaptiveLearningParams(0.90, 0.0001, p_nMaxLearningRate=0.06)#0.008) #6000-RUN-3
                
                #self.LearnParams.SetAdaptiveLearningParams(0.90, 0.0006, p_nMaxLearningRate=0.06)#0.008) #6000-RUN-4, #Setup1
                
                #self.LearnParams.SetAdaptiveLearningParams(0.90, 0.0001, p_nMaxLearningRate=0.06)#Setup2
                
                #self.LearnParams.SetAdaptiveLearningParams(0.90, 0.00025, p_nMaxLearningRate=0.06)#Setup3
    
                #self.LearnParams.SetAdaptiveLearningParams(0.90, 0.001, p_nMaxLearningRate=0.06)#Setup4 
                
                #self.LearnParams.SetAdaptiveLearningParams(0.90, 0.0006, p_nMaxLearningRate=0.06)#0.008) #6000-RUN-4, #Setup1
                
                #MINIBATCH:40 #self.LearnParams.SetAdaptiveLearningParams(0.95, 0.0001, p_nMaxLearningRate=0.06)#0.008) #6000-RUN-2
                
                
                #self.LearnParams.SetAdaptiveLearningParams(0.92, 0.0006, p_nMaxLearningRate=0.06) #Minibatch 15
                
                
                #Default with margin function
                
                self.LearnParams.IsMargin = True
                
                if False:
                    self.LearnParams.SetAdaptiveLearningParams(0.0, 0.0006, p_nMaxLearningRate=0.06) #Minibatch 15
                    self.LearnParams.MarginType = 0
                    self.LearnParams.MarginRatioPositive = 1.3
                    self.LearnParams.MarginRatioNegative = 2.5
                
                if False:
                    # 201712_42616
                    self.LearnParams.SetAdaptiveLearningParams(0.0, 0.0006, p_nMaxLearningRate=0.06) #Minibatch 15
                    self.LearnParams.MarginType = 4
                    self.LearnParams.MarginRatioPositive = 1.3
                if False:
                    self.LearnParams.SetAdaptiveLearningParams(0.0, 0.001, p_nMaxLearningRate=0.06) #Minibatch 15
                    self.LearnParams.MarginType = 8
                    self.LearnParams.MarginRatioPositive = 0.7
                    self.LearnParams.MarginRatioNegative = 0.9                
                
                #201712_42912
                self.LearnParams.SetAdaptiveLearningParams(0.0, 0.001, p_nMaxLearningRate=0.06) #Minibatch 15
                self.LearnParams.MarginType = 11
                self.LearnParams.MarginRatioPositive = 0.2
                self.LearnParams.MarginRatioNegative = 0.05 #0.3           

                            
    
                self.LearnParams.AdaptDeltaValErr=0.02 #Setup1
                
                self.LearnParams.AdaptSlowKickIn=False
                self.LearnParams.AdaptBoostFirstEpochs=True
                #Early stopping with APER monitoring
                self.LearnParams.StopLimitUnchangedBestEpoch=10            
                self.LearnParams.AccuracyHighLimit=0.52
                self.LearnParams.AccuracyLowLimit=0.38        
                
                
                self.LearnParams.LimitOverfit=15
                self.LearnParams.MinDeltaValErr=0.00001
                self.LearnParams.MinValidationErrorStd=0.00001
        
                # ... Stop conditions ...
                self.LearnParams.MinTrainingEpochs=30
                self.LearnParams.MaxTrainingEpochs=60
                
                self.LearnParams.StopConditionInc=[10,6,20]
                self.LearnParams.StopConditionDecDiv=[2,2,4]
                self.LearnParams.StopBigIncreaseValErr=1.2
                self.LearnParams.StopBigDecreaseValAcc=-0.2
            
                #ORIGINAL SETUP VALUE: self.LearnParams.MiniBatches.SetSamplesPerBatch(30, 11, 19)                           
    #------------------------------------------------------------------------------------
                    
#==================================================================================================