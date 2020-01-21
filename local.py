#!/usr/bin/env python
import os, sys
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from argparse import ArgumentParser




parser = ArgumentParser()
parser.add_argument('-i', '--infiles',  dest='infiles', action='store', type=str, default=[ ])
parser.add_argument('-c', '--channel',  dest='channel', action='store', choices=['ll'], type=str, default='ll')
parser.add_argument('-t', '--type', dest='type', action='store', choices=['data','mc'], default='mc')
parser.add_argument('-y', '--year',     dest='year', action='store', choices=[2016,2017,2018], type=int, default=2017)
parser.add_argument('-T', '--tes',      dest='tes', action='store', type=float, default=1.0)
parser.add_argument('-L', '--ltf',      dest='ltf', action='store', type=float, default=1.0)
parser.add_argument('-J', '--jtf',      dest='jtf', action='store', type=float, default=1.0)
parser.add_argument('-l', '--tag',      dest='tag', action='store', type=str, default="")
parser.add_argument('-M', '--Zmass',    dest='Zmass', action='store_true', default=False)
parser.add_argument('-Z', '--doZpt',    dest='doZpt', action='store_true', default=False)
parser.add_argument('-R', '--doRecoil', dest='doRecoil', action='store_true', default=False)
args = parser.parse_args()

channel  = args.channel
year     = args.year
dataType = args.type
infiles  = args.infiles
if args.tag and args.tag[0]!='_': args.tag = '_'+args.tag
postfix  = channel + args.tag + '.root'
kwargs = {
  'year':        args.year,
  'tes':         args.tes,
  'ltf':         args.ltf,
  'jtf':         args.jtf,
  'doZpt':       args.doZpt,
  'doRecoil':    args.doRecoil,
  'ZmassWindow': args.Zmass,
}

print 'channel = ', channel 
print 'DataType = ', dataType
print 'year =', year

if year == 2016:
    if dataType =='data':
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2016B_ver1/SingleElectron/NANOAOD/Nano14Dec2018_ver1-v1/00000/ECD4BD44-5DA0-5940-A5F1-120C84703015.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2016E/SingleMuon/NANOAOD/Nano14Dec2018-v1/10000/DBA5D8C5-88CF-0E4B-935C-3B6541E9E78F.root']
        filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2016H/SingleElectron/NANOAOD/Nano1June2019-v1/230000/C92894D5-6C1D-0C4D-960D-2F8C321FD196.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2016B_ver2/SingleElectron/NANOAOD/Nano14Dec2018_ver2-v1/90000/3059FDE1-E6AA-7347-885A-C7C779DC0E96.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2016C/SingleElectron/NANOAOD/Nano14Dec2018-v1/90000/F8AFD313-9D2F-BD48-ABB0-4752263F84DD.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2016D/SingleElectron/NANOAOD/Nano14Dec2018-v1/80000/E4B29A0D-745D-0943-A69E-D31BFD1BE8B3.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2016E/SingleElectron/NANOAOD/Nano14Dec2018-v1/90000/D5DEB1E5-EE3B-F14D-BA5B-0BA2EB8E1801.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2016F/SingleElectron/NANOAOD/Nano14Dec2018-v1/90000/F81BDE36-4450-B148-B8A9-60CC5153C833.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleElectron/NANOAOD/Nano14Dec2018-v1/90000/F32C15E1-D3DD-AC42-BD3C-9A0007FD2A67.root']
    else:
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv4/DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/10000/3A4FF9EE-E857-2046-AFB7-B5AF9077D05F.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv5/ZprimeToZHToZlepHinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/60000/DBA0A893-3DB3-694C-8099-4A674AD7F9CD.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv4/ZprimeToZHToZlepHinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/240000/E5DE8942-9764-CB45-A789-DE31C08A088E.root']
        filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv5/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/120000/982B3BA2-8A09-634B-9783-33405B63DCE4.root']
