#! /usr/bin/env python
import os,sys
import PhysicsTools
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
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
if infiles[0].find("/SingleMuon/")>0 or infiles[0].find("/MET/")>0 or infiles[0].find("/EGamma/")>0 or infiles[0].find("/SingleElectron/")>0:
  dataType = 'data'


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
##(isMC=True, dataYear=2016, runPeriod="B", jesUncert="Total", redojec=False, jetType = "AK4PFchs", noGroom=False)
##All other parameters will be set in the helper module

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
module2run = lambda : LLProducer(postfix, dataType, infiles, **kwargs)
branchsel = "keep_and_drop.txt"

print "job.py: creating PostProcessor..."
if dataType=='data':
    p = PostProcessor(outdir, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False, 
                      modules=[jmeCorrections()], provenance=False, fwkJobReport=False, jsonInput=json, postfix=postfix)
else:
    p = PostProcessor(outdir, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False,
                      modules=[jmeCorrections()], provenance=False, fwkJobReport=False, postfix=postfix)


"""
if dataType=='data':
    p = PostProcessor(outdir, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False, 
                      modules=[jmeCorrections(),module2run()], provenance=False, fwkJobReport=False, jsonInput=json, postfix=postfix)
else:
    p = PostProcessor(outdir, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False,
                      modules=[jmeCorrections(),module2run()], provenance=False, fwkJobReport=False, postfix=postfix)
"""
print "job.py: going to run PostProcessor..."
p.run()
print "DONE"
