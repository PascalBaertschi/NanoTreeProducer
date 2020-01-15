#! /usr/bin/env python

import os, glob, sys, shlex, re
#import time
from fnmatch import fnmatch
import subprocess
from argparse import ArgumentParser
import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TFile, TTree, TH1, Double

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == '__main__':
    description = '''Check if the job output files are valid, compare the number of events to DAS (-d), hadd them into one file per sample (-m), and merge datasets (-a).'''
    parser = ArgumentParser(prog="checkFiles",description=description,epilog="Good luck!")
    parser.add_argument('-y', '--year',     dest='years', choices=[2016,2017,2018], type=int, nargs='+', default=[2017], action='store',
                                            help="select year" )
    parser.add_argument('-c', '--channel',  dest='channels', choices=['ll'], nargs='+', default=['ll'], action='store' )
    parser.add_argument('-m', '--make',     dest='make', default=False, action='store_true',
                                            help="hadd all output files" )
    parser.add_argument('-a', '--hadd',     dest='haddother', default=False, action='store_true',
                                            help="hadd some samples into one (e.g. all data sets, or the extensions)" )
    parser.add_argument('-d', '--das',      dest='compareToDas', default=False, action='store_true',
                                            help="compare number of events in output to das" )
    parser.add_argument('-D', '--das-ex',   dest='compareToDasExisting', default=False, action='store_true',
                                            help="compare number of events in existing output to das" )
    parser.add_argument('-C', '--check-ex', dest='checkExisting', default=False, action='store_true',
                                            help="check existing output (e.g. 'LHE_Njets')" )
    parser.add_argument('-f', '--force',    dest='force', default=False, action='store_true',
                                            help="overwrite existing hadd'ed files" )
    parser.add_argument('-r', '--clean',    dest='cleanup', default=False, action='store_true',
                                            help="remove all output files after hadd" )
    parser.add_argument('-R', '--rm-bad',   dest='removeBadFiles', default=False, action='store_true',
                                            help="remove files that are bad" )
    parser.add_argument('-o', '--outdir',   dest='outdir', type=str, default=None, action='store' )
    parser.add_argument('-s', '--sample',   dest='samples', type=str, nargs='+', default=[ ], action='store',
                                            help="samples to run over, glob patterns (wildcards * and ?) are allowed." )
    parser.add_argument('-x', '--veto',     dest='veto', action='store', type=str, default=None,
                                            help="veto this sample" )
    parser.add_argument('-t', '--type',     dest='type', choices=['data','mc'], type=str, default=None, action='store',
                                            help="filter data or MC to submit" )
    parser.add_argument('-T', '--tes',      dest='tes', type=float, default=1.0, action='store',
                                            help="tau energy scale" )
    parser.add_argument('-L', '--ltf',      dest='ltf', type=float, default=1.0, action='store',
                                            help="lepton to tau fake energy scale" )
    parser.add_argument('-J', '--jtf',      dest='jtf', type=float, default=1.0, action='store',
                                            help="jet to tau fake energy scale" )
    parser.add_argument('-l', '--tag',      dest='tag', type=str, default="", action='store',
                                            help="add a tag to the output file" )
    parser.add_argument('-v', '--verbose',  dest='verbose', default=False, action='store_true',
                                            help="set verbose" )
    args = parser.parse_args()
else:
  args = None

