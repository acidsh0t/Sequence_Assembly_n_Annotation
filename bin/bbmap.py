#! python3

import os
import subprocess
import shutil

def main():
    n=0

    ref='seq_tools/bin/ribokmers.fa' #path to ribokmers.

    #creates necessary directories if not already present
    try: #removes directory if it exists already to prevent errors
        shutil.rmtree('fastQ_trimmed_norRNA')
        shutil.rmtree('fastQ_trimmed_rRNA')
    except:
        pass
    os.mkdir('fastQ_trimmed_norRNA')
    os.mkdir('fastQ_trimmed_rRNA')
    
    seq_list=[]
    for seq in os.listdir(): 
        try:
            if seq.endswith('_1.fastq') or seq.endswith('_1.fastq.gz'): #assumes _1 and _2 share same name and are both present
                seq_list.append(seq)
        except:
            continue

    for seq in seq_list:
        try:
            if seq.endswith('_1.fastq'): 
                _seq=seq.replace('_1.fastq','') #removes suffix from sequence file
            elif seq.endswith('_1.fastq.gz'):
                _seq=seq.replace('_1.fastq.gz','')

            val1=_seq+'_1_val_1.fq'
            val2=_seq+'_2_val_2.fq'

            bbduk='bbduk.sh in=fastq_trimmed/'+val1+' in2=fastq_trimmed/'+val2+\
                ' out=fastQ_trimmed_norRNA/'+_seq+'_1.fastq.gz out2=fastQ_trimmed_norRNA/'+_seq+'_2.fastq.gz '\
                'outm=fastQ_trimmed_rRNA/'+_seq+'_1.fastq.gz outm2=fastQ_trimmed_rRNA/'+_seq+'_2.fastq.gz '\
                'k=31 ref='+ref
            print(bbduk)
            subprocess.call(bbduk,shell=True)
        except:
            print('Something went wrong running bbmap on '+_seq)
            continue
        n=n+1
        
if __name__ == "__main__":
    main()