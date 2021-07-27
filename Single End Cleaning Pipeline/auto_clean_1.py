#First of 2 scripts necessary for a complete RNA-seq cleaning pipeline. This pipeline is designed to work exclusively on single end files. Begins with index.html file and automates wget, trimmomatic, and prinseq.

#WARNING: HIGHLY MEMORY INTENSIVE, CONSIDER CLEARING INTERMEDIATE FOLDERS TO PRESERVE DISK SPACE

#requires "raw" folder
#requires "trimmomatic" folder
#requires trimmomatic installation
#requires "printseq" folder
#requires prinseq++ installation

import pandas as pd
import pandas
import subprocess

#read list of single ended files
url_index = pandas.read_csv("single_ends.html", header = None, skiprows=9, delimiter=' ')

#create a list from the 16th column or the html file
raw_list = list(url_index[16])

#create list of urls for wget
url_list = []
for url in raw_list:
  if (isinstance(url, str)):
    url_list.append(url.split('"')[1])
print(url_list)
print(len(url_list))

#subprocess wgets each url sourced from file then unzips all gzips present in the current directory
for url in url_list:
    if url == '\n':
        continue
    wget_string = "wget " + url #x[1]
    subprocess.call(wget_string, shell=True)
    print(wget_string)
subprocess.call('gunzip *.gz', shell=True)

#Creates a working list of all fastq files unzipped to the folder raw/
import glob, os
os.chdir(".")
fastq_files = []
for file in glob.glob("raw/*.fastq"):
    fastq_files.append(file)
print(fastq_files)

#trimmomatic command thats takes input from raw folder and sends output to trimmomatic folder
prinseq_names = [] 
for file in fastq_files:
  fqc = "java -jar ../Trimmomatic-0.39/trimmomatic-0.39.jar SE " + file + " trimmomatic/" + file[4:-6] + '_out.fastq -threads 20 ILLUMINACLIP:TruSeq3-PE.fa:2:30:10:1:TRUE SLIDINGWINDOW:4:20 LEADING:3 TRAILING:3 MINLEN:40'
  prinseq_names.append('trimmomatic/' + file[4:-6] + '_out.fastq')
  print(fqc)
  subprocess.call(fqc, shell=True)

#prinseq subprocess calls poly-a removal for each trimmed file and outputs to printseq
bowtie_names = []
for name in prinseq_names:
  prin = "prinseq++ -threads 20 -VERBOSE 0 -fastq " + name + " -min_len 40 -trim_tail_left 10 -trim_tail_right 10 -out_name prinseq/" + name[12:-10]
  bowtie_names.append('printseq/' + name[12:-10] + '_good_out.fastq')
  print(prin)
  subprocess.call(prin, shell=True)
print(bowtie_names)




