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
        filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2016D/SingleElectron/NANOAOD/Nano25Oct2019-v1/230000/29599D08-17B1-BE45-B79E-F63231B2798C.root']
    else:
        filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/70000/67321EE2-1E3D-2742-89CB-9297DC52E08E.root']
elif year == 2017:
    if dataType=='data':
        filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2017B/SingleElectron/NANOAOD/Nano25Oct2019-v1/40000/5A24C552-3BDC-1F40-B228-B5611C84BF43.root']
    else:
        filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv6/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano25Oct2019_new_pmx_102X_mc2017_realistic_v7-v1/260000/A4CFCF54-FBA1-0A48-A7EB-2C7741B5DF89.root']
elif year == 2018:
    if dataType=='data':
        filelist = ['root://cms-xrd-global.cern.ch//store/data/Run2018C/EGamma/NANOAOD/Nano25Oct2019-v1/20000/B1C4EFA6-428F-A04D-B149-A87EA04DCFFC.root']
    else:
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv6/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/40000/DDBEFDC2-E869-0C4A-A77C-B1106B296BAD.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv6/ZprimeToZHToZlepHinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/60000/AD0F3979-DDD0-0345-862D-92C494659EFB.root']
        #filelist= ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv6/Zprime_VBF_Zh_Zlephinc_narrow_M-5000_TuneCP5_PSweights_13TeV-madgraph-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/260000/951BB07C-D78D-1646-B801-41077D41576D.root']
        filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv6/Zprime_VBF_Zh_Zinvhinc_narrow_M-4000_TuneCP5_PSweights_13TeV-madgraph-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/250000/22A83B95-7594-CE4D-9C3A-080CA7DC9582.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv6/Zprime_VBF_Zh_Zinvhinc_narrow_M-5000_TuneCP5_PSweights_13TeV-madgraph-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/40000/371BD07A-A77D-7743-B316-AB4115F0D6B5.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv6/ZprimeToZHToZinvHinc_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/60000/82E99F60-EBEE-D043-9A43-978467AEEAAE.root']
        #filelist = ['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv6/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/30000/5FC5CB27-600B-EF4F-927F-5E9517208937.root']
infiles = filelist

runJEC = False
JEC_samples = ['Zprime','WWTo','WZTo','ZZTo','GluGluHToBB','ZH_HToBB','Wplus','Wminus']
for JEC_sample in JEC_samples:
    if infiles[0].find(JEC_sample)>0:
        runJEC = True

if runJEC:
    if year==2016:
        jmeCorrections = createJMECorrector(True, "2016", "B", "Total", False, "AK8PFPuppi", False,'PuppiMET', True, False)
        METCorrections = createJMECorrector(True, "2016", "B", "Total", False, "AK4PFchs", False,'PuppiMET', True, False)
    elif year==2017:
        jmeCorrections = createJMECorrector(True, "2017", "B", "Total", False, "AK8PFPuppi", False,'PuppiMET', True, False)
        METCorrections = createJMECorrector(True, "2017", "B", "Total", False, "AK4PFchs", False,'PuppiMET', True, False)
    else:
        jmeCorrections = createJMECorrector(True, "2018", "B", "Total", False, "AK8PFPuppi", False,'PuppiMET', True, False)
        METCorrections = createJMECorrector(True, "2018", "B", "Total", False, "AK4PFchs", False,'PuppiMET', True, False)
"""
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
"""        
branchsel = "keep_and_drop.txt"

_postfix = channel + '.root'
from LLModule import *
prefirecorr = lambda : PrefCorr(**kwargs)
module2run = lambda : LLProducer(_postfix, dataType, filelist, **kwargs)

if dataType == 'data':
    p=PostProcessor(".",filelist,None,"keep_and_drop.txt",noOut=True, modules=[module2run()],provenance=False, postfix=_postfix)
else:
    if runJEC:
        p=PostProcessor(".",filelist,None,branchsel,outputbranchsel=branchsel,noOut=False, modules=[prefirecorr(),METCorrections(),jmeCorrections(),module2run()],provenance=False, postfix=_postfix)
    else:
        p=PostProcessor(".",filelist,None,branchsel,outputbranchsel=branchsel,noOut=False, modules=[prefirecorr(),module2run()],provenance=False, postfix=_postfix)
#p=PostProcessor(".",filelist,None,branchsel,outputbranchsel=branchsel,noOut=False, modules=[jmeCorrections()],provenance=False, postfix=_postfix)
#p=PostProcessor(".",filelist,None,branchsel,outputbranchsel=branchsel,noOut=False, modules=[jmeCorrections(),module2run()],provenance=False, postfix=_postfix)
#p=PostProcessor(".",filelist,None,"keep_and_drop.txt",noOut=True, modules=[module2run()],provenance=False, postfix=_postfix)

p.run()
outFileName = os.path.join('.', os.path.basename(filelist[0]))
print "deleting root file with name::",outFileName
os.remove(outFileName)