def main(args):
  #from checkJobs import getSubmittedJobs
  
  years      = args.years
  channels   = args.channels
  outtag     = args.tag
  intag      = ""
  tes        = args.tes
  ltf        = args.ltf
  jtf        = args.jtf
  #submitted  = getSubmittedJobs()


  if outtag and '_' not in outtag[0]:
    outtag = '_'+outtag
  if tes!=1.:
    intag += "_TES%.3f"%(tes)
  if ltf!=1.:
    intag += "_LTF%.3f"%(ltf)
  if jtf!=1.:
    intag += "_JTF%.3f"%(jtf)
  intag  = intag.replace('.','p')
  outtag = intag+outtag
  
  for year in years:
    indir      = "/work/pbaertsc/heavy_resonance/output_%s/"%(year)
    samplesdir = args.outdir if args.outdir else "/work/pbaertsc/heavy_resonance/%s_noweight"%(year)
    os.chdir(indir)
    
    # CHECK EXISTING
    if args.checkExisting:
      for channel in channels:
        infiles  = "%s/*/*_%s.root"%(channel)
        filelist = glob.glob(infiles)
        pattern  = infiles.split('/')[-1]
        for file in filelist:
          if not isValidSample(pattern): continue
          checkFiles(file,pattern)
      continue
    
    # GET LIST
    samplelist = [ ]
    for directory in sorted(os.listdir('./')):
      if not os.path.isdir(directory): continue
      if not isValidSample(directory): continue
      samplelist.append(directory)
    if not samplelist:
      print "No samples found in %s!"%(indir)
    if args.verbose:
      print 'samplelist = %s\n'%(samplelist)
    
    # CHECK samples
    for channel in channels:
      print header(year,channel,intag)
      
      # HADD samples
      if not args.haddother or args.make:
        for directory in samplelist:
            if args.verbose:
              print directory
            
            subdir, samplename = getSampleShortName(directory,year)
            outdir  = "%s/%s"%(samplesdir,subdir)
            outfile = "%s/%s%s.root"%(outdir,samplename,outtag)
            infiles = '%s/*_%s%s.root'%(directory,channel,intag)
            
            if args.verbose:
              print "directory = %s"%(directory)
              print "outdir    = %s"%(outdir)
              print "outfile   = %s"%(outfile)
              print "infiles   = %s"%(infiles)
            
            #if directory.find('W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8__ytakahas-NanoTest_20180507_W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8-a7a5b67d3e3590e4899e147be08660be__USER')==-1: continue
            filelist = glob.glob(infiles)
            if not filelist: continue
            #running = [f for f in filelist if any(j.outfile in f for j in submitted)]
            
            if checkFiles(filelist,directory):
              print bcolors.BOLD + bcolors.OKGREEN + '[OK] ' + directory + ' ... can be hadded ' + bcolors.ENDC
            
            if args.compareToDas:
                compareEventsToDAS(filelist,directory)
            if args.compareToDasExisting and os.path.isfile(outfile):
                print '   check existing file %s:'%(outfile)
                compareEventsToDAS(outfile,directory)
              #else:
              #  print bcolors.BOLD + bcolors.OKBLUE + '   [OK] ' + directory + bcolors.ENDC
              #print
            
            # HADD
            if args.make:
                ensureDirectory(outdir)
                if os.path.isfile(outfile):
                  if args.force:
                    print bcolors.BOLD + bcolors.WARNING + "   [WN] target %s already exists! Overwriting..."%(outfile) + bcolors.ENDC
                  else:
                    print bcolors.BOLD + bcolors.FAIL + "   [NG] target %s already exists! Use --force or -f to overwrite."%(outfile) + bcolors.ENDC
                    continue
                
                haddcmd = 'hadd -f %s %s'%(outfile,infiles)
                print haddcmd
                os.system(haddcmd)
                
                #if 'LQ3' not in directory:
                #     compareEventsToDAS(outfile,directory)
                #    skimcmd = 'python extractTrees.py -c %s -f %s'%(channel,outfile)
                #    rmcmd = 'rm %s'%(infiles)
                #    #os.system(skimcmd)
                #    #os.system(rmcmd)
                #    continue
                
                #skimcmd = 'python extractTrees.py -c %s -f %s'%(channel,outfile)
                #os.system(skimcmd)
                
                # CLEAN UP
                if args.cleanup:
                  rmcmd = 'rm %s; rm %s/logs/*_%s_%s%s*'%(infiles,directory,channel,year,intag)
                  print bcolors.BOLD + bcolors.OKBLUE + "   removing %d output files..."%(len(infiles)) + bcolors.ENDC
                  if args.verbose:
                    print rmcmd
                  os.system(rmcmd)
                print
      
      # HADD other
      if year == 2016:
          haddsets = [
              ('VV', "ZZTo2L2Nu", ['ZZTo2L2Nu_main','ZZTo2L2Nu_ext1']),
              ('VV', "ZZTo4L",    ['ZZTo4L_main','ZZTo4L_ext1']),
              ('SingleMuon',      "SingleMuon_Run2016B",      ['SingleMuon_Run2016B_ver1-v1','SingleMuon_Run2016B_ver2-v1']),
              ('SingleElectron',  "SingleElectron_Run2016B",  ['SingleElectron_Run2016B_ver1-v1','SingleElectron_Run2016B_ver2-v1']),
              ('MET',             "MET_Run2016B",             ['MET_Run2016B_ver1-v1','MET_Run2016B_ver2-v1']),
              ('SinglePhoton',    "SinglePhoton_Run2016B",    ['SinglePhoton_Run2016B_ver1-v1','SinglePhoton_Run2016B_ver2-v1'])
          ]
            
      elif year == 2017:
          haddsets = [
              ('SingleMuon',      "SingleMuon",      ['SingleMuon_Run2017B','SingleMuon_Run2017C','SingleMuon_Run2017D','SingleMuon_Run2017E','SingleMuon_Run2017F']),
              ('SingleElectron',  "SingleElectron",  ['SingleElectron_Run2017B','SingleElectron_Run2017C','SingleElectron_Run2017D','SingleElectron_Run2017E','SingleElectron_Run2017F']),
              ('MET',             "MET",             ['MET_Run2017B','MET_Run2017C','MET_Run2017D','MET_Run2017E','MET_Run2017F'])]
      elif year == 2018:
          haddsets = [
              ('SingleMuon',      "SingleMuon",      ['SingleMuon_Run2018A','SingleMuon_Run2018B','SingleMuon_Run2018C','SingleMuon_Run2018D']),
              ('EGamma',  "EGamma",  ['EGamma_Run2018A','EGamma_Run2018B','EGamma_Run2018C','EGamma_Run2018D']),
              ('MET',             "MET",             ['MET_Run2018A','MET_Run2018B','MET_Run2018C','MET_Run2018D'])]
      if args.haddother:
        for subdir, samplename, sampleset in haddsets:
            if args.verbose:
              print subdir, samplename, sampleset
            if args.samples and not matchSampleToPattern(samplename,args.samples): continue
            if args.veto and matchSampleToPattern(directory,args.veto): continue
            if '2016' in samplename and year!=2016: continue
            if '2017' in samplename and year!=2017: continue
            if '2018' in samplename and year!=2018: continue
            if '$RUN' in samplename:
              samplename = samplename.replace('$RUN','Run%d'%year)
              sampleset  = [s.replace('$RUN','Run%d'%year) for s in sampleset]
            
            outdir  = "%s/%s"%(samplesdir,subdir)
            outfile = "%s/%s%s.root"%(outdir,samplename,outtag)
            infiles = ['%s/%s%s.root'%(outdir,s,outtag) for s in sampleset] #.replace('ele','e')
            ensureDirectory(outdir)
            
            # OVERWRITE ?
            if os.path.isfile(outfile):
              if args.force:
                pass
                #if args.verbose:
                #  print bcolors.BOLD + bcolors.WARNING + "[WN] target %s already exists! Overwriting..."%(outfile) + bcolors.ENDC
              else:
                print bcolors.BOLD + bcolors.FAIL + "[NG] target %s already exists! Use --force or -f to overwrite."%(outfile) + bcolors.ENDC
                continue
            
            # CHECK FILES
            allinfiles = [ ]
            for infile in infiles[:]:
              if '*' in infile or '?' in infile:
                files = glob.glob(infile)
                allinfiles += files
                if not files:
                  print bcolors.BOLD + bcolors.FAIL + '[NG] no match for the glob pattern %s! Removing pattern from hadd list for "%s"...'%(infile,samplename) + bcolors.ENDC
                  infiles.remove(infile)
              elif not os.path.isfile(infile):
                print bcolors.BOLD + bcolors.FAIL + '[NG] infile %s does not exists! Removing from hadd list for "%s"...'%(infile,samplename) + bcolors.ENDC
                infiles.remove(infile)
              else:
                allinfiles.append(infile)
            
            # HADD
            if args.verbose:
              print "infiles =", infiles
              print "allfiles =", allinfiles
            if len(allinfiles)==1:
              print bcolors.BOLD + bcolors.WARNING + "[WN] found only one file (%s) to hadd to %s!"%(allinfiles[0],outfile) + bcolors.ENDC 
            elif len(allinfiles)>1:
              print bcolors.BOLD + bcolors.OKGREEN + '[OK] hadding %s' %(outfile) + bcolors.ENDC
              haddcmd = 'hadd -f %s %s'%(outfile,' '.join(infiles))
              print haddcmd
              os.system(haddcmd)
            else:
              print bcolors.BOLD + bcolors.WARNING + "[WN] no files to hadd!" + bcolors.ENDC
            print
    
    os.chdir('..')
     


def isValidSample(pattern):
  if args.samples and not matchSampleToPattern(pattern,args.samples): return False
  if args.veto and matchSampleToPattern(pattern,args.veto): return False
  if args.type=='mc' and any(s in pattern[:len(s)+2] for s in ['SingleMuon','SingleElectron','EGamma','MET']): return False
  if args.type=='data' and not any(s in pattern[:len(s)+2] for s in ['SingleMuon','SingleElectron','EGamma','MET']): return False
  return True


