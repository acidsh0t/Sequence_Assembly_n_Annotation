#! python3

import subprocess
from configparser import ConfigParser

config=ConfigParser()
config.read('seq_tools/config.ini')

sys_specs=config['sys_specs']
threads=sys_specs['threads']

def main():
    featurecounts='featureCounts -a genomic.gtf -p -T '+str(threads)+' -t CDS -g gene_id -o featureCounts_table.txt BAM_sorted/*.bam'
    print(featurecounts)
    subprocess.call(featurecounts,shell=True)

if __name__ == "__main__":
    main()