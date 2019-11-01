# LD-annot
A bioinformatics tool to automatically provide annotations for genes included in DNA blocks in linkage disequilibrium with candidate SNPs.
## LD-annot
### Email: jprunier.1@gmail.com or arnaud.droit@crchudequebec.ulaval.ca

LD-annot estimates experiment-specific linkage disequilibrium to delineate regions genetically linked to each genetic markers from a list of polymorphisms (most often candidate SNPs from GWAS) and provide coordinates and annotations for genes included or overlapping such regions.


## Citing LD-annot
Prunier J., Lemaçon A., Bastien A., Jafarikia M., Porth I., Robert C and Droit A. _submitted_. **LD-Annot**: a bioinformatics tool to automatically provide annotations for genes in linkage disequilibrium with candidate SNPs.


## Implementation and requirements
LD-annot is meant to be easy to install and use for biologists without advanced bioinformatics skills. It simply requires to be downloaded and placed into a folder. LD-annot is actually divided into to scripts:
1) a python script (LD-annot.py) written in Python3 (not 2.7 that will not run properly and delivered a error message)
2) a bash script (calculLD.sh) that need to be in the same folder and will be invoked by LD-annot.py

The tool also needs PLINK1.9 to run. If you don't have this version installed on your computer, you may find it here: https://www.cog-genomics.org/plink2 , or from this repository (plink_linux_x86_64_20190304.zip or plink_mac_20191028.zip). PLINK1.9 is under GNU GENERAL PUBLIC LICENSE (v3, 29 June 2007).
To install it, simply follow the instructions repeated below.


## Install
### Installing LD-annot on Unix-based OS (Linux & Mac):
####Preliminary steps for MacOS users:
If it's not installed in your system, please install gawk and gnu-sed using your favorite procedure (either brew or ...).

Afterwards run:
```
alias awk='gawk'
alias sed='gsed'
```

#### Installing the LD-annot tool:
From github, download and place LD-annot.tar.gz in the desired folder.
Then extract it here running:
```
gunzip LD-annot.tar.gz
tar -xvf LD-annot.tar
cd LD-annot/
chmod +x LD-annot.py
```

#### Installing PLINK1.9 (if needed)
Note that LD-annot invokes the plink function. If you're also installing PLINK1.9, please run from the Dowloads folder where it should have been downloaded:
```
mkdir ~/bin #if you don't already have one
unzip plink_linux_x86_64_20190304.zip
mv plink ~/bin/
```

Then, you can either change your $PATH variable only for the ongoing session by doing:
```
export PATH=~/bin/:$PATH
```

Alternatively, the $PATH variable can be changed in the .bash_profile which will add the path to "\~/bin" into the $PATH. To do so, the .bash_profile file located into the home folder should be edited and "~/bin:" should be added to the PATH. The line should look something like this at the end :

```
PATH=~/bin:<other paths>:$PATH

```
### Installing LD-annot on Windows OS (10 and following):
The best way to make LD-annot working without nightmares on a windows OS is actually to enable the developper mode and install the Bash shell command-line tool and use it as if it were a linux OS.
This installation can be done by following these steps: https://www.windowscentral.com/how-install-bash-shell-command-line-windows-10.
Afterwards, install unzip and the numpy python package by running the following commands:
```
sudo apt-get install unzip
sudo apt-get install python3-pip
sudo pip3 install 'numpy==1.15.4'
```
Then, download the LINUX plink1.9 from https://www.cog-genomics.org/plink2 and install plink1.9 running:
```
mkdir ~/bin #if you don't already have one
unzip plink_linux_x86_64_20190304.zip
mv plink ~/bin/
export PATH=~/bin/:$PATH
```

Then, the tool itself:
From github, download and place LD-annot.tar.gz in the desired folder. Then extract it here running:
```
gunzip LD-annot.tar.gz
tar -xvf LD-annot.tar
cd LD-annot/
chmod +x LD-annot.py
```


