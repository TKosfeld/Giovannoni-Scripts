#2nd file in a 2 script pipeline for a complete RNA-seq cleaning of single-end files. Picks up where auto clean left off and automates 2 bowties based on LSU and SSU indexes, removes identified sequences, performs hisat2, and uses BTI specific Fei scripts to create a normalized RPKM file.

#WARNING: HIGHLY MEMORY INTENSIVE, CONSIDER CLEARING INTERMEDIATE FOLDERS TO PRESERVE DISK SPACE

#requires "bowtie" folder
#requires bowtie installation
#requires 2 seperate bowtie reference files
#requires folder "rRNA_database" 
#require "bowtie_index" folder 
#require Bioconda installation
#requires "bowtie_output" folder
#requires "hisat_summary" folder
#requires "hisat_output" folder
#requires "hisat_index" folder
#requires index files within hisat_index folder
#require Fei scripts and perl installation

#imports necessary for installations
from Bio import SeqIO
import pandas as pd
import pandas
import subprocess
from multiprocessing import Pool

#creates a list of files to be read from the prinseq folder, specifies good output only
import glob, os
os.chdir(".")
fastq_good = []
for file in glob.glob("prinseq/*good*.fastq"):
    fastq_good.append(file)
fastq_good

#applies bowtie to good prinseq output list
bowtie_name = []
for name in fastq_good:
  bow = "bowtie -v 3 -k 1 -p 20 -x bowtie_index/Silva_LSU " + name + " bowtie/" + name[8:-15] + "_LSU.sam"
  print(bow)
  bowtie_name.append("bowtie/" + name[8:-15])
  subprocess.call(bow, shell=True)

#successive bowtie cleanings to enable selection base on both short and long sequence units
for name in fastq_good:
  bow = "bowtie -v 3 -k 1 -p 20 -x rRNA_database/rRNA_database.fa " + name + " bowtie/" + name[8:-15] + "_SSU.sam"
  print(bow)
  #bowtie_name.append("bowtie/" + name[8:-15] + "_SSU.sam")
  subprocess.call(bow, shell=True)

#function definition allows for multiprocessing pool for increased time efficiency
#this function trimms existing sequence files based on reads identified by successive bowtie iterations
def trim_fastq(bowtie):
  print("Trimming " + bowtie[7:]  + " based on " + bowtie )
  #create list of long sequence reads from LSU files
  header_set = list(line.split()[0] for line in open(bowtie + "_LSU.sam"))
  #create list of short sequence reads from SSu files
  header_set2 = list(line.split()[0] for line in open(bowtie + "_SSU.sam"))
  #merge the lists to create a single list of non-desirable sequences
  header_set.extend(header_set2)
  #clear variable to save memory during computation
  header_set2 = None
  records = []
  #for sequence in file output by prinseq, only add the sequence to the records list if it is not present in the exlcusion list
  for record in SeqIO.parse("prinseq/" + bowtie[7:] + "_good_out.fastq", "fastq"):
    if (record.id in header_set):
      continue
    else:
      records.append(record)
  #using the create list of desireable sequences write to file in folder bowtie_output/
  with open("bowtie_output/" + bowtie[7:] + ".fastq", "w") as output_handle:
    SeqIO.write(records, output_handle, "fastq")

#multiprocessing pool for each file present in prinseq with "good" in the name, 20 specifies cores
pool = Pool(20)
pool.map(trim_fastq, bowtie_name)
pool.close()
pool.join()

#read all filenames from the bowtie_output/ folder
fastq_good = []
for file in glob.glob("bowtie_output/*.fastq"):
    fastq_good.append(file)
print(fastq_good)

#hisat application to every bowtie trimmed file, output summary and resulting sam files to respective folders
for name in fastq_good:
  hisat = "hisat2 --rna-strandness R -p 20 --summary-file hisat_summary/" + name[14:-6] + ".txt  -x /home/tdk38/REU/RNA-Seq/auto_clean/hisat_index/index -k 20 -U " + name + " -S hisat_output/" + name[14:-6] + ".sam" 
  print(hisat)
  subprocess.call(hisat, shell=True)

#calling of Fei scripts present in current directory
subprocess.call('perl mRNAtool.pl -t count -s SS -l fr-firststrand -f ITAG4.1_CDS.bed hisat_output/*.sam', shell=True)
subprocess.call('python3 make_map.py', shell=True)
subprocess.call('perl mRNAtool.pl -t norm -f ITAG4.1_CDS.bed -m 1 -u mapped_reads.tsv -d 2 exp_raw_count.txt > exp_raw_count_normalized.txt', shell=True)
