// $Id: CycleCreators.py 344 2016-08-15 19:52:15Z zucchett $

// Local include(s):
#include "../include/VHAnalysis.h"

// External include(s):
#include "../GoodRunsLists/include/TGoodRunsListReader.h"

#include <TMath.h>

ClassImp( VHAnalysis );


VHAnalysis::VHAnalysis() : SCycleBase(),
    m_eventInfo( this ),
    m_electron( this ),
    m_muon( this ),
    m_tau( this ),
    m_jetAK4( this ),
    m_jetAK8( this ),
    m_jetAK8Puppi( this ),
    m_genjetAK8( this ),
    m_missingEt( this ),
    m_genParticle( this ),
    m_pileupReweightingTool( this ),
    m_bTaggingScaleTool( this ),
    m_ScaleFactorTool( this ),
    m_CorrectionTool( this ),
    m_VariableTool( this )
{

    m_logger << INFO << "Initialization" << SLogger::endmsg;
    SetLogName( GetName() );

    // Read configuration details from XML file
    DeclareProperty( "RecoTreeName",              m_recoTreeName = "physics" );
    // Declare trees
    DeclareProperty( "OutputTreeName",            m_outputTreeName = "VH");

    // Declare varibles in trees
    DeclareProperty( "IsData",                    m_isData                   = false );
    DeclareProperty( "IsSignal",                  m_isSignal                 = false );

    DeclareProperty( "ElectronName",              m_electronName             = "el" );
    DeclareProperty( "MuonName",                  m_muonName                 = "mu" );
    DeclareProperty( "TauName",                   m_tauName                  = "tau" );
    DeclareProperty( "JetAK4Name",                m_jetAK4Name               = "jetAK4" );
    DeclareProperty( "JetAK8Name",                m_jetAK8Name               = "jetAK8" );
    DeclareProperty( "GenJetAK8Name",             m_genjetAK8Name            = "genjetAK8" );
    DeclareProperty( "MissingEtName",             m_missingEtName            = "MET" );
    DeclareProperty( "GenParticleName",           m_genParticleName          = "genParticle" );
    
    
    DeclareProperty( "Elec1PtCut",                m_Elec1PtCut               =  55. );
    DeclareProperty( "Elec2PtCut",                m_Elec2PtCut               =  20. );
    DeclareProperty( "ElecPtCut",                 m_ElecPtCut                =  10. );
    DeclareProperty( "ElecEtaCut",                m_ElecEtaCut               =  2.5 );
    DeclareProperty( "Muon1PtCut",                m_Muon1PtCut               =  55. );
    DeclareProperty( "Muon2PtCut",                m_Muon2PtCut               =  20. );
    DeclareProperty( "MuonPtCut",                 m_MuonPtCut                =  10. );
    DeclareProperty( "MuonEtaCut",                m_MuonEtaCut               =  2.4 );
    DeclareProperty( "TauPtCut",                  m_TauPtCut                 =  18. );
    DeclareProperty( "TauEtaCut",                 m_TauEtaCut                =  2.3 );
    DeclareProperty( "AK4PtCut",                  m_AK4PtCut                 =  30. );
    DeclareProperty( "AK4EtaCut",                 m_AK4EtaCut                =  2.4 );
    DeclareProperty( "AK8PtCut",                  m_AK8PtCut                 = 200. );
    DeclareProperty( "AK8EtaCut",                 m_AK8EtaCut                =  2.4 );
    DeclareProperty( "MEtPtCut",                  m_MEtPtCut                 = 250. );
    DeclareProperty( "VPtCut",                    m_VPtCut                   = 200. );
    DeclareProperty( "Tau21LowerCut",             m_Tau21LowerCut            = 0.35 );
    DeclareProperty( "Tau21UpperCut",             m_Tau21UpperCut            = 0.75 );
    DeclareProperty( "JMassLowerCut",             m_JMassLowerCut            =  30. );
    DeclareProperty( "JMassUpperCut",             m_JMassUpperCut            = 250. );
    DeclareProperty( "VMassLowerCut",             m_VMassLowerCut            =  65. );
    DeclareProperty( "VMassInterCut",             m_VMassInterCut            =  85. );
    DeclareProperty( "VMassUpperCut",             m_VMassUpperCut            = 105. );
    DeclareProperty( "HMassLowerCut",             m_HMassLowerCut            = 105. );
    DeclareProperty( "HMassUpperCut",             m_HMassUpperCut            = 135. );
    DeclareProperty( "XMassLowerCut",             m_XMassLowerCut            = 750. );
    DeclareProperty( "XTMassLowerCut",            m_XTMassLowerCut           = 650. );
    DeclareProperty( "XJJMassLowerCut",           m_XJJMassLowerCut          = 950. );
    
    // External objects name
    DeclareProperty( "JSONFileName",              m_JSONFileName             = "../GoodRunsLists/JSON/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt" ); //Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt

    // Prepend SFrame dir
    m_JSONFileName = std::string (std::getenv("SFRAME_DIR")) + m_JSONFileName;
    
}

// Destructor
VHAnalysis::~VHAnalysis() {

  m_logger << INFO << "Tschoe!" << SLogger::endmsg;

}


// Begin Job
void VHAnalysis::BeginCycle() throw( SError ) {

    m_logger << INFO << "Begin Job" << SLogger::endmsg;

    // Load the GRL:
    if (m_isData) {
        m_logger << INFO << "Loading GoodRunsList from file: " << m_JSONFileName << SLogger::endmsg;
        Root::TGoodRunsListReader reader( TString( m_JSONFileName.c_str() ) );
        if( !reader.Interpret() ) {
            m_logger << FATAL << "Couldn't read in the GRL!" << SLogger::endmsg;
            throw SError( ( "Couldn't read in file: " + m_JSONFileName ).c_str(), SError::SkipCycle );
        }
        m_grl = reader.GetMergedGoodRunsList();
        m_grl.Summary();
        m_grl.SetName( "MyGoodRunsList" );
        // Add it as a configuration object, so that the worker nodes will receive it:
        AddConfigObject( &m_grl );
    }

    m_triggerNames.clear();
//    m_triggerNames[""] = std::vector<std::string> ();
    //m_triggerNames["SingleMu"].push_back("HLT_Mu45_eta2p1_v");
    m_triggerNames["SingleMu"].push_back("HLT_Mu50_v");
    m_triggerNames["SingleMu"].push_back("HLT_TkMu50_v");
    m_triggerNames["SingleIsoMu"].push_back("HLT_IsoMu27_v");
    m_triggerNames["SingleIsoMu"].push_back("HLT_IsoTkMu27_v");
    m_triggerNames["DoubleMu"].push_back("HLT_Mu27_TkMu8_v");
    m_triggerNames["DoubleIsoMu"].push_back("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v");
    m_triggerNames["DoubleIsoMu"].push_back("HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v");
    m_triggerNames["SingleEle"].push_back("HLT_Ele105_CaloIdVT_GsfTrkIdT_v");
    m_triggerNames["SingleEle"].push_back("HLT_Ele115_CaloIdVT_GsfTrkIdT_v");
    //m_triggerNames["SingleIsoEle"].push_back("HLT_Ele35_WPTight_Gsf_v");
    m_triggerNames["SingleIsoEle"].push_back("HLT_Ele32_WPTight_Gsf_v");
    m_triggerNames["SingleIsoEle"].push_back("HLT_Ele32_eta2p1_WPTight_Gsf_v");
    m_triggerNames["SingleIsoEle"].push_back("HLT_Ele27_WPLoose_Gsf_v");
    m_triggerNames["SingleIsoEle"].push_back("HLT_Ele27_WPTight_Gsf_v");
    m_triggerNames["DoubleIsoEle"].push_back("HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v");
    m_triggerNames["DoubleEle"].push_back("HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v");
    m_triggerNames["METMHTNoMu"].push_back("HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v");
    m_triggerNames["METMHTNoMu"].push_back("HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v");
    m_triggerNames["METMHTNoMu"].push_back("HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v");
    m_triggerNames["METMHTNoMu"].push_back("HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v");
    m_triggerNames["METMHTNoMu"].push_back("HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v");
    m_triggerNames["METMHTNoMu"].push_back("HLT_MonoCentralPFJet80_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v");
    m_triggerNames["METMHT"].push_back("HLT_PFMET110_PFMHT110_IDTight_v");
    m_triggerNames["METMHT"].push_back("HLT_PFMET120_PFMHT120_IDTight_v");
    //m_triggerNames["MET"].push_back("HLT_PFMET120_BTagCSV_p067_v");
    m_triggerNames["MET"].push_back("HLT_PFMET170_NoiseCleaned_v");
    m_triggerNames["MET"].push_back("HLT_PFMET170_HBHECleaned_v");
    m_triggerNames["MET"].push_back("HLT_PFMET170_HBHE_BeamHaloCleaned_v");
    m_triggerNames["JET"].push_back("HLT_PFJet450_v");
    m_triggerNames["JET"].push_back("HLT_AK8PFJet450_v");
    m_triggerNames["HT"].push_back("HLT_PFHT900_v");
    m_triggerNames["HT"].push_back("HLT_PFHT800_v");
    m_triggerNames["HTWJ"].push_back("HLT_PFHT650_WideJetMJJ950DEtaJJ1p5_v");
    m_triggerNames["HTWJ"].push_back("HLT_PFHT650_WideJetMJJ900_v");
    //m_triggerNames["HT_PS"].push_back("HLT_PFHT400_v");
    //m_triggerNames["HT_PS"].push_back("HLT_PFHT600_v");
    m_triggerNames["HT_PS"].push_back("HLT_PFHT650_v");
    m_triggerNames["HT_PS"].push_back("HLT_PFJet320_v");
    m_triggerNames["SUBJET"].push_back("HLT_AK8PFJet360_TrimMass30_v");
    m_triggerNames["SUBHT"].push_back("HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v");
    //m_triggerNames["SUB"].push_back("HLT_AK8PFHT650_TrimR0p1PT0p03Mass50_v");
    m_triggerNames["SUBTAG"].push_back("HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV_p20_v");
    m_triggerNames["SUBTAG"].push_back("HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20_v");
    m_triggerNames["SUB_PS"].push_back("HLT_PFJet320_v");
    
    return;
}


// End Job
void VHAnalysis::EndCycle() throw( SError ) {
    std::cout << "Events analyzed:\t" << nEvents <<std::endl;
    return;
}

