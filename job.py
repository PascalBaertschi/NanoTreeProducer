#! /usr/bin/env python
import os,sys
import PhysicsTools
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from argparse import ArgumentParser
from checkFiles import ensureDirectory

infiles = "root://cms-xrd-global.cern.ch//store/user/arizzi/Nano01Fall17/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X-Nano01Fall17/180205_160029/0000/test94X_NANO_70.root"

parser = ArgumentParser()
parser.add_argument('-i', '--infiles', dest='infiles', action='store', type=str, default=infiles)
parser.add_argument('-o', '--outdir',  dest='outdir', action='store', type=str, default="outdir")
parser.add_argument('-N', '--outfile', dest='outfile', action='store', type=str, default="noname")
parser.add_argument('-n', '--nchunck', dest='nchunck', action='store', type=int, default='test')
parser.add_argument('-c', '--channel', dest='channel', action='store', choices=['ll'], type=str, default='ll')
parser.add_argument('-t', '--type',    dest='type', action='store', choices=['data','mc'], default='mc')
parser.add_argument('-y', '--year',    dest='year', action='store', choices=[2016,2017,2018], type=int, default=2017)
parser.add_argument('-T', '--tes',     dest='tes', action='store', type=float, default=1.0)
parser.add_argument('-L', '--ltf',     dest='ltf', action='store', type=float, default=1.0)
parser.add_argument('-J', '--jtf',     dest='jtf', action='store', type=float, default=1.0)
args = parser.parse_args()

channel  = args.channel
dataType = args.type
infiles  = args.infiles
outdir   = args.outdir
outfile  = args.outfile
nchunck  = args.nchunck
year     = args.year
tes      = args.tes
ltf      = args.ltf
jtf      = args.jtf
kwargs   = {
  'year':  year,
  'tes':   tes,
  'ltf':   ltf,
  'jtf':   jtf,
}

if isinstance(infiles,str):
  infiles = infiles.split(',')

ensureDirectory(outdir)

dataType = 'mc'
runJEC = False
if infiles[0].find("/SingleMuon/")>0 or infiles[0].find("/MET/")>0 or infiles[0].find("/EGamma/")>0 or infiles[0].find("/SingleElectron/")>0:
  dataType = 'data'
runJEC = False
JEC_samples = ['Zprime','WWTo','WZTo','ZZTo','GluGluHToBB','ZH_HToBB','Wplus','Wminus']
for JEC_sample in JEC_samples:
    if infiles[0].find(JEC_sample)>0:
        runJEC = True              

JSON = '/work/pbaertsc/heavy_resonance/NanoTreeProducer/json/'
if year==2016:
  json = JSON+'Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'
  #json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Final/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'
elif year==2017:
  json = JSON+'Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
  #json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
else:
  json = JSON+'Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
  #json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'


##Function parameters
##isMC=True, dataYear=2016, runPeriod="B", jesUncert="Total", redojec=False, jetType = "AK8PFPuppi", noGroom=False, metBranchName="PuppiMET", applySmearing=True, isFastSim=False)
##All other parameters will be set in the helper module

#jmeCorrections only needed for MC
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
tag = ""
if tes!=1: tag +="_TES%.3f"%(tes)
if ltf!=1: tag +="_LTF%.3f"%(ltf)
if jtf!=1: tag +="_JTF%.3f"%(jtf)
outfile = "%s_%s_%s%s.root"%(outfile,nchunck,channel,tag.replace('.','p'))
postfix = "%s/%s"%(outdir,outfile)



print '-'*80
print "%-12s = %s"%('input files',infiles)
print "%-12s = %s"%('output directory',outdir)
print "%-12s = %s"%('output file',outfile)
print "%-12s = %s"%('chunck',nchunck)
print "%-12s = %s"%('channel',channel)
print "%-12s = %s"%('dataType',dataType)
print "%-12s = %s"%('year',kwargs['year'])
print "%-12s = %s"%('tes',kwargs['tes'])
print "%-12s = %s"%('ltf',kwargs['ltf'])
print "%-12s = %s"%('jtf',kwargs['jtf'])
print '-'*80


from LLModule import *
prefirecorr = lambda : PrefCorr(**kwargs)
module2run = lambda : LLProducer(postfix, dataType, infiles, **kwargs)
branchsel = "keep_and_drop.txt"

print "job.py: creating PostProcessor..."

if dataType=='data':
    p = PostProcessor(outdir, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False, 
                      modules=[module2run()], provenance=False, fwkJobReport=False, jsonInput=json, postfix=postfix)
else:
  if runJEC:
    p = PostProcessor(outdir, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False,
                      modules=[prefirecorr(),METCorrections(),jmeCorrections(),module2run()], provenance=False, fwkJobReport=False, postfix=postfix)
  else:
    p = PostProcessor(outdir, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False,
                      modules=[prefirecorr(),module2run()], provenance=False, fwkJobReport=False, postfix=postfix)

print "job.py: going to run PostProcessor..."
p.run()
outFileName = os.path.join(outdir, os.path.basename(infiles[0]))
print "deleting root file with name:",outFileName
os.remove(outFileName)
print "DONE"
