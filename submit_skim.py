#! /usr/bin/env python

import os, re, glob
from commands import getoutput
from fnmatch import fnmatch
import itertools
from argparse import ArgumentParser
import checkFiles
from checkFiles import getSampleShortName, matchSampleToPattern, header, ensureDirectory

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument('-f', '--force',   dest='force', action='store_true', default=False,
                                         help="submit jobs without asking confirmation" )
  parser.add_argument('-y', '--year',    dest='years', choices=[2016,2017,2018], type=int, nargs='+', default=[2017], action='store',
                                         help="select year" )
  parser.add_argument('-c', '--channel', dest='channels', choices=['ll'], type=str, nargs='+', default=['ll'], action='store',
                                         help="channels to submit" )
  parser.add_argument('-s', '--sample',  dest='samples', type=str, nargs='+', default=[ ], action='store',
                                         help="filter these samples, glob patterns (wildcards * and ?) are allowed." )
  parser.add_argument('-x', '--veto',    dest='vetos', nargs='+', default=[ ], action='store',
                                         help="veto this sample" )
  parser.add_argument('-t', '--type',    dest='type', choices=['data','mc'], type=str, default=None, action='store',
                                         help="filter data or MC to submit" )
  parser.add_argument('-T', '--tes',     dest='tes', type=float, default=1.0, action='store',
                                         help="tau energy scale" )
  parser.add_argument('-L', '--ltf',     dest='ltf', type=float, default=1.0, action='store',
                                         help="lepton to tau fake energy scale" )
  parser.add_argument('-J', '--jtf',     dest='jtf', type=float, default=1.0, action='store',
                                         help="jet to tau fake energy scale" )
  parser.add_argument('-d', '--das',     dest='useDAS', action='store_true', default=False,
                                         help="get file list from DAS" )
  parser.add_argument('-n', '--njob',    dest='nFilesPerJob', action='store', type=int, default=-1,
                                         help="number of files per job" )
  parser.add_argument('-q', '--queue',   dest='queue', choices=['all.q','short.q','long.q'], type=str, default=None, action='store',
                                         help="select queue for submission" )
  parser.add_argument('-m', '--mock',    dest='mock', action='store_true', default=False,
                                         help="mock-submit jobs for debugging purposes" )
  parser.add_argument('-v', '--verbose', dest='verbose', default=False, action='store_true',
                                         help="set verbose" )
  args = parser.parse_args()
  checkFiles.args = args
else:
  args = None

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def checkExistingFiles(outdir,channel,njob):
    filelist = glob.glob("%s/*%s.root"%(outdir,channel))
    nfiles = len(filelist)
    if nfiles>njob:
      print bcolors.BOLD + bcolors.WARNING + "Warning! There already exist %d files, while the requested number of files per job is %d"%(nfiles,njob) + bcolors.ENDC
      remove = raw_input("Do you want to remove the extra files? [y/n] ")
      if remove.lower()=='y':
        for filename in sorted(filelist):
          matches = re.findall(r"_(\d+)_%s.root"%(channel),filename)
          if matches and int(matches[0])>njob:
            print "Removing %s..."%(filename)
            os.remove(filename)
      else:
        print "Not removing extra files. Please make sure to delete the %d last files before hadd'ing."%(nfiles-njob)
    

def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))
    

def getFileListLocal(dataset):
    """Get list of files from local directory."""
    filename = "/work/pbaertsc/heavy_resonance/NanoTreeProducer/filelist/filelist_%s.txt"%dataset.lstrip('/').replace('/','__')
    filelist = [ ]
    if os.path.exists(filename):
      with open(filename,'r') as file:
        for line in file:
          if '#' not in line:
            filelist.append(line.rstrip('\n'))
    return filelist
    

def saveFileListLocal(dataset,filelist):
    """Save a list of files to a local directory."""
    filename = "filelist/filelist_%s.txt"%dataset.replace('/','__')
    with open(filename,'w+') as file:
      for line in filelist:
        file.write(line+'\n')
    return filename
    

def getFileListDAS(dataset):
    """Get list of files from DAS."""
    dataset  = dataset.replace('__','/')
    instance = 'prod/global'
    if 'USER' in dataset:
        instance = 'prod/phys03'
    #cmd='das_client --limit=0 --query="file dataset=%s instance=%s"'%(dataset,instance)
    cmd = 'das_client --limit=0 --query="file dataset=%s instance=%s status=*"'%(dataset,instance)
    if args.verbose:
      print "Executing ",cmd
    cmd_out  = getoutput( cmd )
    tmpList  = cmd_out.split(os.linesep)
    filelist = [ ]
    for line in tmpList:
      if '.root' in line: 
        #filelist.append("root://xrootd-cms.infn.it/"+line)
        filelist.append("root://cms-xrd-global.cern.ch/"+line)
    return filelist 
    

def getFileListPNFS(dataset):
    """Get list of files from PSI T3's SE."""
    dataset  = dataset.replace('__','/')
    user     = 'ytakahas'
    cmd      = 'ls %s'%(dataset)
    if args.verbose:
      print "Executing ",cmd
    cmd_out  = getoutput( cmd )
    tmpList  = cmd_out.split(os.linesep)
    filelist = [ ]
    for line in tmpList:
      if '.root' in line:
        filelist.append("dcap://t3se01.psi.ch:22125/"+dataset+'/'+line.rstrip())
    return filelist
    