elif year == 2017:
    if dataType=='data':
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2017B/SingleElectron/NANOAOD/Nano14Dec2018-v1/20000/E2655AFE-F9D0-4C4C-9AB4-59A7EB0DB2DE.root']
        filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2017D/SingleElectron/NANOAOD/Nano14Dec2018-v1/90000/BFEB5394-B117-C542-8B2A-5BB3D538F377.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2017C/SingleElectron/NANOAOD/Nano14Dec2018-v1/90000/E2B1106E-2614-3443-8516-A651A11C0DB2.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2017B/SingleMuon/NANOAOD/Nano14Dec2018-v1/90000/E314FF75-8F19-584B-816D-21CE9919404D.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2017B/SingleElectron/NANOAOD/Nano14Dec2018-v1/20000/F00367C2-7DFC-324D-9073-52E63BF71D17.root'] 
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2017B/MET/NANOAOD/Nano14Dec2018-v1/90000/F241B51F-2BDF-4746-8F1C-39926B62C475.root ']
    else:
       
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv5/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/120000/F2F32C49-5C0A-9C4D-B5EA-EB1BF0E5019B.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv5/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/120000/F165FB04-4B4C-9B46-8AA1-7339B2562E31.root']
        filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv5/DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/70000/9E4E6640-454C-BA4F-9935-A6F25F7F7196.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv5/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/120000/877814AF-F719-FC41-A8E1-623CE132A9FC.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv5/ZprimeToZHToZlepHinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/30000/A59F4C3C-F22F-D34F-92EC-810A04D2BA2F.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv5/Zprime_VBF_Zh_Zlephinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/130000/016BEE0C-E8A6-3D40-9CE4-3ED3A30A50B2.root']
elif year == 2018:
    if dataType=='data':
        #filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2018C/SingleMuon/NANOAOD/Nano1June2019-v1/70000/F407D383-C7CF-8E46-A96E-F185F0B4B02B.root']
        filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2018D/EGamma/NANOAOD/Nano1June2019-v1/70000/A6B15DFB-3811-7548-9F9B-9A24E1E166A9.root']

    else:
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19_ext2-v1/30000/71FF2B21-1E74-A042-96B1-ADD9C893A7EC.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/70000/E05CFEAA-4C50-2C4F-AA16-44E3B6A84497.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/40000/60D2AE62-81E7-394F-B914-6DD3A36707F9.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/ZprimeToZHToZinvHinc_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/40000/959E9F2E-F0F0-7A43-A171-0A76C4DB32A4.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/ZprimeToZHToZlepHinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/30000/778D9451-68A0-B34E-9DA1-A89ACC493700.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/120000/374B3F6D-4709-4B41-8569-ACA5D52B3AF2.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19_ext2-v1/70000/4EC34AED-3943-F648-A5F9-E4CE88F50022.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/60000/92B220DA-666E-F540-8A31-7961924CA012.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/ZJetsToNuNu_HT-400To600_13TeV-madgraph/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/70000/AE272F4A-95D7-5143-8714-B09200737210.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/100000/5F83B0DA-C779-3142-83CF-7012B26914D3.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/120000/55B8AFA5-DF0C-E24D-AD50-6841A5849614.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/40000/466CDA79-5B19-F243-BF40-9AC3C4B7FF95.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv6/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/40000/99374796-7910-1348-90F9-9A7AF54577F3.root']
        filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv6/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/40000/DDBEFDC2-E869-0C4A-A77C-B1106B296BAD.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/40000/0035C82F-5EF0-F843-8562-F191062F5D8A.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/120000/374B3F6D-4709-4B41-8569-ACA5D52B3AF2.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/60000/6D6AAD11-A18C-3B40-AC99-BC18FCF25969.root']
