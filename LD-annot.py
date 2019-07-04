#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

import sys, fileinput
import string
import math
import time
import sys
import operator
import copy
import numpy as np
import os


def documentation():
    print('''
    There are missing inputfile in the command

    Usage:
	python LD-annot.py data annotation-file candidate-marker-list type threshold output_name SNP-map-file*
	
    data: either a vcf file or a path to genotype files from SNPchips
    annotation-file: a gff file with annotations
    candidate-marker: a list of candidate variant with chr/contig name, and position
    type: type of region the user wants to use; either "gene", "mRNA", "CDS"
    threshold: r2 (linkage) threshold at which stops the range of interest.
    output_name: selfexplaining name
    SNP-map-file: only required with SNPchips data

    ''')

try:
    da = sys.argv[1]
    an = sys.argv[2]
    cm = sys.argv[3]
    ty = sys.argv[4]
    thr = sys.argv[5]
    o = sys.argv[6]
    if da[-4:] != '.vcf':
        sm = sys.argv[7]
    else:
        pass
        
except:
    documentation()
    sys.exit(1)


lf = os.listdir()

if "checkpoint" not in lf:
    if da[-4:] != '.vcf':

        #format testing for SNPchips data
        os.chdir(da)
        files = os.listdir('./')
        print("File checked to verify format:")
        print(files[0])
        t = files[0]
        f = open(t,'r')
        a = 0
        ln=[] #list of markers names
        for line in f:
            if a > 10:
                line = line.replace('-\t','N\t')
                l = line.strip().split('\t')
                if len(l[2]) == 1 :
                    if len(l[3]) == 1:
                        pass
                    else:
                        print("There's a problem with input files, please make sure your files\nare tabulated separated and alleles are in the third and fourth column")
                        exit(1)
                else:
                    print("There's a problem with input files, please make sure your files\nare tabulated separated and alleles are in the third and fourth column")
                    exit(1)
                ln.append(l[0])
            else:
                a += 1
                pass
            
        f.close()
        os.chdir('../')

        #testing if chromosomes names fit between map and SNP files
        print("Checking format for:")
        print("\t",str(sm))
        map = open(sm,'r')
        lmap = []
        lkmap = []
        line = map.readline()
        for line in map:
            l = line.strip().split('\t')
            lmap.append(l[1])
            lkmap.append(l[2])

        for i in ln:
            if i not in lmap:
                print("genotyped SNPs are not mapped.")
            else:
                pass
        map.close()

        #testing if chromosomes names fit between gff and SNP files 
        print("Checking format for:")
        print('\t',an)
        gff =open(an,'r')
        lannot = []
        for line in gff:
            if line[0] == '#':
                pass
            else:
                l = line.strip().split('\t')
                lannot.append(l[0])
        gff.close()
    
    
        miss = []
        for i in lkmap:
            if i in lannot:
                pass
            else:
                miss.append(i)
        
        umiss = list(set(miss))
        print("There's no annotations for chromosome:")
        print('\t',','.join(umiss))
        print("if this is not empty, At least some SNPs won't have annotations which might be related to discrepancies regarding chromosome names.")
        print("Maybe you should verify chromosome names in the annotation file.",'\n')
        

        #list of chromosome names from candidate SNPs
        print("checking format for:")
        print('\t',cm)
        can = open(cm,'r')
        lcan = []
        for line in can:
            l = line.strip().split('\t')
            if l[0] == 'CHROM':
                pass
            else:
                if l[0].isnumeric() or l[0] == 'X' or l[0] == 'Y':
                    if l[1].isnumeric():
                        lcan.append(l[0])
                    else:
                        print("SNP Position column doesn't contain only numbers")
                        exit(1)
                else:
                    print("Chromosome column contains other names than a number or X or Y")
        
        miss = []
        for i in lcan:
            if i in lkmap:
                pass
            else:
                miss.append(i)
                
        umiss = list(set(miss))
        print("These candidate may not be mapped:")
        print(','.join(umiss))
        print("if this is not empty, At least some SNPs won't have genome location, this might be related to discrepancies regarding chromosome names.")
        print("Maybe you should verify chromosome names in the those files.")

        
    #that's where starts the checkup of data included into a vcf file
    else:
    #format testing for vcf data
        print("checking format for:")
        print('\t',da)
        f = open(da,'r')
        a = 0
        ln = []
        for line in f:
            l = line.strip().split('\t')
            if line[0] == '#CHROM':
                a += 1
                if l[1] !=  'POS' or l[3] != REF or l[4] != ALT:
                    print("There's a problem with the vcf input file, please verify your file")
                    exit(1)
                else:
                    pass
            elif a >= 1:
                if l[0].isnumeric() or l[0] == 'X' or l[0] == 'Y':
                    ln.append(l[0])
                else:  
                    print("chromosome numbers should be numbers or X or Y")
                    exit(1)
            else:
                pass


        #format testing for congruence between chromosome names over data and annotation
        #list of chromosome names from candidate SNPs
        print("checking format for:")
        print('\t',cm)
        can = open(cm,'r')
        lcan = []
        for line in can:
            l = line.strip().split('\t')
            if l[0] == 'CHROM':
                pass
            else:
                if l[0].isnumeric() or l[0] == 'X' or l[0] == 'Y':
                    if l[1].isnumeric():
                        lcan.append(l[0])
                    else:
                        print("Position column doesn't contain only numbers")
                        exit(1)
                else:
                    print("Chromosome column contains other names than a number or X or Y")
            

        #list of chromosome names from annotation file
        print("checking format for:")
        print('\t',an)
        gff = open(an,'r')
        lannot = []
        for line in gff:
            if line[0] == '#':
                pass
            else:
                l = line.strip().split('\t')
                lannot.append(l[0])
        gff.close()

        #real test for congruence
        for i in ln:
            if i in lannot:
                pass
            else:
                print("At least some SNPs are not in the annotation file, might be related to discrepancies regarding chromosome names")
                exit(1)
    
            if i in lcan:
                pass
            else:
                print("None of the SNPs are candidate, might be related to discrepancies regarding chromosome names")
                exit(1)

    c = open("checkpoint", 'w')
    c.write("verif_format\n")
    c.close()


    #run the bash script

    if da[-4:] != '.vcf':
        os.system('bash calculLD.sh %s %s %s %s %s %s' % (da, an, cm, ty, thr,sm))
    else:
        os.system('bash calculLD.sh %s %s %s %s %s' % (da, an, cm, ty, thr))


    
    #continuation of the python procedure
    thr = sys.argv[5] # threshold
    kind = sys.argv[4] #type
    temp = open('meanLD','r') #meanLD
    line = temp.readline()
    l = line.strip().split()
    mean = int(float(l[0]))

    #dictionnary of all genes annotations
    f = open(sys.argv[2],'r') #gff file
    dica = {}
    for line in f:
        if line[0] != '#':
            l = line.strip().split('\t')
            if l[2] == kind:
                reg = l[0]+'_'+l[3]+'_'+l[4]
                dica[reg] = l[-1]

    #list of candidate SNPs
    #SNP = 'chr_pos'
    g = open(sys.argv[3],'r')
    lsc = []
    line = g.readline()

    for line in g:
        l = line.strip().split('\t')
        SNP = l[0]+'_'+l[1]
        lsc.append(SNP)

    #dictionnary of candidate regions
    #SNP = 'chr_pos'

    h = open('mydata.ld','r')
    dics = {}
    for line in h:
        l = line.strip().split('\t')
        SNP1 = l[0]+'_'+l[1]
        SNP2 = l[3]+'_'+l[4]
        if SNP1 in lsc:
            if float(l[-1]) >= float(thr):
                if SNP1 in dics.keys():   
                    dics[SNP1].append(l[4])
                else:
                    dics[SNP1] = [l[4]]

        if SNP2 in lsc:
            if float(l[-1]) >= float(thr):
                if SNP2 in dics.keys():
                    dics[SNP2].append(l[1])
                else:
                    dics[SNP2] = [l[1]]
    #at the end we get a dictionnary with position for SNPs in linkage

    #writing output

    o = open(sys.argv[6],'w')

    for i in lsc:
        j = i.split('_')
        if i not in dics.keys():
            z = str(i)+'_alone'
            dics[z] = [(int(j[1]) - mean) , (int(j[1]) + mean)]
        else:
            pass
        

    for i in dics:
        j = i.split('_')
        up = int(max(dics[i]))
        down = int(min(dics[i]))
        for k in dica.keys():
            l = k.split('_')
            if j[0] == l[0]:
                if int(l[1]) < down < int(l[2]) or int(l[1]) < up < int(l[2]) or down < int(l[1]) < up or down < int(l[2]) < up :
                    res = [str(i),str(l[0]),str(l[1]),str(l[2])]
                    res.append(dica[k])
                    o.write('\t'.join(res)+'\n')
                else:
                    pass
            else:
                pass

    f.close()
    g.close()
    h.close()
    o.close()


