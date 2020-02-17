from ScaleFactorTool import ScaleFactor

# /shome/ytakahas/work/Leptoquark/CMSSW_9_4_4/src/PhysicsTools/NanoAODTools/NanoTreeProducer/leptonSF
# HTT: https://github.com/CMS-HTT/LeptonEfficiencies
# https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffs2017
# https://twiki.cern.ch/twiki/bin/view/CMS/Egamma2017DataRecommendations#Efficiency_Scale_Factors
path    = 'CorrectionTools/leptonEfficiencies/MuonPOG/'

class MuonSFs:
    
    def __init__(self, year=2017):
        """Load histograms from files."""
        assert year in [2016,2017,2018], "MuonSFs: You must choose a year from: 2016, 2017 or 2018."
        self.year = year
        self.lumi_2016_bcdef = 20.2
        self.lumi_2016_gh = 16.6
        if year==2016:
            self.sftool_trig  = ScaleFactor(path+"Run2016/SingleMuonTrigger_2016.root","Mu50_OR_TkMu50_PtEtaBins/abseta_pt_ratio","mu_trig")
            self.sftool_id_bcdef    = ScaleFactor(path+"Run2016/RunBCDEF_SF_ID.root","NUM_HighPtID_DEN_genTracks_eta_pair_newTuneP_probe_pt","mu_id")
            self.sftool_id_gh    = ScaleFactor(path+"Run2016/RunGH_SF_ID.root","NUM_HighPtID_DEN_genTracks_eta_pair_newTuneP_probe_pt","mu_id")
            self.sftool_iso_id_bcdef    = ScaleFactor(path+"Run2016/RunBCDEF_SF_ISO.root","NUM_LooseRelTkIso_DEN_HighPtIDandIPCut_eta_pair_newTuneP_probe_pt","mu_iso_id")
            self.sftool_iso_id_gh    = ScaleFactor(path+"Run2016/RunGH_SF_ISO.root","NUM_LooseRelTkIso_DEN_HighPtIDandIPCut_eta_pair_newTuneP_probe_pt","mu_iso_id")
        elif year==2017:
            self.sftool_trig  = ScaleFactor(path+"Run2017/EfficienciesAndSF_RunBtoF_Nov17Nov2017.root","Mu50_PtEtaBins/abseta_pt_ratio",'mu_trig')
            self.sftool_id    = ScaleFactor(path+"Run2017/RunBCDEF_SF_ID.root","NUM_HighPtID_DEN_genTracks_pair_newTuneP_probe_pt_abseta",'mu_id',ptvseta=False)
            self.sftool_trkid = ScaleFactor(path+"Run2017/RunBCDEF_SF_ID.root","NUM_TrkHighPtID_DEN_genTracks_pair_newTuneP_probe_pt_abseta",'mu_trkid',ptvseta=False)
            self.sftool_iso_id    = ScaleFactor(path+"Run2017/RunBCDEF_SF_ISO.root","NUM_LooseRelTkIso_DEN_HighPtIDandIPCut_pair_newTuneP_probe_pt_abseta",'mu_iso_id',ptvseta=False)
            self.sftool_iso_trkid = ScaleFactor(path+"Run2017/RunBCDEF_SF_ISO.root","NUM_LooseRelTkIso_DEN_TrkHighPtID_pair_newTuneP_probe_pt_abseta",'mu_iso_trkid',ptvseta=False)
        elif year==2018:
            self.sftool_trig  = ScaleFactor(path+"Run2018/EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root","Mu50_OR_OldMu100_OR_TkMu100_PtEtaBins/abseta_pt_ratio",'mu_trig')
            self.sftool_id    = ScaleFactor(path+"Run2018/RunABCD_SF_ID.root","NUM_HighPtID_DEN_TrackerMuons_pair_newTuneP_probe_pt_abseta",'mu_id',ptvseta=False)
            self.sftool_trkid = ScaleFactor(path+"Run2018/RunABCD_SF_ID.root","NUM_TrkHighPtID_DEN_TrackerMuons_pair_newTuneP_probe_pt_abseta",'mu_trkid',ptvseta=False)
            self.sftool_iso_id    = ScaleFactor(path+"Run2018/RunABCD_SF_ISO.root","NUM_LooseRelTkIso_DEN_HighPtIDandIPCut_pair_newTuneP_probe_pt_abseta",'mu_iso_id',ptvseta=False)
            self.sftool_iso_trkid = ScaleFactor(path+"Run2018/RunABCD_SF_ISO.root","NUM_LooseRelTkIso_DEN_TrkHighPtID_pair_newTuneP_probe_pt_abseta",'mu_iso_trkid',ptvseta=False)


        
    def getTriggerSF(self, pt, eta):
        """Get SF for single muon trigger."""
        return self.sftool_trig.getSF(pt,abs(eta))
    
    def getTriggerSFerror(self, pt, eta):
        """Get SF for single muon trigger."""
        return self.sftool_trig.getSFerror(pt,abs(eta))

    
    def getIdSF(self, pt, eta, highptid):
        """Get SF for muon identification."""
        if self.year == 2016:
            return (self.sftool_id_bcdef.getSF(pt,abs(eta))*self.lumi_2016_bcdef+self.sftool_id_gh.getSF(pt,abs(eta))*self.lumi_2016_gh)/(self.lumi_2016_bcdef+self.lumi_2016_gh)
        else:
            if highptid==1:
                return self.sftool_trkid.getSF(pt,abs(eta))
            elif highptid==2:
                return self.sftool_id.getSF(pt,abs(eta))
            else:
                return 1.

    def getIdSFerror(self, pt, eta, highptid):
        """Get SF for muon identification."""
        if self.year == 2016:
            idsferror = (self.sftool_id_bcdef.getSFerror(pt,abs(eta))*self.lumi_2016_bcdef+self.sftool_id_gh.getSFerror(pt,abs(eta))*self.lumi_2016_gh)/(self.lumi_2016_bcdef+self.lumi_2016_gh)
            if highptid==1:
                return idsferror*2
            else:
                return idsferror
        else:
            if highptid==1:
                return self.sftool_trkid.getSFerror(pt,abs(eta))
            elif highptid==2:
                return self.sftool_id.getSFerror(pt,abs(eta))
            else:
                return 0.
            
            
    def getIsoSF(self, pt, eta, highptid):
        """Get SF for muon isolation."""
        if self.year == 2016:
            return (self.sftool_iso_id_bcdef.getSF(pt,abs(eta))*self.lumi_2016_bcdef+self.sftool_iso_id_gh.getSF(pt,abs(eta))*self.lumi_2016_gh)/(self.lumi_2016_bcdef+self.lumi_2016_gh)
        else:
            if highptid==1:
                return self.sftool_iso_trkid.getSF(pt,abs(eta))
            elif highptid==2:
                return self.sftool_iso_id.getSF(pt,abs(eta))
            else:
                return 1.

    def getIsoSFerror(self, pt, eta, highptid):
        """Get SF for muon isolation."""
        if self.year == 2016:
            isosferror = (self.sftool_iso_id_bcdef.getSFerror(pt,abs(eta))*self.lumi_2016_bcdef+self.sftool_iso_id_gh.getSFerror(pt,abs(eta))*self.lumi_2016_gh)/(self.lumi_2016_bcdef+self.lumi_2016_gh)
            if highptid==1:
                return isosferror*2
            else:
                return isosferror
        else:
            if highptid==1:
                return self.sftool_iso_trkid.getSFerror(pt,abs(eta))
            elif highptid==2:
                return self.sftool_iso_id.getSFerror(pt,abs(eta))
            else:
                return 0.