## Running LD-annot
The easiest way to run LD-annot is to move/copy your data within the folder containing LD-annot.4.py and calculLD.1.sh scripts. This folder must also include the list of candidate SNPs as well as the annotation gff/gtf/gff3 file. File examples are provided in the "data" subdirectory but have to be moved into the main folder (encompassing Ld-annot.4.py and calculLD.1.py).

LD-annot runs using only one command line which provide path to files and required parameters.

##### When data come from a vcf file, run the following command line:
```
python3 LD-annot0.4.py ex_data.vcf ex_annotations.gff ex_candidate_SNPs.txt type thr output
```
where "geno.vcf" is the data file, "annot.gff3" is the file containing genomic coordinates and annotations for features (most often genes), "candidate" is a list of chromosomes and positions for candidate polymosphisms, "type" is the feature (mRNA, CDS, gene), "thr" is the threshold for r2, and "output" is an output name specified by the user.



##### When data come from SNP genotyping, files containing genotypes per individual should be placed into a folder located in the same folder as LD-annot.py and calculLD.sh:
```
python3 LD-annot0.4.py PathToSnpFiles ex_annotations.gff ex_candidate_SNPs.txt type thr output SNP_Map
```

where "PathToSnpFiles" is the path to the folder containing all data file, "annot.gff3" is the file containing genomic coordinates and annotations for features (most often genes), "candidate" is a list of chromosomes and positions for candidate polymosphisms, "type" is the feature (mRNA, CDS, gene), "thr" is the threshold for r2, "output" is an output name specified by the user, and "SNP_Map" is a map file indicating chromosome and positions for all SNPs genotyped using the SNP-chip.


**Note** that the chromosome identification should be consistent among the various files. Most often, it is a number maybe prefixed with a “chr”. A format checking step is performed by LD-annot and generates error messages pointing at corrupt files and probable causes.
Also, there is no need to specify "python3" if it is your default python version.



## How LD-annot works

Most researchers want to get annotations for genes close and/or genetically linked to candidate polymorphisms detected using Genome-Wide Association Analyses or other approaches allowing to identify markers likely related to phenotypic or environmental variations of interest. However, the estimator of linkage disequilibrium (r2) is not stable within a species but varies according to population history, actual recombination rate, minor allele frequency and sampling, for instance. Hence, r2 MUST be estimated for each markers and within each experiment.
LD-annot estimates the extent of the genomic region in LD with each candidate polymorphism according to the threshold specified by the user and provides annotations for genes within or overlapping this region (see figure). It also calculates an average distance in bp between markers in LD with r2 > threshold that is used to estimate the region when there's no other markers around the candidate polymorphism allowing to delineate such region. In this case, a flag "\_alone" is added to the SNP name in the output file to signal it.


<pre>
features:                gene1     gene2                   gene3         gene4  
position:                  V         V                       V             V    
sequence:           ------------------------------------------------------------
SNPs:                .  .  .      .   .  .     . .    .  .  ..  . .   .     .  .
                                                 ^
                                            CANDIDATE SNP

region considered
for r2 > 0.9                      |________________________________|  


region for
r2 > 0.8             |__________________________________________________________|

</pre>


The output file is a tab delimited text file including in this order: SNP name, chromosome name, start position for feature (gene, transcript...) in LD, end position for feature in LD, feature annotation according to the gff file.
Chromosome name can be a contig name in case of draft assembly.

## Performances
LD-annot has been developped to be deployed on common desk or laptops computers even though it can also be deployed on linux servers. Using a 4CPU cores and 8 Gbytes of RAM, LD-annot ran for 14 minutes to analyze 14,374,089 SNPs and a list of 1536 candidate ones. If a user wishes to test a range of thresholds for r2 (usually between 0.6 and 0.99) and different features (gene, transcript, exon...) from the same dataset, the program will not rerun the entire algorithm but only the last steps and thus save time to the user. See table published with the article for more numbers regarding the program performances using a standard laptop.