void VHAnalysis::BeginInputData( const SInputData& id ) throw( SError ) {

    m_logger << INFO << "IsData:\t" <<                m_isData               << SLogger::endmsg;
    m_logger << INFO << "IsSignal:\t" <<              m_isSignal             << SLogger::endmsg;

    m_logger << INFO << "ElectronName:\t" <<          m_electronName         << SLogger::endmsg;
    m_logger << INFO << "MuonName:\t" <<              m_muonName             << SLogger::endmsg;
    m_logger << INFO << "TauName:\t" <<               m_tauName              << SLogger::endmsg;
    m_logger << INFO << "JetAK4Name:\t" <<            m_jetAK4Name           << SLogger::endmsg;
    m_logger << INFO << "JetAK8Name:\t" <<            m_jetAK8Name           << SLogger::endmsg;
    m_logger << INFO << "GenJetAK8Name:\t" <<         m_genjetAK8Name        << SLogger::endmsg;
    m_logger << INFO << "MissingEtName:\t" <<         m_missingEtName        << SLogger::endmsg;
    m_logger << INFO << "GenParticleName:\t" <<       m_genParticleName      << SLogger::endmsg;
    
    m_logger << INFO << "Elec1PtCut:\t" <<            m_Elec1PtCut           << SLogger::endmsg;
    m_logger << INFO << "Elec2PtCut:\t" <<            m_Elec2PtCut           << SLogger::endmsg;
    m_logger << INFO << "ElecPtCut:\t" <<             m_ElecPtCut            << SLogger::endmsg;
    m_logger << INFO << "ElecEtaCut:\t" <<            m_ElecEtaCut           << SLogger::endmsg;
    m_logger << INFO << "Muon1PtCut:\t" <<            m_Muon1PtCut           << SLogger::endmsg;
    m_logger << INFO << "Muon2PtCut:\t" <<            m_Muon2PtCut           << SLogger::endmsg;
    m_logger << INFO << "MuonPtCut:\t" <<             m_MuonPtCut            << SLogger::endmsg;
    m_logger << INFO << "MuonEtaCut:\t" <<            m_MuonEtaCut           << SLogger::endmsg;
    m_logger << INFO << "TauPtCut:\t" <<              m_TauPtCut             << SLogger::endmsg;
    m_logger << INFO << "TauEtaCut:\t" <<             m_TauEtaCut            << SLogger::endmsg;
    m_logger << INFO << "AK4PtCut:\t" <<              m_AK4PtCut             << SLogger::endmsg;
    m_logger << INFO << "AK4EtaCut:\t" <<             m_AK4EtaCut            << SLogger::endmsg;
    m_logger << INFO << "AK8PtCut:\t" <<              m_AK8PtCut             << SLogger::endmsg;
    m_logger << INFO << "AK8EtaCut:\t" <<             m_AK8EtaCut            << SLogger::endmsg;
    m_logger << INFO << "MEtPtCut:\t" <<              m_MEtPtCut             << SLogger::endmsg;
    m_logger << INFO << "VPtCut:\t" <<                m_VPtCut               << SLogger::endmsg;
    m_logger << INFO << "Tau21LowerCut:\t" <<         m_Tau21LowerCut        << SLogger::endmsg;
    m_logger << INFO << "Tau21UpperCut:\t" <<         m_Tau21UpperCut        << SLogger::endmsg;
    m_logger << INFO << "JMassLowerCut:\t" <<         m_JMassLowerCut        << SLogger::endmsg;
    m_logger << INFO << "JMassUpperCut:\t" <<         m_JMassUpperCut        << SLogger::endmsg;
    m_logger << INFO << "VMassLowerCut:\t" <<         m_VMassLowerCut        << SLogger::endmsg;
    m_logger << INFO << "VMassInterCut:\t" <<         m_VMassInterCut        << SLogger::endmsg;
    m_logger << INFO << "VMassUpperCut:\t" <<         m_VMassUpperCut        << SLogger::endmsg;
    m_logger << INFO << "HMassLowerCut:\t" <<         m_HMassLowerCut        << SLogger::endmsg;
    m_logger << INFO << "HMassUpperCut:\t" <<         m_HMassUpperCut        << SLogger::endmsg;
    m_logger << INFO << "XMassLowerCut:\t" <<         m_XMassLowerCut        << SLogger::endmsg;
    m_logger << INFO << "XTMassLowerCut:\t" <<        m_XTMassLowerCut       << SLogger::endmsg;
    m_logger << INFO << "XJJMassLowerCut:\t" <<       m_XJJMassLowerCut      << SLogger::endmsg;
    
    // External objects name
    m_logger << INFO << "JSONFileName:\t" <<          m_JSONFileName         << SLogger::endmsg;

    if(m_isData) {
        TObject* grl;
        if( ! ( grl = GetConfigObject( "MyGoodRunsList" ) ) ) {
          m_logger << FATAL << "Can't access the GRL!" << SLogger::endmsg;
          throw SError( "Can't access the GRL!", SError::SkipCycle );
        }
        m_grl = *( dynamic_cast< Root::TGoodRunsList* >( grl ) );
    }
    else {
        m_pileupReweightingTool.BeginInputData( id );
    }
    
    m_bTaggingScaleTool.BeginInputData( id );
    m_ScaleFactorTool.BeginInputData( id );
    m_CorrectionTool.BeginInputData( id );
    m_VariableTool.BeginInputData( id );
    
    if(isMC) {
        m_bTaggingScaleTool.bookHistograms();
    }
    

    //
    // output branches
    //
    DeclareVariable( isMC,                "isMC",  m_outputTreeName.c_str());
    DeclareVariable( EventNumber,         "eventNumber",  m_outputTreeName.c_str());
    DeclareVariable( LumiNumber,          "lumiNumber",  m_outputTreeName.c_str());
    DeclareVariable( RunNumber,           "runNumber",  m_outputTreeName.c_str());

    DeclareVariable( EventWeight,         "eventWeight",  m_outputTreeName.c_str());
//    DeclareVariable( ZewkWeight,          "ZewkWeight",  m_outputTreeName.c_str());
//    DeclareVariable( WewkWeight,          "WewkWeight",  m_outputTreeName.c_str());
    DeclareVariable( TopWeight,           "TopWeight",  m_outputTreeName.c_str());
//    DeclareVariable( PUWeight,            "puWeight",  m_outputTreeName.c_str());
//    DeclareVariable( TriggerWeight,       "triggerWeight",  m_outputTreeName.c_str());
//    DeclareVariable( LeptonWeight,        "leptonWeight",  m_outputTreeName.c_str());
    DeclareVariable( BTagAK8Weight,       "bTagAK8Weight",  m_outputTreeName.c_str());
//    DeclareVariable( BTagAK8WeightUp,     "bTagAK8WeightUp",  m_outputTreeName.c_str());
//    DeclareVariable( BTagAK8WeightDown,   "bTagAK8WeightDown",  m_outputTreeName.c_str());
    DeclareVariable( BTagAK4Weight,       "bTagAK4Weight",  m_outputTreeName.c_str());
//    DeclareVariable( BTagAK4WeightUp,     "bTagAK4WeightUp",  m_outputTreeName.c_str());
//    DeclareVariable( BTagAK4WeightDown,   "bTagAK4WeightDown",  m_outputTreeName.c_str());
    DeclareVariable( BBTagWeight,         "bbTagWeight",  m_outputTreeName.c_str());
//    DeclareVariable( BBTagWeightUp,       "bbTagWeightUp",  m_outputTreeName.c_str());
//    DeclareVariable( BBTagWeightDown,     "bbTagWeightDown",  m_outputTreeName.c_str());
    
    DeclareVariable( isZtoNN,             "isZtoNN",  m_outputTreeName.c_str());
    DeclareVariable( isWtoEN,             "isWtoEN",  m_outputTreeName.c_str());
    DeclareVariable( isWtoMN,             "isWtoMN",  m_outputTreeName.c_str());
    DeclareVariable( isZtoEE,             "isZtoEE",  m_outputTreeName.c_str());
    DeclareVariable( isZtoMM,             "isZtoMM",  m_outputTreeName.c_str());
    DeclareVariable( isVtoQQ,             "isVtoQQ",  m_outputTreeName.c_str());
    DeclareVariable( isTtoEM,             "isTtoEM",  m_outputTreeName.c_str());
    DeclareVariable( isTveto,             "isTveto",  m_outputTreeName.c_str());
    DeclareVariable( isBoostedTau,        "isBoostedTau",  m_outputTreeName.c_str());
    DeclareVariable( isBoosted4B,         "isBoosted4B",  m_outputTreeName.c_str());
    
    DeclareVariable( nPV,                 "nPV",  m_outputTreeName.c_str());
    DeclareVariable( nTaus,               "nTaus",  m_outputTreeName.c_str());
    DeclareVariable( nJetsNoFatJet,       "nJets",  m_outputTreeName.c_str());
    DeclareVariable( JetMetDPhi,          "DPhi",  m_outputTreeName.c_str());
    DeclareVariable( VHDEta,              "DEta",  m_outputTreeName.c_str());
    DeclareVariable( MinJetMetDPhi,       "MinDPhi",  m_outputTreeName.c_str());
    DeclareVariable( MaxJetNoFatJetBTag,  "MaxBTag",  m_outputTreeName.c_str());
    DeclareVariable( CosThetaStar,        "CosThetaStar",  m_outputTreeName.c_str());
    DeclareVariable( CosTheta1,           "CosTheta1",  m_outputTreeName.c_str());
    DeclareVariable( CosTheta2,           "CosTheta2",  m_outputTreeName.c_str());
    DeclareVariable( H_mass,              "H_mass",  m_outputTreeName.c_str());
    DeclareVariable( H_tau21,             "H_tau21",  m_outputTreeName.c_str());
    DeclareVariable( H_ddt,               "H_ddt",  m_outputTreeName.c_str());
    DeclareVariable( H_csv1,              "H_csv1",  m_outputTreeName.c_str());
    DeclareVariable( H_csv2,              "H_csv2",  m_outputTreeName.c_str());
    DeclareVariable( H_flav1,             "H_flav1",  m_outputTreeName.c_str());
    DeclareVariable( H_flav2,             "H_flav2",  m_outputTreeName.c_str());
    DeclareVariable( H_dbt,               "H_dbt",  m_outputTreeName.c_str());
    DeclareVariable( H_ntag,              "H_ntag",  m_outputTreeName.c_str());
    DeclareVariable( H_ptB,               "H_ptB",  m_outputTreeName.c_str());
    DeclareVariable( H_chf,               "H_chf",  m_outputTreeName.c_str());
    DeclareVariable( H_nhf,               "H_nhf",  m_outputTreeName.c_str());
    DeclareVariable( H_phf,               "H_phf",  m_outputTreeName.c_str());
    DeclareVariable( H_muf,               "H_muf",  m_outputTreeName.c_str());
    DeclareVariable( H_emf,               "H_emf",  m_outputTreeName.c_str());
    DeclareVariable( H_chm,               "H_chm",  m_outputTreeName.c_str());
    DeclareVariable( V_mass,              "V_mass",  m_outputTreeName.c_str());
    DeclareVariable( V_tau21,             "V_tau21",  m_outputTreeName.c_str());
    DeclareVariable( V_ddt,               "V_ddt",  m_outputTreeName.c_str());
    DeclareVariable( V_csv1,              "V_csv1",  m_outputTreeName.c_str());
    DeclareVariable( V_csv2,              "V_csv2",  m_outputTreeName.c_str());
    DeclareVariable( V_dbt,               "V_dbt",  m_outputTreeName.c_str());
    DeclareVariable( X_mass,              "X_mass",  m_outputTreeName.c_str());
    
    DeclareVariable( X,                   "X",  m_outputTreeName.c_str());
    DeclareVariable( V,                   "V",  m_outputTreeName.c_str());
    DeclareVariable( H,                   "H",  m_outputTreeName.c_str());

    //
    // Declare the output histograms:
    //
    // Histograms in main directory
    Book( TH1F( "Events", ";;Events", 1, 0, 1));
    
    // Cutflow
    std::vector<std::string> labelsZtoNN = {"All", "Trigger", "MET > 250", "Lepton veto", "Tau veto", "AK8 jet", "Cleaning", "X mass", "T veto", "H mass", "1 b-tag", "2 b-tag"};
    std::vector<std::string> labelsWtoEN = {"All", "Trigger", "Ele in acc.", "Ele p_{T}", "Ele Id+Iso", "W boost", "AK8 jet", "Cleaning", "X mass", "T veto", "H mass", "1 b-tag", "2 b-tag"};
    std::vector<std::string> labelsWtoMN = {"All", "Trigger", "Muon in acc.", "Muon p_{T}", "Muon Id", "Muon Iso", "W boost", "AK8 jet", "Cleaning", "X mass", "T veto", "H mass", "1 b-tag", "2 b-tag"};
    std::vector<std::string> labelsTtoEM = {"All", "Trigger", "2 OS OF", "Muon cand.", "Electron cand.", "Z boost", "AK8 jet", "X mass", "H mass", "1 b-tag", "2 b-tag"};
    std::vector<std::string> labelsZtoEE = {"All", "Trigger", "Ele in acc.", "Z(ee) candidate", "Ele p_{T}", "Ele Id+Iso", "Z boost", "AK8 jet", "Cleaning", "X mass", "H mass", "1 b-tag", "2 b-tag"};
    std::vector<std::string> labelsZtoMM = {"All", "Trigger", "Muon in acc.", "Z(#mu#mu) candidate", "Muon p_{T}", "Muon Id", "Muon Iso", "Z boost", "AK8 jet", "Cleaning", "X mass", "H mass", "1 b-tag", "2 b-tag"};
    std::vector<std::string> labelsVtoQQ = {"All", "Trigger", "2 AK8 jets", "Jet Id", "Jet #Delta#eta", "MET veto", "Lepton veto", "X mass", "H mass", "V mass", "W, HP, 1b", "W, LP, 1b", "W, HP, 2b", "W, LP, 2b", "Z, HP, 1b", "Z, LP, 1b", "Z, HP, 2b", "Z, LP, 2b"};
    
    Book( TH1F( "Events", ";;Events;log", labelsZtoNN.size(), 0, labelsZtoNN.size()), "nnqq" );
    Book( TH1F( "Events", ";;Events;log", labelsWtoEN.size(), 0, labelsWtoEN.size()), "enqq" );
    Book( TH1F( "Events", ";;Events;log", labelsWtoMN.size(), 0, labelsWtoMN.size()), "mnqq" );
    Book( TH1F( "Events", ";;Events;log", labelsTtoEM.size(), 0, labelsTtoEM.size()), "emqq" );
    Book( TH1F( "Events", ";;Events;log", labelsZtoEE.size(), 0, labelsZtoEE.size()), "eeqq" );
    Book( TH1F( "Events", ";;Events;log", labelsZtoMM.size(), 0, labelsZtoMM.size()), "mmqq" );
    Book( TH1F( "Events", ";;Events;log", labelsVtoQQ.size(), 0, labelsVtoQQ.size()), "qqqq" );
    
    for(unsigned int i = 0; i < labelsZtoNN.size(); i++) Hist("Events", "nnqq")->GetXaxis()->SetBinLabel(i+1, labelsZtoNN[i].c_str());
    for(unsigned int i = 0; i < labelsWtoEN.size(); i++) Hist("Events", "enqq")->GetXaxis()->SetBinLabel(i+1, labelsWtoEN[i].c_str());
    for(unsigned int i = 0; i < labelsWtoMN.size(); i++) Hist("Events", "mnqq")->GetXaxis()->SetBinLabel(i+1, labelsWtoMN[i].c_str());
    for(unsigned int i = 0; i < labelsTtoEM.size(); i++) Hist("Events", "emqq")->GetXaxis()->SetBinLabel(i+1, labelsTtoEM[i].c_str());
    for(unsigned int i = 0; i < labelsZtoEE.size(); i++) Hist("Events", "eeqq")->GetXaxis()->SetBinLabel(i+1, labelsZtoEE[i].c_str());
    for(unsigned int i = 0; i < labelsZtoMM.size(); i++) Hist("Events", "mmqq")->GetXaxis()->SetBinLabel(i+1, labelsZtoMM[i].c_str());
    for(unsigned int i = 0; i < labelsVtoQQ.size(); i++) Hist("Events", "qqqq")->GetXaxis()->SetBinLabel(i+1, labelsVtoQQ[i].c_str());
    
    
    // ---------- SEMILEPTONIC Z->nn CHANNEL ----------
    Book( TH1F( "EventWeight", ";Event Weight;Events", 100, 0., 2.), "nnqq" );
    Book( TH1F( "GenWeight", ";Gen Weight;Events", 100, 0., 2.), "nnqq" );
    Book( TH1F( "TopWeight", ";Top Weight;Events", 100, 0., 2.), "nnqq" );
    Book( TH1F( "PUWeight", ";Pileup Weight;Events", 100, 0., 2.), "nnqq" );
    Book( TH1F( "TriggerWeight", ";Trigger Weight;Events", 100, 0., 2.), "nnqq" );
    Book( TH1F( "LeptonWeight", ";Lepton Weight;Events", 100, 0., 2.), "nnqq" );
    Book( TH1F( "BTagWeight", ";BTag Weight;Events", 100, 0., 2.), "nnqq" );
    Book( TH1F( "BBTagWeight", ";BBTag Weight;Events", 100, 0., 2.), "nnqq" );
    Book( TH1F( "Jet_pt", ";AK8 jet p_{T} (GeV);Events;log", 36, 200, 2000), "nnqq" );
    Book( TH1F( "Jet_eta", ";AK8 jet #eta;Events", 30, -3, 3), "nnqq" );
    Book( TH1F( "Jet_phi", ";AK8 jet #varphi;Events", 30, 0, 3.15), "nnqq" );
    Book( TH1F( "Jet_mass", ";AK8 jet ungroomed mass (GeV);Events", 60, 0, 300), "nnqq" );
    Book( TH1F( "Jet_chf", ";AK8 jet charged hadron fraction;Events", 25, 0, 1), "nnqq" );
    Book( TH1F( "Jet_nhf", ";AK8 jet neutral hadron fraction;Events", 25, 0, 1), "nnqq" );
    Book( TH1F( "Jet_phf", ";AK8 jet photon fraction;Events", 25, 0, 1), "nnqq" );
    Book( TH1F( "Jet_muf", ";AK8 jet muon fraction;Events", 25, 0, 1), "nnqq" );
    Book( TH1F( "Jet_emf", ";AK8 jet electron fraction;Events", 25, 0, 1), "nnqq" );
    Book( TH1F( "Jet_chm", ";AK8 jet charged hadron multiplicity;Events", 100, 0, 100), "nnqq" );
    Book( TH1F( "Jet_prunedMass", ";AK8 jet pruned mass (GeV);Events", 60, 0, 300), "nnqq" );
    Book( TH1F( "Jet_prunedCorrMass", ";AK8 jet pruned CHS corrected mass (GeV);Events", 60, 0, 300), "nnqq" );
    Book( TH1F( "Jet_softdropMass", ";AK8 jet softdrop PUPPI mass (GeV);Events", 60, 0, 300), "nnqq" );
    Book( TH1F( "Jet_softdropCorrMass", ";AK8 jet softdrop PUPPI corrected mass (GeV);Events", 60, 0, 300), "nnqq" );
    Book( TH1F( "Jet_chsTau21", ";AK8 jet CHS #tau_{21};Events", 50, 0, 1), "nnqq" );
    Book( TH1F( "Jet_puppiTau21", ";AK8 jet PUPPI #tau_{21};Events", 50, 0, 1), "nnqq" );
    Book( TH1F( "Jet_ddt", ";AK8 jet DDT;Events", 60, 0, 1.2), "nnqq" );
    Book( TH1F( "Jet_csv1", ";AK8 jet subjet1 CSV;Events", 25, 0, 1), "nnqq" );
    Book( TH1F( "Jet_csv2", ";AK8 jet subjet2 CSV;Events", 25, 0, 1), "nnqq" );
    Book( TH1F( "Jet_dbt", ";AK8 jet double b-tagger;Events", 50, -1, 1), "nnqq" );
    Book( TH1F( "MET_pt", ";#slash{E}_{T} (GeV);Events;log", 35, 250, 2000), "nnqq" );
    Book( TH1F( "MET_phi", ";#slash{E}_{T} #varphi;Events", 30, 0, 3.15), "nnqq" );
    Book( TH1F( "ST", ";ST (GeV);Events;log", 50, 0, 4000), "nnqq" );
    Book( TH1F( "HT", ";HT (GeV);Events;log", 50, 0, 3000), "nnqq" );
    Book( TH1F( "MHT", ";missing HT (GeV);Events;log", 50, 0, 2000), "nnqq" );
    Book( TH1F( "nPV", ";number of primary vertices;Events", 60, 0, 60), "nnqq" );
    Book( TH1F( "nElectrons", ";number of electrons;Events;log", 6, -0.5, 5.5), "nnqq" );
    Book( TH1F( "nMuons", ";number of muons;Events;log", 6, -0.5, 5.5), "nnqq" );
    Book( TH1F( "nTaus", ";number of #tau;Events;log", 6, -0.5, 5.5), "nnqq" );
    Book( TH1F( "nPhotons", ";number of photons;Events;log", 6, -0.5, 5.5), "nnqq" );
    Book( TH1F( "nJets", ";number of AK4 jets;Events;log", 10, -0.5, 9.5), "nnqq" );
    Book( TH1F( "nFatJets", ";number of AK8 jets;Events;log", 10, -0.5, 9.5), "nnqq" );
    Book( TH1F( "nBTagJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "nnqq" );
    Book( TH1F( "nBVetoJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "nnqq" );
    Book( TH1F( "JetMetDPhi", ";#Delta #varphi (AK8 jet-#slash{E}_{T});Events", 28, 0, 3.15), "nnqq" );
    Book( TH1F( "MinJetMetDPhi", ";min #Delta #varphi (jet-#slash{E}_{T});Events;log", 28, 0, 3.15), "nnqq" );
    Book( TH1F( "MaxJetNoFatJetBTag", ";max AK4 jet CSV;Events", 25, 0, 1.), "nnqq" );
    Book( TH1F( "Centrality", ";centrality;Events", 50, 0., 1.), "nnqq" );
    Book( TH1F( "CosThetaStar", ";cos(#theta*);Events", 50, -1, 1.), "nnqq" );
    Book( TH1F( "CosTheta1", ";cos(#theta_{1});Events", 50, -1, 1.), "nnqq" );
    Book( TH1F( "CosTheta2", ";cos(#theta_{2});Events", 50, 0., 1.), "nnqq" );
    Book( TH1F( "Phi", ";#phi;Events", 50, -3.15, 3.15), "nnqq" );
    Book( TH1F( "Phi1", ";#phi_{1};Events", 50, -3.15, 3.15), "nnqq" );
    Book( TH1F( "X_mass", ";m_{X} (GeV);Events;log", 44, 600, 5000), "nnqq" );
    Book( TH1F( "X_tmass", ";m_{X}^{T} (GeV);Events;log", 50, 0, 5000), "nnqq" );
    Book( TH1F( "X_cmass", ";m_{X}^{c} (GeV);Events;log", 50, 0, 5000), "nnqq" );
    
    
    // ---------- SEMILEPTONIC W->en CHANNEL ----------
    Book( TH1F( "W_tmass", ";m^{W}_{T} (GeV);Events", 50, 0, 250), "en" );
    Book( TH1F( "W_pt", ";p^{W}_{T} (GeV);Events;log", 100, 0, 2000), "en" );
    Book( TH1F( "W_mass", ";m_{W} (GeV);Events", 160, 0, 160), "en" );
    Book( TH1F( "Electron_pt", ";electron p_{T} (GeV);Events;log", 50, 0, 2000), "en" );
    
    Book( TH1F( "EventWeight", ";Event Weight;Events", 100, 0., 2.), "enqq" );
    Book( TH1F( "GenWeight", ";Gen Weight;Events", 100, 0., 2.), "enqq" );
    Book( TH1F( "TopWeight", ";Top Weight;Events", 100, 0., 2.), "enqq" );
    Book( TH1F( "PUWeight", ";Pileup Weight;Events", 100, 0., 2.), "enqq" );
    Book( TH1F( "TriggerWeight", ";Trigger Weight;Events", 100, 0., 2.), "enqq" );
    Book( TH1F( "LeptonWeight", ";Lepton Weight;Events", 100, 0., 2.), "enqq" );
    Book( TH1F( "BTagWeight", ";BTag Weight;Events", 100, 0., 2.), "enqq" );
    Book( TH1F( "BBTagWeight", ";BBTag Weight;Events", 100, 0., 2.), "enqq" );
    Book( TH1F( "Electron_pt", ";electron p_{T} (GeV);Events;log", 50, 0, 2000), "enqq" );
    Book( TH1F( "Electron_eta", ";electron #eta;Events", 30, -3., 3.), "enqq" );
    Book( TH1F( "Electron_phi", ";electron #varphi;Events", 30, 0, 3.15), "enqq" );
    Book( TH1F( "Electron_mass", ";electron mass (GeV);Events", 50, 0, 1.), "enqq" );
    Book( TH1F( "Electron_pfIso", ";electron PFIso;Events;log", 25, 0, 10.), "enqq" );
    Book( TH1F( "Electron_pt_B", ";electron p_{T} [barrel] (GeV);Events;log", 50, 0, 2000), "enqq" );
    Book( TH1F( "Electron_pt_E", ";electron p_{T} [endcap] (GeV);Events;log", 50, 0, 2000), "enqq" );
    Book( TH1F( "Electron_VIDHEEP", ";electron mis-Id;Events", 5, -2.5, 2.5), "enqq" );
    Book( TH1F( "Electron_VIDHEEP_2J", ";electron mis-Id;Events", 5, -2.5, 2.5), "enqq" );
    Book( TH1F( "Jet_pt", ";AK8 jet p_{T} (GeV);Events;log", 36, 200, 2000), "enqq" );
    Book( TH1F( "Jet_eta", ";AK8 jet #eta;Events", 30, -3, 3), "enqq" );
    Book( TH1F( "Jet_phi", ";AK8 jet #varphi;Events", 30, 0, 3.15), "enqq" );
    Book( TH1F( "Jet_mass", ";AK8 jet ungroomed mass (GeV);Events", 60, 0, 300), "enqq" );
    Book( TH1F( "Jet_chf", ";AK8 jet charged hadron fraction;Events", 25, 0, 1), "enqq" );
    Book( TH1F( "Jet_nhf", ";AK8 jet neutral hadron fraction;Events", 25, 0, 1), "enqq" );
    Book( TH1F( "Jet_phf", ";AK8 jet photon fraction;Events", 25, 0, 1), "enqq" );
    Book( TH1F( "Jet_muf", ";AK8 jet muon fraction;Events", 25, 0, 1), "enqq" );
    Book( TH1F( "Jet_emf", ";AK8 jet electron fraction;Events", 25, 0, 1), "enqq" );
    Book( TH1F( "Jet_chm", ";AK8 jet charged hadron multiplicity;Events", 100, 0, 100), "enqq" );
    Book( TH1F( "Jet_prunedMass", ";AK8 jet pruned mass (GeV);Events", 60, 0, 300), "enqq" );
    Book( TH1F( "Jet_prunedCorrMass", ";AK8 jet pruned CHS corrected mass (GeV);Events", 60, 0, 300), "enqq" );
    Book( TH1F( "Jet_softdropMass", ";AK8 jet softdrop PUPPI mass (GeV);Events", 60, 0, 300), "enqq" );
    Book( TH1F( "Jet_softdropCorrMass", ";AK8 jet softdrop PUPPI corrected mass (GeV);Events", 60, 0, 300), "enqq" );
    Book( TH1F( "Jet_chsTau21", ";AK8 jet CHS #tau_{21};Events", 50, 0, 1), "enqq" );
    Book( TH1F( "Jet_puppiTau21", ";AK8 jet PUPPI #tau_{21};Events", 50, 0, 1), "enqq" );
    Book( TH1F( "Jet_ddt", ";AK8 jet DDT;Events", 60, 0, 1.2), "enqq" );
    Book( TH1F( "Jet_csv1", ";AK8 jet subjet1 CSV;Events", 25, 0, 1), "enqq" );
    Book( TH1F( "Jet_csv2", ";AK8 jet subjet2 CSV;Events", 25, 0, 1), "enqq" );
    Book( TH1F( "Jet_dbt", ";AK8 jet double b-tagger;Events", 50, -1, 1), "enqq" );
    Book( TH1F( "MET_pt", ";#slash{E}_{T} (GeV);Events;log", 50, 0, 1500), "enqq" );
    Book( TH1F( "MET_phi", ";#slash{E}_{T} #varphi;Events", 30, 0, 3.15), "enqq" );
    Book( TH1F( "W_mass", ";m_{W} (GeV);Events", 160, 0, 160), "enqq" );
    Book( TH1F( "W_tmass", ";m^{W}_{T} (GeV);Events", 50, 0, 250), "enqq" );
    Book( TH1F( "W_pt", ";p^{W}_{T} (GeV);Events;log", 90, 200, 2000), "enqq" );
    Book( TH1F( "ST", ";ST (GeV);Events;log", 50, 0, 4000), "enqq" );
    Book( TH1F( "HT", ";HT (GeV);Events;log", 50, 0, 3000), "enqq" );
    Book( TH1F( "MHT", ";missing HT (GeV);Events;log", 50, 0, 3000), "enqq" );
    Book( TH1F( "nPV", ";number of primary vertices;Events", 60, 0, 60), "enqq" );
    Book( TH1F( "nElectrons", ";number of electrons;Events;log", 6, -0.5, 5.5), "enqq" );
    Book( TH1F( "nMuons", ";number of muons;Events;log", 6, -0.5, 5.5), "enqq" );
    Book( TH1F( "nTaus", ";number of #tau;Events;log", 6, -0.5, 5.5), "enqq" );
    Book( TH1F( "nPhotons", ";number of photons;Events;log", 6, -0.5, 5.5), "enqq" );
    Book( TH1F( "nJets", ";number of AK4 jets;Events;log", 10, -0.5, 9.5), "enqq" );
    Book( TH1F( "nFatJets", ";number of AK8 jets;Events;log", 10, -0.5, 9.5), "enqq" );
    Book( TH1F( "nBTagJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "enqq" );
    Book( TH1F( "nBVetoJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "enqq" );
    Book( TH1F( "ElectronJetDPhi", ";#Delta #varphi (electron-AK8 jet);Events", 28, 0, 3.15), "enqq" );
    Book( TH1F( "ElectronMetDPhi", ";#Delta #varphi (electron-#slash{E}_{T});Events", 28, 0, 3.15), "enqq" );
    Book( TH1F( "ElectronMetDPhi_VW", ";#Delta #varphi (electron-#slash{E}_{T});Events", 28, 0, 3.15), "enqq" );
    Book( TH1F( "ElectronMetDPhi_VWJ", ";#Delta #varphi (electron-#slash{E}_{T});Events", 28, 0, 3.15), "enqq" );
    Book( TH1F( "ElectronMetPtRatio", ";p_{T}^{e}/p_{T}^{miss};Events", 50, 0, 5.), "enqq" );
    Book( TH1F( "ElectronJetDR", ";#Delta R (electron-AK8 jet);Events", 25, 0, 5), "enqq" );
    Book( TH1F( "JetMetDPhi", ";#Delta #varphi (AK8 jet-#slash{E}_{T});Events", 28, 0, 3.15), "enqq" );
    Book( TH1F( "WJetDPhi", ";|#Delta #varphi| (W - AK8 jet);Events", 60, 0, 3.15), "enqq" );
    Book( TH1F( "WJetDEta", ";|#Delta #eta| (W - AK8 jet);Events", 50, 0, 5), "enqq" );
    Book( TH1F( "MinJetMetDPhi", ";min #Delta #varphi (jet-#slash{E}_{T});Events;log", 28, 0, 3.15), "enqq" );
    Book( TH1F( "MaxJetNoFatJetBTag", ";max AK4 jet CSV;Events", 25, 0, 1.), "enqq" );
    Book( TH1F( "Centrality", ";centrality;Events", 50, 0., 1.), "enqq" );
    Book( TH1F( "CosThetaStar", ";cos(#theta*);Events", 50, -1, 1.), "enqq" );
    Book( TH1F( "CosTheta1", ";cos(#theta_{1});Events", 50, -1, 1.), "enqq" );
    Book( TH1F( "CosTheta2", ";cos(#theta_{2});Events", 50, 0., 1.), "enqq" );
    Book( TH1F( "Phi", ";#phi;Events", 50, -3.15, 3.15), "enqq" );
    Book( TH1F( "Phi1", ";#phi_{1};Events", 50, -3.15, 3.15), "enqq" );
    Book( TH1F( "X_mass", ";m_{X} (GeV);Events;log", 80, 750, 4750), "enqq" );
    
    
    // ---------- SEMILEPTONIC W->mn CHANNEL ----------
    Book( TH1F( "W_tmass", ";m^{W}_{T} (GeV);Events", 50, 0, 250), "mn" );
    Book( TH1F( "W_pt", ";p^{W}_{T} (GeV);Events;log", 100, 0, 2000), "mn" );
    Book( TH1F( "W_mass", ";m_{W} (GeV);Events", 160, 0, 160), "mn" );
    Book( TH1F( "Muon_pt", ";muon p_{T} (GeV);Events;log", 50, 0, 2000), "mn" );
    
    Book( TH1F( "EventWeight", ";Event Weight;Events", 100, 0., 2.), "mnqq" );
    Book( TH1F( "GenWeight", ";Gen Weight;Events", 100, 0., 2.), "mnqq" );
    Book( TH1F( "TopWeight", ";Top Weight;Events", 100, 0., 2.), "mnqq" );
    Book( TH1F( "PUWeight", ";Pileup Weight;Events", 100, 0., 2.), "mnqq" );
    Book( TH1F( "TriggerWeight", ";Trigger Weight;Events", 100, 0., 2.), "mnqq" );
    Book( TH1F( "LeptonWeight", ";Lepton Weight;Events", 100, 0., 2.), "mnqq" );
    Book( TH1F( "BTagWeight", ";BTag Weight;Events", 100, 0., 2.), "mnqq" );
    Book( TH1F( "BBTagWeight", ";BBTag Weight;Events", 100, 0., 2.), "mnqq" );
    Book( TH1F( "Muon_pt", ";muon p_{T} (GeV);Events;log", 50, 0, 2000), "mnqq" );
    Book( TH1F( "Muon_eta", ";muon #eta;Events", 30, -3., 3.), "mnqq" );
    Book( TH1F( "Muon_phi", ";muon #varphi;Events", 30, 0, 3.15), "mnqq" );
    Book( TH1F( "Muon_mass", ";muon mass (GeV);Events", 50, 0, 1.), "mnqq" );
    Book( TH1F( "Muon_trkIso", ";muon tracker Iso;Events;log", 50, 0, 5.), "mnqq" );
    Book( TH1F( "Muon_pt_B", ";muon p_{T} [barrel] (GeV);Events;log", 50, 0, 2000), "mnqq" );
    Book( TH1F( "Muon_pt_E", ";muon p_{T} [endcap] (GeV);Events;log", 50, 0, 2000), "mnqq" );
    Book( TH1F( "Jet_pt", ";AK8 jet p_{T} (GeV);Events;log", 36, 200, 2000), "mnqq" );
    Book( TH1F( "Jet_eta", ";AK8 jet #eta;Events", 30, -3, 3), "mnqq" );
    Book( TH1F( "Jet_phi", ";AK8 jet #varphi;Events", 30, 0, 3.15), "mnqq" );
    Book( TH1F( "Jet_mass", ";AK8 jet ungroomed mass (GeV);Events", 60, 0, 300), "mnqq" );
    Book( TH1F( "Jet_chf", ";AK8 jet charged hadron fraction;Events", 25, 0, 1), "mnqq" );
    Book( TH1F( "Jet_nhf", ";AK8 jet neutral hadron fraction;Events", 25, 0, 1), "mnqq" );
    Book( TH1F( "Jet_phf", ";AK8 jet photon fraction;Events", 25, 0, 1), "mnqq" );
    Book( TH1F( "Jet_muf", ";AK8 jet muon fraction;Events", 25, 0, 1), "mnqq" );
    Book( TH1F( "Jet_emf", ";AK8 jet electron fraction;Events", 25, 0, 1), "mnqq" );
    Book( TH1F( "Jet_chm", ";AK8 jet charged hadron multiplicity;Events", 100, 0, 100), "mnqq" );
    Book( TH1F( "Jet_prunedMass", ";AK8 jet pruned mass (GeV);Events", 60, 0, 300), "mnqq" );
    Book( TH1F( "Jet_prunedCorrMass", ";AK8 jet pruned CHS corrected mass (GeV);Events", 60, 0, 300), "mnqq" );
    Book( TH1F( "Jet_softdropMass", ";AK8 jet softdrop PUPPI mass (GeV);Events", 60, 0, 300), "mnqq" );
    Book( TH1F( "Jet_softdropCorrMass", ";AK8 jet softdrop PUPPI corrected mass (GeV);Events", 60, 0, 300), "mnqq" );
    Book( TH1F( "Jet_chsTau21", ";AK8 jet CHS #tau_{21};Events", 50, 0, 1), "mnqq" );
    Book( TH1F( "Jet_puppiTau21", ";AK8 jet PUPPI #tau_{21};Events", 50, 0, 1), "mnqq" );
    Book( TH1F( "Jet_ddt", ";AK8 jet DDT;Events", 60, 0, 1.2), "mnqq" );
    Book( TH1F( "Jet_csv1", ";AK8 jet subjet1 CSV;Events", 25, 0, 1), "mnqq" );
    Book( TH1F( "Jet_csv2", ";AK8 jet subjet2 CSV;Events", 25, 0, 1), "mnqq" );
    Book( TH1F( "Jet_dbt", ";AK8 jet double b-tagger;Events", 50, -1, 1), "mnqq" );
    Book( TH1F( "MET_pt", ";#slash{E}_{T} (GeV);Events;log", 50, 0, 1500), "mnqq" );
    Book( TH1F( "MET_phi", ";#slash{E}_{T} #varphi;Events", 30, 0, 3.15), "mnqq" );
    Book( TH1F( "W_mass", ";m_{W} (GeV);Events", 160, 0, 160), "mnqq" );
    Book( TH1F( "W_tmass", ";m^{W}_{T} (GeV);Events", 50, 0, 250), "mnqq" );
    Book( TH1F( "W_pt", ";p^{W}_{T} (GeV);Events;log", 90, 200, 2000), "mnqq" );
    Book( TH1F( "ST", ";ST (GeV);Events;log", 50, 0, 4000), "mnqq" );
    Book( TH1F( "HT", ";HT (GeV);Events;log", 50, 0, 3000), "mnqq" );
    Book( TH1F( "MHT", ";missing HT (GeV);Events;log", 50, 0, 3000), "mnqq" );
    Book( TH1F( "nPV", ";number of primary vertices;Events", 60, 0, 60), "mnqq" );
    Book( TH1F( "nElectrons", ";number of electrons;Events;log", 6, -0.5, 5.5), "mnqq" );
    Book( TH1F( "nMuons", ";number of muons;Events;log", 6, -0.5, 5.5), "mnqq" );
    Book( TH1F( "nTaus", ";number of #tau;Events;log", 6, -0.5, 5.5), "mnqq" );
    Book( TH1F( "nPhotons", ";number of photons;Events;log", 6, -0.5, 5.5), "mnqq" );
    Book( TH1F( "nJets", ";number of AK4 jets;Events;log", 10, -0.5, 9.5), "mnqq" );
    Book( TH1F( "nFatJets", ";number of AK8 jets;Events;log", 10, -0.5, 9.5), "mnqq" );
    Book( TH1F( "nBTagJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "mnqq" );
    Book( TH1F( "nBVetoJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "mnqq" );
    Book( TH1F( "MuonJetDPhi", ";#Delta #varphi (muon-AK8 jet);Events", 28, 0, 3.15), "mnqq" );
    Book( TH1F( "MuonMetDPhi", ";#Delta #varphi (muon-#slash{E}_{T});Events", 28, 0, 3.15), "mnqq" );
    Book( TH1F( "MuonMetDPhi_VW", ";#Delta #varphi (muon-#slash{E}_{T});Events", 28, 0, 3.15), "mnqq" );
    Book( TH1F( "MuonMetDPhi_VWJ", ";#Delta #varphi (muon-#slash{E}_{T});Events", 28, 0, 3.15), "mnqq" );
    Book( TH1F( "MuonMetPtRatio", ";p_{T}^{#mu}/p_{T}^{miss};Events", 50, 0, 5.), "mnqq" );
    Book( TH1F( "MuonJetDR", ";#Delta R (muon-AK8 jet);Events", 25, 0, 5), "mnqq" );
    Book( TH1F( "JetMetDPhi", ";#Delta #varphi (AK8 jet-#slash{E}_{T});Events", 28, 0, 3.15), "mnqq" );
    Book( TH1F( "WJetDPhi", ";|#Delta #varphi| (W - AK8 jet);Events", 60, 0, 3.15), "mnqq" );
    Book( TH1F( "WJetDEta", ";|#Delta #eta| (W - AK8 jet);Events", 50, 0, 5), "mnqq" );
    Book( TH1F( "MinJetMetDPhi", ";min #Delta #varphi (jet-#slash{E}_{T});Events;log", 28, 0, 3.15), "mnqq" );
    Book( TH1F( "MaxJetNoFatJetBTag", ";max AK4 jet CSV;Events", 25, 0, 1.), "mnqq" );
    Book( TH1F( "Centrality", ";centrality;Events", 50, 0., 1.), "mnqq" );
    Book( TH1F( "CosThetaStar", ";cos(#theta*);Events", 50, -1, 1.), "mnqq" );
    Book( TH1F( "CosTheta1", ";cos(#theta_{1});Events", 50, -1, 1.), "mnqq" );
    Book( TH1F( "CosTheta2", ";cos(#theta_{2});Events", 50, 0., 1.), "mnqq" );
    Book( TH1F( "Phi", ";#phi;Events", 50, -3.15, 3.15), "mnqq" );
    Book( TH1F( "Phi1", ";#phi_{1};Events", 50, -3.15, 3.15), "mnqq" );
    Book( TH1F( "X_mass", ";m_{X} (GeV);Events;log", 80, 750, 4750), "mnqq" );
    
    // ---------- DILEPTONIC T->em CHANNEL ----------
    Book( TH1F( "EventWeight", ";Event Weight;Events", 100, 0., 2.), "emqq" );
    Book( TH1F( "GenWeight", ";Gen Weight;Events", 100, 0., 2.), "emqq" );
    Book( TH1F( "TopWeight", ";Top Weight;Events", 100, 0., 2.), "emqq" );
    Book( TH1F( "PUWeight", ";Pileup Weight;Events", 100, 0., 2.), "emqq" );
    Book( TH1F( "TriggerWeight", ";Trigger Weight;Events", 100, 0., 2.), "emqq" );
    Book( TH1F( "LeptonWeight", ";Lepton Weight;Events", 100, 0., 2.), "emqq" );
    Book( TH1F( "BTagWeight", ";BTag Weight;Events", 100, 0., 2.), "emqq" );
    Book( TH1F( "BBTagWeight", ";BBTag Weight;Events", 100, 0., 2.), "emqq" );
    Book( TH1F( "Muon_pt", ";muon p_{T} (GeV);Events;log", 50, 0, 500), "emqq" );
    Book( TH1F( "Muon_eta", ";muon #eta;Events", 30, -3., 3.), "emqq" );
    Book( TH1F( "Muon_phi", ";muon #varphi;Events", 30, 0, 3.15), "emqq" );
    Book( TH1F( "Muon_mass", ";muon mass (GeV);Events", 50, 0, 1.), "emqq" );
    Book( TH1F( "Muon_trkIso", ";muon tracker Iso;Events;log", 50, 0, 5.), "emqq" );
    Book( TH1F( "Electron_pt", ";muon p_{T} (GeV);Events;log", 50, 0, 500), "emqq" );
    Book( TH1F( "Electron_eta", ";muon #eta;Events", 30, -3., 3.), "emqq" );
    Book( TH1F( "Electron_phi", ";muon #varphi;Events", 30, 0, 3.15), "emqq" );
    Book( TH1F( "Electron_mass", ";muon mass (GeV);Events", 50, 0, 1.), "emqq" );
    Book( TH1F( "Electron_pfIso", ";electron PFIso;Events;log", 25, 0, 10.), "emqq" );
    Book( TH1F( "Jet_pt", ";AK8 jet p_{T} (GeV);Events;log", 36, 200, 2000), "emqq" );
    Book( TH1F( "Jet_eta", ";AK8 jet #eta;Events", 30, -3, 3), "emqq" );
    Book( TH1F( "Jet_phi", ";AK8 jet #varphi;Events", 30, 0, 3.15), "emqq" );
    Book( TH1F( "Jet_mass", ";AK8 jet ungroomed mass (GeV);Events", 60, 0, 300), "emqq" );
    Book( TH1F( "Jet_chf", ";AK8 jet charged hadron fraction;Events", 25, 0, 1), "emqq" );
    Book( TH1F( "Jet_nhf", ";AK8 jet neutral hadron fraction;Events", 25, 0, 1), "emqq" );
    Book( TH1F( "Jet_phf", ";AK8 jet photon fraction;Events", 25, 0, 1), "emqq" );
    Book( TH1F( "Jet_muf", ";AK8 jet muon fraction;Events", 25, 0, 1), "emqq" );
    Book( TH1F( "Jet_emf", ";AK8 jet electron fraction;Events", 25, 0, 1), "emqq" );
    Book( TH1F( "Jet_chm", ";AK8 jet charged hadron multiplicity;Events", 100, 0, 100), "emqq" );
    Book( TH1F( "Jet_prunedMass", ";AK8 jet pruned mass (GeV);Events", 60, 0, 300), "emqq" );
    Book( TH1F( "Jet_prunedCorrMass", ";AK8 jet pruned CHS corrected mass (GeV);Events", 60, 0, 300), "emqq" );
    Book( TH1F( "Jet_softdropMass", ";AK8 jet softdrop PUPPI mass (GeV);Events", 60, 0, 300), "emqq" );
    Book( TH1F( "Jet_softdropCorrMass", ";AK8 jet softdrop PUPPI corrected mass (GeV);Events", 60, 0, 300), "emqq" );
    Book( TH1F( "Jet_chsTau21", ";AK8 jet CHS #tau_{21};Events", 50, 0, 1), "emqq" );
    Book( TH1F( "Jet_puppiTau21", ";AK8 jet PUPPI #tau_{21};Events", 50, 0, 1), "emqq" );
    Book( TH1F( "Jet_ddt", ";AK8 jet DDT;Events", 60, 0, 1.2), "emqq" );
    Book( TH1F( "Jet_csv1", ";AK8 jet subjet1 CSV;Events", 25, 0, 1), "emqq" );
    Book( TH1F( "Jet_csv2", ";AK8 jet subjet2 CSV;Events", 25, 0, 1), "emqq" );
    Book( TH1F( "Jet_dbt", ";AK8 jet double b-tagger;Events", 50, -1, 1), "emqq" );
    Book( TH1F( "MET_pt", ";#slash{E}_{T} (GeV);Events;log", 50, 0, 1500), "emqq" );
    Book( TH1F( "MET_phi", ";#slash{E}_{T} #varphi;Events", 30, 0, 3.15), "emqq" );
    Book( TH1F( "V_mass", ";m_{e#mu} (GeV);Events", 50, 0, 500), "emqq" );
    Book( TH1F( "V_pt", ";p^{e#mu}_{T} (GeV);Events;log", 50, 0, 500), "emqq" );
    Book( TH1F( "ST", ";ST (GeV);Events;log", 50, 0, 4000), "emqq" );
    Book( TH1F( "HT", ";HT (GeV);Events;log", 50, 0, 3000), "emqq" );
    Book( TH1F( "MHT", ";missing HT (GeV);Events;log", 50, 0, 3000), "emqq" );
    Book( TH1F( "nPV", ";number of primary vertices;Events", 60, 0, 60), "emqq" );
    Book( TH1F( "nElectrons", ";number of electrons;Events;log", 6, -0.5, 5.5), "emqq" );
    Book( TH1F( "nMuons", ";number of muons;Events;log", 6, -0.5, 5.5), "emqq" );
    Book( TH1F( "nTaus", ";number of #tau;Events;log", 6, -0.5, 5.5), "emqq" );
    Book( TH1F( "nPhotons", ";number of photons;Events;log", 6, -0.5, 5.5), "emqq" );
    Book( TH1F( "nJets", ";number of AK4 jets;Events;log", 10, -0.5, 9.5), "emqq" );
    Book( TH1F( "nFatJets", ";number of AK8 jets;Events;log", 10, -0.5, 9.5), "emqq" );
    Book( TH1F( "nBTagJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "emqq" );
    Book( TH1F( "nBVetoJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "emqq" );
    Book( TH1F( "ElectronJetDPhi", ";#Delta #varphi (electron-AK8 jet);Events", 28, 0, 3.15), "emqq" );
    Book( TH1F( "ElectronMetDPhi", ";#Delta #varphi (electron-#slash{E}_{T});Events", 28, 0, 3.15), "emqq" );
    Book( TH1F( "MuonJetDPhi", ";#Delta #varphi (muon-AK8 jet);Events", 28, 0, 3.15), "emqq" );
    Book( TH1F( "MuonMetDPhi", ";#Delta #varphi (muon-#slash{E}_{T});Events", 28, 0, 3.15), "emqq" );
    Book( TH1F( "ElectronMuonDPhi", ";#Delta #varphi (electron-muon);Events", 28, 0, 3.15), "emqq" );
    Book( TH1F( "ElectronMuonDR", ";#Delta R (electron-muon);Events", 25, 0, 5), "emqq" );
    Book( TH1F( "JetMetDPhi", ";#Delta #varphi (AK8 jet-#slash{E}_{T});Events", 28, 0, 3.15), "emqq" );
    Book( TH1F( "MinJetMetDPhi", ";min #Delta #varphi (jet-#slash{E}_{T});Events;log", 28, 0, 3.15), "emqq" );
    Book( TH1F( "MaxJetNoFatJetBTag", ";max AK4 jet CSV;Events", 25, 0, 1.), "emqq" );
    Book( TH1F( "Centrality", ";centrality;Events", 50, 0., 1.), "emqq" );
    Book( TH1F( "CosThetaStar", ";cos(#theta*);Events", 50, -1, 1.), "emqq" );
    Book( TH1F( "CosTheta1", ";cos(#theta_{1});Events", 50, -1, 1.), "emqq" );
    Book( TH1F( "CosTheta2", ";cos(#theta_{2});Events", 50, 0., 1.), "emqq" );
    Book( TH1F( "Phi", ";#phi;Events", 50, -3.15, 3.15), "emqq" );
    Book( TH1F( "Phi1", ";#phi_{1};Events", 50, -3.15, 3.15), "emqq" );
    Book( TH1F( "X_mass", ";m_{X} (GeV);Events;log", 80, 750, 4750), "emqq" );
    
    // ---------- SEMILEPTONIC Z->ee CHANNEL ----------
    Book( TH1F( "Z_mass", ";Z mass (GeV);Events", 40, 70, 110), "ee" );
    Book( TH1F( "Z_pt", ";p_{T}^{Z} (GeV);Events;log", 100, 0, 2000), "ee" );
    Book( TH1F( "Electron1_pt", ";electron 1 p_{T} (GeV);Events;log", 50, 0, 2000), "ee" );
    Book( TH1F( "Electron2_pt", ";electron 2 p_{T} (GeV);Events;log", 50, 0, 2000), "ee" );
    
    Book( TH1F( "EventWeight", ";Event Weight;Events", 100, 0., 2.), "eeqq" );
    Book( TH1F( "GenWeight", ";Gen Weight;Events", 100, 0., 2.), "eeqq" );
    Book( TH1F( "TopWeight", ";Top Weight;Events", 100, 0., 2.), "eeqq" );
    Book( TH1F( "PUWeight", ";Pileup Weight;Events", 100, 0., 2.), "eeqq" );
    Book( TH1F( "TriggerWeight", ";Trigger Weight;Events", 100, 0., 2.), "eeqq" );
    Book( TH1F( "LeptonWeight", ";Lepton Weight;Events", 100, 0., 2.), "eeqq" );
    Book( TH1F( "BTagWeight", ";BTag Weight;Events", 100, 0., 2.), "eeqq" );
    Book( TH1F( "BBTagWeight", ";BBTag Weight;Events", 100, 0., 2.), "eeqq" );
    Book( TH1F( "Electron1_pt", ";electron 1 p_{T} (GeV);Events;log", 50, 0, 2000), "eeqq" );
    Book( TH1F( "Electron1_eta", ";electron 1 #eta;Events", 30, -3., 3.), "eeqq" );
    Book( TH1F( "Electron1_phi", ";electron 1 #varphi;Events", 30, 0, 3.15), "eeqq" );
    Book( TH1F( "Electron1_mass", ";electron 1 mass (GeV);Events", 50, 0, 1.), "eeqq" );
    Book( TH1F( "Electron1_pfIso", ";electron 1 PFIso;Events;log", 25, 0, 10.), "eeqq" );
    Book( TH1F( "Electron1_pt_B", ";electron 1 p_{T} [barrel] (GeV);Events;log", 50, 0, 2000), "eeqq" );
    Book( TH1F( "Electron1_pt_E", ";electron 1 p_{T} [endcap] (GeV);Events;log", 50, 0, 2000), "eeqq" );
    Book( TH1F( "Electron2_pt", ";electron 2 p_{T} (GeV);Events;log", 50, 0, 1000), "eeqq" );
    Book( TH1F( "Electron2_eta", ";electron 2 #eta;Events", 30, -3., 3.), "eeqq" );
    Book( TH1F( "Electron2_phi", ";electron 2 #varphi;Events", 30, 0, 3.15), "eeqq" );
    Book( TH1F( "Electron2_mass", ";electron 2 mass (GeV);Events", 50, 0, 0.1), "eeqq" );
    Book( TH1F( "Electron2_pfIso", ";electron 2 PFIso;Events;log", 25, 0, 10.), "eeqq" );
    Book( TH1F( "Electron2_pt_B", ";electron 2 p_{T} [barrel] (GeV);Events;log", 50, 0, 2000), "eeqq" );
    Book( TH1F( "Electron2_pt_E", ";electron 2 p_{T} [endcap] (GeV);Events;log", 50, 0, 2000), "eeqq" );
    Book( TH1F( "Jet_pt", ";AK8 jet p_{T} (GeV);Events;log", 36, 200, 2000), "eeqq" );
    Book( TH1F( "Jet_eta", ";AK8 jet #eta;Events", 30, -3, 3), "eeqq" );
    Book( TH1F( "Jet_phi", ";AK8 jet #varphi;Events", 30, 0, 3.15), "eeqq" );
    Book( TH1F( "Jet_mass", ";AK8 jet ungroomed mass (GeV);Events", 60, 0, 300), "eeqq" );
    Book( TH1F( "Jet_chf", ";AK8 jet charged hadron fraction;Events", 25, 0, 1), "eeqq" );
    Book( TH1F( "Jet_nhf", ";AK8 jet neutral hadron fraction;Events", 25, 0, 1), "eeqq" );
    Book( TH1F( "Jet_phf", ";AK8 jet photon fraction;Events", 25, 0, 1), "eeqq" );
    Book( TH1F( "Jet_muf", ";AK8 jet muon fraction;Events", 25, 0, 1), "eeqq" );
    Book( TH1F( "Jet_emf", ";AK8 jet electron fraction;Events", 25, 0, 1), "eeqq" );
    Book( TH1F( "Jet_chm", ";AK8 jet charged hadron multiplicity;Events", 100, 0, 100), "eeqq" );
    Book( TH1F( "Jet_prunedMass", ";AK8 jet pruned mass (GeV);Events", 60, 0, 300), "eeqq" );
    Book( TH1F( "Jet_prunedCorrMass", ";AK8 jet pruned CHS corrected mass (GeV);Events", 60, 0, 300), "eeqq" );
    Book( TH1F( "Jet_softdropMass", ";AK8 jet softdrop PUPPI mass (GeV);Events", 60, 0, 300), "eeqq" );
    Book( TH1F( "Jet_softdropCorrMass", ";AK8 jet softdrop PUPPI corrected mass (GeV);Events", 60, 0, 300), "eeqq" );
    Book( TH1F( "Jet_chsTau21", ";AK8 jet CHS #tau_{21};Events", 50, 0, 1), "eeqq" );
    Book( TH1F( "Jet_puppiTau21", ";AK8 jet PUPPI #tau_{21};Events", 50, 0, 1), "eeqq" );
    Book( TH1F( "Jet_ddt", ";AK8 jet DDT;Events", 60, 0, 1.2), "eeqq" );
    Book( TH1F( "Jet_csv1", ";AK8 jet subjet1 CSV;Events", 25, 0, 1), "eeqq" );
    Book( TH1F( "Jet_csv2", ";AK8 jet subjet2 CSV;Events", 25, 0, 1), "eeqq" );
    Book( TH1F( "Jet_dbt", ";AK8 jet double b-tagger;Events", 50, -1, 1), "eeqq" );
    Book( TH1F( "MET_pt", ";#slash{E}_{T} (GeV);Events;log", 40, 0, 400), "eeqq" );
    Book( TH1F( "MET_phi", ";#slash{E}_{T} #varphi;Events", 30, 0, 3.15), "eeqq" );
    Book( TH1F( "Z_pt", ";p_{T}^{Z} (GeV);Events;log", 90, 200, 2000), "eeqq" );
    Book( TH1F( "Z_mass", ";Z mass (GeV);Events", 40, 70, 110), "eeqq" );
    Book( TH1F( "Z_mass_BB", ";Z mass [barrel-barrel] (GeV);Events", 40, 70, 110), "eeqq" );
    Book( TH1F( "Z_mass_BE", ";Z mass [barrel-endcaps] (GeV);Events", 40, 70, 110), "eeqq" );
    Book( TH1F( "Z_mass_EB", ";Z mass [endcaps-barrel] (GeV);Events", 40, 70, 110), "eeqq" );
    Book( TH1F( "Z_mass_EE", ";Z mass [endcaps-endcaps] (GeV);Events", 40, 70, 110), "eeqq" );
    Book( TH1F( "ST", ";ST (GeV);Events;log", 50, 0, 4000), "eeqq" );
    Book( TH1F( "HT", ";HT (GeV);Events;log", 50, 0, 3000), "eeqq" );
    Book( TH1F( "MHT", ";missing HT (GeV);Events;log", 50, 0, 2000), "eeqq" );
    Book( TH1F( "nPV", ";number of primary vertices;Events", 60, 0, 60), "eeqq" );
    Book( TH1F( "nElectrons", ";number of electrons;Events;log", 6, -0.5, 5.5), "eeqq" );
    Book( TH1F( "nMuons", ";number of muons;Events;log", 6, -0.5, 5.5), "eeqq" );
    Book( TH1F( "nTaus", ";number of #tau;Events;log", 6, -0.5, 5.5), "eeqq" );
    Book( TH1F( "nPhotons", ";number of photons;Events;log", 6, -0.5, 5.5), "eeqq" );
    Book( TH1F( "nJets", ";number of AK4 jets;Events;log", 10, -0.5, 9.5), "eeqq" );
    Book( TH1F( "nFatJets", ";number of AK8 jets;Events;log", 10, -0.5, 9.5), "eeqq" );
    Book( TH1F( "nBTagJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "eeqq" );
    Book( TH1F( "nBVetoJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "eeqq" );
    Book( TH1F( "JetMetDPhi", ";#Delta #varphi (AK8 jet-#slash{E}_{T});Events", 30, 0, 3.15), "eeqq" );
    Book( TH1F( "ZJetDPhi", ";|#Delta #varphi| (Z - AK8 jet);Events", 60, 0, 3.15), "eeqq" );
    Book( TH1F( "ZJetDEta", ";|#Delta #eta| (Z - AK8 jet);Events", 50, 0, 5), "eeqq" );
    Book( TH1F( "ElectronElectronDR", ";#Delta R (electron1 - electron2);Events", 50, 0, 5), "eeqq" );
    Book( TH1F( "MinJetMetDPhi", ";min #Delta #varphi (jet-#slash{E}_{T});Events;log", 30, 0, 3.15), "eeqq" );
    Book( TH1F( "MaxJetNoFatJetBTag", ";max AK4 jet CSV;Events", 25, 0, 1.), "eeqq" );
    Book( TH1F( "Centrality", ";centrality;Events", 50, 0., 1.), "eeqq" );
    Book( TH1F( "CosThetaStar", ";cos(#theta*);Events", 50, -1, 1.), "eeqq" );
    Book( TH1F( "CosTheta1", ";cos(#theta_{1});Events", 50, -1, 1.), "eeqq" );
    Book( TH1F( "CosTheta2", ";cos(#theta_{2});Events", 50, 0., 1.), "eeqq" );
    Book( TH1F( "Phi", ";#phi;Events", 50, -3.15, 3.15), "eeqq" );
    Book( TH1F( "Phi1", ";#phi_{1};Events", 50, -3.15, 3.15), "eeqq" );
    Book( TH1F( "X_mass", ";m_{X} (GeV);Events;log", 80, 750, 4750), "eeqq" );
    
    
    // ---------- SEMILEPTONIC Z->mm CHANNEL ----------
    Book( TH1F( "Z_mass", ";Z mass (GeV);Events", 40, 70, 110), "mm" );
    Book( TH1F( "Z_pt", ";p_{T}^{Z} (GeV);Events;log", 100, 0, 2000), "mm" );
    Book( TH1F( "Muon1_pt", ";muon 1 p_{T} (GeV);Events;log", 50, 0, 2000), "mm" );
    Book( TH1F( "Muon2_pt", ";muon 2 p_{T} (GeV);Events;log", 50, 0, 2000), "mm" );
    
    Book( TH1F( "EventWeight", ";Event Weight;Events", 100, 0., 2.), "mmqq" );
    Book( TH1F( "GenWeight", ";Gen Weight;Events", 100, 0., 2.), "mmqq" );
    Book( TH1F( "TopWeight", ";Top Weight;Events", 100, 0., 2.), "mmqq" );
    Book( TH1F( "PUWeight", ";Pileup Weight;Events", 100, 0., 2.), "mmqq" );
    Book( TH1F( "TriggerWeight", ";Trigger Weight;Events", 100, 0., 2.), "mmqq" );
    Book( TH1F( "LeptonWeight", ";Lepton Weight;Events", 100, 0., 2.), "mmqq" );
    Book( TH1F( "BTagWeight", ";BTag Weight;Events", 100, 0., 2.), "mmqq" );
    Book( TH1F( "BBTagWeight", ";BBTag Weight;Events", 100, 0., 2.), "mmqq" );
    Book( TH1F( "Muon1_pt", ";muon 1 p_{T} (GeV);Events;log", 50, 0, 2000), "mmqq" );
    Book( TH1F( "Muon1_eta", ";muon 1 #eta;Events", 30, -3., 3.), "mmqq" );
    Book( TH1F( "Muon1_phi", ";muon 1 #varphi;Events", 30, 0, 3.15), "mmqq" );
    Book( TH1F( "Muon1_mass", ";muon 1 mass (GeV);Events", 50, 0, 1.), "mmqq" );
    Book( TH1F( "Muon1_trkIso", ";muon 1 tracker Iso;Events;log", 50, 0, 5.), "mmqq" );
    Book( TH1F( "Muon1_pt_B", ";muon 1 p_{T} [barrel] (GeV);Events;log", 50, 0, 2000), "mmqq" );
    Book( TH1F( "Muon1_pt_E", ";muon 1 p_{T} [endcap] (GeV);Events;log", 50, 0, 2000), "mmqq" );
    Book( TH1F( "Muon2_pt", ";muon 2 p_{T};Events;log", 50, 0, 1000), "mmqq" );
    Book( TH1F( "Muon2_eta", ";muon 2 #eta;Events", 30, -3., 3.), "mmqq" );
    Book( TH1F( "Muon2_phi", ";muon 2 #varphi;Events", 30, 0, 3.15), "mmqq" );
    Book( TH1F( "Muon2_mass", ";muon 2 mass (GeV);Events", 50, 0, 0.1), "mmqq" );
    Book( TH1F( "Muon2_trkIso", ";muon 2 tracker Iso;Events;log", 50, 0, 5.), "mmqq" );
    Book( TH1F( "Muon2_pt_B", ";muon 2 p_{T} [barrel] (GeV);Events;log", 50, 0, 2000), "mmqq" );
    Book( TH1F( "Muon2_pt_E", ";muon 2 p_{T} [endcap] (GeV);Events;log", 50, 0, 2000), "mmqq" );
    Book( TH1F( "Jet_pt", ";AK8 jet p_{T} (GeV);Events;log", 36, 200, 2000), "mmqq" );
    Book( TH1F( "Jet_eta", ";AK8 jet #eta;Events", 30, -3, 3), "mmqq" );
    Book( TH1F( "Jet_phi", ";AK8 jet #varphi;Events", 30, 0, 3.15), "mmqq" );
    Book( TH1F( "Jet_mass", ";AK8 jet ungroomed mass (GeV);Events", 60, 0, 300), "mmqq" );
    Book( TH1F( "Jet_chf", ";AK8 jet charged hadron fraction;Events", 25, 0, 1), "mmqq" );
    Book( TH1F( "Jet_nhf", ";AK8 jet neutral hadron fraction;Events", 25, 0, 1), "mmqq" );
    Book( TH1F( "Jet_phf", ";AK8 jet photon fraction;Events", 25, 0, 1), "mmqq" );
    Book( TH1F( "Jet_muf", ";AK8 jet muon fraction;Events", 25, 0, 1), "mmqq" );
    Book( TH1F( "Jet_emf", ";AK8 jet electron fraction;Events", 25, 0, 1), "mmqq" );
    Book( TH1F( "Jet_chm", ";AK8 jet charged hadron multiplicity;Events", 100, 0, 100), "mmqq" );
    Book( TH1F( "Jet_prunedMass", ";AK8 jet pruned mass (GeV);Events", 60, 0, 300), "mmqq" );
    Book( TH1F( "Jet_prunedCorrMass", ";AK8 jet pruned CHS corrected mass (GeV);Events", 60, 0, 300), "mmqq" );
    Book( TH1F( "Jet_softdropMass", ";AK8 jet softdrop PUPPI mass (GeV);Events", 60, 0, 300), "mmqq" );
    Book( TH1F( "Jet_softdropCorrMass", ";AK8 jet softdrop PUPPI corrected mass (GeV);Events", 60, 0, 300), "mmqq" );
    Book( TH1F( "Jet_chsTau21", ";AK8 jet CHS #tau_{21};Events", 50, 0, 1), "mmqq" );
    Book( TH1F( "Jet_puppiTau21", ";AK8 jet PUPPI #tau_{21};Events", 50, 0, 1), "mmqq" );
    Book( TH1F( "Jet_ddt", ";AK8 jet DDT;Events", 60, 0, 1.2), "mmqq" );
    Book( TH1F( "Jet_csv1", ";AK8 jet subjet1 CSV;Events", 25, 0, 1), "mmqq" );
    Book( TH1F( "Jet_csv2", ";AK8 jet subjet2 CSV;Events", 25, 0, 1), "mmqq" );
    Book( TH1F( "Jet_dbt", ";AK8 jet double b-tagger;Events", 50, -1, 1), "mmqq" );
    Book( TH1F( "MET_pt", ";#slash{E}_{T} (GeV);Events;log", 40, 0, 400), "mmqq" );
    Book( TH1F( "MET_phi", ";#slash{E}_{T} #varphi;Events", 30, 0, 3.15), "mmqq" );
    Book( TH1F( "Z_pt", ";p_{T}^{Z} (GeV);Events;log", 90, 200, 2000), "mmqq" );
    Book( TH1F( "Z_mass", ";Z mass (GeV);Events", 40, 70, 110), "mmqq" );
    Book( TH1F( "Z_mass_BB", ";Z mass [barrel-barrel] (GeV);Events", 40, 70, 110), "mmqq" );
    Book( TH1F( "Z_mass_BE", ";Z mass [barrel-endcaps] (GeV);Events", 40, 70, 110), "mmqq" );
    Book( TH1F( "Z_mass_EB", ";Z mass [endcaps-barrel] (GeV);Events", 40, 70, 110), "mmqq" );
    Book( TH1F( "Z_mass_EE", ";Z mass [endcaps-endcaps] (GeV);Events", 40, 70, 110), "mmqq" );
    Book( TH1F( "ST", ";ST (GeV);Events;log", 50, 0, 4000), "mmqq" );
    Book( TH1F( "HT", ";HT (GeV);Events;log", 50, 0, 3000), "mmqq" );
    Book( TH1F( "MHT", ";missing HT (GeV);Events;log", 50, 0, 2000), "mmqq" );
    Book( TH1F( "nPV", ";number of primary vertices;Events", 60, 0, 60), "mmqq" );
    Book( TH1F( "nElectrons", ";number of electrons;Events;log", 6, -0.5, 5.5), "mmqq" );
    Book( TH1F( "nMuons", ";number of muons;Events;log", 6, -0.5, 5.5), "mmqq" );
    Book( TH1F( "nTaus", ";number of #tau;Events;log", 6, -0.5, 5.5), "mmqq" );
    Book( TH1F( "nPhotons", ";number of photons;Events;log", 6, -0.5, 5.5), "mmqq" );
    Book( TH1F( "nJets", ";number of AK4 jets;Events;log", 10, -0.5, 9.5), "mmqq" );
    Book( TH1F( "nFatJets", ";number of AK8 jets;Events;log", 10, -0.5, 9.5), "mmqq" );
    Book( TH1F( "nBTagJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "mmqq" );
    Book( TH1F( "nBVetoJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "mmqq" );
    Book( TH1F( "JetMetDPhi", ";#Delta #varphi (AK8 jet-#slash{E}_{T});Events", 30, 0, 3.15), "mmqq" );
    Book( TH1F( "ZJetDPhi", ";|#Delta #varphi| (Z - AK8 jet);Events", 60, 0, 3.15), "mmqq" );
    Book( TH1F( "ZJetDEta", ";|#Delta #eta| (Z - AK8 jet);Events", 50, 0, 5), "mmqq" );
    Book( TH1F( "MuonMuonDR", ";#Delta R (muon1 - muon2);Events", 50, 0, 5), "mmqq" );
    Book( TH1F( "MinJetMetDPhi", ";min #Delta #varphi (jet-#slash{E}_{T});Events;log", 30, 0, 3.15), "mmqq" );
    Book( TH1F( "MaxJetNoFatJetBTag", ";max AK4 jet CSV;Events", 25, 0, 1.), "mmqq" );
    Book( TH1F( "Centrality", ";centrality;Events", 50, 0., 1.), "mmqq" );
    Book( TH1F( "CosThetaStar", ";cos(#theta*);Events", 50, -1, 1.), "mmqq" );
    Book( TH1F( "CosTheta1", ";cos(#theta_{1});Events", 50, -1, 1.), "mmqq" );
    Book( TH1F( "CosTheta2", ";cos(#theta_{2});Events", 50, 0., 1.), "mmqq" );
    Book( TH1F( "Phi", ";#phi;Events", 50, -3.15, 3.15), "mmqq" );
    Book( TH1F( "Phi1", ";#phi_{1};Events", 50, -3.15, 3.15), "mmqq" );
    Book( TH1F( "X_mass", ";m_{X} (GeV);Events;log", 80, 750, 4750), "mmqq" );
    
    
    
    // ---------- ALL HADRONIC CHANNEL ----------
    Book( TH1F( "EventWeight", ";Event Weight;Events", 100, 0., 2.), "qqqq" );
    Book( TH1F( "GenWeight", ";Gen Weight;Events", 100, 0., 2.), "qqqq" );
    Book( TH1F( "TopWeight", ";Top Weight;Events", 100, 0., 2.), "qqqq" );
    Book( TH1F( "PUWeight", ";Pileup Weight;Events", 100, 0., 2.), "qqqq" );
    Book( TH1F( "TriggerWeight", ";Trigger Weight;Events", 100, 0., 2.), "qqqq" );
    Book( TH1F( "LeptonWeight", ";Lepton Weight;Events", 100, 0., 2.), "qqqq" );
    Book( TH1F( "BTagWeight", ";BTag Weight;Events", 100, 0., 2.), "qqqq" );
    Book( TH1F( "BBTagWeight", ";BBTag Weight;Events", 100, 0., 2.), "qqqq" );
    Book( TH1F( "Jet1_pt", ";AK8 jet 1 p_{T} (GeV);Events;log", 92, 200, 2500), "qqqq" );
    Book( TH1F( "Jet1_eta", ";AK8 jet 1 #eta;Events", 30, -3, 3), "qqqq" );
    Book( TH1F( "Jet1_phi", ";AK8 jet 1 #varphi;Events", 30, 0, 3.15), "qqqq" );
    Book( TH1F( "Jet1_mass", ";AK8 jet 1 ungroomed mass (GeV);Events", 60, 0, 300), "qqqq" );
    Book( TH1F( "Jet1_chf", ";AK8 jet 1 charged hadron fraction;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet1_nhf", ";AK8 jet 1 neutral hadron fraction;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet1_phf", ";AK8 jet 1 photon fraction;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet1_muf", ";AK8 jet 1 muon fraction;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet1_emf", ";AK8 jet 1 electron fraction;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet1_chm", ";AK8 jet 1 charged hadron multiplicity;Events", 100, 0, 100), "qqqq" );
    Book( TH1F( "Jet1_prunedMass", ";AK8 jet 1 pruned mass (GeV);Events", 60, 0, 300), "qqqq" );
    Book( TH1F( "Jet1_prunedCorrMass", ";AK8 jet 1 pruned CHS corrected mass (GeV);Events", 60, 0, 300), "qqqq" );
    Book( TH1F( "Jet1_softdropMass", ";AK8 jet 1 softdrop PUPPI mass (GeV);Events", 60, 0, 300), "qqqq" );
    Book( TH1F( "Jet1_softdropCorrMass", ";AK8 jet 1 softdrop corrected mass (GeV);Events", 60, 0, 300), "qqqq" );
    Book( TH1F( "Jet1_chsTau21", ";AK8 jet 1 CHS #tau_{21};Events", 50, 0, 1), "qqqq" );
    Book( TH1F( "Jet1_puppiTau21", ";AK8 jet 1 PUPPI #tau_{21};Events", 50, 0, 1), "qqqq" );
    Book( TH1F( "Jet1_ddt", ";AK8 jet 1 DDT;Events", 60, 0, 1.2), "qqqq" );
    Book( TH1F( "Jet1_csv1", ";AK8 jet 1 subjet1 CSV;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet1_csv2", ";AK8 jet 1 subjet2 CSV;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet1_dbt", ";AK8 jet 1 double b-tagger;Events", 50, -1, 1), "qqqq" );
    Book( TH1F( "Jet2_pt", ";AK8 jet 2 p_{T} (GeV);Events;log", 92, 200, 2500), "qqqq" );
    Book( TH1F( "Jet2_eta", ";AK8 jet 2 #eta;Events", 30, -3, 3), "qqqq" );
    Book( TH1F( "Jet2_phi", ";AK8 jet 2 #varphi;Events", 30, 0, 3.15), "qqqq" );
    Book( TH1F( "Jet2_mass", ";AK8 jet 2 ungroomed mass (GeV);Events", 60, 0, 300), "qqqq" );
    Book( TH1F( "Jet2_chf", ";AK8 jet 2 charged hadron fraction;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet2_nhf", ";AK8 jet 2 neutral hadron fraction;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet2_phf", ";AK8 jet 2 photon fraction;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet2_muf", ";AK8 jet 2 muon fraction;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet2_emf", ";AK8 jet 2 electron fraction;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet2_chm", ";AK8 jet 2 charged hadron multiplicity;Events", 100, 0, 100), "qqqq" );
    Book( TH1F( "Jet2_prunedMass", ";AK8 jet 2 pruned mass (GeV);Events", 60, 0, 300), "qqqq" );
    Book( TH1F( "Jet2_prunedCorrMass", ";AK8 jet 2 pruned CHS corrected mass (GeV);Events", 60, 0, 300), "qqqq" );
    Book( TH1F( "Jet2_softdropMass", ";AK8 jet 2 softdrop PUPPI mass (GeV);Events", 60, 0, 300), "qqqq" );
    Book( TH1F( "Jet2_softdropCorrMass", ";AK8 jet 2 softdrop corrected mass (GeV);Events", 60, 0, 300), "qqqq" );
    Book( TH1F( "Jet2_chsTau21", ";AK8 jet 2 CHS #tau_{21};Events", 50, 0, 1), "qqqq" );
    Book( TH1F( "Jet2_puppiTau21", ";AK8 jet 2 PUPPI #tau_{21};Events", 50, 0, 1), "qqqq" );
    Book( TH1F( "Jet2_ddt", ";AK8 jet 2 DDT;Events", 60, 0, 1.2), "qqqq" );
    Book( TH1F( "Jet2_csv1", ";AK8 jet 2 subjet1 CSV;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet2_csv2", ";AK8 jet 2 subjet2 CSV;Events", 25, 0, 1), "qqqq" );
    Book( TH1F( "Jet2_dbt", ";AK8 jet 2 double b-tagger;Events", 50, -1, 1), "qqqq" );
    Book( TH1F( "MET_pt", ";#slash{E}_{T} (GeV);Events;log", 40, 0, 400), "qqqq" );
    Book( TH1F( "MET_phi", ";#slash{E}_{T} #varphi;Events", 30, 0, 3.15), "qqqq" );
    Book( TH1F( "ST", ";ST (GeV);Events;log", 100, 0, 5000), "qqqq" );
    Book( TH1F( "HT", ";HT (GeV);Events;log", 100, 0, 5000), "qqqq" );
    Book( TH1F( "MHT", ";missing HT (GeV);Events;log", 100, 0, 1000), "qqqq" );
    Book( TH1F( "nPV", ";number of primary vertices;Events", 60, 0, 60), "qqqq" );
    Book( TH1F( "nElectrons", ";number of electrons;Events;log", 6, -0.5, 5.5), "qqqq" );
    Book( TH1F( "nMuons", ";number of muons;Events;log", 6, -0.5, 5.5), "qqqq" );
    Book( TH1F( "nTaus", ";number of #tau;Events;log", 6, -0.5, 5.5), "qqqq" );
    Book( TH1F( "nPhotons", ";number of photons;Events;log", 6, -0.5, 5.5), "qqqq" );
    Book( TH1F( "nJets", ";number of AK4 jets;Events;log", 15, -0.5, 14.5), "qqqq" );
    Book( TH1F( "nFatJets", ";number of AK8 jets;Events;log", 10, -0.5, 9.5), "qqqq" );
    Book( TH1F( "nBTagJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "qqqq" );
    Book( TH1F( "nBVetoJets", ";number of b-tagged AK4 jets;Events;log", 6, -0.5, 5.5), "qqqq" );
    Book( TH1F( "JetMetDPhi", ";#Delta #varphi (AK8 jet-#slash{E}_{T});Events", 30, 0, 3.15), "qqqq" );
    Book( TH1F( "Jet1MetDPhi", ";#Delta #varphi (AK8 jet-#slash{E}_{T});Events", 30, 0, 3.15), "qqqq" );
    Book( TH1F( "Jet2MetDPhi", ";#Delta #varphi (AK8 jet-#slash{E}_{T});Events", 30, 0, 3.15), "qqqq" );
    Book( TH1F( "Jet1Jet2DPhi", ";|#Delta #varphi| (V - H);Events", 60, 0, 3.15), "qqqq" );
    Book( TH1F( "Jet1Jet2DEta", ";|#Delta #eta| (V - H);Events", 50, 0, 5), "qqqq" );
    Book( TH1F( "MinJetMetDPhi", ";min #Delta #varphi (jet-#slash{E}_{T});Events;log", 30, 0, 3.15), "qqqq" );
    Book( TH1F( "MaxJetNoFatJetBTag", ";max AK4 jet CSV;Events", 25, 0, 1.), "qqqq" );
    Book( TH1F( "X_mass", ";m_{X} (GeV);Events;log", 120, 0, 6000), "qqqq" );
    Book( TH1F( "Centrality", ";centrality;Events", 50, 0., 1.), "qqqq" );
    Book( TH1F( "CosThetaStar", ";cos(#theta*);Events", 50, -1, 1.), "qqqq" );
    Book( TH1F( "CosTheta1", ";cos(#theta_{1});Events", 50, -1, 1.), "qqqq" );
    Book( TH1F( "CosTheta2", ";cos(#theta_{2});Events", 50, 0., 1.), "qqqq" );
    Book( TH1F( "Phi", ";#phi;Events", 50, -3.15, 3.15), "qqqq" );
    Book( TH1F( "Phi1", ";#phi_{1};Events", 50, -3.15, 3.15), "qqqq" );
    Book( TH1F( "CandidateMatching", ";;Events;", 3, -0.5, 2.5), "qqqq" );
    
    
    // Gen
    Book( TH1F( "LheV_pt", ";V p_{T} (GeV);Events;log", 400, 0, 4000), "Gen" );
    Book( TH1F( "GenV_pt", ";V p_{T} (GeV);Events;log", 400, 0, 4000), "Gen" );
    Book( TH1F( "LheV_mass", ";V mass (GeV);Events;log", 50, 0, 150), "Gen" );
    Book( TH1F( "GenV_mass", ";V mass (GeV);Events;log", 50, 0, 150), "Gen" );
    Book( TH1F( "Lhe_HT", ";HT (GeV);Events;log", 400, 0, 4000), "Gen" );
    Book( TH1F( "Gen_HT", ";HT (GeV);Events;log", 400, 0, 4000), "Gen" );
    Book( TH1F( "LheNl", ";number of gen leptons;Events;log", 5, -0.5, 4.5), "Gen" );
    Book( TH1F( "LheNj", ";number of gen partons;Events;log", 5, -0.5, 4.5), "Gen" );
    
    // Trigger
    Book( TH1F( "HLT_PFMET170_vs_SingleElectron_NUM", ";MET (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET170_vs_SingleElectron_DEN", ";MET (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET120_PFMHT120_vs_SingleElectron_NUM", ";MET (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET120_PFMHT120_vs_SingleElectron_DEN", ";MET (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMETNoMu120_PFMHTNoMu120_vs_SingleElectron_NUM", ";min(MET, MHT) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMETNoMu120_PFMHTNoMu120_vs_SingleElectron_DEN", ";min(MET, MHT) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET_OR_vs_SingleElectron_NUM", ";min(MET, MHT) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET_OR_vs_SingleElectron_DEN", ";min(MET, MHT) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET170_vs_SingleMuon_NUM", ";MET (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET170_vs_SingleMuon_DEN", ";MET (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET120_PFMHT120_vs_SingleMuon_NUM", ";MET (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET120_PFMHT120_vs_SingleMuon_DEN", ";MET (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMETNoMu120_PFMHTNoMu120_vs_SingleMuon_NUM", ";min(METNoMu, MHTNoMu) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMETNoMu120_PFMHTNoMu120_vs_SingleMuon_DEN", ";min(METNoMu, MHTNoMu) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET_OR_vs_SingleMuon_NUM", ";min(METNoMu, MHTNoMu) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET_OR_vs_SingleMuon_DEN", ";min(METNoMu, MHTNoMu) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET_OR_vs_JetHT_NUM", ";min(MET, MHT) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET_OR_vs_JetHT_DEN", ";min(MET, MHT) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET_OR_NUM", ";min(METNoMu, MHTNoMu) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_PFMET_OR_DEN", ";min(METNoMu, MHTNoMu) (GeV);Efficiency", 50, 100, 600), "Trigger" );
    Book( TH1F( "HLT_SingleEle_vs_SingleElectron_NUM", ";Electron p_{T} (GeV);Efficiency", 20, 0, 1000), "Trigger" );
    Book( TH1F( "HLT_SingleEle_vs_SingleElectron_DEN", ";Electron p_{T} (GeV);Efficiency", 20, 0, 1000), "Trigger" );
    Book( TH1F( "HLT_SingleEle_vs_MET_NUM", ";Electron p_{T} (GeV);Efficiency", 20, 0, 1000), "Trigger" );
    Book( TH1F( "HLT_SingleEle_vs_MET_DEN", ";Electron p_{T} (GeV);Efficiency", 20, 0, 1000), "Trigger" );
    Book( TH1F( "HLT_SingleIsoEle_vs_MET_NUM", ";Electron p_{T} (GeV);Efficiency", 20, 0, 1000), "Trigger" );
    Book( TH1F( "HLT_SingleIsoEle_vs_MET_DEN", ";Electron p_{T} (GeV);Efficiency", 20, 0, 1000), "Trigger" );
    Book( TH1F( "HLT_SingleNonIsoEle_vs_MET_NUM", ";Electron p_{T} (GeV);Efficiency", 20, 0, 1000), "Trigger" );
    Book( TH1F( "HLT_SingleNonIsoEle_vs_MET_DEN", ";Electron p_{T} (GeV);Efficiency", 20, 0, 1000), "Trigger" );
    Book( TH1F( "HLT_SingleEle_vs_MET_COUNT", ";SingleEle trigger pass (GeV);Events", 2, -0.5, 1.5), "Trigger" );
    Book( TH1F( "HLT_SingleEleMETInclusive_COUNT", ";SingleEle trigger pass (GeV);Events", 2, -0.5, 1.5), "Trigger" );
    Book( TH1F( "HLT_SingleEleMET250_COUNT", ";SingleEle trigger pass (GeV);Events", 2, -0.5, 1.5), "Trigger" );
    Book( TH1F( "HLT_DoubleEleMETInclusive_COUNT", ";DoubleEle trigger pass (GeV);Events", 3, -0.5, 2.5), "Trigger" );
    Book( TH1F( "HLT_DoubleEleMET250_COUNT", ";DoubleEle trigger pass (GeV);Events", 3, -0.5, 2.5), "Trigger" );
    
    Book( TH1F( "HLT_PFHT(800,900)_vs_Xmass_NUM", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_PFHT(800,900)_vs_Xmass_DEN", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AK8PFJet450_vs_Xmass_NUM", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AK8PFJet450_vs_Xmass_DEN", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_PFHT650_WideJetMJJ(900,950)_vs_Xmass_NUM", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_PFHT650_WideJetMJJ(900,950)_vs_Xmass_DEN", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_PFHT_OR_vs_Xmass_NUM", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_PFHT_OR_vs_Xmass_DEN", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AK8PFJet360_TrimMass30_vs_Jmass_NUM", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH1F( "HLT_AK8PFJet360_TrimMass30_vs_Jmass_DEN", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH1F( "HLT_AK8PFHT700_TrimMass50_vs_Jmass_NUM", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH1F( "HLT_AK8PFHT700_TrimMass50_vs_Jmass_DEN", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH1F( "HLT_Subtructure_OR_vs_Jmass_NUM", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH1F( "HLT_Subtructure_OR_vs_Jmass_DEN", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH1F( "HLT_AK8DiPFJet(250,280)_200_TrimMass30_BTagCSV_p20_Cat1B_vs_Jmass_NUM", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH1F( "HLT_AK8DiPFJet(250,280)_200_TrimMass30_BTagCSV_p20_Cat1B_vs_Jmass_DEN", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH1F( "HLT_AK8DiPFJet(250,280)_200_TrimMass30_BTagCSV_p20_Cat2B_vs_Jmass_NUM", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH1F( "HLT_AK8DiPFJet(250,280)_200_TrimMass30_BTagCSV_p20_Cat2B_vs_Jmass_DEN", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_Cat1B_vs_Xmass_NUM", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_Cat1B_vs_Xmass_DEN", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_Cat2B_vs_Xmass_NUM", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_Cat2B_vs_Xmass_DEN", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_CatHP_vs_Xmass_NUM", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_CatHP_vs_Xmass_DEN", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_CatLP_vs_Xmass_NUM", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_CatLP_vs_Xmass_DEN", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_CatWR_vs_Xmass_NUM", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_CatWR_vs_Xmass_DEN", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_CatZR_vs_Xmass_NUM", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_CatZR_vs_Xmass_DEN", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_vs_Xmass_NUM", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_vs_Xmass_DEN", ";m_{jj} invariant mass (GeV);Efficiency", 75, 500, 2000), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_vs_Jmass_NUM", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH1F( "HLT_AllHad_OR_vs_Jmass_DEN", ";jet softdrop puppi mass (GeV);Efficiency", 40, 0, 200), "Trigger" );
    Book( TH2F( "HLT_AllHad_OR_NUM", ";m_{jj} invariant mass (GeV);jet softdrop puppi mass (GeV);Efficiency", 60, 500, 2000, 40, 0, 200), "Trigger" );
    Book( TH2F( "HLT_AllHad_OR_DEN", ";m_{jj} invariant mass (GeV);jet softdrop puppi mass (GeV);Efficiency", 60, 500, 2000, 40, 0, 200), "Trigger" );
    
    // Electron efficiency
    Book( TH1F( "dR", "Electrons;#Delta R_{ee};Efficiency", 25, 0., 1.), "Electrons" );
    Book( TH1F( "pT", "Electrons;p_{T}^{ee} (GeV);Efficiency", 45, 200, 2000), "Electrons" );
    Book( TH1F( "pT1", "Electrons;p_{T}^{e} (GeV);Efficiency", 20, 50, 2050), "Electrons" );
    Book( TH1F( "pT2", "Electrons;p_{T}^{e} (GeV);Efficiency", 20, 50, 2050), "Electrons" );
    Book( TH1F( "pT1_LooseId", "Electrons;p_{T}^{e} (GeV);Efficiency", 20, 50, 2050), "Electrons" );
    Book( TH1F( "pT2_LooseId", "Electrons;p_{T}^{e} (GeV);Efficiency", 20, 50, 2050), "Electrons" );
    Book( TH1F( "dR_VetoVetoId", "Electrons;#Delta R_{ee};Efficiency", 25, 0., 1.), "Electrons" );
    Book( TH1F( "pT_VetoVetoId", "Electrons;p_{T}^{ee} (GeV);Efficiency", 45, 200, 2000), "Electrons" );
    Book( TH1F( "dR_LooseLooseId", "Electrons;#Delta R_{ee};Efficiency", 25, 0., 1.), "Electrons" );
    Book( TH1F( "pT_LooseLooseId", "Electrons;p_{T}^{ee} (GeV);Efficiency", 45, 200, 2000), "Electrons" );
    Book( TH1F( "dR_MediumMediumId", "Electrons;#Delta R_{ee};Efficiency", 25, 0., 1.), "Electrons" );
    Book( TH1F( "pT_MediumMediumId", "Electrons;p_{T}^{ee} (GeV);Efficiency", 45, 200, 2000), "Electrons" );
    Book( TH1F( "dR_TightTightId", "Electrons;#Delta R_{ee};Efficiency", 25, 0., 1.), "Electrons" );
    Book( TH1F( "pT_TightTightId", "Electrons;p_{T}^{ee} (GeV);Efficiency", 45, 200, 2000), "Electrons" );
    Book( TH1F( "dR_HeepHeepId", "Electrons;#Delta R_{ee};Efficiency", 25, 0., 1.), "Electrons" );
    Book( TH1F( "pT_HeepHeepId", "Electrons;p_{T}^{ee} (GeV);Efficiency", 45, 200, 2000), "Electrons" );
    
    // Muon efficiency
    Book( TH1F( "dR", "Muons;#Delta R_{#mu#mu};Efficiency", 25, 0., 1.), "Muons" );
    Book( TH1F( "pT", "Muons;p_{T}^{#mu#mu} (GeV);Efficiency", 45, 200, 2000), "Muons" );
    Book( TH1F( "pT1", "Muons;p_{T}^{#mu} (GeV);Efficiency", 20, 50, 2050), "Muons" );
    Book( TH1F( "pT2", "Muons;p_{T}^{#mu} (GeV);Efficiency", 20, 50, 2050), "Muons" );
    Book( TH1F( "pT1_HighptId", "Muons;p_{T}^{#mu} (GeV);Efficiency", 20, 50, 2050), "Muons" );
    Book( TH1F( "pT2_HighptId", "Muons;p_{T}^{#mu} (GeV);Efficiency", 20, 50, 2050), "Muons" );
    Book( TH1F( "pT1_TrackerId", "Muons;p_{T}^{#mu} (GeV);Efficiency", 20, 50, 2050), "Muons" );
    Book( TH1F( "pT2_TrackerId", "Muons;p_{T}^{#mu} (GeV);Efficiency", 20, 50, 2050), "Muons" );
    Book( TH1F( "dR_HighptHighptId", "Muons;#Delta R_{#mu#mu};Efficiency", 25, 0., 1.), "Muons" );
    Book( TH1F( "pT_HighptHighptId", "Muons;p_{T}^{#mu#mu} (GeV);Efficiency", 45, 200, 2000), "Muons" );
    Book( TH1F( "dR_LooseLooseId", "Muons;#Delta R_{#mu#mu};Efficiency", 25, 0., 1.), "Muons" );
    Book( TH1F( "pT_LooseLooseId", "Muons;p_{T}^{#mu#mu} (GeV);Efficiency", 45, 200, 2000), "Muons" );
    Book( TH1F( "dR_MediumMediumId", "Muons;#Delta R_{#mu#mu};Efficiency", 25, 0., 1.), "Muons" );
    Book( TH1F( "pT_MediumMediumId", "Muons;p_{T}^{#mu#mu} (GeV);Efficiency", 45, 200, 2000), "Muons" );
    Book( TH1F( "dR_TightTightId", "Muons;#Delta R_{#mu#mu};Efficiency", 25, 0., 1.), "Muons" );
    Book( TH1F( "pT_TightTightId", "Muons;p_{T}^{#mu#mu} (GeV);Efficiency", 45, 200, 2000), "Muons" );
    Book( TH1F( "dR_HighptTrackerId", "Muons;#Delta R_{#mu#mu};Efficiency", 25, 0., 1.), "Muons" );
    Book( TH1F( "pT_HighptTrackerId", "Muons;p_{T}^{#mu#mu} (GeV);Efficiency", 45, 200, 2000), "Muons" );
    Book( TH1F( "dR_HighptTrackerIdTrackerIso", "Muons;#Delta R_{#mu#mu};Efficiency", 25, 0., 1.), "Muons" );
    Book( TH1F( "pT_HighptTrackerIdTrackerIso", "Muons;p_{T}^{#mu#mu} (GeV);Efficiency", 45, 200, 2000), "Muons" );
    Book( TH1F( "dR_HighptTrackerIdTrackerNonCorrIso", "Muons;#Delta R_{#mu#mu};Efficiency", 25, 0., 1.), "Muons" );
    Book( TH1F( "pT_HighptTrackerIdTrackerNonCorrIso", "Muons;p_{T}^{#mu#mu} (GeV);Efficiency", 45, 200, 2000), "Muons" );
    Book( TH1F( "dR_HighptTrackerIdPFIso", "Muons;#Delta R_{#mu#mu};Efficiency", 25, 0., 1.), "Muons" );
    Book( TH1F( "pT_HighptTrackerIdPFIso", "Muons;p_{T}^{#mu#mu} (GeV);Efficiency", 45, 200, 2000), "Muons" );
    
    // MET
    Book( TH1F( "METFilters", "Events;", 15, -0.5, 14.5), "MET" );
    
    // Systematics
    Book( TH1F( "J_energy_scale", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "J_energy_res", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "V_mass_scale", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "V_mass_res", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "H_mass_scale", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "H_mass_res", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "W_mass_scale", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "W_mass_res", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "Z_mass_scale", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "Z_mass_res", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "V_tau21_extr_HP", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "V_tau21_extr_LP", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "H_tagging", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "ElecT_eff", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "Elec1_eff", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "Elec2_eff", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "MuonT_eff", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "Muon1_eff", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "Muon2_eff", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "MuonTrkIso_eff", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "Pileup", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "PDF_scale", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "PDF_accept", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "QCD_scale", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "BTagSF_veto", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "H_subjet_notag", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "H_subjet_loose", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "H_subjet_tight", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "H_doubleB_notag", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "H_doubleB_loose", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "H_doubleB_tight", "Events;deviation (s. d.)", 3, -1.5, 1.5), "Sys" );
    Book( TH1F( "X_mass_scale", "Events;m_{X} (GeV)", 500, 0, 5000), "Sys" );
    Book( TH1F( "X_mass_scaleUp", "Events;m_{X} (GeV)", 500, 0, 5000), "Sys" );
    Book( TH1F( "X_mass_scaleDown", "Events;m_{X} (GeV)", 500, 0, 5000), "Sys" );
    Book( TH1F( "X_mass_res", "Events;m_{X} (GeV)", 500, 0, 5000), "Sys" );
    Book( TH1F( "X_mass_resUp", "Events;m_{X} (GeV)", 500, 0, 5000), "Sys" );
    Book( TH1F( "X_mass_resDown", "Events;m_{X} (GeV)", 500, 0, 5000), "Sys" );
    Book( TH1F( "X_mass_unc", "Events;m_{X} (GeV)", 500, 0, 5000), "Sys" );
    Book( TH1F( "X_mass_uncUp", "Events;m_{X} (GeV)", 500, 0, 5000), "Sys" );
    Book( TH1F( "X_mass_uncDown", "Events;m_{X} (GeV)", 500, 0, 5000), "Sys" );
    
    // Propaganda plots
    Book( TH1F( "Data_mass", ";soft drop jet mass (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "Data_tau21", ";N-subjettiness  #tau_{21};Events;", 80, 0., 1.), "Norm" );
    Book( TH1F( "Data_dbt", ";Higgs b tagging discriminator;Events;", 120, -1.2, 1.2), "Norm" );
    Book( TH1F( "Bkg_mass", ";soft drop jet mass (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "Bkg_tau21", ";N-subjettiness  #tau_{21};Events;", 80, 0., 1.), "Norm" );
    Book( TH1F( "Bkg_dbt", ";Higgs b tagging discriminator;Events;", 120, -1.2, 1.2), "Norm" );
    Book( TH1F( "H_mass", ";soft drop jet mass (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "H_tau21", ";N-subjettiness  #tau_{21};Events;", 80, 0., 1.), "Norm" );
    Book( TH1F( "H_dbt", ";Higgs b tagging discriminator;Events;", 120, -1.2, 1.2), "Norm" );
    Book( TH1F( "V_mass", ";soft drop jet mass (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "V_tau21", ";N-subjettiness  #tau_{21};Events;", 80, 0., 1.), "Norm" );
    Book( TH1F( "V_dbt", ";Higgs b tagging discriminator;Events;", 120, -1.2, 1.2), "Norm" );
    Book( TH1F( "H_mass_nGen", ";number of gen leptons in the Higgs jet (GeV);Events;", 5, -0.5, 4.5), "Norm" );
    Book( TH1F( "H_mass_nReco", ";number of reco leptons in the Higgs jet (GeV);Events;", 5, -0.5, 4.5), "Norm" );
    Book( TH1F( "H_mass_0g", ";soft drop jet mass with 0 leptons (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "H_mass_1g", ";soft drop jet mass with 1 lepton (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "H_mass_2g", ";soft drop jet mass with 2 leptons (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "H_mass_0l", ";soft drop jet mass with 0 leptons (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "H_mass_1l", ";soft drop jet mass with 1 lepton (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "H_mass_2l", ";soft drop jet mass with 2 leptons (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "H_mass_gen", ";soft drop jet mass with correction at gen level (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "H_mass_reco", ";soft drop jet mass with collinear correction (GeV);Events;", 80, 0., 200.), "Norm" );
    Book( TH1F( "H_mass_F", ";jet mass correction factor;Events;", 100, 0., 2.), "Norm" );
    return;
}

void VHAnalysis::EndInputData( const SInputData& ) throw( SError ) {
   
   return;

}

void VHAnalysis::BeginInputFile( const SInputData& ) throw( SError ) {
    m_logger << INFO << "Connecting input variables" << SLogger::endmsg;

    if(m_isData) m_eventInfo.ConnectVariables( m_recoTreeName.c_str(), Ntuple::EventInfoTrigger|Ntuple::EventInfoMETFilters|Ntuple::EventInfoMuonFilters, "" );
    else m_eventInfo.ConnectVariables( m_recoTreeName.c_str(), Ntuple::EventInfoBasic|Ntuple::EventInfoTrigger|Ntuple::EventInfoMETFilters|Ntuple::EventInfoTruth|Ntuple::EventInfoPDF, "" );

    if(m_isData) m_electron.ConnectVariables( m_recoTreeName.c_str(), Ntuple::ElectronBasic|Ntuple::ElectronID|Ntuple::ElectronAdvancedID|Ntuple::ElectronIsolation|Ntuple::ElectronSuperCluster, (m_electronName + "_").c_str() ); // |Ntuple::ElectronShowerID
    else m_electron.ConnectVariables( m_recoTreeName.c_str(), Ntuple::ElectronBasic|Ntuple::ElectronID|Ntuple::ElectronAdvancedID|Ntuple::ElectronIsolation|Ntuple::ElectronSuperCluster, (m_electronName + "_").c_str() );
    m_muon.ConnectVariables( m_recoTreeName.c_str(), Ntuple::MuonBasic|Ntuple::MuonID|Ntuple::MuonIsolation|Ntuple::MuonTrack, (m_muonName + "_").c_str() );
    m_tau.ConnectVariables( m_recoTreeName.c_str(), Ntuple::TauBasic|Ntuple::TauID|Ntuple::TauAdvancedID, (m_tauName + "_").c_str() );

    if(m_isData) m_jetAK4.ConnectVariables( m_recoTreeName.c_str(), Ntuple::JetBasic|Ntuple::JetAnalysis, (m_jetAK4Name + "_").c_str() );
    else m_jetAK4.ConnectVariables( m_recoTreeName.c_str(), Ntuple::JetBasic|Ntuple::JetAnalysis|Ntuple::JetTruth, (m_jetAK4Name + "_").c_str() );

    if(m_isData) m_jetAK8.ConnectVariables( m_recoTreeName.c_str(), Ntuple::JetBasic|Ntuple::JetAnalysis|Ntuple::JetSubstructure|Ntuple::JetSoftdropSubjets, (m_jetAK8Name + "_").c_str() );
    else {
        m_jetAK8.ConnectVariables( m_recoTreeName.c_str(), Ntuple::JetBasic|Ntuple::JetAnalysis|Ntuple::JetSubstructure|Ntuple::JetTruth|Ntuple::JetSoftdropSubjets|Ntuple::JetSoftdropSubjetsTruth|Ntuple::JetJER, (m_jetAK8Name + "_").c_str() );
        m_genjetAK8.ConnectVariables( m_recoTreeName.c_str(), Ntuple::GenJetTruth, "" ); //(m_genjetAK8Name + "_").c_str()
    }
    
    m_jetAK8Puppi.ConnectVariables( m_recoTreeName.c_str(), Ntuple::PuppiJetBasic|Ntuple::PuppiJetAnalysis|Ntuple::PuppiJetSoftdropSubjets, "" );
    
    m_missingEt.ConnectVariables( m_recoTreeName.c_str(), Ntuple::MissingEtBasic|Ntuple::MissingEtAnalysis|Ntuple::MissingEtAnalysisSyst , (m_missingEtName + "_").c_str() );
    if(!m_isData) m_genParticle.ConnectVariables( m_recoTreeName.c_str(), Ntuple::GenParticleBasic, (m_genParticleName + "_").c_str() );

    m_logger << INFO << "Connecting input variables completed" << SLogger::endmsg;
    return;
}



void VHAnalysis::ExecuteEvent( const SInputData&, Double_t ) throw( SError ) {
    
    clearBranches();
    std::string sample(this->GetHistInputFile()->GetName());
    
    m_logger << INFO << "ExecuteEvent\tevent: " << m_eventInfo.eventNumber << "\tlumi: " << m_eventInfo.lumiBlock << "\trun: " << m_eventInfo.runNumber << "\tin sample: " << sample << SLogger::endmsg;
    
    // --- Preliminary operations ---
    isMC = !m_isData;
    EventNumber = m_eventInfo.eventNumber;
    LumiNumber = m_eventInfo.lumiBlock;
    RunNumber = m_eventInfo.runNumber;
    nPV = m_eventInfo.PV_N;
    
    // Gen Weight
    if(isMC) {
        GenWeight = (m_eventInfo.genWeight < 0) ? -1 : 1;
        //PUWeight = getPUWeight();
        for(unsigned int v = 0; v < (m_eventInfo.actualIntPerXing)->size(); ++v) {
            if ( (*m_eventInfo.bunchCrossing)[v] == 0 ) {
                int npu( (*m_eventInfo.actualIntPerXing)[v] );
                PUWeight = m_pileupReweightingTool.getPileUpweight( npu );
                PUWeightUp = m_pileupReweightingTool.getPileUpweight( npu, +1 );
                PUWeightDown = m_pileupReweightingTool.getPileUpweight( npu, -1 );
                m_logger << VERBOSE << "Weight: " << PUWeight << " for true: " << (*m_eventInfo.actualIntPerXing)[v] << SLogger::endmsg;
                break;
            }
        }
        EventWeight *= GenWeight;
        EventWeight *= PUWeight;
    }
    // Check JSON
    else {
        if(!isGoodEvent(m_eventInfo.runNumber, m_eventInfo.lumiBlock)) {m_logger << INFO << " - Event not in JSON"  << SLogger::endmsg; throw SError( SError::SkipEvent ); }
    }
    if(!passMETFilters(!isMC)) {m_logger << INFO << " - Event fails MET filters"  << SLogger::endmsg; throw SError( SError::SkipEvent ); }
    
    std::map<std::string, bool> triggerMap;
//    if(!isMC) 
    triggerMap = getTriggerMap();
    
    // --- Electrons ---
    m_logger << INFO << " + Opening Electron collection" << SLogger::endmsg;
    std::vector<UZH::Electron> ElecVect, ElecIsoVect;
    std::vector<TLorentzVector> CalibratedElecVect;
    for(int i = 0; i < m_electron.N; ++i) {
        UZH::Electron el(&m_electron, i);
        if(el.pt() < m_ElecPtCut || fabs(el.eta()) > m_ElecEtaCut) continue;
        if(el.isLooseElectron()) {
            ElecIsoVect.push_back(el);
            ST += el.pt();
        }
        ElecVect.push_back(el);
        //double energy = m_CorrectionTool.GetCorrectedEnergy(el.e(), isMC, m_eventInfo.runNumber, (fabs(el.eta()) < 1.4442), 1., el.superCluster_eta(), el.et()); //isMC ? 1. : el.full5x5_r9()
        TLorentzVector el_tlv;
        el_tlv.SetPtEtaPhiE(el.pt(), el.eta(), el.phi(), el.e());
        //el_tlv *= energy/el.e(); FIXME
        CalibratedElecVect.push_back(el_tlv);
    }
    nElectrons = ElecIsoVect.size();
    
    // --- Muons ---
    m_logger << INFO << " + Opening Muon collection" << SLogger::endmsg;
    std::vector<UZH::Muon> MuonVect, MuonIsoVect;
    for(int i = 0; i < m_muon.N; ++i) {
        UZH::Muon mu(&m_muon, i);
        if(mu.pt() < m_MuonPtCut || fabs(mu.eta()) > m_MuonEtaCut) continue;
        if(mu.isLooseMuon()==1 && mu.pfDeltaCorrRelIso()<0.25) {
            MuonIsoVect.push_back(mu);
            ST += mu.pt();
        }
        MuonVect.push_back(mu);
    }
    nMuons = MuonIsoVect.size();
    
    // --- Taus ---
    m_logger << INFO << " + Opening Tau collection" << SLogger::endmsg;
    std::vector<UZH::Tau> TauVect;
    for(int i = 0; i < m_tau.N; ++i) {
        UZH::Tau tau(&m_tau, i);
        if( !(tau.pt() > m_TauPtCut && fabs(tau.eta()) < m_TauEtaCut && tau.byVTightIsolationMVArun2v1PWnewDMwLT()) ) continue; //byVTightIsolationMVArun2v1DBnewDMwLT()
        bool cleanTau(true);
        for(unsigned int e = 0; e < ElecIsoVect.size(); e++) if(ElecIsoVect[e].tlv().DeltaR(tau.tlv()) < 0.4) cleanTau = false;
        for(unsigned int m = 0; m < MuonIsoVect.size(); m++) if(MuonIsoVect[m].tlv().DeltaR(tau.tlv()) < 0.4) cleanTau = false;
        if(!cleanTau) continue;
        nTaus++;
    }
    
    // --- AK8 Jets ---
    m_logger << INFO << " + Opening AK8 collection" << SLogger::endmsg;
    std::vector<UZH::Jet> FatJetsVect;
    std::vector<TLorentzVector> FatJetsVectRes;
    std::vector<TLorentzVector> FatJetsVectScaleUp;
    std::vector<TLorentzVector> FatJetsVectScaleDown;
    std::vector<TLorentzVector> FatJetsVectResUp;
    std::vector<TLorentzVector> FatJetsVectResDown;
    std::vector<TLorentzVector> FatJetsPuppiVect;
    std::vector<int> FatJetsBTagVect;
    std::vector<float> FatJetsTau21Vect;
    std::vector<float> FatJetsMassVect;
    std::vector<float> FatJetsMassGenVect;
    std::vector<float> FatJetsMassVectScaleUp;
    std::vector<float> FatJetsMassVectScaleDown;
    std::vector<float> FatJetsMassVectResUp;
    std::vector<float> FatJetsMassVectResDown;
    
    for(int i = 0; i < m_jetAK8.N; ++i) {
        UZH::Jet jet(&m_jetAK8, i);
        if(jet.pt() < m_AK8PtCut || fabs(jet.eta()) > m_AK8EtaCut || !jet.IDLoose()) continue;
        if(!jet.IDLoose()) continue;
        bool cleanJet(true);
        for(unsigned int e = 0; e < ElecIsoVect.size(); e++) if(ElecIsoVect[e].tlv().DeltaR(jet.tlv()) < 0.8) cleanJet = false;
        for(unsigned int m = 0; m < MuonIsoVect.size(); m++) if(MuonIsoVect[m].tlv().DeltaR(jet.tlv()) < 0.8) cleanJet = false;
        if(!cleanJet) continue;
        //if(jet.subjet_softdrop_N() < 2) continue; // SoftDrop algorithm has failed
        // Count btags
        int nbtag(0);
        for(unsigned int j = 0; j < 2; j++) if(jet.subjet_softdrop_N() > (int)j && m_bTaggingScaleTool.isTagged( jet.subjet_softdrop_csv()[j]) ) nbtag++;
        // Match with PUPPI jet
        float mass(-1.), genmass(-1.), tau21(-1.);
        TLorentzVector jetPuppi_tlv;
        for(unsigned int j = 0; j < (*m_jetAK8Puppi.jetAK8_puppi_pt).size(); ++j) {
            UZH::PuppiJet jetPuppi( &m_jetAK8Puppi, j );
            if(jetPuppi.jetAK8_puppi_pt() <= 0.) continue;
            jetPuppi_tlv.SetPtEtaPhiE(jetPuppi.jetAK8_puppi_pt(), jetPuppi.jetAK8_puppi_eta(), jetPuppi.jetAK8_puppi_phi(), jetPuppi.jetAK8_puppi_e());
            if(jet.tlv().DeltaR(jetPuppi_tlv) < 0.8) {
                mass = jetPuppi.jetAK8_puppi_softdrop_mass();
                tau21 = jetPuppi.jetAK8_puppi_tau1() ? jetPuppi.jetAK8_puppi_tau2() / jetPuppi.jetAK8_puppi_tau1() : -1.;
                break;
            }
        }
        if(mass < 0.) {//continue;
            jetPuppi_tlv = jet.tlv();
            mass = jet.softdrop_mass();
            tau21 = jet.tau1() ? jet.tau2() / jet.tau1() : -1.;
        }
        if(isMC) {
            // gen Jet matching
            for(unsigned int j = 0; j < (*m_genjetAK8.genJetAK8_pt).size(); ++j) {
                UZH::GenJet genjet(&m_genjetAK8, j);
                TLorentzVector gentlv;
                gentlv.SetPtEtaPhiE(genjet.genJetAK8_pt(), genjet.genJetAK8_eta(), genjet.genJetAK8_phi(), genjet.genJetAK8_e());
                if(gentlv.DeltaR(jet.tlv()) < 0.8 && fabs(gentlv.Pt() - jet.pt())/jet.pt() < 0.3 ) genmass = genjet.genJetAK8_softdropmass();
            }
            // is the genjet matching fails, use gen info
            if(m_isSignal && genmass < 0) {
                for(int j = 0; j < m_genParticle.N; ++j) {
                    UZH::GenParticle gen(&m_genParticle, j);
                    if(abs(gen.pdgId()) >= 23 && abs(gen.pdgId()) <= 25 && gen.tlv().DeltaR(jet.tlv()) < 0.8) genmass = gen.m();
                }
            }
        }
        // Correct mass
        float massScaleUp(mass), massScaleDown(mass), massResUp(mass), massResDown(mass);
        if(m_isSignal) {
            massScaleUp = m_CorrectionTool.GetCorrectedMass(massScaleUp, genmass, jetPuppi_tlv.Pt(), jetPuppi_tlv.Eta(), isMC, +1, 0);
            massScaleDown = m_CorrectionTool.GetCorrectedMass(massScaleDown, genmass, jetPuppi_tlv.Pt(), jetPuppi_tlv.Eta(), isMC, -1, 0);
            massResUp = m_CorrectionTool.GetCorrectedMass(massResUp, genmass, jetPuppi_tlv.Pt(), jetPuppi_tlv.Eta(), isMC, 0, +1);
            massResDown = m_CorrectionTool.GetCorrectedMass(massResDown, genmass, jetPuppi_tlv.Pt(), jetPuppi_tlv.Eta(), isMC, 0, -1);
        }
        mass = m_CorrectionTool.GetCorrectedMass(mass, genmass, jetPuppi_tlv.Pt(), jetPuppi_tlv.Eta(), isMC);
        FatJetsVect.push_back(jet);
        FatJetsPuppiVect.push_back(jetPuppi_tlv);
        FatJetsTau21Vect.push_back(tau21);
        FatJetsBTagVect.push_back(nbtag);
        FatJetsMassVect.push_back(mass);
        FatJetsMassGenVect.push_back(genmass);
        FatJetsMassVectScaleUp.push_back(massScaleUp);
        FatJetsMassVectScaleDown.push_back(massScaleDown);
        FatJetsMassVectResUp.push_back(massResUp);
        FatJetsMassVectResDown.push_back(massResDown);
        // JES
        TLorentzVector jetScaleUp(jet.tlv()), jetScaleDown(jet.tlv()), jetResUp(jet.tlv()), jetResDown(jet.tlv()), jetRes(jet.tlv());
        if(m_isSignal) {
            jetScaleUp *= jet.jecUp() / jet.jec();
            jetScaleDown *= jet.jecDown() / jet.jec();
            jetResUp = m_CorrectionTool.GetCorrectedJet(jet.tlv(), float(jet.jer_sigma_pt()), float(jet.jer_sf()), float(jet.jer_sf_up()), float(jet.jer_sf_down()), +1);
            jetResDown = m_CorrectionTool.GetCorrectedJet(jet.tlv(), float(jet.jer_sigma_pt()), float(jet.jer_sf()), float(jet.jer_sf_up()), float(jet.jer_sf_down()), -1);
            jetRes = m_CorrectionTool.GetCorrectedJet(jet.tlv(), float(jet.jer_sigma_pt()), float(jet.jer_sf()), float(jet.jer_sf_up()), float(jet.jer_sf_down()), 0);
        }
        FatJetsVectRes.push_back( jetRes );
        FatJetsVectScaleUp.push_back( jetScaleUp );
        FatJetsVectScaleDown.push_back( jetScaleDown );
        FatJetsVectResUp.push_back( jetResUp );
        FatJetsVectResDown.push_back( jetResDown );
    }
    nFatJets = FatJetsVect.size();
    
    
    // --- AK4 Jets ---
    m_logger << INFO << " + Opening AK4 collection" << SLogger::endmsg;
    std::vector<UZH::Jet> JetsVect, JetsNoFatJetVect, JetsNoFatJetsVect;
    for(int i = 0; i < m_jetAK4.N; ++i) {
        UZH::Jet jet(&m_jetAK4, i);
        if(jet.pt() < m_AK4PtCut || fabs(jet.eta()) > m_AK4EtaCut || !jet.IDLoose()) continue;
        if(!jet.IDLoose()) continue;
        bool cleanJet(true);
        for(unsigned int e = 0; e < ElecIsoVect.size(); e++) if(ElecIsoVect[e].tlv().DeltaR(jet.tlv()) < 0.4) cleanJet = false;
        for(unsigned int m = 0; m < MuonIsoVect.size(); m++) if(MuonIsoVect[m].tlv().DeltaR(jet.tlv()) < 0.4) cleanJet = false;
        if(!cleanJet) continue;
        JetsVect.push_back(jet);
        if(FatJetsVect.size()>0 && FatJetsVect[0].tlv().DeltaR(jet.tlv()) > 1.2) JetsNoFatJetVect.push_back(jet);
        if(FatJetsVect.size()>1 && FatJetsVect[0].tlv().DeltaR(jet.tlv()) > 1.2 && FatJetsVect[1].tlv().DeltaR(jet.tlv()) > 1.2) JetsNoFatJetsVect.push_back(jet);
        ST += jet.pt();
        HT += jet.pt();
        HTx += jet.tlv().Px();
        HTy += jet.tlv().Py();
    }
    nJets = JetsVect.size();
    MHT = sqrt(HTx*HTx + HTy*HTy);
    MHTNoMu = MHT;

    // --- MET ---
    m_logger << INFO << " + Opening MET collection" << SLogger::endmsg;
    UZH::MissingEt MET( &m_missingEt, 0 );
    TLorentzVector MET_tlv;
    MET_tlv.SetPtEtaPhiE(MET.et(), 0., MET.phi(), MET.et());
    //METNoMu = (MuonIsoVect.size() == 1 && MuonIsoVect[0].pt()>30. && fabs(MuonIsoVect[0].eta()) < 2.1 && MuonIsoVect[0].isTightMuon()==1) ? sqrt(pow(MET_tlv.Px() + MuonVect[0].tlv().Px(), 2) + pow(MET_tlv.Py() + MuonVect[0].tlv().Py(), 2)) : MET.et();
    METNoMu = MET.et();
    float METx(MET_tlv.Px()), METy(MET_tlv.Py());
    for(unsigned int i=0; i<MuonIsoVect.size(); i++) {METx += MuonVect[i].tlv().Px(); METy += MuonVect[i].tlv().Py();}
    METNoMu = sqrt(METx*METx + METy*METy);
    MinMETMHT = std::min(float(MET.et()), MHT);
    MinMETNoMuMHTNoMu = std::min(METNoMu, MHTNoMu);
    MaxMETNoMuMHTNoMu = std::max(METNoMu, MHTNoMu);
    
    // --- GEN ---
    m_logger << INFO << " + Opening Gen collection" << SLogger::endmsg;
    bool m_isZ( sample.find("DYJetsToLL") != std::string::npos || sample.find("DYJetsToNuNu") != std::string::npos || sample.find("ZJetsToNuNu") != std::string::npos );
    bool m_isW( sample.find("WJetsToLNu") != std::string::npos );
    TLorentzVector GenH;
    TLorentzVector GenV;
    TLorentzVector LepP;
    TLorentzVector LepM;
    int GenVpdgId(0), GenLepPpdgId(0), GenLepMpdgId(0), HjetIndex(-1), VjetIndex(-1);
    float GenVPt(-1.), GenHT(0.), GenTopPt(-1.), GenAntiTopPt(-1.), TopPtWeight(1.), AntiTopPtWeight(1.);
    // Z and W electroweak corrections
    if(isMC && (m_isSignal || m_isZ || m_isW)) {
        for(int i = 0; i < m_genParticle.N; ++i) {
            UZH::GenParticle gen(&m_genParticle, i);
            if(gen.status()==23) GenHT += gen.pt();
            if(GenH.Pt()<=0. && (gen.pdgId() == 25)) GenH = gen.tlv();
            if(GenV.Pt()<=0. && (gen.pdgId() == 23 || gen.pdgId() == 24) && gen.nDau()>0. && fabs(gen.dau()[0])!=gen.pdgId()) {GenV = gen.tlv(); GenVpdgId = gen.pdgId();}
            if(LepP.Pt()<=gen.pt() && ((gen.pdgId() >= +11 && gen.pdgId() <= +16 && gen.status()==1) || (gen.pdgId() == +15 && gen.status()==2)) ) {LepP = gen.tlv(); GenLepPpdgId = gen.pdgId();}
            if(LepM.Pt()<=gen.pt() && ((gen.pdgId() >= -16 && gen.pdgId() <= -11 && gen.status()==1) || (gen.pdgId() == -15 && gen.status()==2)) ) {LepM = gen.tlv(); GenLepMpdgId = gen.pdgId();}
        }
        if(GenV.Pt()>0.) GenVPt = GenV.Pt();
        else if(LepP.Pt()>0. && LepM.Pt()>0.) {GenVPt = (LepP+LepM).Pt(); GenVpdgId = (GenLepPpdgId == -GenLepMpdgId) ? 23 : 24;}
        
        if(GenVPt > 0. && m_isZ) ZewkWeight *= m_ScaleFactorTool.GetEwkZ(GenVPt);
        if(GenVPt > 0. && m_isW) WewkWeight *= m_ScaleFactorTool.GetEwkW(GenVPt);
        EventWeight *= WewkWeight * ZewkWeight;
    }
    // TTbar pT reweighting
    if(isMC && (sample.find("TT") != std::string::npos)) {
        //if(m_eventInfo.lheNj < 6) TopWeight *= 0.5;
        for(int i = 0; i < m_genParticle.N; ++i) {
            UZH::GenParticle gen(&m_genParticle, i);
            if(gen.pdgId() == +6) GenTopPt = gen.pt();
            if(gen.pdgId() == -6) GenAntiTopPt = gen.pt();
            //if(gen.status()==23 || gen.status()==33) std::cout << gen.pdgId() << "   " << gen.status() << std::endl;
        }
        if(GenTopPt>0.) TopPtWeight = exp(0.0615 - 0.0005*GenTopPt);
        if(GenAntiTopPt>0.) AntiTopPtWeight = exp(0.0615 - 0.0005*GenAntiTopPt);
        TopWeight *= sqrt(TopPtWeight * AntiTopPtWeight);
        //GenWeight *= TopWeight;
        //EventWeight *= TopWeight;
    }
    // Gen histograms
    Hist("LheV_pt", "Gen")->Fill(m_eventInfo.lheV_pt, GenWeight);
    Hist("GenV_pt", "Gen")->Fill(GenVPt, GenWeight);
    Hist("LheV_mass", "Gen")->Fill(m_eventInfo.lheV_pt, GenWeight);
    Hist("GenV_mass", "Gen")->Fill(GenV.M(), GenWeight);
    Hist("Lhe_HT", "Gen")->Fill(m_eventInfo.lheHT, GenWeight);
    Hist("Gen_HT", "Gen")->Fill(GenHT, GenWeight);
    Hist("LheNl", "Gen")->Fill(m_eventInfo.lheNl, GenWeight);
    Hist("LheNj", "Gen")->Fill(m_eventInfo.lheNj, GenWeight);
    
    LheNl = m_eventInfo.lheNl;
    LheNj = m_eventInfo.lheNj;
    
    // Propaganda plots
    if(m_isSignal) {
        if(nFatJets >= 2) {
            for(int i = 0; i < nFatJets; i++) if(GenH.Pt() > 0. && GenH.DeltaR(FatJetsVect[i].tlv()) < 0.8) {HjetIndex = i; break;}
            for(int i = 0; i < nFatJets; i++) if(GenV.Pt() > 0. && GenV.DeltaR(FatJetsVect[i].tlv()) < 0.8) {VjetIndex = i; break;}
            if(HjetIndex >= 0 && VjetIndex < 0) VjetIndex = (HjetIndex == 0 ? 1 : 0);
            else if(VjetIndex >= 0 && HjetIndex < 0) HjetIndex = (VjetIndex == 0 ? 1 : 0);
            else {
                if(abs(FatJetsVect[0].hadronFlavour()) == 5) {HjetIndex = 0; VjetIndex = 1;}
                else {HjetIndex = 1; VjetIndex = 0;}
            }
            Hist("H_mass", "Norm")->Fill(FatJetsMassVect[HjetIndex], EventWeight);
            Hist("H_tau21", "Norm")->Fill(FatJetsTau21Vect[HjetIndex], EventWeight);
            if(FatJetsMassVect[HjetIndex] > 50. && FatJetsVect[HjetIndex].pt() > 250. && FatJetsVect[HjetIndex].IDTight()) Hist("H_dbt", "Norm")->Fill(FatJetsVect[HjetIndex].Hbbtag(), EventWeight);
            Hist("V_mass", "Norm")->Fill(FatJetsMassVect[VjetIndex], EventWeight);
            Hist("V_tau21", "Norm")->Fill(FatJetsTau21Vect[VjetIndex], EventWeight);
            if(FatJetsMassVect[VjetIndex] > 50. && FatJetsVect[VjetIndex].pt() > 250. && FatJetsVect[VjetIndex].IDTight()) Hist("V_dbt", "Norm")->Fill(FatJetsVect[VjetIndex].Hbbtag(), EventWeight);
            
            // Find gen leptons within H jet
            int nGenInH(0), nLepInH(0);
            TLorentzVector H_gen(FatJetsVect[HjetIndex].tlv()), H_corr(FatJetsVect[HjetIndex].tlv());
            for(int i = 0; i < m_genParticle.N; ++i) {
                UZH::GenParticle gen(&m_genParticle, i);
                if(gen.status()==1 && (abs(gen.pdgId()) == 11 || abs(gen.pdgId()) == 13) && gen.tlv().DeltaR(FatJetsVect[HjetIndex].tlv()) < 0.8 ) {
                    nGenInH++;
                    H_gen += gen.tlv();
                }
            }
            if(nGenInH==0) Hist("H_mass_0g", "Norm")->Fill(FatJetsMassVect[HjetIndex], EventWeight);
            if(nGenInH==1) Hist("H_mass_1g", "Norm")->Fill(FatJetsMassVect[HjetIndex], EventWeight);
            if(nGenInH>=2) Hist("H_mass_2g", "Norm")->Fill(FatJetsMassVect[HjetIndex], EventWeight);
            std::vector<UZH::Muon> MuonVect, MuonIsoVect;
            for(int i = 0; i < m_muon.N; ++i) {
                UZH::Muon mu(&m_muon, i);
                if(mu.pt()>5. && fabs(mu.eta())<2.4 && mu.isLooseMuon()==1 && mu.tlv().DeltaR(FatJetsVect[HjetIndex].tlv()) < 0.8) {
                    nLepInH++;
                    H_corr += mu.tlv();
                }
            }
            for(int i = 0; i < m_electron.N; ++i) {
                UZH::Electron el(&m_electron, i);
                if(el.pt()>5. && fabs(el.eta())<2.5 && el.tlv().DeltaR(FatJetsVect[HjetIndex].tlv()) < 0.8) {
                    nLepInH++;
                    H_corr += el.tlv();
                }
            }
            if(nLepInH==0) Hist("H_mass_0l", "Norm")->Fill(FatJetsMassVect[HjetIndex], EventWeight);
            if(nLepInH==1) Hist("H_mass_1l", "Norm")->Fill(FatJetsMassVect[HjetIndex], EventWeight);
            if(nLepInH>=2) Hist("H_mass_2l", "Norm")->Fill(FatJetsMassVect[HjetIndex], EventWeight);
            // Correction (approximate)
            float corrGen = H_gen.M()/FatJetsVect[HjetIndex].tlv().M();
            float corrReco = H_corr.M()/FatJetsVect[HjetIndex].tlv().M();
            //
            Hist("H_mass_nGen", "Norm")->Fill(nGenInH);
            Hist("H_mass_nReco", "Norm")->Fill(nLepInH);
            Hist("H_mass_F", "Norm")->Fill(corrReco, EventWeight);
            Hist("H_mass_gen", "Norm")->Fill(FatJetsMassVect[HjetIndex]*corrGen, EventWeight);
            Hist("H_mass_reco", "Norm")->Fill(FatJetsMassVect[HjetIndex]*corrReco, EventWeight);
        }
    }
    else if(isMC) {
        if(nFatJets >= 1) {
            Hist("Bkg_mass", "Norm")->Fill(FatJetsMassVect[0], EventWeight);
            Hist("Bkg_tau21", "Norm")->Fill(FatJetsTau21Vect[0], EventWeight);
            if(FatJetsMassVect[0] > 50. && FatJetsVect[0].pt() > 250. && FatJetsVect[0].IDTight()) Hist("Bkg_dbt", "Norm")->Fill(FatJetsVect[0].Hbbtag(), EventWeight);
        }
    }
    else {
        if(nFatJets >= 1) {
            Hist("Data_mass", "Norm")->Fill(FatJetsMassVect[0], EventWeight);
            Hist("Data_tau21", "Norm")->Fill(FatJetsTau21Vect[0], EventWeight);
            if(FatJetsMassVect[0] > 50. && FatJetsVect[0].pt() > 250. && FatJetsVect[0].IDTight()) Hist("Data_dbt", "Norm")->Fill(FatJetsVect[0].Hbbtag(), EventWeight);
        }
    }
    Hist("PDF_accept", "Sys")->Fill(0., EventWeight);
    Hist("PDF_accept", "Sys")->Fill(+1., EventWeight*m_eventInfo.pdf_rms);
    Hist("PDF_accept", "Sys")->Fill(-1., EventWeight*(2.-m_eventInfo.pdf_rms));
    
    // --- TRIGGER ---
    m_logger << INFO << " + Evaluating Trigger" << SLogger::endmsg;
    if(!isMC) {
        if(ElecIsoVect.size() + MuonIsoVect.size() > 0) {
            // MET Trigger with Single Electron
            if(triggerMap["SingleIsoEle"] && ElecIsoVect.size() == 1 && ElecIsoVect[0].pt() > 30. && ElecIsoVect[0].isTightElectron() && fabs(ElecIsoVect[0].tlv().DeltaPhi(MET_tlv))>0.5 && FatJetsVect.size()>0) {
                Hist("HLT_PFMET170_vs_SingleElectron_DEN", "Trigger")->Fill(MET.et(), 1.);
                Hist("HLT_PFMET120_PFMHT120_vs_SingleElectron_DEN", "Trigger")->Fill(MinMETMHT, 1.);
                Hist("HLT_PFMETNoMu120_PFMHTNoMu120_vs_SingleElectron_DEN", "Trigger")->Fill(MinMETMHT, 1.);
                Hist("HLT_PFMET_OR_vs_SingleElectron_DEN", "Trigger")->Fill(MinMETMHT, 1.);
                Hist("HLT_PFMET_OR_DEN", "Trigger")->Fill(MinMETMHT, 1.);
                if(triggerMap["MET"]) Hist("HLT_PFMET170_vs_SingleElectron_NUM", "Trigger")->Fill(MET.et(), 1.);
                if(triggerMap["METMHT"]) Hist("HLT_PFMET120_PFMHT120_vs_SingleElectron_NUM", "Trigger")->Fill(MinMETMHT, 1.);
                if(triggerMap["METMHTNoMu"]) Hist("HLT_PFMETNoMu120_PFMHTNoMu120_vs_SingleElectron_NUM", "Trigger")->Fill(MinMETMHT, 1.);
                if(triggerMap["MET"] || triggerMap["METMHT"] || triggerMap["METMHTNoMu"]) {
                    Hist("HLT_PFMET_OR_vs_SingleElectron_NUM", "Trigger")->Fill(MinMETMHT, 1.);
                    Hist("HLT_PFMET_OR_NUM", "Trigger")->Fill(MinMETMHT, 1.);
                }
            }
            // MET Trigger with Single Muon
            if(triggerMap["SingleIsoMu"] && MuonIsoVect.size() == 1 && MuonIsoVect[0].pt() > 30. && fabs(MuonIsoVect[0].eta()) < 2.1 && MuonIsoVect[0].isTightMuon()==1 && FatJetsVect.size()>0) {
                Hist("HLT_PFMET170_vs_SingleMuon_DEN", "Trigger")->Fill(MET.et(), 1.);
                Hist("HLT_PFMET120_PFMHT120_vs_SingleMuon_DEN", "Trigger")->Fill(MinMETMHT, 1.);
                Hist("HLT_PFMETNoMu120_PFMHTNoMu120_vs_SingleMuon_DEN", "Trigger")->Fill(MinMETNoMuMHTNoMu, 1.);
                Hist("HLT_PFMET_OR_vs_SingleMuon_DEN", "Trigger")->Fill(MinMETMHT, 1.);
                Hist("HLT_PFMET_OR_DEN", "Trigger")->Fill(MinMETMHT, 1.);
                if(triggerMap["MET"]) Hist("HLT_PFMET170_vs_SingleMuon_NUM", "Trigger")->Fill(MET.et(), 1.);
                if(triggerMap["METMHT"]) Hist("HLT_PFMET120_PFMHT120_vs_SingleMuon_NUM", "Trigger")->Fill(MinMETMHT, 1.);
                if(triggerMap["METMHTNoMu"]) Hist("HLT_PFMETNoMu120_PFMHTNoMu120_vs_SingleMuon_NUM", "Trigger")->Fill(MinMETNoMuMHTNoMu, 1.);
                if(triggerMap["MET"] || triggerMap["METMHT"] || triggerMap["METMHTNoMu"]) {
                    Hist("HLT_PFMET_OR_vs_SingleMuon_NUM", "Trigger")->Fill(MinMETMHT, 1.);
                    Hist("HLT_PFMET_OR_NUM", "Trigger")->Fill(MinMETMHT, 1.);
                }
            }
            // MET Trigger with JetHT
            if(triggerMap["JET"] && FatJetsVect.size() >= 1 && FatJetsVect[0].pt() > 500. && FatJetsVect[0].IDTight()) {
                Hist("HLT_PFMET_OR_vs_JetHT_DEN", "Trigger")->Fill(MinMETMHT, 1.);
                if(triggerMap["MET"] || triggerMap["METMHT"] || triggerMap["METMHTNoMu"]) {
                    Hist("HLT_PFMET_OR_vs_JetHT_NUM", "Trigger")->Fill(MinMETMHT, 1.);
                }
            }
        }
        if(triggerMap["SingleIsoEle"] && ElecIsoVect.size() >= 1 && ElecIsoVect[0].isTightElectron()) {
            Hist("HLT_SingleEle_vs_SingleElectron_DEN", "Trigger")->Fill(ElecIsoVect[0].pt());
            if(triggerMap["SingleEle"]) Hist("HLT_SingleEle_vs_SingleElectron_NUM", "Trigger")->Fill(ElecIsoVect[0].pt());
        }
        if((triggerMap["MET"] || triggerMap["METMHT"] || triggerMap["METMHTNoMu"])/*MinMETMHT > 200.*/ && ElecIsoVect.size() >= 1 && ElecIsoVect[0].isTightElectron() && fabs(ElecIsoVect[0].tlv().DeltaPhi(MET_tlv))> 0.3 ) {
            Hist("HLT_SingleEle_vs_MET_DEN", "Trigger")->Fill(ElecIsoVect[0].pt());
            Hist("HLT_SingleIsoEle_vs_MET_DEN", "Trigger")->Fill(ElecIsoVect[0].pt());
            Hist("HLT_SingleNonIsoEle_vs_MET_DEN", "Trigger")->Fill(ElecIsoVect[0].pt());
            if(triggerMap["SingleIsoEle"] || triggerMap["SingleEle"]) Hist("HLT_SingleEle_vs_MET_NUM", "Trigger")->Fill(ElecIsoVect[0].pt());
            if(triggerMap["SingleIsoEle"]) Hist("HLT_SingleIsoEle_vs_MET_NUM", "Trigger")->Fill(ElecIsoVect[0].pt());
            if(triggerMap["SingleEle"]) Hist("HLT_SingleNonIsoEle_vs_MET_NUM", "Trigger")->Fill(ElecIsoVect[0].pt());
        }
        if(FatJetsVect.size() >= 2) {
            double Xmass( (FatJetsVect[0].tlv() + FatJetsVect[1].tlv()).M() ), Jmass(FatJetsMassVect[0]); //(std::min(FatJetsMassVect[0], FatJetsMassVect[1])); // std::max(FatJetsMassVect[0], FatJetsMassVect[1]) 
            int iH( FatJetsMassVect[0] > FatJetsMassVect[1] ? 0 : 1 ), iV( FatJetsMassVect[0] > FatJetsMassVect[1] ? 1 : 0 );
            double Jmass1(FatJetsMassVect[iH]), Jmass2(FatJetsMassVect[iV]), Tau2(FatJetsTau21Vect[iV]);
            bool isJetHT(Xmass > 900. && FatJetsVect[0].pt() > 600.); // || FatJetsVect[1].pt() > 600.)
            bool isJetMass(Jmass > m_HMassLowerCut); // && FatJetsVect[0].pt() > 320.
            bool isJetId(FatJetsVect[0].IDTight() && FatJetsVect[1].IDTight() && fabs(FatJetsVect[0].eta()-FatJetsVect[1].eta()) < 1.3);
            bool isBTag1(FatJetsBTagVect[iH] > 0), isBTag2(FatJetsBTagVect[iH] > 1);
            bool isHmass(Jmass1 > m_HMassLowerCut && Jmass1 < m_HMassUpperCut);
            bool isWmass(Jmass2 > m_VMassLowerCut && Jmass2 < m_VMassInterCut);
            bool isZmass(Jmass2 > m_VMassInterCut && Jmass2 < m_VMassUpperCut);
            bool isHP(Jmass2 < m_Tau21LowerCut);
            bool isLP(Tau2 > m_Tau21LowerCut && Tau2 < m_Tau21UpperCut);
            bool isTriggerOR(triggerMap["HT"] || triggerMap["JET"] || triggerMap["HTWJ"] || triggerMap["SUBJET"] || triggerMap["SUBHT"] || triggerMap["SUBTAG"]);
            // HT Trigger
            if(triggerMap["HT_PS"] && isJetId && isJetMass) {
                Hist("HLT_PFHT(800,900)_vs_Xmass_DEN", "Trigger")->Fill(Xmass, 1.);
                Hist("HLT_AK8PFJet450_vs_Xmass_DEN", "Trigger")->Fill(Xmass, 1.);
                Hist("HLT_PFHT650_WideJetMJJ(900,950)_vs_Xmass_DEN", "Trigger")->Fill(Xmass, 1.);
                Hist("HLT_PFHT_OR_vs_Xmass_DEN", "Trigger")->Fill(Xmass, 1.);
                if(triggerMap["HT"]) Hist("HLT_PFHT(800,900)_vs_Xmass_NUM", "Trigger")->Fill(Xmass, 1.);
                if(triggerMap["JET"]) Hist("HLT_AK8PFJet450_vs_Xmass_NUM", "Trigger")->Fill(Xmass, 1.);
                if(triggerMap["HTWJ"]) Hist("HLT_PFHT650_WideJetMJJ(900,950)_vs_Xmass_NUM", "Trigger")->Fill(Xmass, 1.);
                if(triggerMap["HT"] || triggerMap["JET"] || triggerMap["HTWJ"]) Hist("HLT_PFHT_OR_vs_Xmass_NUM", "Trigger")->Fill(Xmass, 1.);
            }
            // Substructure Trigger
            if(triggerMap["SUB_PS"] && isJetHT) {
                Hist("HLT_AK8PFJet360_TrimMass30_vs_Jmass_DEN", "Trigger")->Fill(Jmass, 1.);
                Hist("HLT_AK8PFHT700_TrimMass50_vs_Jmass_DEN", "Trigger")->Fill(Jmass, 1.);
                Hist("HLT_Subtructure_OR_vs_Jmass_DEN", "Trigger")->Fill(Jmass, 1.);
                if(triggerMap["SUBJET"]) Hist("HLT_AK8PFJet360_TrimMass30_vs_Jmass_NUM", "Trigger")->Fill(Jmass, 1.);
                if(triggerMap["SUBHT"]) Hist("HLT_AK8PFHT700_TrimMass50_vs_Jmass_NUM", "Trigger")->Fill(Jmass, 1.);
                if(triggerMap["SUBJET"] || triggerMap["SUBHT"]) Hist("HLT_Subtructure_OR_vs_Jmass_NUM", "Trigger")->Fill(Jmass, 1.);
                if(isBTag1) {
                    Hist("HLT_AK8DiPFJet(250,280)_200_TrimMass30_BTagCSV_p20_Cat1B_vs_Jmass_DEN", "Trigger")->Fill(Jmass, 1.);
                    if(triggerMap["SUBTAG"]) Hist("HLT_AK8DiPFJet(250,280)_200_TrimMass30_BTagCSV_p20_Cat1B_vs_Jmass_NUM", "Trigger")->Fill(Jmass, 1.);
                }
                if(isBTag2) {
                    Hist("HLT_AK8DiPFJet(250,280)_200_TrimMass30_BTagCSV_p20_Cat2B_vs_Jmass_DEN", "Trigger")->Fill(Jmass, 1.);
                    if(triggerMap["SUBTAG"]) Hist("HLT_AK8DiPFJet(250,280)_200_TrimMass30_BTagCSV_p20_Cat2B_vs_Jmass_NUM", "Trigger")->Fill(Jmass, 1.);
                }
            }
            // 2D
            if((triggerMap["HT_PS"] || triggerMap["SUB_PS"]) && isJetId) {
                Hist("HLT_AllHad_OR_DEN", "Trigger")->Fill(Xmass, Jmass);
                if(isTriggerOR) Hist("HLT_AllHad_OR_NUM", "Trigger")->Fill(Xmass, Jmass);
                if(isJetMass) {
                    Hist("HLT_AllHad_OR_vs_Xmass_DEN", "Trigger")->Fill(Xmass, 1.);
                    if(isTriggerOR) Hist("HLT_AllHad_OR_vs_Xmass_NUM", "Trigger")->Fill(Xmass, 1.);
                }
                if(FatJetsVect[0].pt() > 600.) {
                    Hist("HLT_AllHad_OR_vs_Jmass_DEN", "Trigger")->Fill(Jmass, 1.);
                    if(isTriggerOR) Hist("HLT_AllHad_OR_vs_Jmass_NUM", "Trigger")->Fill(Jmass, 1.);
                }
            }
            // With analysis cuts
            if((triggerMap["HT_PS"] || triggerMap["SUB_PS"]) && isJetId && isHmass && (isWmass || isZmass) && (isHP || isLP) && isBTag1) {
                Hist("HLT_AllHad_OR_Cat1B_vs_Xmass_DEN", "Trigger")->Fill(Xmass);
                if(isTriggerOR) Hist("HLT_AllHad_OR_Cat1B_vs_Xmass_NUM", "Trigger")->Fill(Xmass);
            }
            if((triggerMap["HT_PS"] || triggerMap["SUB_PS"]) && isJetId && isHmass && (isWmass || isZmass) && (isHP || isLP) && isBTag2) {
                Hist("HLT_AllHad_OR_Cat2B_vs_Xmass_DEN", "Trigger")->Fill(Xmass);
                if(isTriggerOR) Hist("HLT_AllHad_OR_Cat2B_vs_Xmass_NUM", "Trigger")->Fill(Xmass);
            }
            if((triggerMap["HT_PS"] || triggerMap["SUB_PS"]) && isJetId && isHmass && (isWmass || isZmass) && isHP && (isBTag1 || isBTag2)) {
                Hist("HLT_AllHad_OR_CatHP_vs_Xmass_DEN", "Trigger")->Fill(Xmass);
                if(isTriggerOR) Hist("HLT_AllHad_OR_CatHP_vs_Xmass_NUM", "Trigger")->Fill(Xmass);
            }
            if((triggerMap["HT_PS"] || triggerMap["SUB_PS"]) && isJetId && isHmass && (isWmass || isZmass) && isLP && (isBTag1 || isBTag2)) {
                Hist("HLT_AllHad_OR_CatLP_vs_Xmass_DEN", "Trigger")->Fill(Xmass);
                if(isTriggerOR) Hist("HLT_AllHad_OR_CatLP_vs_Xmass_NUM", "Trigger")->Fill(Xmass);
            }
            if((triggerMap["HT_PS"] || triggerMap["SUB_PS"]) && isJetId && isHmass && isWmass && (isHP || isLP) && (isBTag1 || isBTag2)) {
                Hist("HLT_AllHad_OR_CatWR_vs_Xmass_DEN", "Trigger")->Fill(Xmass);
                if(isTriggerOR) Hist("HLT_AllHad_OR_CatWR_vs_Xmass_NUM", "Trigger")->Fill(Xmass);
            }
            if((triggerMap["HT_PS"] || triggerMap["SUB_PS"]) && isJetId && isHmass && isZmass && (isHP || isLP) && (isBTag1 || isBTag2)) {
                Hist("HLT_AllHad_OR_CatZR_vs_Xmass_DEN", "Trigger")->Fill(Xmass);
                if(isTriggerOR) Hist("HLT_AllHad_OR_CatZR_vs_Xmass_NUM", "Trigger")->Fill(Xmass);
            }
        }
    }
    
    Hist("Events")->Fill(0., GenWeight);
    Hist("Events", "nnqq")->Fill(0., EventWeight);
    Hist("Events", "enqq")->Fill(0., EventWeight);
    Hist("Events", "mnqq")->Fill(0., EventWeight);
    Hist("Events", "emqq")->Fill(0., EventWeight);
    Hist("Events", "eeqq")->Fill(0., EventWeight);
    Hist("Events", "mmqq")->Fill(0., EventWeight);
    Hist("Events", "qqqq")->Fill(0., EventWeight);
    
    // Filter by Trigger
//    if(!isMC) {
        if(!triggerMap["SingleMu"] && !triggerMap["SingleEle"] && !triggerMap["SingleIsoEle"] && !(MET.et() > m_MEtPtCut)/*!triggerMap["MET"] && !triggerMap["METMHT"] && !triggerMap["METMHTNoMu"]*/ && !triggerMap["HT"] && !triggerMap["HTWJ"] && !triggerMap["SUBJET"] && !triggerMap["SUBHT"] && !triggerMap["SUBTAG"]) {m_logger << INFO << " - No trigger"  << SLogger::endmsg; throw SError( SError::SkipEvent ); }
//    }
    
    
    Hist("Events", "nnqq")->Fill(1., EventWeight);
    Hist("Events", "enqq")->Fill(1., EventWeight);
    Hist("Events", "mnqq")->Fill(1., EventWeight);
    Hist("Events", "emqq")->Fill(1., EventWeight);
    Hist("Events", "eeqq")->Fill(1., EventWeight);
    Hist("Events", "mmqq")->Fill(1., EventWeight);
    Hist("Events", "qqqq")->Fill(1., EventWeight);
    
    
    
    // -----------------------------------
    //           VECTOR BOSON
    // -----------------------------------
    m_logger << INFO << " + Vector boson reconstruction" << SLogger::endmsg;
    
    int e1(-1), e2(-1);
    int m1(-1), m2(-1), mHPT(-1), mTHPT(-1);
    TLorentzVector Neutrino;
    // Categorization depending on the number of leptons
    
    // ---------- Z TO LEPTONS ----------
    // Cascade: Zmm -> Zee -> Wmn -> Wen -> Znn -> Zqq
    // --- Z -> mumu ---
    if( MuonVect.size()>=2 || (MuonVect.size()>=2 && ElecVect.size()>=2 && MuonVect.at(0).pt() > ElecVect.at(0).pt()) ) {
        m_logger << INFO << " + Try to reconstruct Z -> mm"  << SLogger::endmsg;
        Hist("Events", "mmqq")->Fill(2., EventWeight);
        // Indentify leptons
        float maxZpt(-1.), Zpt(-1.), Zmass(-1.), dRll(-1.), pTll(-1.);
        for(unsigned int i = 0; i < MuonVect.size(); i++) {
            for(unsigned int j = 1; j < MuonVect.size(); j++) {
                if(i==j || MuonVect[i].charge() == MuonVect[j].charge()) continue;
                Zpt = (MuonVect[i].tlv() + MuonVect[j].tlv()).Pt();
                Zmass = (MuonVect[i].tlv() + MuonVect[j].tlv()).M();
                if(Zmass > 70. && Zmass < 110. && Zpt > maxZpt) {m1 = i; m2 = j; maxZpt = Zpt;}
            }
        }
        // Check suitable muons
        if(m1 < 0 || m2 < 0) {m_logger << INFO << " - No OS muons"  << SLogger::endmsg;}
        else {
            Hist("Events", "mmqq")->Fill(3., EventWeight);
            if( !(MuonVect[m1].pt() > m_Muon1PtCut && MuonVect[m2].pt() > m_Muon2PtCut) ) {m_logger << INFO << " - No muons above threshold" << SLogger::endmsg;}
            else {
                Hist("Events", "mmqq")->Fill(4., EventWeight);
                //fillMuonPlots(MuonVect[m1], MuonVect[m2], LepP, LepM);
                bool isMatched( isMC && LepP.Pt()>0. && LepM.Pt()>0. && (MuonVect[m1].tlv().DeltaR(LepP) < 0.05 || MuonVect[m1].tlv().DeltaR(LepM) < 0.05) && (MuonVect[m2].tlv().DeltaR(LepP) < 0.05 || MuonVect[m2].tlv().DeltaR(LepM) < 0.05));
                if(isMatched) {
                    dRll = LepP.DeltaR(LepM);
                    pTll = (LepP+LepM).Pt();
                    Hist("dR", "Muons")->Fill(dRll); Hist("pT", "Muons")->Fill(pTll); Hist("pT1", "Muons")->Fill(MuonVect[m1].pt()); Hist("pT2", "Muons")->Fill(MuonVect[m2].pt());
                    if(MuonVect[m1].isHighPtMuon()==1 && MuonVect[m2].isHighPtMuon()==1) {Hist("dR_HighptHighptId", "Muons")->Fill(dRll); Hist("pT_HighptHighptId", "Muons")->Fill(pTll);}
                    if(MuonVect[m1].isLooseMuon()==1 && MuonVect[m2].isLooseMuon()==1) {Hist("dR_LooseLooseId", "Muons")->Fill(dRll); Hist("pT_LooseLooseId", "Muons")->Fill(pTll);}
                    if(MuonVect[m1].isMediumMuon()==1 && MuonVect[m2].isMediumMuon()==1) {Hist("dR_MediumMediumId", "Muons")->Fill(dRll); Hist("pT_MediumMediumId", "Muons")->Fill(pTll);}
                    if(MuonVect[m1].isTightMuon()==1 && MuonVect[m2].isTightMuon()==1) {Hist("dR_TightTightId", "Muons")->Fill(dRll); Hist("pT_TightTightId", "Muons")->Fill(pTll);}
                    if(MuonVect[m1].isHighPtMuon()==1) Hist("pT1_HighptId", "Muons")->Fill(MuonVect[m1].pt());
                    if(MuonVect[m2].isHighPtMuon()==1) Hist("pT2_HighptId", "Muons")->Fill(MuonVect[m2].pt());
                    if(MuonVect[m1].isTrackerHighPtMuon()==1) Hist("pT1_TrackerId", "Muons")->Fill(MuonVect[m1].pt());
                    if(MuonVect[m2].isTrackerHighPtMuon()==1) Hist("pT2_TrackerId", "Muons")->Fill(MuonVect[m2].pt());
                }
                // Apply muon Id
                if( !( (MuonVect[m1].isHighPtMuon()==1 && MuonVect[m2].isTrackerHighPtMuon()) || (MuonVect[m2].isHighPtMuon()==1 && MuonVect[m1].isTrackerHighPtMuon()) ) ) {m_logger << INFO << " - No double muon Id" << SLogger::endmsg;}
                else {
                    if(MuonVect[m1].isHighPtMuon()) {mHPT = m1; mTHPT = m2;}
                    else {mHPT = m2; mTHPT = m1;}
                    Hist("Events", "mmqq")->Fill(5., EventWeight);
                    if(isMatched) {Hist("dR_HighptTrackerId", "Muons")->Fill(dRll); Hist("pT_HighptTrackerId", "Muons")->Fill(pTll);}
                    if(isMatched && MuonVect[m1].pfDeltaCorrRelIso() < 0.20 && MuonVect[m2].pfDeltaCorrRelIso() < 0.20) {Hist("dR_HighptTrackerIdPFIso", "Muons")->Fill(dRll); Hist("pT_HighptTrackerIdPFIso", "Muons")->Fill(pTll);}
                    // Correct muon tracker iso UZH::Muon::trackCorrIso()
                    float trackIso1( MuonVect[m1].trackIso() ), trackIso2( MuonVect[m2].trackIso() );
                    if(MuonVect[m1].tlv().DeltaR(MuonVect[m2].tlv()) < 0.3) {
                        trackIso1 -= MuonVect[m2].innerTrack_pt();
                        trackIso2 -= MuonVect[m1].innerTrack_pt();
                    }
                    trackIso1 /= MuonVect[m1].pt();
                    trackIso2 /= MuonVect[m2].pt();
                    if(trackIso1 < 0. || std::isinf(trackIso1) || trackIso1 != trackIso1) trackIso1 = 0.;
                    if(trackIso2 < 0. || std::isinf(trackIso2) || trackIso2 != trackIso2) trackIso2 = 0.;
                    if(maxZpt > m_VPtCut) {
                        Hist("Muon1_trkIso", "mmqq")->Fill(trackIso1, EventWeight);
                        Hist("Muon2_trkIso", "mmqq")->Fill(trackIso2, EventWeight);
                    }
                    if(isMatched && MuonVect[m1].trackIso()/MuonVect[m1].pt() < 0.10 && MuonVect[m2].trackIso()/MuonVect[m2].pt() < 0.10) {Hist("dR_HighptTrackerIdTrackerNonCorrIso", "Muons")->Fill(dRll); Hist("pT_HighptTrackerIdTrackerNonCorrIso", "Muons")->Fill(pTll);}
                    // Apply muon iso
                    if( !(trackIso1 < 0.10 && trackIso2 < 0.10) ) {m_logger << INFO << " - No double muon Iso" << SLogger::endmsg;}
                    else {
                        Hist("Events", "mmqq")->Fill(6., EventWeight);
                        Hist("Z_mass", "mm")->Fill(Zmass, EventWeight);
                        Hist("Z_pt", "mm")->Fill(maxZpt, EventWeight);
                        Hist("Muon1_pt", "mm")->Fill(MuonVect[m1].pt(), EventWeight);
                        Hist("Muon2_pt", "mm")->Fill(MuonVect[m2].pt(), EventWeight);
                        if(isMatched) {Hist("dR_HighptTrackerIdTrackerIso", "Muons")->Fill(dRll); Hist("pT_HighptTrackerIdTrackerIso", "Muons")->Fill(pTll);}
                        // Build candidate
                        V = MuonVect[m1].tlv() + MuonVect[m2].tlv();
                        if(maxZpt < m_VPtCut) {m_logger << INFO << " - No V boost" << SLogger::endmsg;}
                        else {
                            // Check trigger consistency
                            if(!triggerMap["SingleMu"] && !triggerMap["MET"] && !triggerMap["METMHT"] && !triggerMap["METMHTNoMu"]) { m_logger << INFO << " - Trigger inconsistency" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
                            if(!isMC && ((sample.find("MET")!=std::string::npos && triggerMap["SingleMu"]) || (sample.find("Muon")!=std::string::npos && !triggerMap["SingleMu"]))) { m_logger << INFO << " - Trigger double counting" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
                            // SF
                            if(isMC) {
//                                float TrigMETWeight = m_ScaleFactorTool.GetTrigMET(MaxMETNoMuMHTNoMu);
//                                float TrigMuon1Weight = m_ScaleFactorTool.GetTrigSingleMuon(MuonVect[0].pt(), MuonVect[0].eta());
//                                float TrigMuon2Weight = m_ScaleFactorTool.GetTrigSingleMuon(MuonVect[1].pt(), MuonVect[1].eta());
//                                float TrigMuonWeight = TrigMuon1Weight + TrigMuon2Weight - TrigMuon1Weight*TrigMuon2Weight;
//                                TriggerWeight *= TrigMuonWeight + TrigMETWeight - TrigMuonWeight*TrigMETWeight;
                                TriggerWeight *= m_ScaleFactorTool.GetTrigMuonMET(MuonVect[m1].pt(), MuonVect[m1].eta(), MuonVect[m2].pt(), MuonVect[m2].eta(), MaxMETNoMuMHTNoMu);
                                LeptonWeight *= m_ScaleFactorTool.GetMuonHighptId(MuonVect[mHPT].pt(), MuonVect[mHPT].eta());
                                LeptonWeight *= m_ScaleFactorTool.GetMuonTrkId(MuonVect[mTHPT].pt(), MuonVect[mTHPT].eta());
                                LeptonWeight *= m_ScaleFactorTool.GetMuonLooseTrkIso(MuonVect[m1].pt(), MuonVect[m1].eta());
                                LeptonWeight *= m_ScaleFactorTool.GetMuonLooseTrkIso(MuonVect[m2].pt(), MuonVect[m2].eta());
                                LeptonWeight *= pow(m_ScaleFactorTool.GetMuonTrk(nPV), 2);
                                EventWeight *= TriggerWeight * LeptonWeight;
                                //
//                                float TrigMuon1WeightUp = m_ScaleFactorTool.GetTrigSingleMuon(MuonVect[0].pt(), MuonVect[0].eta(), +1);
//                                float TrigMuon2WeightUp = m_ScaleFactorTool.GetTrigSingleMuon(MuonVect[1].pt(), MuonVect[1].eta(), +1);
//                                float TrigMuonWeightUp = TrigMuon1WeightUp + TrigMuon2WeightUp - TrigMuon1WeightUp*TrigMuon2WeightUp;
//                                TriggerWeightUp *= TrigMuonWeightUp + TrigMETWeight - TrigMuonWeightUp*TrigMETWeight;
                                TriggerWeightUp *= m_ScaleFactorTool.GetTrigMuonMET(MuonVect[m1].pt(), MuonVect[m1].eta(), MuonVect[m2].pt(), MuonVect[m2].eta(), MaxMETNoMuMHTNoMu, +1);
                                LeptonWeightUp *= m_ScaleFactorTool.GetMuonHighptId(MuonVect[mHPT].pt(), MuonVect[mHPT].eta(), +1);
                                LeptonWeightUp *= m_ScaleFactorTool.GetMuonTrkId(MuonVect[mTHPT].pt(), MuonVect[mTHPT].eta(), +1);
                                LeptonWeightUp *= m_ScaleFactorTool.GetMuonLooseTrkIso(MuonVect[m1].pt(), MuonVect[m1].eta(), +1);
                                LeptonWeightUp *= m_ScaleFactorTool.GetMuonLooseTrkIso(MuonVect[m2].pt(), MuonVect[m2].eta(), +1);
                                LeptonWeightUp *= pow(m_ScaleFactorTool.GetMuonTrk(nPV, +1), 2);
//                                float TrigMuon1WeightDown = m_ScaleFactorTool.GetTrigSingleMuon(MuonVect[0].pt(), MuonVect[0].eta(), -1);
//                                float TrigMuon2WeightDown = m_ScaleFactorTool.GetTrigSingleMuon(MuonVect[1].pt(), MuonVect[1].eta(), -1);
//                                float TrigMuonWeightDown = TrigMuon1WeightDown + TrigMuon2WeightDown - TrigMuon1WeightDown*TrigMuon2WeightDown;
//                                TriggerWeightDown *= TrigMuonWeightDown + TrigMETWeight - TrigMuonWeightDown*TrigMETWeight;
                                TriggerWeightDown *= m_ScaleFactorTool.GetTrigMuonMET(MuonVect[m1].pt(), MuonVect[m1].eta(), MuonVect[m2].pt(), MuonVect[m2].eta(), MaxMETNoMuMHTNoMu, -1);
                                LeptonWeightDown *= m_ScaleFactorTool.GetMuonHighptId(MuonVect[mHPT].pt(), MuonVect[mHPT].eta(), -1);
                                LeptonWeightDown *= m_ScaleFactorTool.GetMuonTrkId(MuonVect[mTHPT].pt(), MuonVect[mTHPT].eta(), -1);
                                LeptonWeightDown *= m_ScaleFactorTool.GetMuonLooseTrkIso(MuonVect[m1].pt(), MuonVect[m1].eta(), -1);
                                LeptonWeightDown *= m_ScaleFactorTool.GetMuonLooseTrkIso(MuonVect[m2].pt(), MuonVect[m2].eta(), -1);
                                LeptonWeightDown *= pow(m_ScaleFactorTool.GetMuonTrk(nPV, -1), 2);
                            }
                            isZtoMM = true;
                            Hist("Events", "mmqq")->Fill(7., EventWeight);
                            m_logger << INFO << " + Z -> mm candidate reconstructed" << SLogger::endmsg;
                        }
                    }
                }
            }
        }
    }
    // --- Z -> ee ---
    if(!isZtoMM && ElecVect.size()>=2) {
        m_logger << INFO << " + Try to reconstruct Z -> ee"  << SLogger::endmsg;
        Hist("Events", "eeqq")->Fill(2., EventWeight);
        // Indentify leptons
        float maxZpt(-1.), Zpt(-1.), Zmass(-1.), dRll(-1.), pTll(-1.);
        for(unsigned int i = 0; i < ElecVect.size(); i++) {
            for(unsigned int j = 1; j < ElecVect.size(); j++) {
                if(i==j || ElecVect[i].charge() == ElecVect[j].charge()) continue;
                Zpt = (CalibratedElecVect[i] + CalibratedElecVect[j]).Pt();
                Zmass = (CalibratedElecVect[i] + CalibratedElecVect[j]).M();
                if(Zmass > 70. && Zmass < 110. && Zpt > maxZpt) {e1 = i; e2 = j; maxZpt = Zpt;}
            }
        }
        // Check suitable electrons
        if(e1 < 0 || e2 < 0) {m_logger << INFO << " - No OS electrons" << SLogger::endmsg;}
        else {
            Hist("Events", "eeqq")->Fill(3., EventWeight);
            if( !(CalibratedElecVect[e1].Pt() > m_Elec1PtCut && CalibratedElecVect[e2].Pt() > m_Elec2PtCut) ) {m_logger << INFO << " - No electrons above threshold" << SLogger::endmsg;}
            else {
                Hist("Events", "eeqq")->Fill(4., EventWeight);
                //fillElectronPlots(&ElecVect[m1], &ElecVect[m2], LepP, LepM);
                bool isMatched( isMC && LepP.Pt()>0. && LepM.Pt()>0. && (ElecVect[e1].tlv().DeltaR(LepP) < 0.05 || ElecVect[e1].tlv().DeltaR(LepM) < 0.05) && (ElecVect[e2].tlv().DeltaR(LepP) < 0.05 || ElecVect[e2].tlv().DeltaR(LepM) < 0.05));
                if(isMatched) {
                    dRll = LepP.DeltaR(LepM);
                    pTll = (LepP+LepM).Pt();
                    Hist("dR", "Electrons")->Fill(dRll); Hist("pT", "Electrons")->Fill(pTll); Hist("pT1", "Electrons")->Fill(CalibratedElecVect[e1].Pt()); Hist("pT2", "Electrons")->Fill(CalibratedElecVect[e2].Pt());
                    if(ElecVect[e1].isVetoElectron() && ElecVect[e2].isVetoElectron()) {Hist("dR_VetoVetoId", "Electrons")->Fill(dRll); Hist("pT_VetoVetoId", "Electrons")->Fill(pTll);}
                    if(ElecVect[e1].isLooseElectron() && ElecVect[e2].isLooseElectron()) {Hist("dR_LooseLooseId", "Electrons")->Fill(dRll); Hist("pT_LooseLooseId", "Electrons")->Fill(pTll);}
                    if(ElecVect[e1].isMediumElectron() && ElecVect[e2].isMediumElectron()) {Hist("dR_MediumMediumId", "Electrons")->Fill(dRll); Hist("pT_MediumMediumId", "Electrons")->Fill(pTll);}
                    if(ElecVect[e1].isTightElectron() && ElecVect[e2].isTightElectron()) {Hist("dR_TightTightId", "Electrons")->Fill(dRll); Hist("pT_TightTightId", "Electrons")->Fill(pTll);}
                    if(ElecVect[e1].isHeepElectron()==1 && ElecVect[e2].isHeepElectron()==1) {Hist("dR_HeepHeepId", "Electrons")->Fill(dRll); Hist("pT_HeepHeepId", "Electrons")->Fill(pTll);}
                    if(ElecVect[e1].isLooseElectron()) Hist("pT1_LooseId", "Electrons")->Fill(CalibratedElecVect[e1].Pt());
                    if(ElecVect[e2].isLooseElectron()) Hist("pT2_LooseId", "Electrons")->Fill(CalibratedElecVect[e2].Pt());
                }
                if(maxZpt > m_VPtCut) {
                    Hist("Electron1_pfIso", "eeqq")->Fill(ElecVect[e1].pfRhoCorrRelIso03(), EventWeight);
                    Hist("Electron2_pfIso", "eeqq")->Fill(ElecVect[e2].pfRhoCorrRelIso03(), EventWeight);
                }
                // Apply electron Id
                if( !(ElecVect[e1].isLooseElectron() && ElecVect[e2].isLooseElectron()) ) {m_logger << INFO << " - No double electron Id/Iso" << SLogger::endmsg;}
                else {
                    Hist("Events", "eeqq")->Fill(5., EventWeight);
                    Hist("Z_mass", "ee")->Fill(Zmass, EventWeight);
                    Hist("Z_pt", "ee")->Fill(maxZpt, EventWeight);
                    Hist("Electron1_pt", "ee")->Fill(CalibratedElecVect[e1].Pt(), EventWeight);
                    Hist("Electron2_pt", "ee")->Fill(CalibratedElecVect[e2].Pt(), EventWeight);
                    // Build candidate
                    V = CalibratedElecVect[e1] + CalibratedElecVect[e2];
                    if(maxZpt < m_VPtCut) {m_logger << INFO << " - No V boost" << SLogger::endmsg;}
                    else {
                        // Check trigger consistency
                        Hist("HLT_DoubleEleMETInclusive_COUNT", "Trigger")->Fill(0., EventWeight);
                        if(!triggerMap["SingleEle"] && !triggerMap["SingleIsoEle"] && !triggerMap["MET"] && !triggerMap["METMHT"] && !triggerMap["METMHTNoMu"]) {
                            if(triggerMap["MET"] || triggerMap["METMHT"] || triggerMap["METMHTNoMu"]) {
                                Hist("HLT_DoubleEleMETInclusive_COUNT", "Trigger")->Fill(1., EventWeight);
                            }
                            m_logger << INFO << " - Trigger inconsistency" << SLogger::endmsg; throw SError( SError::SkipEvent );
                        }
                        if(!isMC && ((sample.find("MET")!=std::string::npos && (triggerMap["SingleEle"] || triggerMap["SingleIsoEle"])) || (sample.find("Electron")!=std::string::npos && !(triggerMap["SingleEle"] || triggerMap["SingleIsoEle"])))) { m_logger << INFO << " - Trigger double counting" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
                        // SF
                        if(isMC) {
//                            float TrigEle1Weight = m_ScaleFactorTool.GetTrigSingleEle(ElecVect[e1].pt(), ElecVect[e1].eta());
//                            float TrigEle2Weight = m_ScaleFactorTool.GetTrigSingleEle(ElecVect[e2].pt(), ElecVect[e2].eta());
//                            TriggerWeight *= TrigEle1Weight + TrigEle2Weight - TrigEle1Weight*TrigEle2Weight;
                            TriggerWeight *= m_ScaleFactorTool.GetTrigEleMET(ElecVect[e1].pt(), ElecVect[e1].eta(), ElecVect[e2].pt(), ElecVect[e2].eta(), MaxMETNoMuMHTNoMu);
                            LeptonWeight *= m_ScaleFactorTool.GetEleIdLooseWP(ElecVect[e1].pt(), ElecVect[e1].eta());
                            LeptonWeight *= m_ScaleFactorTool.GetEleIdLooseWP(ElecVect[e2].pt(), ElecVect[e2].eta());
                            LeptonWeight *= m_ScaleFactorTool.GetEleReco(ElecVect[e1].pt(), ElecVect[e1].eta());
                            LeptonWeight *= m_ScaleFactorTool.GetEleReco(ElecVect[e2].pt(), ElecVect[e2].eta());
                            EventWeight *= TriggerWeight * LeptonWeight;
                            //
//                            float TrigEle1WeightUp = m_ScaleFactorTool.GetTrigSingleEle(ElecVect[e1].pt(), ElecVect[e1].eta(), +1);
//                            float TrigEle2WeightUp = m_ScaleFactorTool.GetTrigSingleEle(ElecVect[e2].pt(), ElecVect[e2].eta(), +1);
//                            TriggerWeight *= TrigEle1WeightUp + TrigEle2WeightUp - TrigEle1WeightUp*TrigEle2WeightUp;
                            TriggerWeightUp *= m_ScaleFactorTool.GetTrigEleMET(ElecVect[e1].pt(), ElecVect[e1].eta(), ElecVect[e2].pt(), ElecVect[e2].eta(), MaxMETNoMuMHTNoMu, +1);
                            LeptonWeightUp *= m_ScaleFactorTool.GetEleIdLooseWP(ElecVect[e1].pt(), ElecVect[e1].eta(), +1);
                            LeptonWeightUp *= m_ScaleFactorTool.GetEleIdLooseWP(ElecVect[e2].pt(), ElecVect[e2].eta(), +1);
                            LeptonWeightUp *= m_ScaleFactorTool.GetEleReco(ElecVect[e1].pt(), ElecVect[e1].eta(), +1);
                            LeptonWeightUp *= m_ScaleFactorTool.GetEleReco(ElecVect[e2].pt(), ElecVect[e2].eta(), +1);
//                            float TrigEle1WeightDown = m_ScaleFactorTool.GetTrigSingleEle(ElecVect[e1].pt(), ElecVect[e1].eta(), -1);
//                            float TrigEle2WeightDown = m_ScaleFactorTool.GetTrigSingleEle(ElecVect[e2].pt(), ElecVect[e2].eta(), -1);
//                            TriggerWeightDown *= TrigEle1WeightDown + TrigEle2WeightDown - TrigEle1WeightDown*TrigEle2WeightDown;
                            TriggerWeightDown *= m_ScaleFactorTool.GetTrigEleMET(ElecVect[e1].pt(), ElecVect[e1].eta(), ElecVect[e2].pt(), ElecVect[e2].eta(), MaxMETNoMuMHTNoMu, -1);
                            LeptonWeightDown *= m_ScaleFactorTool.GetEleIdLooseWP(ElecVect[e1].pt(), ElecVect[e1].eta(), -1);
                            LeptonWeightDown *= m_ScaleFactorTool.GetEleIdLooseWP(ElecVect[e2].pt(), ElecVect[e2].eta(), -1);
                            LeptonWeightDown *= m_ScaleFactorTool.GetEleReco(ElecVect[e1].pt(), ElecVect[e1].eta(), -1);
                            LeptonWeightDown *= m_ScaleFactorTool.GetEleReco(ElecVect[e2].pt(), ElecVect[e2].eta(), -1);
                        }
                        isZtoEE = true;
                        Hist("Events", "eeqq")->Fill(6., EventWeight);
                        m_logger << INFO << " + Z -> ee candidate reconstructed" << SLogger::endmsg;
                    }
                }
            }
        }
    }
    // ---------- INTERMEZZO: dileptonic Top CR ----------
    if(!isZtoMM && !isZtoEE && MuonVect.size()==1 && ElecVect.size()==1 && ElecVect[0].charge() != MuonVect[0].charge()) {
        m_logger << INFO << " + Try to reconstruct T -> em" << SLogger::endmsg;
        Hist("Events", "emqq")->Fill(2., EventWeight);
        if( !(MuonVect[0].pt() > 30. && MuonVect[0].isTrackerHighPtMuon()==1 && MuonVect[0].isPFMuon() && MuonVect[0].trackIso()/MuonVect[0].pt()<0.10) ) {m_logger << INFO << " - No muon above threshold" << SLogger::endmsg;}
        else {
            Hist("Events", "emqq")->Fill(3., EventWeight);
            if( !(ElecVect[0].pt() > 30. && ElecVect[0].isTightElectron()) ) {m_logger << INFO << " - No electron above threshold" << SLogger::endmsg;}
            else {
                Hist("Events", "emqq")->Fill(4., EventWeight);
                V = MuonVect[0].tlv() + CalibratedElecVect[0];
                if(false/*V.Pt() < m_VPtCut*/) {m_logger << INFO << " - No V boost" << SLogger::endmsg;}
                else {
                    // Check trigger consistency
                    if(!triggerMap["SingleEle"] && !triggerMap["SingleIsoEle"]) { m_logger << INFO << " - Trigger inconsistency" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
                    if(isMC) {
                        //TriggerWeight *= m_ScaleFactorTool.GetTrigMuonMET(MuonVect[0].pt(), MuonVect[0].eta(), MaxMETNoMuMHTNoMu);
                        LeptonWeight *= m_ScaleFactorTool.GetMuonHighptId(MuonVect[0].pt(), fabs(MuonVect[0].eta()));
                        LeptonWeight *= m_ScaleFactorTool.GetMuonTightTrkIso(MuonVect[0].pt(), fabs(MuonVect[0].eta()));
                        LeptonWeight *= m_ScaleFactorTool.GetMuonTrk(nPV);
                        //TriggerWeightUp *= m_ScaleFactorTool.GetTrigMuonMET(MuonVect[0].pt(), MuonVect[0].eta(), MaxMETNoMuMHTNoMu, +1);
                        LeptonWeightUp *= m_ScaleFactorTool.GetMuonHighptId(MuonVect[0].pt(), fabs(MuonVect[0].eta()), +1);
                        LeptonWeightUp *= m_ScaleFactorTool.GetMuonTightTrkIso(MuonVect[0].pt(), fabs(MuonVect[0].eta()), +1);
                        LeptonWeightUp *= m_ScaleFactorTool.GetMuonTrk(nPV, +1);
                        //TriggerWeightDown *= m_ScaleFactorTool.GetTrigMuonMET(MuonVect[0].pt(), MuonVect[0].eta(), MaxMETNoMuMHTNoMu, -1);
                        LeptonWeightDown *= m_ScaleFactorTool.GetMuonHighptId(MuonVect[0].pt(), fabs(MuonVect[0].eta()), -1);
                        LeptonWeightDown *= m_ScaleFactorTool.GetMuonTightTrkIso(MuonVect[0].pt(), fabs(MuonVect[0].eta()), -1);
                        LeptonWeightDown *= m_ScaleFactorTool.GetMuonTrk(nPV, -1);
                        //
                        TriggerWeight *= m_ScaleFactorTool.GetTrigEle(ElecVect[0].pt(), ElecVect[0].eta());
                        LeptonWeight *= m_ScaleFactorTool.GetEleIdLooseWP(ElecVect[0].pt(), ElecVect[0].eta());
                        LeptonWeight *= m_ScaleFactorTool.GetEleReco(ElecVect[0].pt(), ElecVect[0].eta());
                        TriggerWeightUp *= m_ScaleFactorTool.GetTrigSingleEle(ElecVect[0].pt(), ElecVect[0].eta(), +1);
                        LeptonWeightUp *= m_ScaleFactorTool.GetEleIdLooseWP(ElecVect[0].pt(), ElecVect[0].eta(), +1);
                        LeptonWeightUp *= m_ScaleFactorTool.GetEleReco(ElecVect[0].pt(), ElecVect[0].eta(), +1);
                        TriggerWeightDown *= m_ScaleFactorTool.GetTrigSingleEle(ElecVect[0].pt(), ElecVect[0].eta(), -1);
                        LeptonWeightDown *= m_ScaleFactorTool.GetEleIdLooseWP(ElecVect[0].pt(), ElecVect[0].eta(), -1);
                        LeptonWeightDown *= m_ScaleFactorTool.GetEleReco(ElecVect[0].pt(), ElecVect[0].eta(), -1);
                        //
                        EventWeight *= TriggerWeight * LeptonWeight;
                    }
                    Hist("Events", "emqq")->Fill(5., EventWeight);
                    Hist("Electron_pfIso", "emqq")->Fill(ElecVect[0].pfRhoCorrRelIso03(), EventWeight);
                    Hist("Muon_trkIso", "emqq")->Fill(MuonVect[0].trackIso()/MuonVect[0].pt(), EventWeight);
                    isTtoEM = true;
                    m_logger << INFO << " + TT -> mnen candidate reconstructed" << SLogger::endmsg;
                }
            }
        }           
    }
    // ---------- W TO LEPTON and NEUTRINO ----------
    // --- W -> munu ---
    if(!isZtoMM && !isZtoEE && !isTtoEM && MuonVect.size()>=1) {
        m_logger << INFO << " + Try to reconstruct W -> mn" << SLogger::endmsg;
        Hist("Events", "mnqq")->Fill(2., EventWeight);
        if( !(MuonVect[0].pt() > m_Muon1PtCut) ) {m_logger << INFO << " - No muon above threshold" << SLogger::endmsg;}
        else {
            Hist("Events", "mnqq")->Fill(3., EventWeight);
            // Apply muon Id
            if( !(MuonVect[0].isHighPtMuon()==1 && MuonVect[0].isPFMuon()) ) {m_logger << INFO << " - No single muon Id" << SLogger::endmsg;}
            else {
                Hist("Events", "mnqq")->Fill(4., EventWeight);
                // Apply muon Iso
                float trackIso = MuonVect[0].trackIso()/MuonVect[0].pt();
                if(MuonVect[0].pt() + MET.et() > m_VPtCut) Hist("Muon_trkIso", "mnqq")->Fill(trackIso, EventWeight);
                //
                if(trackIso < 0.05) Hist("MuonTrkIso_eff", "Sys")->Fill(0., EventWeight);
                if(trackIso < 0.02) Hist("MuonTrkIso_eff", "Sys")->Fill(1., EventWeight);
                //
                if( !(trackIso < 0.02) ) {m_logger << INFO << " - No single muon Iso" << SLogger::endmsg;}
                else {
                    Hist("Events", "mnqq")->Fill(5., EventWeight);
                    // W kinematic reconstruction
                    m_logger << INFO << " + Try to recover neutrino pz" << SLogger::endmsg;
                    float pz = m_VariableTool.RecoverNeutrinoPz(MuonVect[0].tlv(), MET_tlv);
                    Neutrino.SetPxPyPzE(MET_tlv.Px(), MET_tlv.Py(), pz, sqrt(MET_tlv.Px()*MET_tlv.Px() + MET_tlv.Py()*MET_tlv.Py() + pz*pz) );
                    V = MuonVect[0].tlv() + Neutrino;
                    V_tmass = sqrt(2.*MET.et()*MuonVect[0].pt()*(1.-cos(MuonVect[0].tlv().DeltaPhi(MET_tlv))));
                    Hist("W_mass", "mn")->Fill(V.M(), EventWeight);
                    Hist("W_tmass", "mn")->Fill(V_tmass, EventWeight);
                    Hist("W_pt", "mn")->Fill(V.Pt(), EventWeight);
                    Hist("Muon_pt", "mn")->Fill(MuonVect[0].pt(), EventWeight);
                    if(V.Pt() < m_VPtCut) {m_logger << INFO << " - No V boost" << SLogger::endmsg;}
                    else {
                        // Check trigger consistency
                        if(!triggerMap["SingleMu"] && !triggerMap["MET"] && !triggerMap["METMHT"] && !triggerMap["METMHTNoMu"]) { m_logger << INFO << " - Trigger inconsistency" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
                        if(!isMC && ((sample.find("MET")!=std::string::npos && triggerMap["SingleMu"]) || (sample.find("Muon")!=std::string::npos && !triggerMap["SingleMu"]))) { m_logger << INFO << " - Trigger double counting" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
                        // SF
                        if(isMC) {
//                            float TrigMETWeight = m_ScaleFactorTool.GetTrigMET(MaxMETNoMuMHTNoMu);
//                            float TrigMuonWeight = m_ScaleFactorTool.GetTrigSingleMuon(MuonVect[0].pt(), MuonVect[0].eta());
//                            TriggerWeight *= TrigMuonWeight + TrigMETWeight - TrigMuonWeight*TrigMETWeight;
                            TriggerWeight *= m_ScaleFactorTool.GetTrigMuonMET(MuonVect[0].pt(), MuonVect[0].eta(), MaxMETNoMuMHTNoMu);
                            LeptonWeight *= m_ScaleFactorTool.GetMuonHighptId(MuonVect[0].pt(), fabs(MuonVect[0].eta()));
                            LeptonWeight *= m_ScaleFactorTool.GetMuonTightTrkIso(MuonVect[0].pt(), fabs(MuonVect[0].eta()));
                            LeptonWeight *= m_ScaleFactorTool.GetMuonTrk(nPV);
                            EventWeight *= TriggerWeight * LeptonWeight;
                            //
//                            float TrigMuonWeightUp = m_ScaleFactorTool.GetTrigSingleMuon(MuonVect[0].pt(), MuonVect[0].eta(), +1);
//                            TriggerWeightUp *= TrigMuonWeightUp + TrigMETWeight - TrigMuonWeightUp*TrigMETWeight;
                            TriggerWeightUp *= m_ScaleFactorTool.GetTrigMuonMET(MuonVect[0].pt(), MuonVect[0].eta(), MaxMETNoMuMHTNoMu, +1);
                            LeptonWeightUp *= m_ScaleFactorTool.GetMuonHighptId(MuonVect[0].pt(), fabs(MuonVect[0].eta()), +1);
                            LeptonWeightUp *= m_ScaleFactorTool.GetMuonTightTrkIso(MuonVect[0].pt(), fabs(MuonVect[0].eta()), +1);
                            LeptonWeightUp *= m_ScaleFactorTool.GetMuonTrk(nPV, +1);
//                            float TrigMuonWeightDown = m_ScaleFactorTool.GetTrigSingleMuon(MuonVect[0].pt(), MuonVect[0].eta(), -1);
//                            TriggerWeightDown *= TrigMuonWeightDown + TrigMETWeight - TrigMuonWeightDown*TrigMETWeight;
                            TriggerWeightDown *= m_ScaleFactorTool.GetTrigMuonMET(MuonVect[0].pt(), MuonVect[0].eta(), MaxMETNoMuMHTNoMu, -1);
                            LeptonWeightDown *= m_ScaleFactorTool.GetMuonHighptId(MuonVect[0].pt(), fabs(MuonVect[0].eta()), -1);
                            LeptonWeightDown *= m_ScaleFactorTool.GetMuonTightTrkIso(MuonVect[0].pt(), fabs(MuonVect[0].eta()), -1);
                            LeptonWeightDown *= m_ScaleFactorTool.GetMuonTrk(nPV, -1);
                        }
                        isWtoMN = true;
                        Hist("Events", "mnqq")->Fill(6., EventWeight);
                        m_logger << INFO << " + W -> mn candidate reconstructed" << SLogger::endmsg;
                    }
                }
            }
        }
    }
    // --- W -> enu ---
    if(!isZtoMM && !isZtoEE && !isWtoMN && !isTtoEM && ElecVect.size()>=1) {
        m_logger << INFO << " + Try to reconstruct W -> en" << SLogger::endmsg;
        Hist("Events", "enqq")->Fill(2., EventWeight);
        if( !(ElecVect[0].pt() > m_Elec1PtCut) ) {m_logger << INFO << " - No electron above threshold" << SLogger::endmsg;}
        else {
            Hist("Events", "enqq")->Fill(3., EventWeight);
            if( ElecVect[0].isTightElectron() && ElecVect[0].isHeepElectron() ) Hist("Electron_VIDHEEP", "enqq")->Fill(2, EventWeight);
            if( ElecVect[0].isTightElectron() && !ElecVect[0].isHeepElectron() ) Hist("Electron_VIDHEEP", "enqq")->Fill(1, EventWeight);
            if( !ElecVect[0].isTightElectron() && ElecVect[0].isHeepElectron() ) Hist("Electron_VIDHEEP", "enqq")->Fill(-1, EventWeight);
            if( !ElecVect[0].isTightElectron() && !ElecVect[0].isHeepElectron() ) Hist("Electron_VIDHEEP", "enqq")->Fill(-2, EventWeight);
            if(FatJetsVect.size()>=2) {
                if( ElecVect[0].isTightElectron() && ElecVect[0].isHeepElectron() ) Hist("Electron_VIDHEEP_2J", "enqq")->Fill(2, EventWeight);
                if( ElecVect[0].isTightElectron() && !ElecVect[0].isHeepElectron() ) Hist("Electron_VIDHEEP_2J", "enqq")->Fill(1, EventWeight);
                if( !ElecVect[0].isTightElectron() && ElecVect[0].isHeepElectron() ) Hist("Electron_VIDHEEP_2J", "enqq")->Fill(-1, EventWeight);
                if( !ElecVect[0].isTightElectron() && !ElecVect[0].isHeepElectron() ) Hist("Electron_VIDHEEP_2J", "enqq")->Fill(-2, EventWeight);
            }
            // Apply electron id/iso
            //if( !(ElecVect[0].isTightElectron()==1) ) {m_logger << INFO << " - No single electron Id/Iso" << SLogger::endmsg;}
            if(ElecVect[0].pt() + MET.et() > m_VPtCut) Hist("Electron_pfIso", "enqq")->Fill(ElecVect[0].pfRhoCorrRelIso03(), EventWeight);
            if( !(ElecVect[0].isTightElectron()) ) {m_logger << INFO << " - No single electron Id/Iso" << SLogger::endmsg;}
            else {
                Hist("Events", "enqq")->Fill(4., EventWeight);
                // W kinematic reconstruction
                m_logger << INFO << " + Try to recover neutrino pz" << SLogger::endmsg;
                float pz = m_VariableTool.RecoverNeutrinoPz(CalibratedElecVect[0], MET_tlv);
                Neutrino.SetPxPyPzE(MET_tlv.Px(), MET_tlv.Py(), pz, sqrt(MET_tlv.Px()*MET_tlv.Px() + MET_tlv.Py()*MET_tlv.Py() + pz*pz) );
                V = CalibratedElecVect[0] + Neutrino;
                V_tmass = sqrt(2.*MET.et()*CalibratedElecVect[0].Pt()*(1.-cos(CalibratedElecVect[0].DeltaPhi(MET_tlv))));
                Hist("W_mass", "en")->Fill(V.M(), EventWeight);
                Hist("W_tmass", "en")->Fill(V_tmass, EventWeight);
                Hist("W_pt", "en")->Fill(V.Pt(), EventWeight);
                Hist("Electron_pt", "en")->Fill(CalibratedElecVect[0].Pt(), EventWeight);
                if(V.Pt() < m_VPtCut) {m_logger << INFO << " - No V boost" << SLogger::endmsg;}
                else {
                    // Check trigger consistency
                    Hist("HLT_SingleEleMETInclusive_COUNT", "Trigger")->Fill(0., EventWeight);
                    if(METNoMu>250. && ElecVect[0].pt()>300.) Hist("HLT_SingleEleMET250_COUNT", "Trigger")->Fill(0., EventWeight);
                    if(!triggerMap["SingleEle"] && !triggerMap["SingleIsoEle"] && !triggerMap["MET"] && !triggerMap["METMHT"] && !triggerMap["METMHTNoMu"]) {
                        if(triggerMap["MET"] || triggerMap["METMHT"] || triggerMap["METMHTNoMu"]) {
                            Hist("HLT_SingleEleMETInclusive_COUNT", "Trigger")->Fill(1., EventWeight);
                            if(METNoMu>250. && ElecVect[0].pt()>300.) Hist("HLT_SingleEleMET250_COUNT", "Trigger")->Fill(1., EventWeight);
                        }
                        m_logger << INFO << " - Trigger inconsistency" << SLogger::endmsg; throw SError( SError::SkipEvent );
                    }
                    if(!isMC && ((sample.find("MET")!=std::string::npos && (triggerMap["SingleEle"] || triggerMap["SingleIsoEle"])) || (sample.find("Electron")!=std::string::npos && !(triggerMap["SingleEle"] || triggerMap["SingleIsoEle"])))) { m_logger << INFO << " - Trigger double counting" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
                    // SF
                    if(isMC) {
//                        TriggerWeight *= std::max(m_ScaleFactorTool.GetTrigSingleEle(ElecVect[0].pt(), ElecVect[0].eta()), m_ScaleFactorTool.GetTrigSingleIsoEle(ElecVect[0].pt(), ElecVect[0].eta()));
//                        TriggerWeight *= m_ScaleFactorTool.GetTrigSingleEle(ElecVect[0].pt(), ElecVect[0].eta());
                        TriggerWeight *= m_ScaleFactorTool.GetTrigEleMET(ElecVect[0].pt(), ElecVect[0].eta(), MaxMETNoMuMHTNoMu);
                        LeptonWeight *= m_ScaleFactorTool.GetEleIdTightWP(ElecVect[0].pt(), ElecVect[0].eta());
                        LeptonWeight *= m_ScaleFactorTool.GetEleReco(ElecVect[0].pt(), ElecVect[0].eta());
                        EventWeight *= TriggerWeight * LeptonWeight;
                        //
//                        TriggerWeightUp *= m_ScaleFactorTool.GetTrigSingleEle(ElecVect[0].pt(), ElecVect[0].eta(), +1);
                        TriggerWeightUp *= m_ScaleFactorTool.GetTrigEleMET(ElecVect[0].pt(), ElecVect[0].eta(), MaxMETNoMuMHTNoMu, +1);
                        LeptonWeightUp *= m_ScaleFactorTool.GetEleIdTightWP(ElecVect[0].pt(), ElecVect[0].eta(), +1);
                        LeptonWeightUp *= m_ScaleFactorTool.GetEleReco(ElecVect[0].pt(), ElecVect[0].eta(), +1);
//                        TriggerWeightDown *= m_ScaleFactorTool.GetTrigSingleEle(ElecVect[0].pt(), ElecVect[0].eta(), -1);
                        TriggerWeightDown *= m_ScaleFactorTool.GetTrigEleMET(ElecVect[0].pt(), ElecVect[0].eta(), MaxMETNoMuMHTNoMu, -1);
                        LeptonWeightDown *= m_ScaleFactorTool.GetEleIdTightWP(ElecVect[0].pt(), ElecVect[0].eta(), -1);
                        LeptonWeightDown *= m_ScaleFactorTool.GetEleReco(ElecVect[0].pt(), ElecVect[0].eta(), -1);
                    }
                    isWtoEN = true;
                    Hist("Events", "enqq")->Fill(5., EventWeight);
                    m_logger << INFO << " + W -> en candidate reconstructed" << SLogger::endmsg;
                }
            }
        }
    }
    // ----------- Z TO NEUTRINOS ---------------
    if(!isZtoMM && !isZtoEE && !isWtoMN && !isWtoEN && !isTtoEM) {
        m_logger << INFO << " + Try to reconstruct Z -> nn" << SLogger::endmsg;
        if(MET.et() < m_MEtPtCut) {m_logger << INFO << " - Low MET" << SLogger::endmsg;}
        else {
            Hist("Events", "nnqq")->Fill(2., EventWeight);
            if(!(nElectrons==0 && nMuons==0)) {
                Hist("nElectrons", "nnqq")->Fill(nElectrons, EventWeight);
                Hist("nMuons", "nnqq")->Fill(nMuons, EventWeight);
                m_logger << INFO << " - Iso Leptons" << SLogger::endmsg;
            }
            else {
                Hist("Events", "nnqq")->Fill(3., EventWeight);
                if(!(nTaus==0)) {
                    Hist("nTaus", "nnqq")->Fill(nTaus, EventWeight);
                    m_logger << INFO << " - Iso Taus" << SLogger::endmsg;
                }
                else {
                    // Dummy V candidate
                    if(MET.et()!=MET.et()) { m_logger << WARNING << " - MET is nan" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
                    V.SetPtEtaPhiE(MET.et(), 0., MET.phi(), MET.et());
                    // Check trigger consistency
                    if(!isMC && !triggerMap["MET"] && !triggerMap["METMHT"] && !triggerMap["METMHTNoMu"]) { m_logger << INFO << " - Trigger inconsistency" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
                    if(isMC) {
                        TriggerWeight *= m_ScaleFactorTool.GetTrigMET(MaxMETNoMuMHTNoMu);
                    }
                    isZtoNN=true;
                    Hist("Events", "nnqq")->Fill(4., EventWeight);
                    m_logger << INFO << " + Z -> nn candidate reconstructed" << SLogger::endmsg;
                }
            }
        }
    }
    // ----------- Z TO HADRONS ---------------
    if(!isZtoMM && !isZtoEE && !isWtoMN && !isWtoEN && !isZtoNN && !isTtoEM) {
        m_logger << INFO << " + Try to reconstruct V -> qq" << SLogger::endmsg;
        if(FatJetsVect.size() < 2) {m_logger << INFO << " - No 2 fat jets" << SLogger::endmsg;}
        else {
            Hist("Events", "qqqq")->Fill(2., EventWeight);
            float dijetMass = (FatJetsVect[0].tlv() + FatJetsVect[1].tlv()).M();
            if(!(FatJetsVect[0].IDTight() && FatJetsVect[1].IDTight())) {m_logger << INFO << " - Failed noise cleaning" << SLogger::endmsg;}
            else {
                Hist("Events", "qqqq")->Fill(3., EventWeight);
                if(dijetMass > m_XJJMassLowerCut && FatJetsMassVect[0] > m_HMassLowerCut) {
                    Hist("Jet1Jet2DPhi", "qqqq")->Fill(fabs(FatJetsVect[0].tlv().DeltaPhi(FatJetsVect[1].tlv())), EventWeight);
                    Hist("Jet1Jet2DEta", "qqqq")->Fill(fabs(FatJetsVect[0].eta()-FatJetsVect[1].eta()), EventWeight);
                }
                if(fabs(FatJetsVect[0].eta()-FatJetsVect[1].eta()) > 1.3) {m_logger << INFO << " - Jet dEta" << SLogger::endmsg;} //FatJetsVect[0].pt() < 400.
                else {
                    Hist("Events", "qqqq")->Fill(4., EventWeight);
                    if(MET.et() > 250.) {
                        Hist("MET_pt", "qqqq")->Fill(MET.et(), EventWeight);
                        m_logger << INFO << " - MET veto" << SLogger::endmsg;
                    }
                    else {
                        Hist("Events", "qqqq")->Fill(5., EventWeight);
                        if(!(nElectrons==0 && nMuons==0)) {
                            Hist("nElectrons", "qqqq")->Fill(nElectrons, EventWeight);
                            Hist("nMuons", "qqqq")->Fill(nMuons, EventWeight);
                            m_logger << INFO << " - Iso Leptons" << SLogger::endmsg;
                        }
                        else {
                            Hist("Events", "qqqq")->Fill(6., EventWeight);
                            if(isZtoMM || isZtoEE || isWtoMN || isWtoEN || isZtoNN) m_logger << WARNING << " - Overlap with leptonic channels" << SLogger::endmsg;
                            if(FatJetsMassVect[1] > FatJetsMassVect[0]) {
                                std::swap(FatJetsVect[0], FatJetsVect[1]);
                                std::swap(FatJetsPuppiVect[0], FatJetsPuppiVect[1]);
                                std::swap(FatJetsTau21Vect[0], FatJetsTau21Vect[1]);
                                std::swap(FatJetsMassVect[0], FatJetsMassVect[1]);
                                std::swap(FatJetsMassVectScaleUp[0], FatJetsMassVectScaleUp[1]);
                                std::swap(FatJetsMassVectScaleDown[0], FatJetsMassVectScaleDown[1]);
                                std::swap(FatJetsMassVectResUp[0], FatJetsMassVectResUp[1]);
                                std::swap(FatJetsMassVectResDown[0], FatJetsMassVectResDown[1]);
                                std::swap(FatJetsBTagVect[0], FatJetsBTagVect[1]);
                            }
                            if(dijetMass < m_XJJMassLowerCut) {
                                m_logger << INFO << " - X mass < " << m_XJJMassLowerCut << SLogger::endmsg;
                                if(FatJetsMassVect[0] > m_HMassLowerCut) Hist("X_mass", "qqqq")->Fill(dijetMass, EventWeight);
                            }
                            else {
                                Hist("Events", "qqqq")->Fill(7., EventWeight);
                                // Require at least one of the two to be H-tag
                                if(FatJetsMassVect[0] < m_JMassLowerCut) { //m_HMassLowerCut FIXME
                                    m_logger << INFO << " - No H-tagged jet" << SLogger::endmsg;
                                    Hist("Jet1_softdropCorrMass", "qqqq")->Fill(FatJetsMassVect[0], EventWeight);
                                }
                                else {
                                    H = FatJetsVect[0].tlv();
                                    V = FatJetsVect[1].tlv();
                                    // Check trigger consistency
                                    if(!isMC && !triggerMap["HT"] && !triggerMap["JET"] && !triggerMap["HTWJ"] && !triggerMap["SUBJET"] && !triggerMap["SUBHT"] && !triggerMap["SUBTAG"]) { m_logger << INFO << " - Trigger inconsistency" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
                                    isVtoQQ = true;
                                    Hist("Events", "qqqq")->Fill(8., EventWeight);
                                    m_logger << INFO << " + V -> qq candidate reconstructed" << SLogger::endmsg;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    // ----------- Nothing else matters ---------------
    if(!isZtoMM && !isZtoEE && !isWtoMN && !isWtoEN && !isZtoNN && !isTtoEM && !isVtoQQ) { m_logger << INFO << " - No V candidate" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
    

    // -----------------------------------
    //           HADRONIC HIGGS
    // -----------------------------------

    if(FatJetsVect.size()==0) { m_logger << INFO << " - N Fat Jets = 0" << SLogger::endmsg; throw SError( SError::SkipEvent ); }
    
    if(isZtoNN) Hist("Events", "nnqq")->Fill(5., EventWeight);
    if(isWtoEN) Hist("Events", "enqq")->Fill(6., EventWeight);
    if(isWtoMN) Hist("Events", "mnqq")->Fill(7., EventWeight);
    if(isTtoEM) Hist("Events", "emqq")->Fill(6., EventWeight);
    if(isZtoEE) Hist("Events", "eeqq")->Fill(7., EventWeight);
    if(isZtoMM) Hist("Events", "mmqq")->Fill(8., EventWeight);
    m_logger << INFO << " + N Fat Jets > 0" << SLogger::endmsg;
    
    H = FatJetsVect[0].tlv();
    
    
    
    // In case of VtoQQ channel, replace JetsNoFatJetVect, which makes no sense anymore, with JetsNoFatJetsVect
    if(isVtoQQ && !isZtoMM && !isZtoEE && !isWtoMN && !isWtoEN && !isZtoNN && !isTtoEM) {JetsNoFatJetVect = JetsNoFatJetsVect; nJetsNoFatJet = JetsNoFatJetsVect.size();}
    else {nJetsNoFatJet = JetsNoFatJetVect.size();}
    
    JetMetDPhi = isVtoQQ ? std::min(fabs(MET_tlv.DeltaPhi(V)), fabs(MET_tlv.DeltaPhi(H))) : fabs(MET_tlv.DeltaPhi(H));
    for(unsigned int i=0; i<JetsNoFatJetVect.size(); i++) if(fabs( MET_tlv.DeltaPhi(JetsNoFatJetVect[i].tlv()) ) < MinJetMetDPhi) MinJetMetDPhi = fabs( MET_tlv.DeltaPhi(JetsNoFatJetVect[i].tlv()) );
    
    for(unsigned int i=0; i<JetsNoFatJetVect.size(); i++) {
        if(JetsNoFatJetVect[i].csv() > MaxJetNoFatJetBTag) MaxJetNoFatJetBTag = JetsNoFatJetVect[i].csv();
        if(m_bTaggingScaleTool.isTagged_tag( JetsNoFatJetVect[i].csv() )) nBTagJets++; // Count Tight b-tagged jets
        if(m_bTaggingScaleTool.isTagged_veto( JetsNoFatJetVect[i].csv() )) nBVetoJets++; // Count Loose b-tagged jets
    }
    
    // -----------------------------------
    //           HIGGS to TauTau
    // -----------------------------------

    for(int i = 0; i < m_tau.N; ++i) {
        UZH::Tau tau(&m_tau, i);
        if(tau.pt() > m_TauPtCut && fabs(tau.eta()) < m_TauEtaCut && tau.TauType()==2 && tau.byVLooseIsolationMVArun2v1PWnewDMwLT()>0.5) {
            //if(tau.tlv().DeltaR(FatJetsVect[0].tlv()) < 0.8) {
                isBoostedTau = true;
                //if(tau.byVLooseIsolationMVArun2v1PWnewDMwLT() > isBoostedTau) isBoostedTau = tau.byVLooseIsolationMVArun2v1PWnewDMwLT();
            //}
            m_logger << INFO << " - Boosted H->tautau candidate found" << SLogger::endmsg;
        }
    }
    
    for(unsigned int i = 1; i < FatJetsVect.size(); ++i) {
        if(FatJetsVect[i].Hbbtag() > 0.3) isBoosted4B = true;
        m_logger << INFO << " - Boosted H->tautau candidate found" << SLogger::endmsg;
    }
    
    // --- BTV ---
    if(isMC) {
        float BTagAK8WeightBUp(1.), BTagAK8WeightBDown(1.), BTagAK8WeightLUp(1.), BTagAK8WeightLDown(1.), BTagAK8WeightB1(1.), BTagAK8WeightB2(1.), BTagAK8WeightL1(1.), BTagAK8WeightL2(1.);
        float BTagAK4WeightBUp(1.), BTagAK4WeightBDown(1.), BTagAK4WeightLUp(1.), BTagAK4WeightLDown(1.), BTagAK4WeightB1(1.), BTagAK4WeightB2(1.), BTagAK4WeightL1(1.), BTagAK4WeightL2(1.);
        BTagAK8Weight = m_bTaggingScaleTool.getSoftdropSubjetScaleFactor(FatJetsVect[0]); // event b-tag SF weight
        BTagAK8WeightB1 = m_bTaggingScaleTool.getSoftdropSubjetScaleFactor(FatJetsVect[0], +1, 0);
        BTagAK8WeightB2 = m_bTaggingScaleTool.getSoftdropSubjetScaleFactor(FatJetsVect[0], -1, 0);
        BTagAK8WeightL1 = m_bTaggingScaleTool.getSoftdropSubjetScaleFactor(FatJetsVect[0], 0, +1);
        BTagAK8WeightL2 = m_bTaggingScaleTool.getSoftdropSubjetScaleFactor(FatJetsVect[0], 0, -1);
        BTagAK8WeightBUp = std::min(BTagAK8WeightB1, BTagAK8WeightB2);
        BTagAK8WeightBDown = std::max(BTagAK8WeightB1, BTagAK8WeightB2);
        BTagAK8WeightLUp = std::min(BTagAK8WeightL1, BTagAK8WeightL2);
        BTagAK8WeightLDown = std::max(BTagAK8WeightL1, BTagAK8WeightL2);
        BTagAK8WeightUp = BTagAK8Weight + sqrt( pow(BTagAK8WeightBUp-BTagAK8Weight, 2) + pow(BTagAK8WeightLUp-BTagAK8Weight, 2) );
        BTagAK8WeightDown = BTagAK8Weight - sqrt( pow(BTagAK8Weight-BTagAK8WeightBDown, 2) + pow(BTagAK8Weight-BTagAK8WeightLDown, 2) );
        // AK4 weights
        if(!m_bTaggingScaleTool.isTagged_veto(MaxJetNoFatJetBTag)) {// Veto Loose (SB and SR)
            BTagAK4Weight = m_bTaggingScaleTool.getScaleFactor_veto(JetsNoFatJetVect);
            BTagAK4WeightBUp = m_bTaggingScaleTool.getScaleFactor_veto(JetsNoFatJetVect, +1, 0);
            BTagAK4WeightBDown = m_bTaggingScaleTool.getScaleFactor_veto(JetsNoFatJetVect, -1, 0);
            BTagAK4WeightLUp = m_bTaggingScaleTool.getScaleFactor_veto(JetsNoFatJetVect, 0, +1);
            BTagAK4WeightLDown = m_bTaggingScaleTool.getScaleFactor_veto(JetsNoFatJetVect, 0, -1);
        }
        else if(m_bTaggingScaleTool.isTagged(MaxJetNoFatJetBTag) && !m_bTaggingScaleTool.isTagged_tag(MaxJetNoFatJetBTag)) { // Middle-Earth: Loose b-tagged but NOT tight b-tagged
            BTagAK4Weight = m_bTaggingScaleTool.getScaleFactor(JetsNoFatJetVect);
            BTagAK4WeightBUp = m_bTaggingScaleTool.getScaleFactor(JetsNoFatJetVect, +1, 0);
            BTagAK4WeightBDown = m_bTaggingScaleTool.getScaleFactor(JetsNoFatJetVect, -1, 0);
            BTagAK4WeightLUp = m_bTaggingScaleTool.getScaleFactor(JetsNoFatJetVect, 0, +1);
            BTagAK4WeightLDown = m_bTaggingScaleTool.getScaleFactor(JetsNoFatJetVect, 0, -1);
        }
        else if(m_bTaggingScaleTool.isTagged_tag(MaxJetNoFatJetBTag)) {// Tight b-tag (TR)
            BTagAK4Weight = m_bTaggingScaleTool.getScaleFactor_tag(JetsNoFatJetVect);
            BTagAK4WeightBUp = m_bTaggingScaleTool.getScaleFactor_tag(JetsNoFatJetVect, +1, 0);
            BTagAK4WeightBDown = m_bTaggingScaleTool.getScaleFactor_tag(JetsNoFatJetVect, -1, 0);
            BTagAK4WeightLUp = m_bTaggingScaleTool.getScaleFactor_tag(JetsNoFatJetVect, 0, +1);
            BTagAK4WeightLDown = m_bTaggingScaleTool.getScaleFactor_tag(JetsNoFatJetVect, 0, -1);
        }
        if(isinf(BTagAK4Weight) || isnan(BTagAK4Weight)) BTagAK4Weight = 1.;
        //if(!(BTagAK4Weight>0. && BTagAK4Weight<2. )) m_logger << WARNING << " + BTag weights: " << BTagAK4Weight << " : " << MaxJetNoFatJetBTag << SLogger::endmsg;//BTagAK4Weight = 1.;
        BTagAK4WeightUp = BTagAK4Weight + sqrt( pow(BTagAK4WeightBUp-BTagAK4Weight, 2) + pow(BTagAK4WeightLUp-BTagAK4Weight, 2) );
        BTagAK4WeightDown = BTagAK4Weight - sqrt( pow(BTagAK4Weight-BTagAK4WeightBDown, 2) + pow(BTagAK4Weight-BTagAK4WeightLDown, 2) );
        
        m_logger << INFO << " + BTag weights: " << BTagAK8Weight << ", B Up: "<<BTagAK8WeightBUp << ", B Down: " << BTagAK8WeightBDown << ", L Up"  << BTagAK8WeightLUp << ", L Down" << BTagAK8WeightLDown << " | Up: " << BTagAK8WeightUp << ", Down: " << BTagAK8WeightDown << SLogger::endmsg;
        m_logger << INFO << " + BTag weights: tag " << BTagAK8Weight << ", veto: " << BTagAK4Weight << SLogger::endmsg;
        BTagWeight = BTagAK8Weight * BTagAK4Weight;
        BTagWeightUp = BTagAK8WeightBUp * BTagAK4WeightBUp;
        BTagWeightDown = BTagAK8WeightBDown * BTagAK4WeightBDown;
        //EventWeight *= BTagWeight; // not yet
        
        // Fill histograms
        if(isMC) {
            m_bTaggingScaleTool.fillEfficiencies(JetsVect);
            m_bTaggingScaleTool.fillEfficiencies_veto(JetsVect);
            m_bTaggingScaleTool.fillEfficiencies_tag(JetsVect);
            m_bTaggingScaleTool.fillSoftdropSubjetEfficiencies(FatJetsVect);
            m_bTaggingScaleTool.fillDoubleBEfficiencies_loose(FatJetsVect);
            m_bTaggingScaleTool.fillDoubleBEfficiencies_tight(FatJetsVect);
        }
        
        // Double b-tagger
        BBTagWeight = m_bTaggingScaleTool.getDoubleBScaleFactor(FatJetsVect[0].pt(), FatJetsVect[0].eta(), FatJetsVect[0].hadronFlavour(), FatJetsVect[0].Hbbtag(), 0);
        BBTagWeightUp = m_bTaggingScaleTool.getDoubleBScaleFactor(FatJetsVect[0].pt(), FatJetsVect[0].eta(), FatJetsVect[0].hadronFlavour(), FatJetsVect[0].Hbbtag(), +1);
        BBTagWeightDown = m_bTaggingScaleTool.getDoubleBScaleFactor(FatJetsVect[0].pt(), FatJetsVect[0].eta(), FatJetsVect[0].hadronFlavour(), FatJetsVect[0].Hbbtag(), -1);
        m_logger << INFO << " - ZtoQQ event with doubleB weight: " << BBTagWeight << SLogger::endmsg;
    }
    
    
    // -----------------------------------
    //           X and VARIABLES
    // -----------------------------------
    X = V + H;
    float Hcsv1 = FatJetsVect[0].subjet_softdrop_N() >= 1 ? FatJetsVect[0].subjet_softdrop_csv()[0] : -1.;
    float Hcsv2 = FatJetsVect[0].subjet_softdrop_N() >= 2 ? FatJetsVect[0].subjet_softdrop_csv()[1] : -1.;
    TLorentzVector L1, L2, B1, B2;
    if(FatJetsVect[0].subjet_softdrop_N()>=1) B1.SetPtEtaPhiE(FatJetsVect[0].subjet_softdrop_pt()[0], FatJetsVect[0].subjet_softdrop_eta()[0], FatJetsVect[0].subjet_softdrop_phi()[0], FatJetsVect[0].subjet_softdrop_e()[0]);
    if(FatJetsVect[0].subjet_softdrop_N()>=2) B2.SetPtEtaPhiE(FatJetsVect[0].subjet_softdrop_pt()[1], FatJetsVect[0].subjet_softdrop_eta()[1], FatJetsVect[0].subjet_softdrop_phi()[1], FatJetsVect[0].subjet_softdrop_e()[1]);
    if(isZtoMM) {L1 = MuonVect[m1].charge() > MuonVect[m2].charge() ? MuonVect[m1].tlv() : MuonVect[m2].tlv(); L2 = MuonVect[m1].charge() > MuonVect[m2].charge() ? MuonVect[m2].tlv() : MuonVect[m1].tlv();}
    if(isZtoEE) {L1 = ElecVect[e1].charge() > ElecVect[e2].charge() ? CalibratedElecVect[e1] : CalibratedElecVect[e2]; L2 = ElecVect[e1].charge() > ElecVect[e2].charge() ? CalibratedElecVect[e2] : CalibratedElecVect[e1];}
    if(isWtoMN) {L1 = MuonVect[0].charge() > 0 ? MuonVect[0].tlv() : Neutrino; L2 = MuonVect[0].charge() > 0 ? Neutrino : MuonVect[0].tlv();}
    if(isWtoEN) {L1 = ElecVect[0].charge() > 0 ? ElecVect[0].tlv() : Neutrino; L2 = ElecVect[0].charge() > 0 ? Neutrino : ElecVect[0].tlv();}
    if(isVtoQQ) {
        if(FatJetsVect[1].subjet_softdrop_N()>=1) L1.SetPtEtaPhiE(FatJetsVect[1].subjet_softdrop_pt()[0], FatJetsVect[1].subjet_softdrop_eta()[0], FatJetsVect[1].subjet_softdrop_phi()[0], FatJetsVect[1].subjet_softdrop_e()[0]);
        if(FatJetsVect[1].subjet_softdrop_N()>=2) L2.SetPtEtaPhiE(FatJetsVect[1].subjet_softdrop_pt()[1], FatJetsVect[1].subjet_softdrop_eta()[1], FatJetsVect[1].subjet_softdrop_phi()[1], FatJetsVect[1].subjet_softdrop_e()[1]);
    }
    if(!isZtoNN) {
        Centrality = m_VariableTool.ReturnCentrality(L1, L2, B1, B2);
        CosThetaStar = m_VariableTool.ReturnCosThetaStar(X, V);
        CosTheta1 = m_VariableTool.ReturnCosTheta1(V, L1, L2, B1, B2);
        CosTheta2 = m_VariableTool.ReturnCosTheta2(H, L1, L2, B1, B2);
        Phi = m_VariableTool.ReturnPhi(X, L1, L2, B1, B2);
        Phi1 = m_VariableTool.ReturnPhi1(X, L1, L2);
    }
    else {
        CosTheta2 = fabs(m_VariableTool.ReturnCosThetaJ(V, B1)); // Cos Theta J
    }
    VHDEta = fabs(V.Eta() - H.Eta());
    
    isTveto = (nBVetoJets==0 && nTaus==0);
    H_mass = FatJetsMassVect[0];
    H_tau21 = FatJetsTau21Vect[0];
    H_ddt = H_mass != 0. ? H_tau21 + 0.063 * log( H_mass*H_mass/H.Pt() ) : -1.;
    H_csv1 = std::max(Hcsv1, Hcsv2);
    H_csv2 = std::min(Hcsv1, Hcsv2);
    H_flav1 = isMC && FatJetsVect[0].subjet_softdrop_N() > 0 ? FatJetsVect[0].subjet_softdrop_partonFlavour()[0] : 0;
    H_flav2 = isMC && FatJetsVect[0].subjet_softdrop_N() > 1 ? FatJetsVect[0].subjet_softdrop_partonFlavour()[1] : 0;
    H_dbt = FatJetsVect[0].Hbbtag();
    H_ntag = FatJetsBTagVect[0];
    H_ptB = FatJetsVect[0].subjet_softdrop_N() > 1 ? FatJetsVect[0].subjet_softdrop_pt()[1] / (FatJetsVect[0].subjet_softdrop_pt()[0] + FatJetsVect[0].subjet_softdrop_pt()[1]) : -1.;
    H_chf = FatJetsVect[0].chf();
    H_nhf = FatJetsVect[0].nhf();
    H_phf = FatJetsVect[0].phf();
    H_muf = FatJetsVect[0].muf();
    H_emf = FatJetsVect[0].emf();
    H_chm = FatJetsVect[0].chm();
    V_mass = V.M();
    if(isZtoNN) V_mass = V.Pt();
    if(isWtoEN or isWtoMN) V_mass = V_tmass;
    if(isVtoQQ) {
        float Vcsv1 = FatJetsVect[1].subjet_softdrop_N() >= 1 ? FatJetsVect[1].subjet_softdrop_csv()[0] : -1.;
        float Vcsv2 = FatJetsVect[1].subjet_softdrop_N() >= 2 ? FatJetsVect[1].subjet_softdrop_csv()[1] : -1.;
        V_mass = FatJetsMassVect[1];
        V_tau21 = FatJetsTau21Vect[1];
        V_ddt = V_mass != 0. ? V_tau21 + 0.063 * log( V_mass*V_mass/V.Pt() ) : -1.;
        V_csv1 = std::max(Vcsv1, Vcsv2);
        V_csv2 = std::min(Vcsv1, Vcsv2);
        V_dbt = FatJetsVect[1].Hbbtag();
        V_ntag = FatJetsBTagVect[1];
    }
    X_tmass = sqrt( 2.*V.Pt()*FatJetsVect[0].pt()*(1.-cos(FatJetsVect[0].tlv().DeltaPhi(V))) );
    X_mass = isZtoNN ? X_tmass : X.M();
    
    m_logger << INFO << " - Variables filled, now cleaning" << SLogger::endmsg;
    
    // -----------------------------------
    //           CLEANING
    // -----------------------------------
    if(isZtoNN) {
        // N-1 plots
        if(X_mass > m_XTMassLowerCut) {
            Hist("MinJetMetDPhi", "nnqq")->Fill(MinJetMetDPhi, EventWeight);
            Hist("JetMetDPhi", "nnqq")->Fill(JetMetDPhi, EventWeight);
        }
        // min dPhi
        if(MinJetMetDPhi < 0.5) {
            if(X_mass > m_XTMassLowerCut) {
                Hist("Jet_chf", "nnqq")->Fill(FatJetsVect[0].chf(), EventWeight);
                Hist("Jet_phf", "nnqq")->Fill(FatJetsVect[0].phf(), EventWeight);
            }
            m_logger << INFO << " - X candidate fails minDPhi cut" << SLogger::endmsg;
            throw SError( SError::SkipEvent );
        }
        // jet cleaning
        if(!(JetMetDPhi >= 2. && FatJetsVect[0].IDTight() && FatJetsVect[0].chf() > 0.1)) {m_logger << INFO << " - ZtoNN event failed noise cleaning" << SLogger::endmsg; throw SError( SError::SkipEvent );}
        Hist("Events", "nnqq")->Fill(6., EventWeight);
        // X mass
        if(X_mass < m_XTMassLowerCut) {
            Hist("X_mass", "nnqq")->Fill(X.M(), EventWeight);
            Hist("X_tmass", "nnqq")->Fill(X_mass, EventWeight);
            Hist("X_cmass", "nnqq")->Fill(0., EventWeight);
            m_logger << INFO << " - X candidate low mass" << SLogger::endmsg;
            throw SError( SError::SkipEvent );
        }
        Hist("Events", "nnqq")->Fill(7., EventWeight);
        fillJetPlots(FatJetsVect[0], FatJetsMassVect[0], FatJetsTau21Vect[0], "Jet", "nnqq");
        fillMEtPlots(MET, "nnqq");
        fillEventPlots("nnqq");
        Hist("X_mass", "nnqq")->Fill(X.M(), EventWeight);
        Hist("X_tmass", "nnqq")->Fill(X_mass, EventWeight);
        Hist("X_cmass", "nnqq")->Fill(0., EventWeight);
    }
    if(isWtoEN) {
        // Orthogonality with W'->enu
        if(X_mass > 800. && MET.et() >= 80. && CalibratedElecVect[0].DeltaR(H) > 3.1415/2. && fabs(MET_tlv.DeltaPhi(H)) > 2. && fabs(V.DeltaPhi(H)) > 2. && (CalibratedElecVect[0].Pt()/MET.et()>0.4 && CalibratedElecVect[0].Pt()/MET.et()<1.5) && MET.et() > 150. && CalibratedElecVect[0].Pt()>130. && V_mass>250.) Hist("ElectronMetDPhi_VW", "enqq")->Fill(fabs(CalibratedElecVect[0].DeltaPhi(MET_tlv)), EventWeight);
        if(X_mass > 800. && MET.et() >= 80. && CalibratedElecVect[0].DeltaR(H) > 3.1415/2. && fabs(MET_tlv.DeltaPhi(H)) > 2. && fabs(V.DeltaPhi(H)) > 2. && (CalibratedElecVect[0].Pt()/MET.et()>0.4 && CalibratedElecVect[0].Pt()/MET.et()<1.5) && MET.et() > 150. && CalibratedElecVect[0].Pt()>130. && V_mass>250. && FatJetsMassVect[0]>30.) Hist("ElectronMetDPhi_VWJ", "enqq")->Fill(fabs(CalibratedElecVect[0].DeltaPhi(MET_tlv)), EventWeight);
        // N-1 plots
        Hist("MET_pt", "enqq")->Fill(MET.et(), EventWeight);
        if(!(MET.et() >= 80.)) {m_logger << INFO << " - WtoEN event failed MET noise cleaning" << SLogger::endmsg; throw SError( SError::SkipEvent );}
        Hist("ElectronJetDPhi", "enqq")->Fill(fabs(CalibratedElecVect[0].DeltaPhi(H)), EventWeight);
        Hist("ElectronMetDPhi", "enqq")->Fill(fabs(CalibratedElecVect[0].DeltaPhi(MET_tlv)), EventWeight);
        Hist("ElectronMetPtRatio", "enqq")->Fill(CalibratedElecVect[0].Pt()/MET.et(), EventWeight);
        Hist("WJetDPhi", "enqq")->Fill(fabs(V.DeltaPhi(H)), EventWeight);
        Hist("WJetDEta", "enqq")->Fill(fabs(V.Eta()-H.Eta()), EventWeight);
        if(!(fabs(MET_tlv.DeltaPhi(CalibratedElecVect[0])) < 1.5 && JetMetDPhi > 2. && fabs(CalibratedElecVect[0].DeltaPhi(H)) > 2.)) {m_logger << INFO << " - WtoEN event failed noise cleaning" << SLogger::endmsg; throw SError( SError::SkipEvent );}
        Hist("Events", "enqq")->Fill(7., EventWeight);
        if(X_mass < m_XMassLowerCut) {
            m_logger << INFO << " - X candidate low mass" << SLogger::endmsg;
            throw SError( SError::SkipEvent );
        }
        Hist("Events", "enqq")->Fill(8., EventWeight);
        fill4VectPlots(CalibratedElecVect[0], "Electron", "enqq");
        fillJetPlots(FatJetsVect[0], FatJetsMassVect[0], FatJetsTau21Vect[0], "Jet", "enqq");
        fillMEtPlots(MET, "enqq");
        fillEventPlots("enqq");
        if(fabs(ElecVect[0].eta()) < 1.4442) Hist("Electron_pt_B", "enqq")->Fill(CalibratedElecVect[0].Pt(), EventWeight);
        else if(fabs(ElecVect[0].eta()) < 1.566) Hist("Electron_pt_E", "enqq")->Fill(CalibratedElecVect[0].Pt(), EventWeight);
        //Hist("Electron_pfIso", "enqq")->Fill(ElecVect[0].pfRhoCorrRelIso03(), EventWeight);
        Hist("ElectronJetDR", "enqq")->Fill(fabs(CalibratedElecVect[0].DeltaR(H)), EventWeight);
        Hist("W_mass", "enqq")->Fill(V.M(), EventWeight);
        Hist("W_tmass", "enqq")->Fill(V_tmass, EventWeight);
        Hist("W_pt", "enqq")->Fill(V.Pt(), EventWeight);
        Hist("X_mass", "enqq")->Fill(X_mass, EventWeight);
//        if(X_mass>3900 && H_mass>105 && H_mass<135 && isWtoEN && MaxJetNoFatJetBTag<0.5426 && (H_csv1>0.5426 && H_csv2>0.5426)) {
//            std::cout << std::endl << std::endl << "EVENT   Run Number: " << RunNumber << " lumi "<< LumiNumber << " EventNumber " << EventNumber << " Ele pt: " << CalibratedElecVect[0].Pt() << "  eta: " << CalibratedElecVect[0].Eta() << " met pt: " << MET.et() << " W pt: " << V.Pt() << " ElectronJetDR: " << fabs(CalibratedElecVect[0].DeltaR(H)) << " WJetDPhi: " << fabs(V.DeltaPhi(H)) << " WJetDEta: " << fabs(V.Eta()-H.Eta()) << " ElectronJetDPhi: " << fabs(CalibratedElecVect[0].DeltaPhi(H)) << " ElectronMetDPhi: " << fabs(CalibratedElecVect[0].DeltaPhi(MET_tlv)) << std::endl << std::endl;
//        }
    }
    if(isWtoMN) {
        // Orthogonality with W'->lnu
        if(X_mass > 800. && MuonVect[0].tlv().DeltaR(H) > 3.1415/2. && fabs(MET_tlv.DeltaPhi(H)) > 2. && fabs(V.DeltaPhi(H)) > 2. && (MuonVect[0].pt()/MET.et()>0.4 && MuonVect[0].pt()/MET.et()<1.5) && V_mass>100.) Hist("MuonMetDPhi_VW", "mnqq")->Fill(fabs(MuonVect[0].tlv().DeltaPhi(MET_tlv)), EventWeight);
        if(X_mass > 800. && MuonVect[0].tlv().DeltaR(H) > 3.1415/2. && fabs(MET_tlv.DeltaPhi(H)) > 2. && fabs(V.DeltaPhi(H)) > 2. && (MuonVect[0].pt()/MET.et()>0.4 && MuonVect[0].pt()/MET.et()<1.5) && V_mass>100. && FatJetsMassVect[0]>30.) Hist("MuonMetDPhi_VWJ", "mnqq")->Fill(fabs(MuonVect[0].tlv().DeltaPhi(MET_tlv)), EventWeight);
        // N-1 plots
        //Hist("MHT", "mnqq")->Fill(MHT, EventWeight);
        //if(!(MHT >= 100.)) {m_logger << INFO << " - WtoMN event failed MET noise cleaning" << SLogger::endmsg; throw SError( SError::SkipEvent );}
        Hist("MuonJetDPhi", "mnqq")->Fill(fabs(MuonVect[0].tlv().DeltaPhi(H)), EventWeight);
        Hist("MuonMetDPhi", "mnqq")->Fill(fabs(MuonVect[0].tlv().DeltaPhi(MET_tlv)), EventWeight);
        Hist("MuonMetPtRatio", "mnqq")->Fill(MuonVect[0].pt()/MET.et(), EventWeight);
        Hist("WJetDPhi", "mnqq")->Fill(fabs(V.DeltaPhi(H)), EventWeight);
        Hist("WJetDEta", "mnqq")->Fill(fabs(V.Eta()-H.Eta()), EventWeight);
        if(!(fabs(MET_tlv.DeltaPhi(MuonVect[0].tlv())) < 1.5 && JetMetDPhi > 2. && fabs(MuonVect[0].tlv().DeltaPhi(H)) > 2.)) {m_logger << INFO << " - WtoMN event failed noise cleaning" << SLogger::endmsg; throw SError( SError::SkipEvent );}
        Hist("Events", "mnqq")->Fill(8., EventWeight);
        if(X_mass < m_XMassLowerCut) {
            m_logger << INFO << " - X candidate low mass" << SLogger::endmsg;
            throw SError( SError::SkipEvent );
        }
        Hist("Events", "mnqq")->Fill(9., EventWeight);
        fill4VectPlots(MuonVect[0].tlv(), "Muon", "mnqq");
        fillJetPlots(FatJetsVect[0], FatJetsMassVect[0], FatJetsTau21Vect[0], "Jet", "mnqq");
        fillMEtPlots(MET, "mnqq");
        fillEventPlots("mnqq");
        if(fabs(MuonVect[0].eta()) < 1.2) Hist("Muon_pt_B", "mnqq")->Fill(MuonVect[0].pt(), EventWeight);
        else Hist("Muon_pt_E", "mnqq")->Fill(MuonVect[0].pt(), EventWeight);
        Hist("MuonJetDR", "mnqq")->Fill(fabs(MuonVect[0].tlv().DeltaR(H)), EventWeight);
        Hist("W_mass", "mnqq")->Fill(V.M(), EventWeight);
        Hist("W_tmass", "mnqq")->Fill(V_tmass, EventWeight);
        Hist("W_pt", "mnqq")->Fill(V.Pt(), EventWeight);
        Hist("X_mass", "mnqq")->Fill(X_mass, EventWeight);
    }
    if(isTtoEM) {
        //if(X_mass < m_XMassLowerCut) {
        //    m_logger << INFO << " - X candidate low mass" << SLogger::endmsg;
        //    throw SError( SError::SkipEvent );
        //}
        Hist("ElectronJetDPhi", "emqq")->Fill(fabs(ElecVect[0].tlv().DeltaPhi(H)), EventWeight);
        Hist("ElectronMetDPhi", "emqq")->Fill(fabs(ElecVect[0].tlv().DeltaPhi(MET_tlv)), EventWeight);
        Hist("MuonJetDPhi", "emqq")->Fill(fabs(MuonVect[0].tlv().DeltaPhi(H)), EventWeight);
        Hist("MuonMetDPhi", "emqq")->Fill(fabs(MuonVect[0].tlv().DeltaPhi(MET_tlv)), EventWeight);
        Hist("ElectronMuonDPhi", "emqq")->Fill(fabs(MuonVect[0].tlv().DeltaR(ElecVect[0].tlv())), EventWeight);
        Hist("ElectronMuonDR", "emqq")->Fill(fabs(MuonVect[0].tlv().DeltaR(ElecVect[0].tlv())), EventWeight);
        fill4VectPlots(MuonVect[0].tlv(), "Muon", "emqq");
        fill4VectPlots(ElecVect[0].tlv(), "Electron", "emqq");
        fillJetPlots(FatJetsVect[0], FatJetsMassVect[0], FatJetsTau21Vect[0], "Jet", "emqq");
        fillMEtPlots(MET, "emqq");
        fillEventPlots("emqq");
        Hist("V_mass", "emqq")->Fill(V.M(), EventWeight);
        Hist("V_pt", "emqq")->Fill(V.Pt(), EventWeight);
        Hist("X_mass", "emqq")->Fill(X_mass, EventWeight);
        Hist("Events", "emqq")->Fill(7., EventWeight);
    }
    if(isZtoEE) {
        // N-1 plots
        if(X_mass > m_XMassLowerCut) {
            Hist("ZJetDPhi", "eeqq")->Fill(fabs(V.DeltaPhi(H)), EventWeight);
            Hist("ZJetDEta", "eeqq")->Fill(fabs(V.Eta()-H.Eta()), EventWeight);
        }
        if(!(fabs(V.DeltaPhi(H)) > 2.)) {
            m_logger << INFO << " - ZtoEE event failed noise cleaning" << SLogger::endmsg;
            throw SError( SError::SkipEvent );
        }
        Hist("Events", "eeqq")->Fill(8., EventWeight);
        if(X_mass < m_XMassLowerCut) {
            m_logger << INFO << " - X candidate low mass" << SLogger::endmsg;
            throw SError( SError::SkipEvent );
        }
        Hist("Events", "eeqq")->Fill(9., EventWeight);
        fill4VectPlots(CalibratedElecVect[e1], "Electron1", "eeqq");
        fill4VectPlots(CalibratedElecVect[e2], "Electron2", "eeqq");
        fillJetPlots(FatJetsVect[0], FatJetsMassVect[0], FatJetsTau21Vect[0], "Jet", "eeqq");
        fillMEtPlots(MET, "eeqq");
        fillEventPlots("eeqq");
        if(fabs(ElecVect[e1].eta()) < 1.4442) Hist("Electron1_pt_B", "eeqq")->Fill(CalibratedElecVect[e1].Pt(), EventWeight);
        else if(fabs(ElecVect[e1].eta()) < 1.566) Hist("Electron1_pt_E", "eeqq")->Fill(CalibratedElecVect[e1].Pt(), EventWeight);
        if(fabs(ElecVect[e2].eta()) < 1.4442) Hist("Electron2_pt_B", "eeqq")->Fill(CalibratedElecVect[e2].Pt(), EventWeight);
        else if(fabs(ElecVect[e2].eta()) < 1.566) Hist("Electron2_pt_E", "eeqq")->Fill(CalibratedElecVect[e2].Pt(), EventWeight);
        //Hist("Electron1_pfIso", "eeqq")->Fill(ElecVect[e1].pfRhoCorrRelIso03(), EventWeight);
        //Hist("Electron2_pfIso", "eeqq")->Fill(ElecVect[e2].pfRhoCorrRelIso03(), EventWeight);
        Hist("ElectronElectronDR", "eeqq")->Fill(fabs(CalibratedElecVect[e1].DeltaR(CalibratedElecVect[e2])), EventWeight);
        Hist("Z_pt", "eeqq")->Fill(V.Pt(), EventWeight);
        Hist("Z_mass", "eeqq")->Fill(V.M(), EventWeight);
        Hist("X_mass", "eeqq")->Fill(X_mass, EventWeight);
        if(fabs(ElecVect[e1].eta()) < 1.4442 && fabs(ElecVect[e2].eta()) < 1.4442) Hist("Z_mass_BB", "eeqq")->Fill(V.M(), EventWeight);
        if(fabs(ElecVect[e1].eta()) < 1.4442 && fabs(ElecVect[e2].eta()) > 1.4442) Hist("Z_mass_BE", "eeqq")->Fill(V.M(), EventWeight);
        if(fabs(ElecVect[e1].eta()) > 1.4442 && fabs(ElecVect[e2].eta()) < 1.4442) Hist("Z_mass_EB", "eeqq")->Fill(V.M(), EventWeight);
        if(fabs(ElecVect[e1].eta()) > 1.4442 && fabs(ElecVect[e2].eta()) > 1.4442) Hist("Z_mass_EE", "eeqq")->Fill(V.M(), EventWeight);
        
    }
    if(isZtoMM) {
        // N-1 plots
        if(X_mass > m_XMassLowerCut) {
            Hist("ZJetDPhi", "mmqq")->Fill(fabs(V.DeltaPhi(H)), EventWeight);
            Hist("ZJetDEta", "mmqq")->Fill(fabs(V.Eta()-H.Eta()), EventWeight);
        }
        if(!(fabs(V.DeltaPhi(H)) > 2.)) {
            m_logger << INFO << " - ZtoMM event failed noise cleaning" << SLogger::endmsg;
            throw SError( SError::SkipEvent );
        }
        Hist("Events", "mmqq")->Fill(9., EventWeight);
        if(X_mass < m_XMassLowerCut) {
            m_logger << INFO << " - X candidate low mass" << SLogger::endmsg;
            throw SError( SError::SkipEvent );
        }
        Hist("Events", "mmqq")->Fill(10., EventWeight);
        fill4VectPlots(MuonVect[m1].tlv(), "Muon1", "mmqq");
        fill4VectPlots(MuonVect[m2].tlv(), "Muon2", "mmqq");
        fillJetPlots(FatJetsVect[0], FatJetsMassVect[0], FatJetsTau21Vect[0], "Jet", "mmqq");
        fillMEtPlots(MET, "mmqq");
        fillEventPlots("mmqq");
        if(fabs(MuonVect[m1].eta()) < 1.2) Hist("Muon1_pt_B", "mmqq")->Fill(MuonVect[m1].pt(), EventWeight);
        else Hist("Muon1_pt_E", "mmqq")->Fill(MuonVect[m1].pt(), EventWeight);
        if(fabs(MuonVect[m2].eta()) < 1.2) Hist("Muon2_pt_B", "mmqq")->Fill(MuonVect[m2].pt(), EventWeight);
        else Hist("Muon2_pt_E", "mmqq")->Fill(MuonVect[m2].pt(), EventWeight);
        //Hist("Muon1_trkIso", "mmqq")->Fill(trackIso1, EventWeight); // to be filled together with candidate
        //Hist("Muon2_trkIso", "mmqq")->Fill(trackIso2, EventWeight);
        Hist("MuonMuonDR", "mmqq")->Fill(fabs(MuonVect[m1].DeltaR(MuonVect[m2])), EventWeight);
        Hist("Z_pt", "mmqq")->Fill(V.Pt(), EventWeight);
        Hist("Z_mass", "mmqq")->Fill(V.M(), EventWeight);
        Hist("X_mass", "mmqq")->Fill(X_mass, EventWeight);
        if(fabs(MuonVect[m1].eta()) < 1.2 && fabs(MuonVect[m2].eta()) < 1.2) Hist("Z_mass_BB", "mmqq")->Fill(V.M(), EventWeight);
        if(fabs(MuonVect[m1].eta()) < 1.2 && fabs(MuonVect[m2].eta()) > 1.2) Hist("Z_mass_BE", "mmqq")->Fill(V.M(), EventWeight);
        if(fabs(MuonVect[m1].eta()) > 1.2 && fabs(MuonVect[m2].eta()) < 1.2) Hist("Z_mass_EB", "mmqq")->Fill(V.M(), EventWeight);
        if(fabs(MuonVect[m1].eta()) > 1.2 && fabs(MuonVect[m2].eta()) > 1.2) Hist("Z_mass_EE", "mmqq")->Fill(V.M(), EventWeight);
    }
    

    // Semileptonic analysis categorization
    if(isZtoEE || isZtoMM || ((isZtoNN || isWtoEN || isWtoMN) && isTveto)) {
    
        if(isZtoNN) Hist("Events", "nnqq")->Fill(8., EventWeight);
        if(isWtoEN) Hist("Events", "enqq")->Fill(9., EventWeight);
        if(isWtoMN) Hist("Events", "mnqq")->Fill(10., EventWeight);
        
        // Signal Regions
        if(H_mass > m_HMassLowerCut && H_mass < m_HMassUpperCut) {
            // Cut flow
            if(isZtoNN) Hist("Events", "nnqq")->Fill(9., EventWeight);
            if(isWtoEN) Hist("Events", "enqq")->Fill(10., EventWeight);
            if(isWtoMN) Hist("Events", "mnqq")->Fill(11., EventWeight);
            if(isZtoEE) Hist("Events", "eeqq")->Fill(10., EventWeight);
            if(isZtoMM) Hist("Events", "mmqq")->Fill(11., EventWeight);
            // Single b-tag
            if(H_ntag >= 1) {
                if(isZtoNN) Hist("Events", "nnqq")->Fill(10., EventWeight);
                if(isWtoEN) Hist("Events", "enqq")->Fill(11., EventWeight);
                if(isWtoMN) Hist("Events", "mnqq")->Fill(12., EventWeight);
                if(isZtoEE) Hist("Events", "eeqq")->Fill(11., EventWeight);
                if(isZtoMM) Hist("Events", "mmqq")->Fill(12., EventWeight);
            }
            // Double b-tag
            if(H_ntag == 2) {
                if(isZtoNN) Hist("Events", "nnqq")->Fill(11., EventWeight);
                if(isWtoEN) Hist("Events", "enqq")->Fill(12., EventWeight);
                if(isWtoMN) Hist("Events", "mnqq")->Fill(13., EventWeight);
                if(isZtoEE) Hist("Events", "eeqq")->Fill(12., EventWeight);
                if(isZtoMM) Hist("Events", "mmqq")->Fill(13., EventWeight);
            }
        }
        
        
        
    }
    
    if(isVtoQQ) {
        Hist("Jet1MetDPhi", "qqqq")->Fill(fabs(FatJetsVect[0].tlv().DeltaPhi(MET_tlv)), EventWeight);
        Hist("Jet2MetDPhi", "qqqq")->Fill(fabs(FatJetsVect[1].tlv().DeltaPhi(MET_tlv)), EventWeight);
//        Hist("Events", "qqqq")->Fill(6., EventWeight);
//        if(X_mass < m_XJJMassLowerCut) {
//            m_logger << INFO << " - X candidate low mass" << SLogger::endmsg;
//            throw SError( SError::SkipEvent );
//        }
//        Hist("Events", "qqqq")->Fill(6., EventWeight);
        fillJetPlots(FatJetsVect[0], FatJetsMassVect[0], FatJetsTau21Vect[0], "Jet1", "qqqq");
        fillJetPlots(FatJetsVect[1], FatJetsMassVect[1], FatJetsTau21Vect[1], "Jet2", "qqqq");
        fillMEtPlots(MET, "qqqq");
        fillEventPlots("qqqq");
        Hist("X_mass", "qqqq")->Fill(X_mass, EventWeight);
        
        // NOT for SM backgrounds
        //float hpSF(1.03), lpSF(0.88);
        //if(V_tau21 <= m_Tau21LowerCut) Tau21Weight = hpSF;
        //else if(V_tau21 > m_Tau21LowerCut && V_tau21 < m_Tau21UpperCut) Tau21Weight = lpSF;
        //EventWeight *= Tau21Weight;
        
        // Control Region
        if((V_mass >= m_JMassLowerCut && V_mass < m_VMassLowerCut) || (V_mass >= m_HMassUpperCut && H_mass < m_JMassUpperCut)) {
            // Single b-tag
            if(H_ntag == 1) {
                // High Purity
                if(V_tau21 <= m_Tau21LowerCut) {
                }
                // Low Purity
                if(V_tau21 > m_Tau21LowerCut && V_tau21 < m_Tau21UpperCut) {
                }
            }
            // Double b-tag
            if(H_ntag == 2) {
                // High Purity
                if(V_tau21 <= m_Tau21LowerCut) {
                }
                // Low Purity
                if(V_tau21 > m_Tau21LowerCut && V_tau21 < m_Tau21UpperCut) {
                }
            }
        }
        // W Signal Region
        if(V_mass >= m_VMassLowerCut && V_mass < m_VMassInterCut) {
            Hist("Events", "qqqq")->Fill(9., EventWeight);
            // Single b-tag
            if(H_ntag == 1) {
                // High Purity
                if(V_tau21 <= m_Tau21LowerCut) {
                    Hist("Events", "qqqq")->Fill(10., EventWeight);
                }
                // Low Purity
                if(V_tau21 > m_Tau21LowerCut && V_tau21 < m_Tau21UpperCut) {
                    Hist("Events", "qqqq")->Fill(11., EventWeight);
                }
            }
            // Double b-tag
            if(H_ntag == 2) {
                // High Purity
                if(V_tau21 <= m_Tau21LowerCut) {
                    Hist("Events", "qqqq")->Fill(12., EventWeight);
                }
                // Low Purity
                if(V_tau21 > m_Tau21LowerCut && V_tau21 < m_Tau21UpperCut) {
                    Hist("Events", "qqqq")->Fill(13., EventWeight);
                }
            }
        }
        // Z Signal Region
        if(V_mass >= m_VMassInterCut && V_mass < m_VMassUpperCut) {
            Hist("Events", "qqqq")->Fill(9., EventWeight);
            // Single b-tag
            if(H_ntag == 1) {
                // High Purity
                if(V_tau21 <= m_Tau21LowerCut) {
                    Hist("Events", "qqqq")->Fill(14., EventWeight);
                }
                // Low Purity
                if(V_tau21 > m_Tau21LowerCut && V_tau21 < m_Tau21UpperCut) {
                    Hist("Events", "qqqq")->Fill(15., EventWeight);
                }
            }
            // Double b-tag
            if(H_ntag == 2) {
                // High Purity
                if(V_tau21 <= m_Tau21LowerCut) {
                    Hist("Events", "qqqq")->Fill(16., EventWeight);
                }
                // Low Purity
                if(V_tau21 > m_Tau21LowerCut && V_tau21 < m_Tau21UpperCut) {
                    Hist("Events", "qqqq")->Fill(17., EventWeight);
                }
            }
        }
    }
    
    if(isWtoEN || isZtoEE) {
        Hist("ElecT_eff", "Sys")->Fill(0., EventWeight);
        Hist("ElecT_eff", "Sys")->Fill(+1., EventWeight*TriggerWeightUp/TriggerWeight);
        Hist("ElecT_eff", "Sys")->Fill(-1., EventWeight*TriggerWeightDown/TriggerWeight);
    }
    if(isWtoMN || isZtoMM) {
        Hist("MuonT_eff", "Sys")->Fill(0., EventWeight);
        Hist("MuonT_eff", "Sys")->Fill(+1., EventWeight*TriggerWeightUp/TriggerWeight);
        Hist("MuonT_eff", "Sys")->Fill(-1., EventWeight*TriggerWeightDown/TriggerWeight);
    }
    
    if(isWtoEN) {
        Hist("Elec1_eff", "Sys")->Fill(0., EventWeight);
        Hist("Elec1_eff", "Sys")->Fill(+1., EventWeight*LeptonWeightUp/LeptonWeight);
        Hist("Elec1_eff", "Sys")->Fill(-1., EventWeight*LeptonWeightDown/LeptonWeight);
    }
    if(isWtoMN) {
        Hist("Muon1_eff", "Sys")->Fill(0., EventWeight);
        Hist("Muon1_eff", "Sys")->Fill(+1., EventWeight*LeptonWeightUp/LeptonWeight);
        Hist("Muon1_eff", "Sys")->Fill(-1., EventWeight*LeptonWeightDown/LeptonWeight);
    }
    if(isZtoEE) {
        Hist("Elec2_eff", "Sys")->Fill(0., EventWeight);
        Hist("Elec2_eff", "Sys")->Fill(+1., EventWeight*LeptonWeightUp/LeptonWeight);
        Hist("Elec2_eff", "Sys")->Fill(-1., EventWeight*LeptonWeightDown/LeptonWeight);
    }
    if(isZtoMM) {
        Hist("Muon2_eff", "Sys")->Fill(0., EventWeight);
        Hist("Muon2_eff", "Sys")->Fill(+1., EventWeight*LeptonWeightUp/LeptonWeight);
        Hist("Muon2_eff", "Sys")->Fill(-1., EventWeight*LeptonWeightDown/LeptonWeight);
    }
    if(H_mass > m_JMassLowerCut && !isTveto) {
        Hist("BTagSF_veto", "Sys")->Fill(0., EventWeight*BTagAK4Weight);
        Hist("BTagSF_veto", "Sys")->Fill(-1., EventWeight*BTagAK4WeightUp);
        Hist("BTagSF_veto", "Sys")->Fill(+1., EventWeight*BTagAK4WeightDown);
    }

    if(!isVtoQQ) {
        // H mass scale
        if(FatJetsMassVect[0] > m_HMassLowerCut && FatJetsMassVect[0] < m_HMassUpperCut) Hist("H_mass_scale", "Sys")->Fill(0., EventWeight);
        if(FatJetsMassVectScaleUp[0] > m_HMassLowerCut && FatJetsMassVectScaleUp[0] < m_HMassUpperCut) Hist("H_mass_scale", "Sys")->Fill(+1., EventWeight);
        if(FatJetsMassVectScaleDown[0] > m_HMassLowerCut && FatJetsMassVectScaleDown[0] < m_HMassUpperCut) Hist("H_mass_scale", "Sys")->Fill(-1., EventWeight);
        // H mass res
        if(FatJetsMassVect[0] > m_HMassLowerCut && FatJetsMassVect[0] < m_HMassUpperCut) Hist("H_mass_res", "Sys")->Fill(0., EventWeight);
        if(FatJetsMassVectResUp[0] > m_HMassLowerCut && FatJetsMassVectResUp[0] < m_HMassUpperCut) Hist("H_mass_res", "Sys")->Fill(+1., EventWeight);
        if(FatJetsMassVectResDown[0] > m_HMassLowerCut && FatJetsMassVectResDown[0] < m_HMassUpperCut) Hist("H_mass_res", "Sys")->Fill(-1., EventWeight);
        
        // Shape
        Hist("X_mass_scale", "Sys")->Fill(isZtoNN ? sqrt( 2.*(MET.et())*FatJetsVect[0].pt()*(1.-cos(FatJetsVect[0].tlv().DeltaPhi(V))) ) : (FatJetsVect[0].tlv()+V).M(), EventWeight);
        Hist("X_mass_scaleUp", "Sys")->Fill(isZtoNN ? sqrt( 2.*(MET.et()*MET.JetEnUp())*FatJetsVectScaleUp[0].Pt()*(1.-cos(FatJetsVectScaleUp[0].DeltaPhi(V))) ) : (FatJetsVectScaleUp[0]+V).M(), EventWeight);
        Hist("X_mass_scaleDown", "Sys")->Fill(isZtoNN ? sqrt( 2.*(MET.et()*MET.JetEnDown())*FatJetsVectScaleDown[0].Pt()*(1.-cos(FatJetsVectScaleDown[0].DeltaPhi(V))) ) : (FatJetsVectScaleDown[0]+V).M(), EventWeight);
        Hist("X_mass_res", "Sys")->Fill(isZtoNN ? sqrt( 2.*(MET.et())*FatJetsVect[0].pt()*(1.-cos(FatJetsVect[0].tlv().DeltaPhi(V))) ) : (FatJetsVect[0].tlv()+V).M(), EventWeight);
        Hist("X_mass_resUp", "Sys")->Fill(isZtoNN ? sqrt( 2.*(MET.et()*MET.JetResUp())*FatJetsVectResUp[0].Pt()*(1.-cos(FatJetsVectResUp[0].DeltaPhi(V))) ) : (FatJetsVectResUp[0]+V).M(), EventWeight);
        Hist("X_mass_resDown", "Sys")->Fill(isZtoNN ? sqrt( 2.*(MET.et()*MET.JetResDown())*FatJetsVectResDown[0].Pt()*(1.-cos(FatJetsVectResDown[0].DeltaPhi(V))) ) : (FatJetsVectResDown[0]+V).M(), EventWeight);
        Hist("X_mass_unc", "Sys")->Fill(isZtoNN ? sqrt( 2.*(MET.et())*FatJetsVect[0].pt()*(1.-cos(FatJetsVect[0].tlv().DeltaPhi(V))) ) : (FatJetsVect[0].tlv()+V).M(), EventWeight);
        Hist("X_mass_uncUp", "Sys")->Fill(isZtoNN ? sqrt( 2.*(MET.et()*MET.UnclusteredEnUp())*FatJetsVectResUp[0].Pt()*(1.-cos(FatJetsVectResUp[0].DeltaPhi(V))) ) : (FatJetsVectResUp[0]+V).M(), EventWeight);
        Hist("X_mass_uncDown", "Sys")->Fill(isZtoNN ? sqrt( 2.*(MET.et()*MET.UnclusteredEnDown())*FatJetsVectResDown[0].Pt()*(1.-cos(FatJetsVectResDown[0].DeltaPhi(V))) ) : (FatJetsVectResDown[0]+V).M(), EventWeight);
    }
    
    if(isVtoQQ) {
        // Jet mass scale and resolution
        //if(V_tau21 < m_Tau21UpperCut) {
        // V mass scale
        if(FatJetsMassVect[1] > m_VMassLowerCut && FatJetsMassVect[1] < m_VMassUpperCut) Hist("V_mass_scale", "Sys")->Fill(0., EventWeight);
        if(FatJetsMassVectScaleUp[1] > m_VMassLowerCut && FatJetsMassVectScaleUp[1] < m_VMassUpperCut) Hist("V_mass_scale", "Sys")->Fill(+1., EventWeight);
        if(FatJetsMassVectScaleDown[1] > m_VMassLowerCut && FatJetsMassVectScaleDown[1] < m_VMassUpperCut) Hist("V_mass_scale", "Sys")->Fill(-1., EventWeight);
        // V mass res
        if(FatJetsMassVect[1] > m_VMassLowerCut && FatJetsMassVect[1] < m_VMassUpperCut) Hist("V_mass_res", "Sys")->Fill(0., EventWeight);
        if(FatJetsMassVectResUp[1] > m_VMassLowerCut && FatJetsMassVectResUp[1] < m_VMassUpperCut) Hist("V_mass_res", "Sys")->Fill(+1., EventWeight);
        if(FatJetsMassVectResDown[1] > m_VMassLowerCut && FatJetsMassVectResDown[1] < m_VMassUpperCut) Hist("V_mass_res", "Sys")->Fill(-1., EventWeight);

        // H mass scale
        if(FatJetsMassVect[0] > m_HMassLowerCut && FatJetsMassVect[0] < m_HMassUpperCut) Hist("H_mass_scale", "Sys")->Fill(0., EventWeight);
        if(FatJetsMassVectScaleUp[0] > m_HMassLowerCut && FatJetsMassVectScaleUp[0] < m_HMassUpperCut) Hist("H_mass_scale", "Sys")->Fill(+1., EventWeight);
        if(FatJetsMassVectScaleDown[0] > m_HMassLowerCut && FatJetsMassVectScaleDown[0] < m_HMassUpperCut) Hist("H_mass_scale", "Sys")->Fill(-1., EventWeight);
        // H mass res
        if(FatJetsMassVect[0] > m_HMassLowerCut && FatJetsMassVect[0] < m_HMassUpperCut) Hist("H_mass_res", "Sys")->Fill(0., EventWeight);
        if(FatJetsMassVectResUp[0] > m_HMassLowerCut && FatJetsMassVectResUp[0] < m_HMassUpperCut) Hist("H_mass_res", "Sys")->Fill(+1., EventWeight);
        if(FatJetsMassVectResDown[0] > m_HMassLowerCut && FatJetsMassVectResDown[0] < m_HMassUpperCut) Hist("H_mass_res", "Sys")->Fill(-1., EventWeight);

        // Migration
        // W mass region
        if(FatJetsMassVect[1] > m_VMassLowerCut && FatJetsMassVect[1] < m_VMassInterCut) { Hist("W_mass_scale", "Sys")->Fill(0., EventWeight); Hist("W_mass_res", "Sys")->Fill(0., EventWeight); }
        if(FatJetsMassVectScaleUp[1] > m_VMassLowerCut && FatJetsMassVectScaleUp[1] < m_VMassInterCut) Hist("W_mass_scale", "Sys")->Fill(+1., EventWeight);
        if(FatJetsMassVectScaleDown[1] > m_VMassLowerCut && FatJetsMassVectScaleDown[1] < m_VMassInterCut) Hist("W_mass_scale", "Sys")->Fill(-1., EventWeight);
        if(FatJetsMassVectResUp[1] > m_VMassLowerCut && FatJetsMassVectResUp[1] < m_VMassInterCut) Hist("W_mass_res", "Sys")->Fill(+1., EventWeight);
        if(FatJetsMassVectResDown[1] > m_VMassLowerCut && FatJetsMassVectResDown[1] < m_VMassInterCut) Hist("W_mass_res", "Sys")->Fill(-1., EventWeight);
        // Z mass region
        if(FatJetsMassVect[1] > m_VMassInterCut && FatJetsMassVect[1] < m_VMassUpperCut) { Hist("Z_mass_scale", "Sys")->Fill(0., EventWeight); Hist("Z_mass_res", "Sys")->Fill(0., EventWeight); }
        if(FatJetsMassVectScaleUp[1] > m_VMassInterCut && FatJetsMassVectScaleUp[1] < m_VMassUpperCut) Hist("Z_mass_scale", "Sys")->Fill(+1., EventWeight);
        if(FatJetsMassVectScaleDown[1] > m_VMassInterCut && FatJetsMassVectScaleDown[1] < m_VMassUpperCut) Hist("Z_mass_scale", "Sys")->Fill(-1., EventWeight);
        if(FatJetsMassVectResUp[1] > m_VMassInterCut && FatJetsMassVectResUp[1] < m_VMassUpperCut) Hist("Z_mass_res", "Sys")->Fill(+1., EventWeight);
        if(FatJetsMassVectResDown[1] > m_VMassInterCut && FatJetsMassVectResDown[1] < m_VMassUpperCut) Hist("Z_mass_res", "Sys")->Fill(-1., EventWeight);
        
        //}
        // jet energy scale and resolution
        if(FatJetsVect[0].pt() > 250. && FatJetsVect[1].pt() > 250.) Hist("J_energy_scale", "Sys")->Fill(0., EventWeight);
        if(FatJetsVectScaleUp[0].Pt() > 250. && FatJetsVectScaleUp[1].Pt() > 250.) Hist("J_energy_scale", "Sys")->Fill(+1., EventWeight);
        if(FatJetsVectScaleDown[0].Pt() > 250. && FatJetsVectScaleDown[1].Pt() > 250.) Hist("J_energy_scale", "Sys")->Fill(-1., EventWeight);
        if(FatJetsVectRes[0].Pt() > 250. && FatJetsVectRes[1].Pt() > 250.) Hist("J_energy_res", "Sys")->Fill(0., EventWeight);
        if(FatJetsVectResUp[0].Pt() > 250. && FatJetsVectResUp[1].Pt() > 250.) Hist("J_energy_res", "Sys")->Fill(+1., EventWeight);
        if(FatJetsVectResDown[0].Pt() > 250. && FatJetsVectResDown[1].Pt() > 250.) Hist("J_energy_res", "Sys")->Fill(-1., EventWeight);
        Hist("X_mass_scale", "Sys")->Fill((FatJetsVect[0].tlv()+FatJetsVect[1].tlv()).M(), EventWeight);
        Hist("X_mass_scaleUp", "Sys")->Fill((FatJetsVectScaleUp[0]+FatJetsVectScaleUp[1]).M(), EventWeight);
        Hist("X_mass_scaleDown", "Sys")->Fill((FatJetsVectScaleDown[0]+FatJetsVectScaleDown[1]).M(), EventWeight);
        Hist("X_mass_res", "Sys")->Fill((FatJetsVectRes[0]+FatJetsVectRes[1]).M(), EventWeight);
        Hist("X_mass_resUp", "Sys")->Fill((FatJetsVectResUp[0]+FatJetsVectResUp[1]).M(), EventWeight);
        Hist("X_mass_resDown", "Sys")->Fill((FatJetsVectResDown[0]+FatJetsVectResDown[1]).M(), EventWeight);
        
        // Tau21 extrapolation
        if(V_tau21 < m_Tau21LowerCut) {
            float tau21unc = 0.085*log(FatJetsVect[1].pt()/200.);
            Hist("V_tau21_extr_HP", "Sys")->Fill(0., EventWeight);
            Hist("V_tau21_extr_HP", "Sys")->Fill(+1., EventWeight*(1.+tau21unc));
            Hist("V_tau21_extr_HP", "Sys")->Fill(-1., EventWeight*(1.-tau21unc));
        }
        else {
            float tau21unc = 0.039*log(FatJetsVect[1].pt()/200.);
            Hist("V_tau21_extr_LP", "Sys")->Fill(0., EventWeight);
            Hist("V_tau21_extr_LP", "Sys")->Fill(+1., EventWeight*(1.-tau21unc));
            Hist("V_tau21_extr_LP", "Sys")->Fill(-1., EventWeight*(1.+tau21unc));
        }
        // Matching
        if(H_dbt >= 0.3 && V_tau21 < m_Tau21UpperCut) {
            Hist("CandidateMatching", "qqqq")->Fill(0., EventWeight);
            if(GenH.DeltaR(FatJetsVect[0].tlv()) < 0.8) {
                Hist("CandidateMatching", "qqqq")->Fill(+1, EventWeight);
                if(GenV.DeltaR(FatJetsVect[1].tlv()) < 0.8) Hist("CandidateMatching", "qqqq")->Fill(+2, EventWeight);
            }
        }
    }
    
    m_logger << INFO << " - Common uncertainties" << SLogger::endmsg;
    
    // Common uncertainties
    
    if((H_mass > m_HMassLowerCut && H_mass < m_HMassUpperCut) && ((isVtoQQ && V_mass >= m_VMassLowerCut && V_mass < m_VMassUpperCut && V_tau21 < m_Tau21UpperCut) || !isVtoQQ) ) {
        
        // Herwig
        float Hunc = 1.30636e-01*log(FatJetsVect[0].pt() + 1.53474e+03);
        Hist("H_tagging", "Sys")->Fill(0., EventWeight);
        Hist("H_tagging", "Sys")->Fill(+1., EventWeight*(Hunc));
        Hist("H_tagging", "Sys")->Fill(-1., EventWeight/(Hunc));
        
        // Pile-up
        Hist("Pileup", "Sys")->Fill(0., EventWeight);
        Hist("Pileup", "Sys")->Fill(+1., EventWeight*PUWeightUp/PUWeight);
        Hist("Pileup", "Sys")->Fill(-1., EventWeight*PUWeightDown/PUWeight);
        
        // PDF
        Hist("PDF_scale", "Sys")->Fill(0., EventWeight);
        Hist("PDF_scale", "Sys")->Fill(+1., EventWeight*m_eventInfo.pdf_rms);
        Hist("PDF_scale", "Sys")->Fill(-1., EventWeight*(2.-m_eventInfo.pdf_rms));
        
        // Scale
        Hist("QCD_scale", "Sys")->Fill(0., EventWeight);
        Hist("QCD_scale", "Sys")->Fill(-1., EventWeight*std::min(std::min(m_eventInfo.genFacWeightUp, m_eventInfo.genRenWeightUp), m_eventInfo.genFacRenWeightUp));
        Hist("QCD_scale", "Sys")->Fill(+1., EventWeight*std::max(std::max(m_eventInfo.genFacWeightDown, m_eventInfo.genRenWeightDown), m_eventInfo.genFacRenWeightDown));
        
        // b-tagging - SF taken as ANTI-CORRELATED
        if(H_dbt >= 0.9) {
            Hist("H_doubleB_tight", "Sys")->Fill(0., EventWeight*BBTagWeight);
            Hist("H_doubleB_tight", "Sys")->Fill(+1., EventWeight*BBTagWeightUp);
            Hist("H_doubleB_tight", "Sys")->Fill(-1., EventWeight*BBTagWeightDown);
        }
        if(H_dbt >= 0.3 && H_dbt < 0.9) {
            Hist("H_doubleB_loose", "Sys")->Fill(0., EventWeight*BBTagWeight);
            Hist("H_doubleB_loose", "Sys")->Fill(-1., EventWeight*BBTagWeightUp);
            Hist("H_doubleB_loose", "Sys")->Fill(+1., EventWeight*BBTagWeightDown);
        }
        if(H_dbt < 0.3) {
            Hist("H_doubleB_notag", "Sys")->Fill(0., EventWeight*BBTagWeight);
            Hist("H_doubleB_notag", "Sys")->Fill(-1., EventWeight*BBTagWeightUp);
            Hist("H_doubleB_notag", "Sys")->Fill(+1., EventWeight*BBTagWeightDown);
        }
        if(H_ntag == 2) {
            Hist("H_subjet_tight", "Sys")->Fill(0., EventWeight*BTagAK8Weight);
            Hist("H_subjet_tight", "Sys")->Fill(+1., EventWeight*BTagAK8WeightUp);
            Hist("H_subjet_tight", "Sys")->Fill(-1., EventWeight*BTagAK8WeightDown);
        }
        if(H_ntag == 1) {
            Hist("H_subjet_loose", "Sys")->Fill(0., EventWeight*BTagAK8Weight);
            Hist("H_subjet_loose", "Sys")->Fill(-1., EventWeight*BTagAK8WeightUp);
            Hist("H_subjet_loose", "Sys")->Fill(+1., EventWeight*BTagAK8WeightDown);
        }
        if(H_ntag == 0) {
            Hist("H_subjet_notag", "Sys")->Fill(0., EventWeight*BTagAK8Weight);
            Hist("H_subjet_notag", "Sys")->Fill(-1., EventWeight*BTagAK8WeightUp);
            Hist("H_subjet_notag", "Sys")->Fill(+1., EventWeight*BTagAK8WeightDown);
        }
        
    }
    
    // End of systematics
    
    m_logger << INFO << " + Tree filled" << SLogger::endmsg;
    
    return;
}







bool VHAnalysis::isGoodEvent(int runNumber, int lumiSection) {
  
  bool isGood = true;
  if (m_isData) {
    isGood = m_grl.HasRunLumiBlock( runNumber, lumiSection );
    if( !isGood ) {
      m_logger << WARNING << "Bad event! Run: " << runNumber <<  " - Lumi Section: " << lumiSection << SLogger::endmsg;
      // throw SError( SError::SkipEvent );
    }
    else m_logger << VERBOSE << "Good event! Run: " << runNumber <<  " - Lumi Section: " << lumiSection << SLogger::endmsg;
  }

  return isGood;
}


std::map<std::string, bool> VHAnalysis::getTriggerMap() {
    std::map<std::string, bool> map;
    for(std::map<std::string, std::vector<std::string> >::iterator it = m_triggerNames.begin(); it != m_triggerNames.end(); ++it) {
        bool pass(false);
        for(unsigned int i = 0; i < it->second.size(); i++) {
            // Iterate trigger map
            //if(!pass && (*m_eventInfo.trigDecision)[(it->second).at(i)]) pass = true;
            for(std::map<std::string,bool>::iterator tt = (m_eventInfo.trigDecision)->begin(); tt != (m_eventInfo.trigDecision)->end(); ++tt) {
                if((tt->first).find((it->second).at(i)) != std::string::npos && tt->second == true) {
                    m_logger << INFO << "Trigger pass: " << (tt->first) << SLogger::endmsg;
                    pass = true;
                    break;
                }
            }
            if(pass) break;
        }
        map[it->first] = pass;
    }
    return map;
}

bool VHAnalysis::passTrigger(std::string cat) {
  bool passTrigger = false;
  for(std::map<std::string,bool>::iterator it = (m_eventInfo.trigDecision)->begin(); it != (m_eventInfo.trigDecision)->end(); ++it) {
      for (unsigned int t = 0; t < m_triggerNames[cat].size(); ++t ){
          if ((it->first).find(m_triggerNames[cat][t]) != std::string::npos) {
              if (it->second == true) {
                  m_logger << INFO << "Trigger pass: " << (it->first) << SLogger::endmsg;
                  passTrigger = true;
                  return passTrigger;
              }
          }
      }
  }
  return passTrigger;
}


bool VHAnalysis::passMETFilters(bool data) {
    // using only what's recommended in https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
    if( !(m_eventInfo.PV_filter) ) return false;
    Hist( "METFilters", "MET" )->Fill(1);
    if( !(m_eventInfo.passFilter_CSCHalo) ) return false; // This should be enabled
    Hist( "METFilters", "MET" )->Fill(2);
    if( !(m_eventInfo.passFilter_HBHE) ) return false;
    Hist( "METFilters", "MET" )->Fill(3);
    if( !(m_eventInfo.passFilter_HBHEIso) ) return false;
    Hist( "METFilters", "MET" )->Fill(4);
    if( !(m_eventInfo.passFilter_ECALDeadCell) ) return false;
    Hist( "METFilters", "MET" )->Fill(5);
    if(data) if( !(m_eventInfo.passFilter_EEBadSc) ) return false;
    Hist( "METFilters", "MET" )->Fill(6);
    if( !(m_eventInfo.passFilter_globalTightHalo2016) ) return false;
    Hist( "METFilters", "MET" )->Fill(7);
    if( !(m_eventInfo.passFilter_muonBadTrack) ) return false;
    Hist( "METFilters", "MET" )->Fill(8);
    if( !(m_eventInfo.passFilter_chargedHadronTrackResolution) ) return false;       
    Hist( "METFilters", "MET" )->Fill(9);
    //  if( !(m_eventInfo.passFilter_METFilters) ) return false; // This should be enabled
    //   Hist( "METFilters" )->Fill(10);
    if(data) {
        if( (m_eventInfo.flag_badMuons) ) return false;
        Hist( "METFilters", "MET" )->Fill(10);
        if( (m_eventInfo.flag_duplicateMuons) ) return false;
        Hist( "METFilters", "MET" )->Fill(11);
        if( (m_eventInfo.flag_nobadMuons) ) return false; // This should be enabled
        Hist( "METFilters", "MET" )->Fill(12);
    }
    return true;
}


double VHAnalysis::getPUWeight() {
  
    double weight = 1.;
    for(unsigned int v = 0; v < (m_eventInfo.actualIntPerXing)->size(); ++v) {
        if ( (*m_eventInfo.bunchCrossing)[v] == 0 ) {
            weight = m_pileupReweightingTool.getPileUpweight( (*m_eventInfo.actualIntPerXing)[v] );
            m_logger << VERBOSE << "Weight: " << weight << " for true: " << (*m_eventInfo.actualIntPerXing)[v] << SLogger::endmsg;
            break;
        }
    }
    return weight;
}


//bool VHAnalysis::isTrackerHighPt(UZH::Muon mu) {
//    //if (! (mu.isMuon()) ) return false;
//    //if (! (mu.isTrackerMuon()) ) return false;
//    //if (! (mu.tunePMuonBestTrack().isNonnull()) ) return false;
//    if (! (mu.matchedStations() > 1) ) return false;
//    if (! (mu.trackerHits() > 5) ) return false;
//    if (! (mu.pixelHits() > 0) ) return false;
//    if (! (mu.bestTrack_ptErr()/mu.bestTrack_pt() < 0.3) ) return false;
//    if (! (fabs(mu.d0()) < 0.2) ) return false;
//    if (! (fabs(mu.dz()) < 0.5) ) return false;
//    return true;
//}


// Neutrino pz recovering by trading W mass

//float VHAnalysis::recoverNeutrinoPz(TLorentzVector lep, TLorentzVector met) {
//    // W kinematical reconstruction
//    float pz = 0.;
//    float a = pow(80.4,2) - pow(lep.M(),2) + 2.*lep.Px()*met.Px() + 2.*lep.Py()*met.Py();
//    float A = 4*( pow(lep.E(),2) - pow(lep.Pz(),2) );
//    float B = -4*a*lep.Pz();
//    float C = 4*pow(lep.E(),2) * (pow(met.Px(),2)  + pow(met.Py(),2)) - pow(a,2);
//    float D = pow(B,2) - 4*A*C;
//    // If there are real solutions, use the one with lowest pz                                            
//    if (D>=0) {
//        float s1 = (-B+sqrt(D))/(2*A);
//        float s2 = (-B-sqrt(D))/(2*A);
//        if(fabs(s1)<fabs(s2)) pz=s1;
//        else pz=s2;
//    }
//    // Otherwise, use real part                                                                           
//    else {
//        pz = -B/(2*A);
//    }
//    return pz;
//}





void VHAnalysis::fill4VectPlots(TLorentzVector obj, std::string name, std::string channel) {
    Hist((name+"_pt").c_str(), channel.c_str())->Fill(obj.Pt(), EventWeight);
    Hist((name+"_eta").c_str(), channel.c_str())->Fill(obj.Eta(), EventWeight);
    Hist((name+"_phi").c_str(), channel.c_str())->Fill(obj.Phi(), EventWeight);
    Hist((name+"_mass").c_str(), channel.c_str())->Fill(obj.M(), EventWeight);
}

void VHAnalysis::fillJetPlots(UZH::Jet obj, double mass, double tau21, std::string name, std::string channel) {
    float csv1 = obj.subjet_softdrop_N() >= 2 ? std::max(obj.subjet_softdrop_csv()[0], obj.subjet_softdrop_csv()[1]) : -99.;
    float csv2 = obj.subjet_softdrop_N() >= 2 ? std::min(obj.subjet_softdrop_csv()[0], obj.subjet_softdrop_csv()[1]) : -99.;
    float chsTau21 = obj.tau1() != 0. ? obj.tau2()/obj.tau1() : -1.;
    float puppiTau21 = tau21;//obj.jetAK8_puppi_tau1() != 0. ? obj.jetAK8_puppi_tau2()/obj.jetAK8_puppi_tau1() : -1.;
    float ddt = obj.softdrop_massCorr() != 0. ? puppiTau21 + 0.063 * log( obj.softdrop_massCorr()*obj.softdrop_massCorr()/obj.pt() ) : -1.;
    Hist((name+"_pt").c_str(), channel.c_str())->Fill(obj.pt(), EventWeight);
    Hist((name+"_eta").c_str(), channel.c_str())->Fill(obj.eta(), EventWeight);
    Hist((name+"_phi").c_str(), channel.c_str())->Fill(obj.phi(), EventWeight);
    Hist((name+"_mass").c_str(), channel.c_str())->Fill(obj.m(), EventWeight);
    Hist((name+"_chf").c_str(), channel.c_str())->Fill(obj.chf(), EventWeight);
    Hist((name+"_nhf").c_str(), channel.c_str())->Fill(obj.nhf(), EventWeight);
    Hist((name+"_phf").c_str(), channel.c_str())->Fill(obj.phf(), EventWeight);
    Hist((name+"_muf").c_str(), channel.c_str())->Fill(obj.muf(), EventWeight);
    Hist((name+"_emf").c_str(), channel.c_str())->Fill(obj.emf(), EventWeight);
    Hist((name+"_chm").c_str(), channel.c_str())->Fill(obj.chm(), EventWeight);
    Hist((name+"_prunedMass").c_str(), channel.c_str())->Fill(obj.pruned_mass(), EventWeight);
    Hist((name+"_prunedCorrMass").c_str(), channel.c_str())->Fill(obj.pruned_massCorr(), EventWeight);
    Hist((name+"_softdropMass").c_str(), channel.c_str())->Fill(obj.softdrop_mass(), EventWeight);
    Hist((name+"_softdropCorrMass").c_str(), channel.c_str())->Fill(mass, EventWeight);
    Hist((name+"_chsTau21").c_str(), channel.c_str())->Fill(chsTau21, EventWeight);
    Hist((name+"_puppiTau21").c_str(), channel.c_str())->Fill(puppiTau21, EventWeight);
    Hist((name+"_ddt").c_str(), channel.c_str())->Fill(ddt, EventWeight);
    Hist((name+"_csv1").c_str(), channel.c_str())->Fill(csv1, EventWeight);
    Hist((name+"_csv2").c_str(), channel.c_str())->Fill(csv2, EventWeight);
    Hist((name+"_dbt").c_str(), channel.c_str())->Fill(obj.Hbbtag(), EventWeight);
}

void VHAnalysis::fillMEtPlots(UZH::MissingEt obj, std::string channel) {
    Hist("MET_pt", channel.c_str())->Fill(obj.et(), EventWeight);
    Hist("MET_phi", channel.c_str())->Fill(obj.phi(), EventWeight);
}

void VHAnalysis::fillEventPlots(std::string channel) {
    Hist("EventWeight", channel.c_str())->Fill(EventWeight, 1.);
    Hist("GenWeight", channel.c_str())->Fill(ZewkWeight*WewkWeight, 1.);
    Hist("TopWeight", channel.c_str())->Fill(TopWeight, 1.);
    Hist("PUWeight", channel.c_str())->Fill(PUWeight, 1.);
    Hist("TriggerWeight", channel.c_str())->Fill(TriggerWeight, 1.);
    Hist("LeptonWeight", channel.c_str())->Fill(LeptonWeight, 1.);
    Hist("BTagWeight", channel.c_str())->Fill(BTagWeight, 1.);
    Hist("BBTagWeight", channel.c_str())->Fill(BBTagWeight, 1.);
    Hist("nPV", channel.c_str())->Fill(nPV, EventWeight);
    Hist("nElectrons", channel.c_str())->Fill(nElectrons, EventWeight);
    Hist("nMuons", channel.c_str())->Fill(nMuons, EventWeight);
    Hist("nTaus", channel.c_str())->Fill(nTaus, EventWeight);
    Hist("nPhotons", channel.c_str())->Fill(nPhotons, EventWeight);
    Hist("nJets", channel.c_str())->Fill(nJetsNoFatJet, EventWeight);
    Hist("nFatJets", channel.c_str())->Fill(nFatJets, EventWeight);
    Hist("nBTagJets", channel.c_str())->Fill(nBTagJets, EventWeight);
    Hist("nBVetoJets", channel.c_str())->Fill(nBVetoJets, EventWeight);
    Hist("JetMetDPhi", channel.c_str())->Fill(JetMetDPhi, EventWeight);
    Hist("MinJetMetDPhi", channel.c_str())->Fill(MinJetMetDPhi, EventWeight);
    Hist("MaxJetNoFatJetBTag", channel.c_str())->Fill(MaxJetNoFatJetBTag, EventWeight);
    Hist("ST", channel.c_str())->Fill(ST, EventWeight);
    Hist("HT", channel.c_str())->Fill(HT, EventWeight);
    Hist("MHT", channel.c_str())->Fill(MHT, EventWeight);
    Hist("Centrality", channel.c_str())->Fill(Centrality, EventWeight);
    Hist("CosThetaStar", channel.c_str())->Fill(CosThetaStar, EventWeight);
    Hist("CosTheta1", channel.c_str())->Fill(CosTheta1, EventWeight);
    Hist("CosTheta2", channel.c_str())->Fill(fabs(CosTheta2), EventWeight);
    Hist("Phi", channel.c_str())->Fill(Phi, EventWeight);
    Hist("Phi1", channel.c_str())->Fill(Phi1, EventWeight);
}

    
//void VHAnalysis::fillAnalysisPlots(std::string channel, bool AH) {
//    Hist("H_pt", channel.c_str())->Fill(H_pt, EventWeight);
//    Hist("H_mass", channel.c_str())->Fill(H_mass, EventWeight);
//    Hist("H_tau21", channel.c_str())->Fill(H_tau21, EventWeight);
//    Hist("H_csv1", channel.c_str())->Fill(H_csv1, EventWeight);
//    Hist("H_csv2", channel.c_str())->Fill(H_csv2, EventWeight);
//    Hist("H_dbt", channel.c_str())->Fill(H_dbt, EventWeight);
//    Hist("V_pt", channel.c_str())->Fill(V_pt, EventWeight);
//    Hist("V_mass", channel.c_str())->Fill(V_mass, EventWeight);
//    if(AH) {
//        Hist("V_tau21", channel.c_str())->Fill(V_tau21, EventWeight);
//        Hist("V_csv1", channel.c_str())->Fill(V_csv1, EventWeight);
//        Hist("V_csv2", channel.c_str())->Fill(V_csv2, EventWeight);
//        Hist("V_dbt", channel.c_str())->Fill(V_dbt, EventWeight);
//    }
//    Hist("X_mass", channel.c_str())->Fill(X_mass, EventWeight);
//}

//void VHAnalysis::fillTopControlPlots(std::string channel) {
//    Hist("H_pt", channel.c_str())->Fill(H_pt, EventWeight);
//    Hist("H_mass", channel.c_str())->Fill(H_mass, EventWeight);
//    Hist("H_tau21", channel.c_str())->Fill(H_tau21, EventWeight);
//    Hist("H_csv1", channel.c_str())->Fill(H_csv1, EventWeight);
//    Hist("H_csv2", channel.c_str())->Fill(H_csv2, EventWeight);
//    Hist("H_dbt", channel.c_str())->Fill(H_dbt, EventWeight);
//    Hist("V_pt", channel.c_str())->Fill(V_pt, EventWeight);
//    Hist("V_mass", channel.c_str())->Fill(V_mass, EventWeight);
//    Hist("X_mass", channel.c_str())->Fill(X_mass, EventWeight);
//    Hist("nJets", channel.c_str())->Fill(nJetsNoFatJet, EventWeight);
//    Hist("nBTagJets", channel.c_str())->Fill(nBTagJets, EventWeight);
//    Hist("nBVetoJets", channel.c_str())->Fill(nBVetoJets, EventWeight);
//    Hist("MaxJetNoFatJetBTag", channel.c_str())->Fill(MaxJetNoFatJetBTag, EventWeight);
//}

//void VHAnalysis::fillElectronPlots(UZH::Electron* r1, UZH::Electron* r2, TLorentzVector& g1, TLorentzVector& g2) {
//    if(r1->tlv().Pt()<=0. || r2->tlv().Pt()<=0. || g1.Pt()<=0. || g2.Pt()<=0.) return;
//    float dRll = g1.DeltaR(g2);
//    float pTll = (g1+g2).Pt();
//    // Match both reco and gen leptons
//    if(r1->tlv().DeltaR(g1) > 0.1 || r1->tlv().DeltaR(g2) > 0.1) return;
//    if(r2->tlv().DeltaR(g1) > 0.1 || r2->tlv().DeltaR(g2) > 0.1) return;
//    
//    Hist("dR", "Leptons")->Fill(dRll);
//    Hist("pT", "Leptons")->Fill(pTll);
//    
//    if(r1->isVetoElectron()==1 && r2->isVetoElectron()==1) {
//        Hist("dR_HighptHighptId", "Leptons")->Fill(dRll);
//        Hist("pT_HighptHighptId", "Leptons")->Fill(pTll);
//    }
//    if(r1->isLooseElectron()==1 && r2->isLooseElectron()==1) {
//        Hist("dR_LooseLooseId", "Leptons")->Fill(dRll);
//        Hist("pT_LooseLooseId", "Leptons")->Fill(pTll);
//    }
//    if(r1->isMediumElectron()==1 && r2->isMediumElectron()==1) {
//        Hist("dR_MediumMediumId", "Leptons")->Fill(dRll);
//        Hist("pT_MediumMediumId", "Leptons")->Fill(pTll);
//    }
//    if(r1->isTightElectron()==1 && r2->isTightElectron()==1) {
//        Hist("dR_TightTightId", "Leptons")->Fill(dRll);
//        Hist("pT_TightTightId", "Leptons")->Fill(pTll);
//    }
//    if(r1->isHeepElectron()==1 && r2->isHeepElectron()==1) {
//        Hist("dR_HeepHeepId", "Leptons")->Fill(dRll);
//        Hist("pT_HeepHeepId", "Leptons")->Fill(pTll);
//    }
//}

//void VHAnalysis::fillMuonPlots(UZH::Muon& r1, UZH::Muon& r2, TLorentzVector& g1, TLorentzVector& g2) {
//    if(r1.tlv().Pt()<=0. || r2.tlv().Pt()<=0. || g1.Pt()<=0. || g2.Pt()<=0.) return;
//    float dRll = g1.DeltaR(g2);
//    float pTll = (g1+g2).Pt();
//    // Match both reco and gen leptons
//    if(r1.tlv().DeltaR(g1) > 0.1 || r1.tlv().DeltaR(g2) > 0.1) return;
//    if(r2.tlv().DeltaR(g1) > 0.1 || r2.tlv().DeltaR(g2) > 0.1) return;
//    
//    Hist("dR", "Leptons")->Fill(dRll);
//    Hist("pT", "Leptons")->Fill(pTll);
//    
//    if(r1.isHighPtMuon()==1 && r2.isHighPtMuon()==1) {Hist("dR_HighptHighptId", "Leptons")->Fill(dRll); Hist("pT_HighptHighptId", "Leptons")->Fill(pTll);}
//    if(r1.isLooseMuon()==1 && r2.isLooseMuon()==1) {Hist("dR_LooseLooseId", "Leptons")->Fill(dRll); Hist("pT_LooseLooseId", "Leptons")->Fill(pTll);}
//    if(r1.isMediumMuon()==1 && r2.isMediumMuon()==1) {Hist("dR_MediumMediumId", "Leptons")->Fill(dRll); Hist("pT_MediumMediumId", "Leptons")->Fill(pTll);}
//    if(r1.isTightMuon()==1 && r2.isTightMuon()==1) {Hist("dR_TightTightId", "Leptons")->Fill(dRll); Hist("pT_TightTightId", "Leptons")->Fill(pTll);}
//    
//    if((r1.isHighPtMuon()==1 && r2.isTrackerHighPtMuon()) || (r2.isHighPtMuon()==1 && r1.isTrackerHighPtMuon())) {
//        Hist("dR_HighptTrackerId", "Leptons")->Fill(dRll); Hist("pT_HighptTrackerId", "Leptons")->Fill(pTll);
//                           
//        if(trackIso1 < 0.1 && trackIso2 < 0.1) {
//            Hist("dR_HighptTrackerIdTrackerIso", "Leptons")->Fill(dRll);
//            Hist("pT_HighptTrackerIdTrackerIso", "Leptons")->Fill(pTll);
//        }
//        if(r1.pfDeltaCorrRelIso() < 0.20 && r2.pfDeltaCorrRelIso() < 0.20) {
//            Hist("dR_HighptTrackerIdPFIso", "Leptons")->Fill(dRll);
//            Hist("pT_HighptTrackerIdPFIso", "Leptons")->Fill(pTll);
//        }
//    }
//}

//bool VHAnalysis::electronId(UZH::Electron* e, int id) {
//    if(id < 0 || id >= 4) return false;
//    
//    if(id == 0) return (e->isVetoElectron()==1);
//    if(id == 1) return (e->isLooseElectron()==1);
//    if(id == 2) return (e->isMediumElectron()==1);
//    if(id == 3) return (e->isTightElectron()==1);
//    
//    // 0: Veto, 1: Loose, 2: Medium, 3: Tight
//    float b_full5x5_sigmaIetaIeta[4] = {0.0115, 0.011, 0.00998, 0.00998};
//    float b_dEtaInSeed[4] = {0.00749, 0.00477, 0.00311, 0.00308};
//    float b_dPhiIn[4] = {0.228, 0.222, 0.103, 0.0816};
//    float b_hOverE[4] = {0.356, 0.298, 0.253, 0.0414};
//    float b_pfRhoCorrRelIso03[4] = {0.175, 0.0994, 0.0695, 0.0588};
//    float b_ooEmooP[4] = {0.299, 0.241, 0.134, 0.0129};
//    int b_expectedMissingInnerHits[4] = {2, 1, 1, 1};
//    bool b_passConversionVeto[4] = {true, true, true, true};

//    float e_full5x5_sigmaIetaIeta[4] = {0.037, 0.0314, 0.0298, 0.0292};
//    float e_dEtaInSeed[4] = {0.00895, 0.00868, 0.00609, 0.00605};
//    float e_dPhiIn[4] = {0.213, 0.213, 0.045, 0.0394};
//    float e_hOverE[4] = {0.211, 0.101, 0.0878, 0.0641};
//    float e_pfRhoCorrRelIso03[4] = {0.159, 0.107, 0.0821 , 0.0571};
//    float e_ooEmooP[4] = {0.15, 0.14, 0.13, 0.0129};
//    int e_expectedMissingInnerHits[4] = {3, 1, 1, 1};
//    bool e_passConversionVeto[4] = {true, true, true, true};

//    bool pass = true;
//    if(fabs(e->superCluster_eta() <= 1.479)) {
//        if(e->full5x5_sigmaIetaIeta() >= b_full5x5_sigmaIetaIeta[id]) pass = false;
//        if(fabs(e->dEtaInSeed()) >= b_dEtaInSeed[id]) pass = false;
//        if(fabs(e->dPhiIn()) >= b_dPhiIn[id]) pass = false;
//        if(e->hOverE() >= b_hOverE[id]) pass = false;
//        if(e->relIsoWithDBeta() >= b_pfRhoCorrRelIso03[id]) pass = false;
//        if(fabs(e->ooEmooP()) >= b_ooEmooP[id]) pass = false;
//        if(e->expectedMissingInnerHits() > b_expectedMissingInnerHits[id]) pass = false;
//        if(!e->passConversionVeto()) pass = false;
//    }
//    else {
//        if(e->full5x5_sigmaIetaIeta() >= e_full5x5_sigmaIetaIeta[id]) pass = false;
//        if(fabs(e->dEtaInSeed()) >= e_dEtaInSeed[id]) pass = false;
//        if(fabs(e->dPhiIn()) >= e_dPhiIn[id]) pass = false;
//        if(e->hOverE() >= e_hOverE[id]) pass = false;
//        if(e->relIsoWithDBeta() >= e_pfRhoCorrRelIso03[id]) pass = false;
//        if(fabs(e->ooEmooP()) >= e_ooEmooP[id]) pass = false;
//        if(e->expectedMissingInnerHits() > e_expectedMissingInnerHits[id]) pass = false;
//        if(!e->passConversionVeto()) pass = false;
//    }
//    return pass;
//}


void VHAnalysis::clearBranches() {
    EventWeight = GenWeight = StitchWeight = ZewkWeight = WewkWeight = TopWeight = PUWeight = PUWeightUp = PUWeightDown = TriggerWeight = TriggerWeightUp = TriggerWeightDown = LeptonWeight = LeptonWeightUp = LeptonWeightDown = 1.;
    BTagWeight = BTagWeightUp = BTagWeightDown = BTagAK4Weight = BTagAK4WeightUp = BTagAK4WeightDown = BTagAK8Weight = BTagAK8WeightUp = BTagAK8WeightDown = BBTagWeight = BBTagWeightUp = BBTagWeightDown = 1.;
    isZtoEE = isZtoMM = isWtoEN = isWtoMN = isZtoNN = isVtoQQ = isTtoEM = isTveto = false;
    isBoostedTau = isBoosted4B = false;
    nPV = nElectrons = nMuons = nTaus = nPhotons = nJets = nJetsNoFatJet = nFatJets = nBTagJets = nBVetoJets = LheNl = LheNj = 0;
    HT = HTx = HTy = MHT = MHTNoMu = METNoMu = MinMETMHT = MinMETNoMuMHTNoMu = MaxMETNoMuMHTNoMu = ST = V_tmass = X_tmass = 0.;
    Centrality = CosThetaStar = CosTheta1 = CosTheta2 = Phi = Phi1 = -9.;
    VHDEta = JetMetDPhi = MaxJetBTag = MaxJetNoFatJetBTag = -1.;
    MinJetMetDPhi = 10.;
    
    X = V = H = TLorentzVector();
    H_mass = H_tau21 = H_ddt = H_csv1 = H_csv2 = H_flav1 = H_flav2 = H_dbt = H_ntag = -1.;
    H_ptB = H_chf = H_nhf = H_phf = H_chm = -1.;
    V_mass = V_tau21 = V_ddt = V_csv1 = V_csv2 = V_dbt = V_ntag = -1.;
    X_mass = -1.;
}