indexpattern = re.compile(r".*_(\d+)_[a-z]+(?:_[A-Z]+\dp\d+)?\.root")
def checkFiles(filelist,directory,clean=False):
    if args.verbose:
      print "checkFiles: %s, %s"%(filelist,directory)
    if isinstance(filelist,str):
      filelist = [filelist]
    badfiles = [ ]
    ifound   = [ ]
    for filename in filelist:
      file  = TFile(filename, 'READ')
      isbad = False
      if file.IsZombie():
        print bcolors.FAIL + '[NG] file %s is a zombie'%(filename) + bcolors.ENDC
        isbad = True
      else:
        tree = file.Get('tree')
        if not isinstance(tree,TTree):
          print bcolors.FAIL + '[NG] no tree found in ' + filename + bcolors.ENDC
          isbad = True
        elif not isinstance(file.Get('pileup'),TH1):
          print bcolors.FAIL + '[NG] no pileup found in ' + filename + bcolors.ENDC
          isbad = True
        elif any(s in filename for s in ['DYJets','WJets']) and tree.GetMaximum('LHE_Njets')>10:
          print bcolors.WARNING + '[WN] LHE_Njets = %d > 10 in %s'%(tree.GetMaximum('LHE_Njets'),filename) + bcolors.ENDC
      if isbad:
        badfiles.append(filename)
        #rmcmd = 'rm %s' %filename
        #print rmcmd
        #os.system(rmcmd)
      file.Close()
      match = indexpattern.search(filename)
      if match: ifound.append(int(match.group(1)))
    
    if len(badfiles)>0:
      print bcolors.BOLD + bcolors.FAIL + "[NG] %s:   %d out of %d files %s no tree!"%(directory,len(badfiles),len(filelist),"have" if len(badfiles)>1 else "has") + bcolors.ENDC
      if clean:
        for filename in badfiles:
          os.remove(filename)
      return False
    
    # TODO: check all chunks (those>imax)
    if ifound:
      imax = max(ifound)+1
      if len(filelist)<imax:
        imiss = [ i for i in range(0,max(ifound)) if i not in ifound ]
        chunktext = ('chunks ' if len(imiss)>1 else 'chunk ') + ', '.join(str(i) for i in imiss)
        print bcolors.BOLD + bcolors.WARNING + "[WN] %s missing %d/%d files (%s) ?"%(directory,len(imiss),len(filelist),chunktext) + bcolors.ENDC
    else:
      print bcolors.BOLD + bcolors.WARNING + "[WN] %s did not find any valid chunk pattern in file list ?"%(directory) + bcolors.ENDC
    
    return True
    
