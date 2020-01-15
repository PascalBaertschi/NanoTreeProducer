import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TreeProducer import *
from CorrectionTools.PileupWeightTool import *
from CorrectionTools.BTaggingTool import BTagWeightTool, BTagWPs
import struct
import numpy as np

class AK4btagProducer(Module):

    def __init__(self, name, DataType, filelist):
        
        self.name = name
        self.out = TreeProducer(name)
        self.sample = filelist

        if DataType=='data':
            self.isData = True
            self.isMC = False
        else:
            self.isData = False
            self.isMC = True
        if not self.isData:
            self.puTool = PileupWeightTool(year = 2017)
            self.btagTool = BTagWeightTool('CSVv2','medium',channel='mutau',year = 2017)
    def beginJob(self):
        pass

    def endJob(self):
        self.out.outputfile.Write()
        self.out.outputfile.Close()

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):     
        pass


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if self.isData and event.PV_npvs == 0:
            return False
        if not self.isData:
            self.out.pileup.Fill(event.Pileup_nTrueInt)
            if event.Pileup_nTrueInt == 0:
                return False

        #####   set variables     ####
        
        self.nElectrons            = 0
        self.nMuons                = 0
        self.nTaus                 = 0
        self.nFatJets              = 0
        
        self.EventWeight           = 0.
        self.TopWeight             = 0.
        self.BTagAK8Weight         = 0.
        self.BTagAK4Weight         = 0.
        self.BBTagWeight           = 0.
        self.isZtoMM               = False
        self.isZtoEE               = False
        self.isZtoNN               = False
        self.isWtoMN               = False
        self.isWtoEN               = False
        self.isTtoEM               = False
        self.isVtoQQ               = False
        self.isTveto               = False
        self.isBoostedTau          = False
        self.isBoosted4B           = False
        self.nTaus                 = 0
        self.nJetsNoFatJet         = 0
        self.JetMetDPhi            = 0.
        self.VHDEta                = 0.
        self.MinJetMetDPhi         = 0.
        self.MaxJetNoFatJetBTag    = 0.
        self.CosThetaStar          = 0.
        self.CosTheta1             = 0.
        self.CosTheta2             = 0.
        self.H_pt                  = 0.
        self.H_eta                 = 0.
        self.H_phi                 = 0.
        self.H_mass                = 0.
        self.H_tau21               = 0.
        self.H_ddt                 = 0.
        self.H_csv1                = 0.
        self.H_csv2                = 0.
        self.H_flav1               = 0.
        self.H_flav2               = 0.
        self.H_dbt                 = 0.
        self.H_ntag                = 0
        self.V_pt                  = 0.
        self.V_eta                 = 0.
        self.V_phi                 = 0.
        self.V_mass                = 0. 
        self.V_tau21               = 0.
        self.V_ddt                 = 0.
        self.V_csv1                = 0.
        self.V_csv2                = 0.
        self.V_dbt                 = 0.
        self.X_pt                  = 0.
        self.X_eta                 = 0.
        self.X_phi                 = 0.
        self.X_mass                = 0.
        
        idx_electrons = []
        idx_loose_electrons = []
        idx_muons = []
        idx_loose_muons = []
        idx_fatjet = []
        idx_jet = []
        idx_jets = []

        electrons_tlv_list = []
        loose_electrons_tlv_list = []
        muons_tlv_list = []
        loose_muons_tlv_list = []
        fatjet_tlv_list = []
        jet_tlv_list = []
        jets_tlv_list = []
        fatjet_tau21_list = []
        fatjet_nbtag_list = []

        V = ROOT.TLorentzVector()
        H = ROOT.TLorentzVector()
        X = ROOT.TLorentzVector()

        #########     cuts    #########
        elec1_pt_cut = 55.
        elec2_pt_cut = 20.
        elec_pt_cut = 10.
        elec_eta_cut = 2.5
        muon1_pt_cut = 55.
        muon2_pt_cut = 20.          
        muon_pt_cut = 10.
        muon_eta_cut = 2.4
        tau_pt_cut = 18.
        tau_eta_cut = 2.3
        ak4_pt_cut = 30.
        ak4_eta_cut = 2.4
        fatjet_pt_cut = 200.
        fatjet_eta_cut = 2.4
        met_pt_cut = 250.
        v_pt_cut = 200.
        tau21_lowercut = 0.35
        tau21_uppercut = 0.75
        j_mass_lowercut = 30.
        j_mass_uppercut = 250.
        v_mass_lowercut = 65.
        v_mass_intercut = 85.
        v_mass_uppercut = 105.
        h_mass_lowercut = 105.
        h_mass_uppercut = 135.
        x_mass_lowercut = 750.
        xt_mass_lowercut = 650.
        xjj_mass_lowercut = 950.
        

    
        #########     triggers     #########
        trigger_SingleMu      = all([event.HLT_Mu50,
                                     event.HLT_TkMu100])
                                #old: event.HLT_TkMu50
        trigger_SingleIsoMu   = event.HLT_IsoMu27
                                #no replacement for: event.HLT_IsoTkMu27
        trigger_DoubleMu      = event.HLT_Mu37_TkMu27
                                #old: event.HLT_Mu27_TkMu8
        trigger_DoubleIsoMu   = event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ
                                #no replacement for: event.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ
        trigger_SingleEle     = event.HLT_Ele115_CaloIdVT_GsfTrkIdT
                                #no replacement for: event.HLT_Ele105_CaloIdVT_GsfTrkIdT
        trigger_SingleIsoEle  = all([event.HLT_Ele32_WPTight_Gsf,
                                     event.HLT_Ele27_WPTight_Gsf,
                                     event.HLT_Ele20_WPLoose_Gsf,
                                     event.HLT_Ele28_eta2p1_WPTight_Gsf_HT150])
                                     #old:event.HLT_Ele27_WPLoose_Gsf and event.HLT_Ele32_eta2p1_WPTight_Gsf
        trigger_DoubleIsoEle  = event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ
                                #old: event.HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ
        trigger_DoubleEle     = event.HLT_DoubleEle33_CaloIdL_MW
                                #old: event.HLT_DoubleEle33_CaloIdL_GsfTrkIdVL
        trigger_METMHTNoMu    = all([event.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight,
                                     event.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight,
                                     event.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight])
                                     #old:  event.HLT_MonoCentralPFJet80_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight
                                     # no replacement for event.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight and event.HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight and event.HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight
        trigger_METMHT        = all([event.HLT_PFMET110_PFMHT110_IDTight, 
                                     event.HLT_PFMET120_PFMHT120_IDTight])
        trigger_MET           = all([event.HLT_PFMET200_HBHECleaned,
                                     event.HLT_PFMET200_HBHE_BeamHaloCleaned])
                                     #old: event.HLT_PFMET170_NoiseCleaned and event.HLT_PFMET170_HBHECleaned and event.HLT_PFMET170_HBHE_BeamHaloCleaned
        trigger_JET           = all([event.HLT_PFJet450,
                                     event.HLT_AK8PFJet450])
        trigger_HT            = all([event.HLT_PFHT780,
                                     event.HLT_PFHT890])
                                     #old: event.HLT_PFHT900 and event.HLT_PFHT800
        trigger_HT_PS         =  all([event.HLT_PFJet320,
                                      event.HLT_PFJet550])
                                      #old: event.HLT_PFHT650
        trigger_SUBJET        = event.HLT_AK8PFJet360_TrimMass30
        trigger_SUBHT         = event.HLT_AK8PFHT750_TrimMass50
                                #old : event.HLT_AK8PFHT700_TrimR0p1PT0p03Mass50
        trigger_SUB_PS        = event.HLT_PFJet320
        #triggers not found for:
        #trigger_HTWJ          = all([event.HLT_PFHT650_WideJetMJJ950DEtaJJ1p5,
        #                             event.HLT_PFHT650_WideJetMJJ900])
        #trigger_SUBTAG        = all([event.HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20,
        #                             event.HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20])
        
        ###########     electrons ##########
        for ielectron in range(event.nElectron):
            electron_pt = event.Electron_pt[ielectron]
            electron_eta = event.Electron_eta[ielectron]
            electron_phi = event.Electron_phi[ielectron]
            electron_mass = event.Electron_mass[ielectron]
            electron_tlv = ROOT.TLorentzVector()
            electron_tlv.SetPtEtaPhiM(electron_pt, electron_eta,electron_phi, electron_mass)
            if electron_pt > elec_pt_cut and abs(electron_eta) < elec_eta_cut:
                idx_electrons.append(ielectron)
                electrons_tlv_list.append(electron_tlv)
                if event.Electron_cutBased[ielectron] >= 2:
                    idx_loose_electrons.append(ielectron)
                    loose_electrons_tlv_list.append(electron_tlv)
        self.nElectrons = len(loose_electrons_tlv_list)
        
        ###########     muons     #########
        for imuon in range(event.nMuon):
            muon_pt = event.Muon_pt[imuon]
            muon_eta = event.Muon_eta[imuon]
            muon_phi = event.Muon_phi[imuon]
            muon_mass = event.Muon_mass[imuon]
            muon_tlv = ROOT.TLorentzVector()
            muon_tlv.SetPtEtaPhiM(muon_pt, muon_eta, muon_phi, muon_mass)
            if muon_pt > muon_pt_cut and abs(muon_eta) < muon_eta_cut:
                idx_muons.append(imuon)
                muons_tlv_list.append(muon_tlv)
                if event.Muon_isPFcand[imuon] and (event.Muon_isGlobal[imuon] or event.Muon_isTracker[imuon]):
                    idx_loose_muons.append(imuon)
                    loose_muons_tlv_list.append(muon_tlv)
        self.nMuons = len(loose_muons_tlv_list)


        ############    taus         #########
        for itau in range(event.nTau):
            tau_pt = event.Tau_pt[itau]
            tau_eta = event.Tau_eta[itau]
            tau_phi = event.Tau_phi[itau]
            tau_mass = event.Tau_mass[itau]
            tau_tlv = ROOT.TLorentzVector()
            tau_tlv.SetPtEtaPhiM(tau_pt, tau_eta, tau_phi, tau_mass)
            if tau_pt > tau_pt_cut and abs(tau_eta) < tau_eta_cut:
                cleanTau = True
                for loose_electrons_tlv in loose_electrons_tlv_list:
                    if loose_electrons_tlv.DeltaR(tau_tlv) < 0.4:
                        cleanTau = False
                for loose_muons_tlv in loose_muons_tlv_list:
                    if loose_muons_tlv.DeltaR(tau_tlv) < 0.4:
                        cleanTau = False
                if cleanTau:
                    self.nTaus += 1

        ###########    FatJet        #########
        for ifatjet in range(event.nFatJet):
            fatjet_pt = event.FatJet_pt[ifatjet]
            fatjet_eta = event.FatJet_eta[ifatjet]
            fatjet_phi = event.FatJet_phi[ifatjet]
            fatjet_mass = event.FatJet_mass[ifatjet]
            fatjet_jetid = event.FatJet_jetId[ifatjet]
            fatjet_tlv = ROOT.TLorentzVector()
            fatjet_tlv.SetPtEtaPhiM(fatjet_pt, fatjet_eta, fatjet_phi, fatjet_mass)
            if fatjet_pt > fatjet_pt_cut and abs(fatjet_eta) < fatjet_eta_cut:
                cleanJet = True
                for loose_electrons_tlv in loose_electrons_tlv_list:
                    if loose_electrons_tlv.DeltaR(fatjet_tlv) < 0.8:
                        cleanJet = False
                for loose_muons_tlv in loose_muons_tlv_list:
                    if loose_muons_tlv.DeltaR(fatjet_tlv) < 0.8:
                        cleanJet = False
                if cleanJet:
                    fatjet_tau21_list.append(event.FatJet_tau2[ifatjet]/event.FatJet_tau1[ifatjet])
                    fatjet_tlv_list.append(fatjet_tlv)
                    idx_fatjet.append(ifatjet)
                    fatjet_nbtag = 0
                    for isubjet in [event.FatJet_subJetIdx1[ifatjet], event.FatJet_subJetIdx2[ifatjet]]:
                        if isubjet >= 0 and event.SubJet_btagCSVV2[isubjet] > 0.5426: 
                            fatjet_nbtag += 1
                    fatjet_nbtag_list.append(fatjet_nbtag)
        self.nFatJets = len(fatjet_tlv_list)
        ############  AK4 Jet       ###########
        ST = 0
        HT = 0
        HTx = 0
        HTy = 0
        for ijet in range(event.nJet):
            jet_pt = event.Jet_pt[ijet]
            jet_eta = event.Jet_eta[ijet]
            jet_phi = event.Jet_phi[ijet]
            jet_mass = event.Jet_mass[ijet]
            jet_tlv = ROOT.TLorentzVector()
            jet_tlv.SetPtEtaPhiM(jet_pt,jet_eta,jet_phi,jet_mass)
            if jet_pt > ak4_pt_cut and abs(jet_eta) < ak4_eta_cut:
                cleanJet = True
                for loose_electrons_tlv in loose_electrons_tlv_list:
                    if loose_electrons_tlv.DeltaR(jet_tlv) < 0.4:
                        cleanJet = False
                for loose_muons_tlv in loose_muons_tlv_list:
                    if loose_muons_tlv.DeltaR(jet_tlv) < 0.4:
                        cleanJet = False
                if cleanJet:
                    if len(fatjet_tlv_list) > 0 and fatjet_tlv_list[0].DeltaR(jet_tlv) > 1.2:
                        jet_tlv_list.append(jet_tlv)
                        idx_jet.append(ijet)
                    if len(fatjet_tlv_list) > 1 and fatjet_tlv_list[0].DeltaR(jet_tlv) > 1.2 and fatjet_tlv_list[1].DeltaR(jet_tlv) > 1.2:
                        jets_tlv_list.append(jet_tlv)
                        idx_jets.append(ijet)
                    ST += jet_pt
                    HT += jet_pt
                    HTx += jet_tlv.Px()
                    HTy += jet_tlv.Py()
        MHT = np.sqrt(HTx*HTx+HTy*HTy)
        MHTNoMu = MHT
        if not self.isData:
            if idx_jets > 0:
                self.out.btag_eff = self.btagTool.fillEfficiencies(event,idx_jets)
            else:
                self.out.btag_eff = self.btagTool.fillEfficiencies(event,idx_jet)
            return True
        else:
            return False
