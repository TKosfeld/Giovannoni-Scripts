#First of 2 scripts necessary for a complete RNA-seq cleaning pipeline. This pipeline is designed to work exclusively on paired end files. Begins with index.html file and automates wget, trimmomatic, and prinseq.

#WARNING: HIGHLY MEMORY INTENSIVE, CONSIDER CLEARING INTERMEDIATE FOLDERS TO PRESERVE DISK SPACE

#requires "raw" folder
#requires "trimmomatic" folder
#requires trimmomatic installation
#requires "printseq" folder
#requires prinseq++ installation

import pandas as pd
import pandas
import subprocess

#read paired end html for wget targets
url_index = pandas.read_csv("paired_ends.html", header = None, skiprows=9, delimiter=' ')

#using string trimming create list of wget targets for subprocessing
raw_list = list(url_index[16])
print(raw_list)
url_list = []
trimmed_list = []
for url in raw_list:
  if (isinstance(url, str)):
    url_list.append(url.split('"')[1])
#housekeeping prints
#print(url_list)
#print(len(url_list))

#create list of accessions related to leaf morphology
for url in url_list:
    if ('/L' in url):
        trimmed_list.append(url)
#print(len(trimmed_list))
#wget all accessions related to leaf morphology
for url in trimmed_list:
    if url == '\n':
        continue
    wget_string = "wget " + url #x[1]
    subprocess.call(wget_string, shell=True)
#    print(wget_string)
subprocess.call('gunzip *.gz', shell=True)

#Load all R1 componets of paired_end files into a list
import glob, os
os.chdir(".")
fastq_files = []
for file in glob.glob("raw/*_R1.fastq"):
    fastq_files.append(file)
print(fastq_files)



#perform paired end trimmomatic on each paired_end grouping
prinseq_names = [] 
for file in fastq_files:
  fqc = "java -jar ../Trimmomatic-0.39/trimmomatic-0.39.jar PE " + file + " " + file[:-7] + "2.fastq " + "trimmomatic/" + file[4:-6] + '_out.fastq ' + 'trash/trash ' + "trimmomatic/" + file[4:-7] + '2_out.fastq ' + 'trash/trash ' + '-threads 20 ILLUMINACLIP:TruSeq3-PE.fa:2:30:10:1:TRUE SLIDINGWINDOW:4:20 LEADING:3 TRAILING:3 MINLEN:40'
  prinseq_names.append('trimmomatic/' + file[4:-6] + '_out.fastq')
  prinseq_names.append('trimmomatic/' + file[4:-7] + '2_out.fastq')
  print(fqc)
  subprocess.call(fqc, shell=True)
print(prinseq_names)

#prinseq subprocess calls poly-a removal for each trimmed file and outputs to printseq folder
bowtie_names = []
for name in prinseq_names:
  prin = "prinseq++ -threads 20 -VERBOSE 0 -fastq " + name + " -min_len 40 -trim_tail_left 10 -trim_tail_right 10 -out_name prinseq/" + name[12:-10]
  bowtie_names.append('printseq/' + name[12:-10] + '_good_out.fastq')
  print(prin)
  subprocess.call(prin, shell=True)
print(bowtie_names)




