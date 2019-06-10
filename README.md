# LD-annot
A bioinformatics tool to automatically provide candidate SNPs with annotations for genes in linkage disequilibrium.
## LD-annot/0.1
## Email: jprunier.1@gmail.com

LD-annot estimates experiment-specific linkage disequilibrium to delineate regions genetically linked to each genetic markers from a list of polymorphisms (most often candidate SNPs from GWAS) and provide coordinates and annotations for genes included or overlapping such regions.

## Citing LD-annot
Prunier J, Lemaçon A, Bastien A, Mohsen, Porth I., Robert C and Droit A. submitted. LD-Annot: a bioinformatics tool to automatically provide candidate SNPs with annotations for genes in linkage disequilibrium.


## Implementation and requirements
LD-annot is meant to be easy to install and use for biologists without advanced bioinformatics skills. It simply requires to be downloaded and placed into a folder. LD-annot is actually divided into to scripts:
1) a python script (LD-annot.py) written in Python3 (not 2.7 that will not run properly and delivered a error message)
2) a bash script (calculLD.sh) that need to be in the same folder and will be invoked by LD-annot.py

The tool also needs PLINK1.9 to run. If you don't have this version installed on your computer, you may find here: https://www.cog-genomics.org/plink2 or here.
To install it, simply follow the instructions repeated below.


## Install
### Installing LD-annot
From github, download and place LD-annot.tar.gz in the desired folder.
Then extract it here:
```
gunzip LD-annot.tar.gz
tar -xvf LD-annot.tar
```
### Installing PLINK1.9 (if needed)
Note that LD-annot invokes the plink function. If you're also installing PLINK1.9, please run from the Dowloads folder where it should have been downloaded:
If you're using a linux operating system:
```
mkdir ~/bin #if you don't already have one
unzip plink_linux_x86_64_20190304.zip
cd plink_linux_x86_64_20190304.zip
mv plink ~/bin/
```
Then, you can either change your $PATH variable only for this session by doing:
```
export PATH=~/bin/:$PATH
```
Alternatively, the $PATH variable can be changed in the .bash_probile which will add the path to ~/bin/ into the $PATH. To do so, the .bash_profile file located into the home folder should be edited and "~/bin:" should be added to the PATH. The line should look something like this at the end :
```
PATH=~/bin:<other paths>:$PATH
```

## Running LD-annot




