#Quick script to download, analyze with fastqc, and merge analysis results. Operates on fastqc urls given from and index.html file.

#Requires pandas and subprocess packages
#requires index file provided by BTI for wget information, specified as "single_ends.html" below
#requires fastqc installation
#requires multiqc installation

import pandas as pd
import pandas
import subprocess

#Creates output folder for download target
subprocess.call('mkdir Output', shell=True)

#Reads html file into dataframe based on space delimeters
url_index = pandas.read_csv("single_ends.html", header = None, skiprows=9, delimiter=' ')

#Create list from the 16th column
raw_list = list(url_index[16])
url_list = []
#Isolate url from raw_list and append to a wget list
for url in raw_list:
  if (isinstance(url, str)):
    url_list.append(url.split('"')[1])
print(url_list)

#wget and unzipping of urls read from file
for url in url_list:
    if url == '\n':
        continue
    #x = line.split("\"")
    wget_string = "wget " + url #x[1]
    subprocess.call(wget_string, shell=True)
    print(wget_string)
subprocess.call('gunzip *.gz', shell=True)

#Read names of all fastq files in the current working directory
import glob, os
os.chdir(".")
fastq_files = []
for file in glob.glob("*.fastq"):
    fastq_files.append(file)
fastq_files

#!sudo apt-get install -y fastqc

#Runs fastqc on each fastq file in the working directory 
for file in fastq_files:
  fqc = "fastqc -o Output -t 4 --noextract " + file
  print(fqc)
  subprocess.call(fqc, shell=True)

#!pip install multiqc
#Multiqc joins all fastqc outputs into a single representative file
subprocess.call('multiqc .', shell=True)

#Display multiqc outputs for user examination
gen_stats = pandas.read_csv("multiqc_data/multiqc_general_stats.txt", header=0, delimiter='\t')
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(gen_stats)

multiqc_fastqc = pandas.read_csv("multiqc_data/multiqc_fastqc.txt", header=0, delimiter='\t')
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(multiqc_fastqc)

