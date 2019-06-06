#!/bin/bash

#Careful ...

#required when using the server.
#module load plink
#module load vcftools/0.1.13


#$1=all SNPs vcf file or a path to genotype files
#$2=gtf/gff or gff3 formated file
#$3=list of candidate SNPs: chr, pos
#$4=type of region for annotation. usually: 'gene','mRNA','CDS'
#$5=minimum value for r2 to consider a SNP linked to candidate
#$6=output name for output file.
#$7=SNP-map file

#get total number of autosomes.
NR=$(cut -f1 $2 | awk '{if ($1 ~ /^[:0-9:]/) print $1}' | sort -u | wc -l)


#make condition for either .vcf or .txt

if [ ${1: -4} != ".vcf" ]
then
#converting .txt to ped, map and fam files
	Step=$(grep "txt2ped" checkpoint)
	if [ "${Step}" != "txt2ped" ]
	then
		crdir=$PWD
		cd "$1"
		for i in *.txt; do echo "${i//.txt/}" >> toto; \
		echo "${i//.txt/}" >> toto; \
		echo -e 0 '\t' 0 '\t' 0 '\t' 0 >> toto ; \
		tail -n +12 $i | cut -f3,4 | tr '\n' '\t' >> toto; \
		echo '' >> toto; done; paste -d '\t' - - - - < toto > mydata.ped; sed -i 's/\t*$//g' mydata.ped; sed -i 's/-/0/g' mydata.ped; \
		
		rm toto
		
		mv mydata.ped $crdir
		cd $crdir
		awk '{print $3"\t"$3"."$4"\t"".""\t"$4}' < $6 | tail -n +2 > mydata.map
		for i in $1*txt; do echo "${i//.txt/}\t0\t0\t0\t-9" >> mydata.fam; done
		printf "txt2ped\n" >> checkpoint	
	else
		printf "\t\ttxt2ped already done\n"
	fi
	

	Step=$(grep "bedfiles" checkpoint)
	if [ "${Step}" != "bedfiles" ]
        	then
                plink2 --file mydata --out mydata --make-bed --noweb --chr-set $NR
                printf "bedfiles\n" >> checkpoint
		else
        	printf "\t\tbedfiles already existing\n"
	fi
else
#no convertion required when using a vcf file
	Step=$(grep "vcf file no need convertion" checkpoint)
	if [ "${step}" != "vcf file no need convertion" ]
	then
		printf "vcf file no need for convertion\n" >> checkpoint
	else
		printf "\tvcf file still no need for convertion\n"
	fi
	
fi

#central function, here I have to precise SNP names
Step=$(grep "LDestimation" checkpoint)
if [ "${Step}" != "LDestimation" ]
then
	if [ ${1: -4} != ".vcf" ]
		then
		plink2 --file mydata --r2 --ld-window-r2 0.4 --out mydata --noweb --chr-set $NR
		printf "LDestimation\n" >> checkpoint
	else
		plink2 --vcf $1 --r2 --ld-window-r2 0.4 --out mydata --noweb --allow-extra-chr --chr-set 95
		printf "LDestimation\n" >> checkpoint
	fi
else
	printf "\t\tlinkage disequilibrium calculation already done\n"
fi

#the output would be kept as a variable that would be 
#use by ptyhon

#format the ld file
Step=$(grep "mydataFormat" checkpoint)
if [ "${Step}" != "mydataFormat" ]
        then
        	sed -i 's/ \+/\t/g' mydata.ld
        	printf "mydataFormat\n" >> checkpoint
else
	printf "\t\tmydata.ld formatting done\n"
fi


#here would be the calculation of mean r2 using awk

awk '{if ($7 > "'$5'" && $1 != "0") sum+= (dif=($5-$2))}END{print sum/NR}' mydata.ld > meanLD