#here start the pipeline when format has already been checked
#as written in the checkpoint file
else:


    #run the bash script

    if da[-4:] != '.vcf':
        os.system('bash calculLD.sh %s %s %s %s %s %s' % (da, an, cm, ty, thr,sm))
    else:
        os.system('bash calculLD.sh %s %s %s %s %s' % (da, an, cm, ty, thr))


    #continuation of the python procedure

    thr = sys.argv[5] # threshold
    kind = sys.argv[4] #type
    temp = open('meanLD','r') #meanLD
    line = temp.readline()
    l = line.strip().split()
    mean = int(float(l[0]))

    #dictionnary of all genes annotations
    f = open(sys.argv[2],'r') #gff file
    dica = {}
    for line in f:
        if line[0] != '#':
            l = line.strip().split('\t')
            if l[2] == kind:
                reg = l[0]+'_'+l[3]+'_'+l[4]
                dica[reg] = l[-1]

    #list of candidate SNPs
    #SNP = 'chr_pos'
    g = open(sys.argv[3],'r')
    lsc = []
    line = g.readline()

    for line in g:
        l = line.strip().split('\t')
        SNP = l[0]+'_'+l[1]
        lsc.append(SNP)

    #dictionnary of candidate regions
    #SNP = 'chr_pos'

    h = open('mydata.ld','r')
    dics = {}
    for line in h:
        l = line.strip().split('\t')
        SNP1 = l[0]+'_'+l[1]
        SNP2 = l[3]+'_'+l[4]
        if SNP1 in lsc:
            if float(l[-1]) >= float(thr):
                if SNP1 in dics.keys():        
                    dics[SNP1].append(l[4])
                else:
                    dics[SNP1] = [l[4]]

        if SNP2 in lsc:
            if float(l[-1]) >= float(thr):
                if SNP2 in dics.keys():
                    dics[SNP2].append(l[1])
                else:
                    dics[SNP2] = [l[1]]
    #at the end we get a dictionnary with position for SNPs in linkage



    #writing output

    o = open(sys.argv[6],'w')
    
    for i in lsc:
        j = i.split('_')
        if i not in dics.keys():
            z = str(i)+'_alone'
            dics[z] = [(int(j[1]) - mean) , (int(j[1]) + mean)]
        else:
            pass


    for i in dics:
        j = i.split('_')
        up = int(max(dics[i]))
        down = int(min(dics[i]))
        for k in dica.keys():
            l = k.split('_')
            if j[0] == l[0]:
                if int(l[1]) < up < int(l[2]) or int(l[1]) < down < int(l[2]) or down < int(l[1]) < up or down < int(l[2]) < up:
                    res = [str(i),str(l[0]),str(l[1]),str(l[2])]
                    res.append(dica[k])
                    o.write('\t'.join(res)+'\n')
                else:
                    pass
            else:
                pass

    f.close()
    g.close()
    h.close()
    o.close()
