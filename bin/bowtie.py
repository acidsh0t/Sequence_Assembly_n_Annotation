#! python3

import subprocess
import os
import shutil
from configparser import ConfigParser

config=ConfigParser()
config.read('seq_tools/config.ini')

sys_specs=config['sys_specs']
threads=sys_specs['threads']

strain='MG1655'

def build():
    #gets name of reference sequence (.fna)
    fna=[]
    for file in os.listdir():
        if file.endswith('.fna'):
            fna.append(file) 
    
    #ensures only 1 reference genome is present in the directory
    if len(fna)>1:
        print('Too many reference genomes in directory')
        quit()
    elif len(fna)<1:
        print('There are not enough reference genomes in directory')
        quit()
    
    print(fna[0])

    try:
        build='bowtie2-build --threads '+str(threads)+' '+fna[0]+' '+strain
        print(build)
        subprocess.call(build,shell=True)
    except:
        pass

def sam():
    #create necessary SAM directory for output
    try:
        shutil.rmtree('Bowtie2_SAM') #removes if it already exists to prevent errors
    except:
        pass
    os.mkdir('Bowtie2_SAM')

    fastq=[]
    for file in os.listdir('fastQ_trimmed_norRNA'):
        try:
            if file.endswith('_1.fastq.gz'):
                fastq.append(file) #assumes that _1 and _2 have same beginning of name
        except:
            print('File '+file+' not found.')
    for seq in fastq:
        try:
            sam=seq.replace('_1.fastq.gz','')    
            _1=seq
            _2=seq.replace('_1.fastq.gz','_2.fastq.gz')
            bowtie='bowtie2 -x '+strain+' -1 fastQ_trimmed_norRNA/'+_1+' -2 fastQ_trimmed_norRNA/'+_2+\
                ' -S Bowtie2_SAM/'+sam+'.sam --no-mixed --threads '+str(threads)
            print('The following command may take some time to complete.')
            print(bowtie)
            subprocess.call(bowtie,shell=True)
        except:
            print('Something went wrong running bowtie2 on '+sam)
            continue

if __name__ == "__main__":
    build()
    sam()