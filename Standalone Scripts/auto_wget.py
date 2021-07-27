#Quick script designed to automate wget from a .txt file.

#requires subprocess
#requires "Accession_urls.txt" file to specify wget urls

import subprocess
#Open url file sourced from excel document
f = open("Accession_urls.txt", "r")

#wgets each file url specified in .txt file
for line in f:
    if line == '\n':
        continue
    #x = line.split("\"")

    wget_string = "wget " + line #x[1]
    subprocess.call(wget_string, shell=True)

    print(wget_string)
