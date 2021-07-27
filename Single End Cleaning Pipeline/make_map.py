#Quick script necessary to allow for Fei scripts to normalized RPKM data, outputs a metadata .tsv file.

import glob, os

os.chdir(".")
sams = []
raw = []
raw_seq = []
map_seq = []
for file in glob.glob("hisat_output/*.sam"):
  sams.append(file)
print(sams)

for file in glob.glob("hisat_summary/*.txt"):
  raw.append(file)
print(raw)

for file in raw:
  count = 0
  mapped = 0
  for line in open(file, "r"):
    if (line == '\n'):
      continue
    if (count == 0):
      raw_seq.append(int(line.split()[0]))
    if (count == 2 or count == 3):
      mapped = mapped + int(line.split()[0])
    if (count == 5):
      map_seq.append(mapped) 
    print(mapped)
    count = count + 1
f = open("mapped_reads.tsv", "a")
f.write("Sample\ttotal_reads\tmapped_reads\n")
for i in range(len(sams)):
  print(sams[i])
  print(raw_seq[i])
  print(map_seq[i])
  f.write(sams[i] + '\t' + str(raw_seq[i]) + '\t' + str(map_seq[i]) + '\n') 
f.close
