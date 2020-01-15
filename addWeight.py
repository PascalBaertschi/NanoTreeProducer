#! /usr/bin/env python

import os, multiprocessing, math
import numpy as np
from array import array
from ROOT import TFile, TH1, TF1, TLorentzVector
import ROOT

from xsections import xsection

import optparse
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-y', '--year', action='store', type='string', dest='year',default='2017')
parser.add_option('-f', '--filter', action='store', type='string', dest='filter', default='')
parser.add_option('-s', '--single', action='store_true', dest='single', default=False)
parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False)

(options, args) = parser.parse_args()

filterset   = options.filter
singlecore  = options.single
verboseout  = options.verbose
year        = options.year


origin = '/work/pbaertsc/heavy_resonance/%s_noweight' %(year)
target = '/work/pbaertsc/heavy_resonance/Ntuples%s' %(year)

if year=='2016':
    LUMI=35920.
elif year=='2017':
    LUMI=41530.
elif year=='2018':
    LUMI=59740.


#LUMI  = 36220
#LUMI  = 27220 #24470
#LUMI = 12700
#Tau21_SF = { 1.03 : [0., 0.4], 0.88 : [0.4, 0.75], }

if not os.path.exists(origin):
    print 'Origin directory', origin, 'does not exist, aborting...'
    exit()
if not os.path.exists(target):
    print 'Target directory', target,'does not exist, aborting...'
    exit()


##############################

def processFile(sample_name, verbose=False):
    sample = sample_name.replace(".root", "")
    isMC = not ('SingleElectron' in sample or 'SingleMuon' in sample  or 'EGamma' in sample or 'MET' in sample or 'SinglePhoton' in sample)
    
    # Unweighted input
    ref_file_name = origin + '/' + sample_name
    if not os.path.exists(ref_file_name): 
        print '  WARNING: file', ref_file_name, 'does not exist, continuing'
        return True
    
    # Weighted output
    new_file_name = target + '/' + sample + '.root'
    #if os.path.exists(new_file_name):
    #    print '  WARNING: weighted file exists, overwriting'
        #return True
    
    new_file = TFile(new_file_name, 'RECREATE')
    new_file.cd()
    
    # Open old file
    ref_file = TFile(ref_file_name, 'READ')
    ref_hist = ref_file.Get('Events')
    try:
        totalEntries = abs(ref_hist.GetBinContent(1))
        #print "sample:",sample,"totalEntries:", totalEntries
    except:
        print '  ERROR: nEvents not found in file', sample
        exit(1)   
    # Cross section
    XS = xsection[sample]['xsec']*xsection[sample]['kfactor']*xsection[sample]['br']
    
    Leq = LUMI*XS/totalEntries if totalEntries > 0 else 0.
    print sample, ": Leq =", (Leq if isMC else "Data")
    
    # Variables declaration
    VH_mass = array('f', [1.0])
    eventWeightLumi = array('f', [1.0])# global event weight with lumi
    eventWeightLumi_nobtag = array('f', [1.0])
    # Looping over file content
    for key in ref_file.GetListOfKeys():
        obj = key.ReadObj()
        # Histograms
        if obj.IsA().InheritsFrom('TH1'):
            if verbose: print ' + TH1:', obj.GetName()
            new_file.cd()
            #if isMC:
            #    if not 'Events' in obj.GetName(): obj.Scale(Leq)
            obj.Write()
        # Tree
        elif obj.IsA().InheritsFrom('TTree'):
            nev = obj.GetEntriesFast()
            new_file.cd()
            new_tree = obj.CopyTree("")
            # New branches
            VH_massBranch = new_tree.Branch('VH_mass', VH_mass, 'VH_mass/F')
            eventWeightLumiBranch = new_tree.Branch('eventWeightLumi', eventWeightLumi, 'eventWeightLumi/F')
            eventWeightLumiBranch_nobtag = new_tree.Branch('eventWeightLumi_nobtag', eventWeightLumi_nobtag, 'eventWeightLumi_nobtag/F')
            # looping over events
            for event in range(0, obj.GetEntries()):
                if verbose and (event%10000==0 or event==nev-1): print ' = TTree:', obj.GetName(), 'events:', nev, '\t', int(100*float(event+1)/float(nev)), '%\r',
                #print '.',#*int(20*float(event)/float(nev)),#printProgressBar(event, nev)
                obj.GetEntry(event)
                # Initialize
                VH_mass[0] = -1.
                eventWeightLumi[0] = 1.
                eventWeightLumi_nobtag[0] = 1.
                
                VH_mass[0] = obj.X_mass
                # Weights
                if isMC:
                    eventWeightLumi_nobtag[0] = obj.EventWeight * Leq * obj.TopWeight
                    eventWeightLumi[0] = obj.EventWeight * Leq
                    eventWeightLumi[0] *= (obj.BTagAK4Weight_deep if obj.BTagAK4Weight_deep>0. and obj.BTagAK4Weight_deep<2. else 1.) * obj.TopWeight
                # Fill the branches
                VH_massBranch.Fill()
                eventWeightLumiBranch.Fill()
                eventWeightLumiBranch_nobtag.Fill()
            new_file.cd()
            new_tree.Write("", TObject.kOverwrite)
            if verbose: print ' '
        
        # Directories
        elif obj.IsFolder():
            subdir = obj.GetName()
            if verbose: print ' \ Directory', subdir, ':'
            new_file.mkdir(subdir)
            new_file.cd(subdir)
            for subkey in ref_file.GetDirectory(subdir).GetListOfKeys():
                subobj = subkey.ReadObj()
                if subobj.IsA().InheritsFrom('TH1'):
                    if verbose: print '   + TH1:', subobj.GetName()
                    new_file.cd(subdir)
                    #if isMC: subobj.Scale(Leq)
                    subobj.Write()
            new_file.cd('..')
    new_file.Close() 



jobs = []
if year=='2016':
    samples_subdir = ['DY','MET','ST','SingleElectron','SingleMuon','SinglePhoton','TT','VV','WJ','ZJ','XZH','XZHVBF']
elif year=='2017':
    samples_subdir = ['DY','MET','ST','SingleElectron','SingleMuon','SinglePhoton','TT','VV','WJ','XZH','XZHVBF','ZJ']
elif year=='2018':
    samples_subdir = ['DY','MET','ST','EGamma','SingleMuon','TT','VV','WJ','XZH','XZHVBF','ZJ']
for i in range(0,len(samples_subdir)):
    origin = '/work/pbaertsc/heavy_resonance/%s_noweight/%s'%(year,samples_subdir[i])
    target = '/work/pbaertsc/heavy_resonance/Ntuples%s/%s'%(year,samples_subdir[i])
    if not os.path.exists(target):
        os.makedirs(target)
    for d in os.listdir(origin):
        if not '.root' in d: continue
        if not d.replace(".root", "") in xsection.keys(): 
            print "no cross section for",d,"found in xsections.py"
            continue
        if len(filterset)>0 and not filterset in d:
            continue
        if singlecore:
            print " -", d
            processFile(d, verboseout)
        else:
            p = multiprocessing.Process(target=processFile, args=(d,verboseout,))
            jobs.append(p)
            p.start()
    #exit()
    
#print '\nDone.'