def createJobs(jobsfile, infiles, outdir, name, nchunks, channel, year, **kwargs):
    """Create file with commands to execute per job."""
    tes     = kwargs.get('tes', 1.)
    ltf     = kwargs.get('ltf', 1.)
    jtf     = kwargs.get('jtf', 1.)
    cmd = 'python job_skim.py -i %s -o %s -N %s -n %i -c %s -y %s'%(','.join(infiles),outdir,name,nchunks,channel,year)
    if tes!=1.:
      cmd += " --tes %.3f"%(tes)
    if ltf!=1.:
      cmd += " --ltf %.3f"%(ltf)
    if jtf!=1.:
      cmd += " --jtf %.3f"%(jtf)
    if args.verbose:
      print cmd
    jobsfile.write(cmd+'\n')
    return 1
    

def submitJobs(jobName, jobList, nchunks, outdir, batchSystem):
    """Submit job."""
    if args.verbose:
      print 'Reading joblist...'
      print jobList
    extraopts = "-t 1-%s -N %s -o %s/logs/ -e %s/logs/" %(nchunks,jobName,outdir,outdir)
    if args.queue:
      extraopts += " -q %s"%(args.queue)
    #subCmd = 'qsub -t 1-%s -o logs nafbatch_runner_GEN.sh %s' %(nchunks,jobList)
    subCmd = 'qsub %s %s %s'%(extraopts,batchSystem,jobList)
    subCmd = subCmd.rstrip()
    print bcolors.BOLD + bcolors.OKBLUE + "Submitting %d jobs with \n    %s"%(nchunks,subCmd) + bcolors.ENDC
    if not args.mock:
      os.system(subCmd)
    return 1
    

def main():
    
    channels    = args.channels
    years       = args.years
    tes         = args.tes
    ltf         = args.ltf
    jtf         = args.jtf
    batchSystem = 'psibatch_runner.sh'
    tag         = ""
    
    if tes!=1.:
      tag += "_TES%.3f"%(tes)
    if ltf!=1.:
      tag += "_LTF%.3f"%(ltf)
    if jtf!=1.:
      tag += "_JTF%.3f"%(jtf)
    tag = tag.replace('.','p')
    
    for year in years:
      
      # READ SAMPLES
      directories = [ ]
      samplelist  = "samples_%s.cfg"%(year)
      with open(samplelist, 'r') as file:
        for line in file:
          line = line.rstrip().lstrip().split(' ')[0].rstrip('/')
          if line[:2].count('#')>0: continue
          if line=='': continue
          if args.samples and not matchSampleToPattern(line,args.samples): continue
          if args.vetos and matchSampleToPattern(line,args.vetos): continue
          if args.type=='mc' and any(s in line[:len(s)+2] for s in ['SingleMuon','SingleElectron','EGamma','MET']): continue
          if args.type=='data' and not any(s in line[:len(s)+2] for s in ['SingleMuon','SingleElectron','EGamma','MET']): continue
          directories.append(line)
      #print directories
      
      for channel in channels:
        print header(year,channel,tag)
        
        # SUBMIT SAMPLES
        for directory in directories:
            
            if args.verbose:
              print "\ndirectory =",directory
            
            # FILTER
    
            print bcolors.BOLD + bcolors.OKGREEN + directory + bcolors.ENDC
            
            # FILE LIST
            files = [ ]
            name  = directory.split('/')[-3].replace('/','') + '__' + directory.split('/')[-2].replace('/','') + '__' + directory.split('/')[-1].replace('/','')
            if not args.useDAS:
                files = getFileListLocal(directory)
            if not files:
              if not args.useDAS:
                print "Getting file list from DAS..."
              if 'pnfs' in directory:
                files = getFileListPNFS(directory)
              else:
                files = getFileListDAS(directory)
              if files:
                saveFileListLocal(name,files)
            if not files:
              print bcolors.BOLD + bcolors.WARNING + "Warning!!! FILELIST empty" + bcolors.ENDC
              continue
            elif args.verbose:
              print "FILELIST = "+files[0]
              for file in files[1:]:
                print "           "+file
            
            # JOB LIST
            ensureDirectory('joblist_skim')
            jobList      = 'joblist_skim/joblist_%s_%s%s.txt'%(name,channel,tag)
            print "Creating job file %s..."%(jobList)
            jobName      = getSampleShortName(directory,year)[1]
            jobName     += "_%s_%s"%(channel,year)+tag
            jobs         = open(jobList,'w')
            outdir       = ensureDirectory("/work/pbaertsc/heavy_resonance/output_skim_%s/%s"%(year,name))
            ensureDirectory(outdir+'/logs/')
            
            # NFILESPERJOBS
            nFilesPerJob = 1
            if nFilesPerJob<1:
              for default, patterns in nFilesPerJob_defaults:
                if matchSampleToPattern(directory,patterns):
                  nFilesPerJob = default
                  break
              else:
                nFilesPerJob = 4 # default
            if args.verbose:
              print "nFilesPerJob = %s"%nFilesPerJob
            filelists = list(split_seq(files,nFilesPerJob))
            
            # CREATE JOBS
            nChunks = 0
            checkExistingFiles(outdir,channel,len(filelists))
            #filelists = list(split_seq(files,1))
            for file in filelists:
            #print "FILES = ",f
                createJobs(jobs,file,outdir,name,nChunks,channel,year=year,tes=tes,ltf=ltf,jtf=jtf)
                nChunks = nChunks+1
            jobs.close()
            
            # SUBMIT
            if args.force:
              submitJobs(jobName,jobList,nChunks,outdir,batchSystem)
            else:
              submit = raw_input("Do you also want to submit %d jobs to the batch system? [y/n] "%(nChunks))
              if submit.lower()=='force':
                submit = 'y'
                args.force = True
              if submit.lower()=='quit':
                exit(0)
              if submit.lower()=='y':
                submitJobs(jobName,jobList,nChunks,outdir,batchSystem)
              else:
                print "Not submitting jobs"
            print



if __name__ == "__main__":
    print
    main()
print "Done\n"