infiles = filelist
if year==2016:
  if dataType=='mc':      
    jmeCorrections = createJMECorrector(True, "2016", "B", "Total", False, "AK8PFPuppi", False)
  else:
      if infiles[0].find("2016B")>0:
        jmeCorrections = createJMECorrector(False, "2016", "B", "Total", False, "AK8PFPuppi", False)
      elif infiles[0].find("2016C")>0:
        jmeCorrections = createJMECorrector(False, "2016", "C", "Total", False, "AK8PFPuppi", False)
      elif infiles[0].find("2016D")>0:
        jmeCorrections = createJMECorrector(False, "2016", "D", "Total", False, "AK8PFPuppi", False)
      elif infiles[0].find("2016E")>0:
        jmeCorrections = createJMECorrector(False, "2016", "E", "Total", False, "AK8PFPuppi", False)
      elif infiles[0].find("2016F")>0:
        jmeCorrections = createJMECorrector(False, "2016", "F", "Total", False, "AK8PFPuppi", False)
      elif infiles[0].find("2016G")>0:
        jmeCorrections = createJMECorrector(False, "2016", "G", "Total", False, "AK8PFPuppi", False)
      elif infiles[0].find("2016H")>0:
        jmeCorrections = createJMECorrector(False, "2016", "H", "Total", False, "AK8PFPuppi", False)
elif year==2017:
  if dataType=='mc':
    jmeCorrections = createJMECorrector(True, "2017", "B", "Total", False, "AK8PFPuppi", False)
  else:
    if infiles[0].find("2017B")>0:
        jmeCorrections = createJMECorrector(False, "2017", "B", "Total", False, "AK8PFPuppi", False)
    elif infiles[0].find("2017C")>0:
        jmeCorrections = createJMECorrector(False, "2017", "C", "Total", False, "AK8PFPuppi", False)
    elif infiles[0].find("2017D")>0:
        jmeCorrections = createJMECorrector(False, "2017", "D", "Total", False, "AK8PFPuppi", False)
    elif infiles[0].find("2017E")>0:
        jmeCorrections = createJMECorrector(False, "2017", "E", "Total", False, "AK8PFPuppi", False)
    elif infiles[0].find("2017F")>0:
        jmeCorrections = createJMECorrector(False, "2017", "F", "Total", False, "AK8PFPuppi", False)
else:
  if dataType=='mc':
    jmeCorrections = createJMECorrector(True, "2018", "B", "Total", False, "AK8PFPuppi", False)
  else:
    if infiles[0].find("2018A")>0:
        jmeCorrections = createJMECorrector(False, "2018", "A", "Total", False, "AK8PFPuppi", False)
    elif infiles[0].find("2018B")>0:
        jmeCorrections = createJMECorrector(False, "2018", "B", "Total", False, "AK8PFPuppi", False)
    elif infiles[0].find("2018C")>0:
        jmeCorrections = createJMECorrector(False, "2018", "C", "Total", False, "AK8PFPuppi", False)
    elif infiles[0].find("2018D")>0:
        jmeCorrections = createJMECorrector(False, "2018", "D", "Total", False, "AK8PFPuppi", False)
        
branchsel = "keep_and_drop.txt"

_postfix = channel + '.root'
from LLModule import *
prefirecorr = lambda : PrefCorr(**kwargs)
module2run = lambda : LLProducer(_postfix, dataType, filelist, **kwargs)

p=PostProcessor(".",filelist,None,branchsel,outputbranchsel=branchsel,noOut=False, modules=[prefirecorr(),jmeCorrections(),module2run()],provenance=False, postfix=_postfix)
#p=PostProcessor(".",filelist,None,branchsel,outputbranchsel=branchsel,noOut=False, modules=[jmeCorrections()],provenance=False, postfix=_postfix)
#p=PostProcessor(".",filelist,None,branchsel,outputbranchsel=branchsel,noOut=False, modules=[jmeCorrections(),module2run()],provenance=False, postfix=_postfix)
#p=PostProcessor(".",filelist,None,"keep_and_drop.txt",noOut=True, modules=[module2run()],provenance=False, postfix=_postfix)

p.run()
outFileName = os.path.join('.', os.path.basename(filelist[0]))
print "deleting root file with name::",outFileName
os.remove(outFileName)