def compareEventsToDAS(filenames,dasname):
    """Compare a number of processed events in an output file to the available number of events in DAS."""
    dasname = dasname.replace('__', '/')
    if args.verbose:
      print "compareEventsToDAS: %s, %s"%(filenames,dasname)
      #start = time.time()
    if isinstance(filenames,str):
      filenames = [filenames]
    total_processed = 0
    nfiles = len(filenames)
    for filename in filenames:
      file = TFile(filename, 'READ')
      if file.IsZombie():
        continue
      #else:
      #  print bcolors.FAIL + '[NG] compareEventsToDAS: no cutflow found in ' + filename + bcolors.ENDC
      file.Close()
    
    instance = 'prod/phys03' if 'USER' in dasname else 'prod/global'
    dascmd   = 'das_client --limit=0 --query=\"summary dataset=/%s instance=%s\"'%(dasname,instance)
    if args.verbose:
      print dascmd
    dasargs  = shlex.split(dascmd)
    output, error = subprocess.Popen(dasargs, stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
    
    if not "nevents" in output:
        print bcolors.BOLD + bcolors.FAIL + '   [NG] Did not find nevents for "%s" in DAS. Return message:'%(dasname) + bcolors.ENDC 
        print bcolors.FAIL + '     ' + output + bcolors.ENDC
        return False
    total_das = Double(output.split('"nevents":')[1].split(',')[0])
    fraction = total_processed/total_das
    
    nfiles = ", %d files"%(nfiles) if nfiles>1 else ""
    if fraction > 1.001:
        print bcolors.BOLD + bcolors.FAIL + '   [NG] DAS entries = %d, Processed in tree = %d (frac = %.2f > 1%s)'%(total_das,total_processed,fraction,nfiles) + bcolors.ENDC
    elif fraction > 0.8:
        print bcolors.BOLD + bcolors.OKBLUE + '   [OK] DAS entries = %d, Processed in tree = %d (frac = %.2f%s)'%(total_das,total_processed,fraction,nfiles) + bcolors.ENDC
    else:
        print bcolors.BOLD + bcolors.FAIL + '   [NG] DAS entries = %d, Processed in tree = %d (frac = %.2f < 0.8%s)'%(total_das,total_processed,fraction,nfiles) + bcolors.ENDC
    return True
    
def getSampleShortName(dasname,year):
  """Get short subdir and sample name from sample_dict."""
  #if '__nanoaod' in dasname.lower():
  #  dasname = dasname[:dasname.lower().index('__nanoaod')]
  #if '__user' in dasname.lower():
  #  dasname = dasname[:dasname.lower().index('__user')]

  if year==2016:
      subdirs = [ 'DY', 'ZJ', 'WJ', 'ST', 'TT', 'VV', 'XZH', 'XZHVBF',  'SingleMuon', 'SingleElectron', 'MET', 'SinglePhoton']
      sample_dict = [
          ('DY', "DYJetsToLL_HT-100to200",   "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('DY', "DYJetsToLL_HT-200to400",   "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('DY', "DYJetsToLL_HT-400to600",   "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('DY', "DYJetsToLL_HT-600to800",   "DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('DY', "DYJetsToLL_HT-800to1200",  "DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('DY', "DYJetsToLL_HT-1200to2500", "DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('DY', "DYJetsToLL_HT-2500toInf",  "DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('ZJ', "ZJetsToNuNu_HT-100to200",  "ZJetsToNuNu_HT-100To200_13TeV-madgraph"),
          ('ZJ', "ZJetsToNuNu_HT-200to400",  "ZJetsToNuNu_HT-200To400_13TeV-madgraph"),
          ('ZJ', "ZJetsToNuNu_HT-400to600",  "ZJetsToNuNu_HT-400To600_13TeV-madgraph"),
          ('ZJ', "ZJetsToNuNu_HT-600to800",  "ZJetsToNuNu_HT-600To800_13TeV-madgraph"),
          ('ZJ', "ZJetsToNuNu_HT-800to1200", "ZJetsToNuNu_HT-800To1200_13TeV-madgraph"),
          ('ZJ', "ZJetsToNuNu_HT-1200to2500","ZJetsToNuNu_HT-1200To2500_13TeV-madgraph"),
          ('ZJ', "ZJetsToNuNu_HT-2500toInf", "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph"),
          ('WJ', "WJetsToLNu_HT-100to200",   "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('WJ', "WJetsToLNu_HT-200to400",   "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('WJ', "WJetsToLNu_HT-400to600",   "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('WJ', "WJetsToLNu_HT-600to800",   "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('WJ', "WJetsToLNu_HT-800to1200",  "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('WJ', "WJetsToLNu_HT-1200to2500", "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('WJ', "WJetsToLNu_HT-2500toInf",  "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
          ('ST', "ST_s-channel",             "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1"),
          ('ST', "ST_t-channel_top",         "ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1"),
          ('ST', "ST_t-channel_antitop",     "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1"),
          ('ST', "ST_tW_top",                "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4"),
          ('ST', "ST_tW_antitop",            "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4"),
          ('TT', "TTTo2L2Nu",                "TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"),
          ('TT', "TTToSemiLeptonic",         "TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"),
          ('TT', "TTWJetsToLNu",             "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8"),
          ('TT', "TTZToLLNuNu",              "TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8"), 
          ('VV', "WWTo1L1Nu2Q",              "WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8"),
          ('VV', "WWTo2L2Nu",                "WWTo2L2Nu_13TeV-powheg"),
          ('VV', "WWTo4Q",                   "WWTo4Q_13TeV-powheg"),
          ('VV', "WZTo1L1Nu2Q",              "WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8"),
          ('VV', "WZTo2L2Q",                 "WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8"),
          ('VV', "ZZTo2L2Q",                 "ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8"),
          ('VV', "ZZTo2Q2Nu",                "ZZTo2Q2Nu_13TeV_amcatnloFXFX_madspin_pythia8"),
          ('VV', "ZZTo2L2Nu_ext1",           "ZZTo2L2Nu_13TeV_powheg_pythia8_ext1"),
          ('VV', "ZZTo2L2Nu_main",           "ZZTo2L2Nu_13TeV_powheg_pythia8"),
          ('VV', "ZZTo4L_ext1",              "ZZTo4L_13TeV_powheg_pythia8_ext1"),
          ('VV', "ZZTo4L_main",              "ZZTo4L_13TeV_powheg_pythia8"),
          ('VV', "GluGluHToBB",              "GluGluHToBB_M125_13TeV_amcatnloFXFX_pythia8"),
          ('VV', "ZH_HToBB_ZToNuNu",         "ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8"),
          ('VV', "ZH_HToBB_ZToLL",           "ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8"),
          ('VV', "WplusH_HToBB_WToLNu",      "WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8"),
          ('VV', "WminusH_HToBB_WToLNu",     "WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M600",    "ZprimeToZHToZlepHinc_narrow_M-600_TuneCP5_13TeV-madgraph-pythia8" ),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M800",    "ZprimeToZHToZlepHinc_narrow_M-800_TuneCP5_13TeV-madgraph-pythia8" ),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M1000",   "ZprimeToZHToZlepHinc_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M1200",   "ZprimeToZHToZlepHinc_narrow_M-1200_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M1400",   "ZprimeToZHToZlepHinc_narrow_M-1400_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M1600",   "ZprimeToZHToZlepHinc_narrow_M-1600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M1800",   "ZprimeToZHToZlepHinc_narrow_M-1800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M2000",   "ZprimeToZHToZlepHinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M2500",   "ZprimeToZHToZlepHinc_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M3000",   "ZprimeToZHToZlepHinc_narrow_M-3000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M3500",   "ZprimeToZHToZlepHinc_narrow_M-3500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M4000",   "ZprimeToZHToZlepHinc_narrow_M-4000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M4500",   "ZprimeToZHToZlepHinc_narrow_M-4500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M5000",   "ZprimeToZHToZlepHinc_narrow_M-5000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M5500",   "ZprimeToZHToZlepHinc_narrow_M-5500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M6000",   "ZprimeToZHToZlepHinc_narrow_M-6000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M7000",   "ZprimeToZHToZlepHinc_narrow_M-7000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',"ZprimeToZHToZlepHinc_narrow_M8000",   "ZprimeToZHToZlepHinc_narrow_M-8000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M600",    "ZprimeToZHToZinvHall_narrow_M-600_TuneCP5_13TeV-madgraph-pythia8" ),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M800",    "ZprimeToZHToZinvHall_narrow_M-800_TuneCP5_13TeV-madgraph-pythia8" ),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1000",   "ZprimeToZHToZinvHall_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1200",   "ZprimeToZHToZinvHall_narrow_M-1200_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1400",   "ZprimeToZHToZinvHall_narrow_M-1400_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1600",   "ZprimeToZHToZinvHall_narrow_M-1600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1800",   "ZprimeToZHToZinvHall_narrow_M-1800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M2000",   "ZprimeToZHToZinvHall_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M2500",   "ZprimeToZHToZinvHall_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M3000",   "ZprimeToZHToZinvHall_narrow_M-3000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M3500",   "ZprimeToZHToZinvHall_narrow_M-3500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M4000",   "ZprimeToZHToZinvHall_narrow_M-4000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M4500",   "ZprimeToZHToZinvHall_narrow_M-4500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M5000",   "ZprimeToZHToZinvHall_narrow_M-5000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M5500",   "ZprimeToZHToZinvHall_narrow_M-5500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M6000",   "ZprimeToZHToZinvHall_narrow_M-6000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M7000",   "ZprimeToZHToZinvHall_narrow_M-7000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M8000",   "ZprimeToZHToZinvHall_narrow_M-8000_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-600",  "Zprime_VBF_Zh_Zlephinc_narrow_M-600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-800",  "Zprime_VBF_Zh_Zlephinc_narrow_M-800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1200",  "Zprime_VBF_Zh_Zlephinc_narrow_M-1200_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1400",  "Zprime_VBF_Zh_Zlephinc_narrow_M-1400_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1600",  "Zprime_VBF_Zh_Zlephinc_narrow_M-1600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1800",  "Zprime_VBF_Zh_Zlephinc_narrow_M-1800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-2000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-2500",  "Zprime_VBF_Zh_Zlephinc_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-3000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-3000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-3500",  "Zprime_VBF_Zh_Zlephinc_narrow_M-3500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-4000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-4000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-4500",  "Zprime_VBF_Zh_Zlephinc_narrow_M-4500_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-5000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-5000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-5500",  "Zprime_VBF_Zh_Zlephinc_narrow_M-5500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-6000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-6000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-7000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-7000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-8000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-8000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-600",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-800",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1200",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-1200_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1400",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-1400_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1600",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-1600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1800",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-1800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-2000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-2500",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-3000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-3000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-3500",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-3500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-4000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-4000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-4500",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-4500_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-5000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-5000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-5500",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-5500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-6000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-6000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-7000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-7000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-8000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-8000_TuneCP5_13TeV-madgraph-pythia8"),
          ('SingleMuon',     "SingleMuon_Run2016B_ver1-v1",         "SingleMuon/Run2016B_ver1"),
          ('SingleMuon',     "SingleMuon_Run2016B_ver2-v1",         "SingleMuon/Run2016B_ver2"),
          ('SingleMuon',     "SingleMuon_Run2016C",              "SingleMuon/Run2016C"),
          ('SingleMuon',     "SingleMuon_Run2016D",              "SingleMuon/Run2016D"),
          ('SingleMuon',     "SingleMuon_Run2016E",              "SingleMuon/Run2016E"),
          ('SingleMuon',     "SingleMuon_Run2016F",              "SingleMuon/Run2016F"),
          ('SingleMuon',     "SingleMuon_Run2016G",              "SingleMuon/Run2016G"),
          ('SingleMuon',     "SingleMuon_Run2016H",              "SingleMuon/Run2016H"),
          ('SingleElectron',     "SingleElectron_Run2016B_ver1-v1",         "SingleElectron/Run2016B_ver1"),
          ('SingleElectron',     "SingleElectron_Run2016B_ver2-v1",         "SingleElectron/Run2016B_ver2"),
          ('SingleElectron',     "SingleElectron_Run2016C",              "SingleElectron/Run2016C"),
          ('SingleElectron',     "SingleElectron_Run2016D",              "SingleElectron/Run2016D"),
          ('SingleElectron',     "SingleElectron_Run2016E",              "SingleElectron/Run2016E"),
          ('SingleElectron',     "SingleElectron_Run2016F",              "SingleElectron/Run2016F"),
          ('SingleElectron',     "SingleElectron_Run2016G",              "SingleElectron/Run2016G"),
          ('SingleElectron',     "SingleElectron_Run2016H",              "SingleElectron/Run2016H"),
          ('MET',     "MET_Run2016B_ver1-v1",         "MET/Run2016B_ver1"),
          ('MET',     "MET_Run2016B_ver2-v1",         "MET/Run2016B_ver2"),
          ('MET',     "MET_Run2016C",              "MET/Run2016C"),
          ('MET',     "MET_Run2016D",              "MET/Run2016D"),
          ('MET',     "MET_Run2016E",              "MET/Run2016E"),
          ('MET',     "MET_Run2016F",              "MET/Run2016F"),
          ('MET',     "MET_Run2016G",              "MET/Run2016G"),
          ('MET',     "MET_Run2016H",              "MET/Run2016H"),
          ('SinglePhoton',     "SinglePhoton_Run2016B_ver1-v1",         "SinglePhoton/Run2016B_ver1"),
          ('SinglePhoton',     "SinglePhoton_Run2016B_ver2-v1",         "SinglePhoton/Run2016B_ver2"),
          ('SinglePhoton',     "SinglePhoton_Run2016C",              "SinglePhoton/Run2016C"),
          ('SinglePhoton',     "SinglePhoton_Run2016D",              "SinglePhoton/Run2016D"),
          ('SinglePhoton',     "SinglePhoton_Run2016E",              "SinglePhoton/Run2016E"),
          ('SinglePhoton',     "SinglePhoton_Run2016F",              "SinglePhoton/Run2016F"),
          ('SinglePhoton',     "SinglePhoton_Run2016G",              "SinglePhoton/Run2016G"),
          ('SinglePhoton',     "SinglePhoton_Run2016H",              "SinglePhoton/Run2016H")]                                       

  elif year==2017:
      subdirs = [ 'DY', 'ZJ', 'WJ', 'ST', 'TT', 'VV', 'XZH', 'XZHVBF', 'SingleMuon', 'SingleElectron', 'MET', 'SinglePhoton']
      sample_dict = [
          ('DY',             "DYJetsToLL_HT-100to200",       "DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8"    ),
          ('DY',             "DYJetsToLL_HT-200to400",       "DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8"    ),
          ('DY',             "DYJetsToLL_HT-400to600",       "DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8"    ),
          ('DY',             "DYJetsToLL_HT-600to800",       "DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8"    ),
          ('DY',             "DYJetsToLL_HT-800to1200",      "DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8"   ),
          ('DY',             "DYJetsToLL_HT-1200to2500",     "DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8"  ),
          ('DY',             "DYJetsToLL_HT-2500toInf",      "DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8"   ),
          ('ZJ',             "ZJetsToNuNu_HT-100to200",      "ZJetsToNuNu_HT-100To200_13TeV-madgraph"                           ),
          ('ZJ',             "ZJetsToNuNu_HT-200to400",      "ZJetsToNuNu_HT-200To400_13TeV-madgraph"                           ),
          ('ZJ',             "ZJetsToNuNu_HT-400to600",      "ZJetsToNuNu_HT-400To600_13TeV-madgraph"                           ),
          ('ZJ',             "ZJetsToNuNu_HT-600to800",      "ZJetsToNuNu_HT-600To800_13TeV-madgraph"                           ),
          ('ZJ',             "ZJetsToNuNu_HT-800to1200",     "ZJetsToNuNu_HT-800To1200_13TeV-madgraph"                          ),
          ('ZJ',             "ZJetsToNuNu_HT-1200to2500",    "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph"                         ),
          ('ZJ',             "ZJetsToNuNu_HT-2500toInf",     "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph"                          ),
          ('WJ',             "WJetsToLNu_HT-100to200",       "WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8"         ),
          ('WJ',             "WJetsToLNu_HT-200to400",       "WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8"         ),
          ('WJ',             "WJetsToLNu_HT-400to600",       "WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8"         ),
          ('WJ',             "WJetsToLNu_HT-600to800",       "WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8"         ),
          ('WJ',             "WJetsToLNu_HT-800to1200",      "WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8"        ),
          ('WJ',             "WJetsToLNu_HT-1200to2500",     "WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8"       ),
          ('WJ',             "WJetsToLNu_HT-2500toInf",      "WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8"        ),
          ('ST',             "ST_s-channel",                 "ST_s-channel_4f_leptonDecays"                                     ),
          ('ST',             "ST_t-channel_antitop",         "ST_t-channel_antitop_4f_inclusiveDecays"                          ),
          ('ST',             "ST_t-channel_top",             "ST_t-channel_top_4f_inclusiveDecays"                              ),
          ('ST',             "ST_tW_antitop",                "ST_tW_antitop_5f_inclusiveDecays"                                 ),
          ('ST',             "ST_tW_top",                    "ST_tW_top_5f_inclusiveDecays"                                     ),
          ('TT',             "TTTo2L2Nu",                    "TTTo2L2Nu"                                                        ),
          ('TT',             "TTToSemiLeptonic",             "TTToSemiLeptonic"                                                 ),
          ('TT',             "TTWJetsToLNu",                 "TTWJetsToLNu"                                                     ),
          ('TT',             "TTZToLLNuNu",                  "TTZToLLNuNu"                                                      ),
          ('VV',             "WWTo1L1Nu2Q",                  "WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8"                   ),
          ('VV',             "WWTo2L2Nu",                    "WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8"                   ),
          ('VV',             "WWTo4Q",                       "WWTo4Q_NNPDF31_TuneCP5_13TeV-powheg-pythia8"                      ),
          ('VV',             "WZTo1L1Nu2Q",                  "WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8"                   ),
          ('VV',             "WZTo2L2Q",                     "WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8"                      ),
          ('VV',             "ZZTo2L2Q",                     "ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8"                      ),
          ('VV',             "ZZTo2Q2Nu",                    "ZZTo2Q2Nu_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8"             ),
          ('VV',             "ZZTo2L2Nu",                    "ZZTo2L2Nu_13TeV_powheg_pythia8"                                   ),
          ('VV',             "ZZTo4L",                       "ZZTo4L_13TeV_powheg_pythia8"                                      ),
          ('VV',             "GluGluHToBB",                  "GluGluHToBB_M125_13TeV_amcatnloFXFX_pythia8"                      ),
          ('VV',             "ZH_HToBB_ZToNuNu",             "ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8"                       ),
          ('VV',             "ZH_HToBB_ZToLL",               "ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8"                         ),
          ('VV',             "WplusH_HToBB_WToLNu",          "WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8"                    ),
          ('VV',             "WminusH_HToBB_WToLNu",         "WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8"                   ),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M600",    "ZprimeToZHToZlepHinc_narrow_M-600_TuneCP5_13TeV-madgraph-pythia8" ),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M800",    "ZprimeToZHToZlepHinc_narrow_M-800_TuneCP5_13TeV-madgraph-pythia8" ),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1000",   "ZprimeToZHToZlepHinc_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1200",   "ZprimeToZHToZlepHinc_narrow_M-1200_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1400",   "ZprimeToZHToZlepHinc_narrow_M-1400_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1600",   "ZprimeToZHToZlepHinc_narrow_M-1600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1800",   "ZprimeToZHToZlepHinc_narrow_M-1800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M2000",   "ZprimeToZHToZlepHinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M2500",   "ZprimeToZHToZlepHinc_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M3000",   "ZprimeToZHToZlepHinc_narrow_M-3000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M3500",   "ZprimeToZHToZlepHinc_narrow_M-3500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M4000",   "ZprimeToZHToZlepHinc_narrow_M-4000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M4500",   "ZprimeToZHToZlepHinc_narrow_M-4500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M5000",   "ZprimeToZHToZlepHinc_narrow_M-5000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M5500",   "ZprimeToZHToZlepHinc_narrow_M-5500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M6000",   "ZprimeToZHToZlepHinc_narrow_M-6000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M7000",   "ZprimeToZHToZlepHinc_narrow_M-7000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M8000",   "ZprimeToZHToZlepHinc_narrow_M-8000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M600",    "ZprimeToZHToZinvHall_narrow_M-600_TuneCP5_13TeV-madgraph-pythia8" ),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M800",    "ZprimeToZHToZinvHall_narrow_M-800_TuneCP5_13TeV-madgraph-pythia8" ),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1000",   "ZprimeToZHToZinvHall_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1200",   "ZprimeToZHToZinvHall_narrow_M-1200_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1400",   "ZprimeToZHToZinvHall_narrow_M-1400_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1600",   "ZprimeToZHToZinvHall_narrow_M-1600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1800",   "ZprimeToZHToZinvHall_narrow_M-1800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M2000",   "ZprimeToZHToZinvHall_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M2500",   "ZprimeToZHToZinvHall_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M3000",   "ZprimeToZHToZinvHall_narrow_M-3000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M3500",   "ZprimeToZHToZinvHall_narrow_M-3500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M4000",   "ZprimeToZHToZinvHall_narrow_M-4000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M4500",   "ZprimeToZHToZinvHall_narrow_M-4500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M5000",   "ZprimeToZHToZinvHall_narrow_M-5000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M5500",   "ZprimeToZHToZinvHall_narrow_M-5500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M6000",   "ZprimeToZHToZinvHall_narrow_M-6000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M7000",   "ZprimeToZHToZinvHall_narrow_M-7000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M8000",   "ZprimeToZHToZinvHall_narrow_M-8000_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-600",  "Zprime_VBF_Zh_Zlephinc_narrow_M-600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-800",  "Zprime_VBF_Zh_Zlephinc_narrow_M-800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1200",  "Zprime_VBF_Zh_Zlephinc_narrow_M-1200_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1400",  "Zprime_VBF_Zh_Zlephinc_narrow_M-1400_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1600",  "Zprime_VBF_Zh_Zlephinc_narrow_M-1600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1800",  "Zprime_VBF_Zh_Zlephinc_narrow_M-1800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-2000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-2500",  "Zprime_VBF_Zh_Zlephinc_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-3000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-3000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-3500",  "Zprime_VBF_Zh_Zlephinc_narrow_M-3500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-4000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-4000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-4500",  "Zprime_VBF_Zh_Zlephinc_narrow_M-4500_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-5000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-5000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-5500",  "Zprime_VBF_Zh_Zlephinc_narrow_M-5500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-6000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-6000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-7000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-7000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-8000",  "Zprime_VBF_Zh_Zlephinc_narrow_M-8000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-600",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-800",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1200",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-1200_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1400",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-1400_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1600",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-1600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1800",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-1800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-2000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-2500",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-3000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-3000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-3500",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-3500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-4000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-4000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-4500",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-4500_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-5000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-5000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-5500",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-5500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-6000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-6000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-7000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-7000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-8000",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-8000_TuneCP5_13TeV-madgraph-pythia8"),
          ('SingleMuon',     "SingleMuon_$RUN",              "SingleMuon/$RUN"                                                  ),
          ('SingleElectron', "SingleElectron_$RUN",          "SingleElectron/$RUN"                                              ),
          ('MET',            "MET_$RUN",                     "MET/$RUN"                                                         ),
          ('SinglePhoton',   "SinglePhoton_$RUN",            "SinglePhoton/$RUN"                                                )]


  elif year==2018:
      subdirs = [ 'DY', 'ZJ', 'WJ', 'ST', 'TT', 'VV', 'XZH', 'XZHVBF', 'SingleMuon', 'EGamma', 'MET']
      sample_dict = [
          ('DY',             "DYJetsToLL_HT-100to200",   "DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8"),
          ('DY',             "DYJetsToLL_HT-200to400",   "DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8"),
          ('DY',             "DYJetsToLL_HT-400to600",   "DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8"),
          ('DY',             "DYJetsToLL_HT-600to800",   "DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8"),
          ('DY',             "DYJetsToLL_HT-800to1200",   "DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8"),
          ('DY',             "DYJetsToLL_HT-1200to2500",  "DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8"),
          ('DY',             "DYJetsToLL_HT-2500toInf",   "DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8"),
          ('ZJ',             "ZJetsToNuNu_HT-100to200",  "ZJetsToNuNu_HT-100To200_13TeV-madgraph"),
          ('ZJ',             "ZJetsToNuNu_HT-200to400",  "ZJetsToNuNu_HT-200To400_13TeV-madgraph"),
          ('ZJ',             "ZJetsToNuNu_HT-400to600",  "ZJetsToNuNu_HT-400To600_13TeV-madgraph"),
          ('ZJ',             "ZJetsToNuNu_HT-600to800",  "ZJetsToNuNu_HT-600To800_13TeV-madgraph"),
          ('ZJ',             "ZJetsToNuNu_HT-800to1200",  "ZJetsToNuNu_HT-800To1200_13TeV-madgraph"),
          ('ZJ',             "ZJetsToNuNu_HT-1200to2500",  "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph"),
          ('ZJ',             "ZJetsToNuNu_HT-2500toInf",  "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph"),
          ('WJ',             "WJetsToLNu_HT-100to200",   "WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8"),
          ('WJ',             "WJetsToLNu_HT-200to400",   "WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8"),
          ('WJ',             "WJetsToLNu_HT-400to600",   "WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8"),
          ('WJ',             "WJetsToLNu_HT-600to800",   "WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8"),
          ('WJ',             "WJetsToLNu_HT-800to1200",   "WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8"),
          ('WJ',             "WJetsToLNu_HT-1200to2500",   "WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8"),
          ('WJ',             "WJetsToLNu_HT-2500toInf",   "WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8"),
          ('ST',             "ST_s-channel",             "ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8"),
          ('ST',             "ST_t-channel_top",         "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8"),
          ('ST',             "ST_t-channel_antitop",     "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8"),
          ('ST',             "ST_tW_top",                "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8"),
          ('ST',             "ST_tW_antitop",            "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8"),
          ('TT',             "TTTo2L2Nu",                "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8"),
          ('TT',             "TTToSemiLeptonic",         "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8"),
          ('TT',             "TTWJetsToLNu",             "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8"),
          ('TT',             "TTZToLLNuNu",              "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8"),
          ('VV',             "WWTo2L2Nu",                "WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8"),
          ('VV',             "WWTo4Q",                   "WWTo4Q_NNPDF31_TuneCP5_13TeV-powheg-pythia8"),
          ('VV',             "WWTo1L1Nu2Q",              "WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8"),
          ('VV',             "WZTo2L2Q",                 "WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8"),
          ('VV',             "ZZTo2Q2Nu",                "ZZTo2Q2Nu_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8"),
          ('VV',             "ZZTo2L2Q",                 "ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8"),
          ('VV',             "ZZTo2L2Nu",                "ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8"),
          ('VV',             "ZZTo4L",                   "ZZTo4L_TuneCP5_13TeV_powheg_pythia8"),
          ('VV',             "GluGluHToBB",              "GluGluHToBB_M125_13TeV_powheg_pythia8"),
          ('VV',             "ZH_HToBB_ZToNuNu",         "ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8"),
          ('VV',             "ZH_HToBB_ZToLL",           "ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8"),
          ('VV',             "WplusH_HToBB_WToLNu",      "WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8"),
          ('VV',             "WminusH_HToBB_WToLNu",     "WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M600", "ZprimeToZHToZlepHinc_narrow_M-600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M800", "ZprimeToZHToZlepHinc_narrow_M-800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1000","ZprimeToZHToZlepHinc_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1200","ZprimeToZHToZlepHinc_narrow_M-1200_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1400","ZprimeToZHToZlepHinc_narrow_M-1400_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1600","ZprimeToZHToZlepHinc_narrow_M-1600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1800","ZprimeToZHToZlepHinc_narrow_M-1800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M2000","ZprimeToZHToZlepHinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M2500","ZprimeToZHToZlepHinc_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M3000","ZprimeToZHToZlepHinc_narrow_M-3000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M3500","ZprimeToZHToZlepHinc_narrow_M-3500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M4000","ZprimeToZHToZlepHinc_narrow_M-4000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M4500","ZprimeToZHToZlepHinc_narrow_M-4500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M5000","ZprimeToZHToZlepHinc_narrow_M-5000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M5500","ZprimeToZHToZlepHinc_narrow_M-5500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M6000","ZprimeToZHToZlepHinc_narrow_M-6000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M7000","ZprimeToZHToZlepHinc_narrow_M-7000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZlepHinc_narrow_M8000","ZprimeToZHToZlepHinc_narrow_M-8000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M600",    "ZprimeToZHToZinvHall_narrow_M-600_TuneCP5_13TeV-madgraph-pythia8" ),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M800",    "ZprimeToZHToZinvHall_narrow_M-800_TuneCP5_13TeV-madgraph-pythia8" ),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1000",   "ZprimeToZHToZinvHall_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1200",   "ZprimeToZHToZinvHall_narrow_M-1200_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1400",   "ZprimeToZHToZinvHall_narrow_M-1400_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1600",   "ZprimeToZHToZinvHall_narrow_M-1600_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M1800",   "ZprimeToZHToZinvHall_narrow_M-1800_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M2000",   "ZprimeToZHToZinvHall_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M2500",   "ZprimeToZHToZinvHall_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M3000",   "ZprimeToZHToZinvHall_narrow_M-3000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M3500",   "ZprimeToZHToZinvHall_narrow_M-3500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M4000",   "ZprimeToZHToZinvHall_narrow_M-4000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M4500",   "ZprimeToZHToZinvHall_narrow_M-4500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M5000",   "ZprimeToZHToZinvHall_narrow_M-5000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M5500",   "ZprimeToZHToZinvHall_narrow_M-5500_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M6000",   "ZprimeToZHToZinvHall_narrow_M-6000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M7000",   "ZprimeToZHToZinvHall_narrow_M-7000_TuneCP5_13TeV-madgraph-pythia8"),
          ('XZH',            "ZprimeToZHToZinvHall_narrow_M8000",   "ZprimeToZHToZinvHall_narrow_M-8000_TuneCP5_13TeV-madgraph-pythia8"), 
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-600",  "Zprime_VBF_Zh_Zlephinc_narrow_M-600_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-800",  "Zprime_VBF_Zh_Zlephinc_narrow_M-800_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1000", "Zprime_VBF_Zh_Zlephinc_narrow_M-1000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1200", "Zprime_VBF_Zh_Zlephinc_narrow_M-1200_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1400", "Zprime_VBF_Zh_Zlephinc_narrow_M-1400_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1600", "Zprime_VBF_Zh_Zlephinc_narrow_M-1600_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-1800", "Zprime_VBF_Zh_Zlephinc_narrow_M-1800_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-2000", "Zprime_VBF_Zh_Zlephinc_narrow_M-2000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-2500", "Zprime_VBF_Zh_Zlephinc_narrow_M-2500_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-3000", "Zprime_VBF_Zh_Zlephinc_narrow_M-3000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-3500", "Zprime_VBF_Zh_Zlephinc_narrow_M-3500_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-4000", "Zprime_VBF_Zh_Zlephinc_narrow_M-4000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-4500", "Zprime_VBF_Zh_Zlephinc_narrow_M-4500_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-5000", "Zprime_VBF_Zh_Zlephinc_narrow_M-5000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-5500", "Zprime_VBF_Zh_Zlephinc_narrow_M-5500_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-6000", "Zprime_VBF_Zh_Zlephinc_narrow_M-6000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-7000", "Zprime_VBF_Zh_Zlephinc_narrow_M-7000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zlephinc_narrow_M-8000", "Zprime_VBF_Zh_Zlephinc_narrow_M-8000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-600",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-600_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-800",  "Zprime_VBF_Zh_Zinvhinc_narrow_M-800_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1000", "Zprime_VBF_Zh_Zinvhinc_narrow_M-1000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1200", "Zprime_VBF_Zh_Zinvhinc_narrow_M-1200_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1400", "Zprime_VBF_Zh_Zinvhinc_narrow_M-1400_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1600", "Zprime_VBF_Zh_Zinvhinc_narrow_M-1600_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-1800", "Zprime_VBF_Zh_Zinvhinc_narrow_M-1800_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-2000", "Zprime_VBF_Zh_Zinvhinc_narrow_M-2000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-2500", "Zprime_VBF_Zh_Zinvhinc_narrow_M-2500_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-3000", "Zprime_VBF_Zh_Zinvhinc_narrow_M-3000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-3500", "Zprime_VBF_Zh_Zinvhinc_narrow_M-3500_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-4000", "Zprime_VBF_Zh_Zinvhinc_narrow_M-4000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-4500", "Zprime_VBF_Zh_Zinvhinc_narrow_M-4500_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-5000", "Zprime_VBF_Zh_Zinvhinc_narrow_M-5000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-5500", "Zprime_VBF_Zh_Zinvhinc_narrow_M-5500_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-6000", "Zprime_VBF_Zh_Zinvhinc_narrow_M-6000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-7000", "Zprime_VBF_Zh_Zinvhinc_narrow_M-7000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('XZHVBF',        "Zprime_VBF_Zh_Zinvhinc_narrow_M-8000", "Zprime_VBF_Zh_Zinvhinc_narrow_M-8000_TuneCP5_PSweights_13TeV-madgraph-pythia8"),
          ('SingleMuon',     "SingleMuon_$RUN",              "SingleMuon/$RUN"                                                  ),
          ('EGamma',         "EGamma_$RUN",                  "EGamma/$RUN"                                              ),
          ('MET',            "MET_$RUN",                     "MET/$RUN"                                                         )]

  sample_dict = [(d,s,p.replace('*','.*').replace('$MASS','(\d+)').replace('$RUN','(Run201\d[A-H])')) for d,s,p in sample_dict] # convert to regex pattern
  if args.verbose:
    print "getSampleShortName: %s"%(dasname)
  dasname = dasname.replace('__','/').lstrip('/')
  for subdir, samplename, pattern in sample_dict:
    matches = re.findall(pattern,dasname)
    if matches:
      samplename = samplename.replace('$MASS',matches[0]).replace('$RUN',matches[0])
      if args.verbose:
         print "getSampleShortName: MATCH! subdir=%s, samplename=%s, pattern=%s"%(subdir, samplename, pattern)
      return subdir, samplename
  print bcolors.BOLD + bcolors.WARNING + '[WN] getSampleShortName: did not find subdir and short sample name for "%s"! Will save in subdir \'unknown\''%(dasname) + bcolors.ENDC 
  return "unknown", dasname.replace('/','__')
  
def getSubdir(dir):
  for subdir in subdirs:
    if '*' in subdir or '?' in subdir:
      if fnmatch(dir,subdir):
        return subdir
    else:
      if subdir==dir[:len(subdir)]:
        return subdir
  return "unknown"
  
def matchSampleToPattern(sample,patterns):
  """Match sample name to some pattern."""
  sample = sample.lstrip('/')
  if not isinstance(patterns,list):
    patterns = [patterns]
  for pattern in patterns:
    if '*' in pattern or '?' in pattern:
      if fnmatch(sample,pattern+'*'):
        return True
    else:
      if pattern in sample[:len(pattern)+1]:
        return True
  return False
  
def ensureDirectory(dirname):
  """Make directory if it does not exist."""
  if not os.path.exists(dirname):
    os.makedirs(dirname)
    print '>>> made directory "%s"'%(dirname)
    if not os.path.exists(dirname):
      print '>>> failed to make directory "%s"'%(dirname)
  return dirname
  
headeri = 0
def header(year,channel,tag=""):
  global headeri
  title  = "%s, %s"%(year,channel)
  if tag: title += ", %s"%(tag.lstrip('_'))
  string = ("\n\n" if headeri>0 else "") +\
           "   ###%s\n"    % ('#'*(len(title)+3)) +\
           "   #  %s  #\n" % (title) +\
           "   ###%s\n"    % ('#'*(len(title)+3))
  headeri += 1
  return string


if __name__ == '__main__':
    
    print
    main(args)
    print
