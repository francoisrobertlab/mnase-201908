import logging
import os
import subprocess

import click
import pandas as pd
import seqtools.SplitBed

BASE_SCALE = 1000000


@click.command()
@click.option('--samples', '-s', type=click.Path(exists=True), default='samples.txt',
              help='Sample names listed one sample name by line.')
@click.option('--sizes', '-S', type=click.Path(exists=True), default='sacCer3.chrom.sizes',
              help='Size of chromosomes.')
@click.option('--index', '-i', type=int, default=None,
              help='Index of sample to process in samples file.')
def main(samples, sizes, index):
    '''Prepare BED file used for genome coverage on samples.'''
    logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    sample_names = pd.read_csv(samples, header=None, sep='\t', comment='#')[0]
    if index != None:
        sample_names = [sample_names[index]]
    for sample in sample_names:
        prepare_genome_coverage(sample, sizes)


def prepare_genome_coverage(sample, sizes):
    '''Prepare BED file used for genome coverage on a single sample.'''
    print ('Compute genome coverage on sample {}'.format(sample))
    do_genome_coverage(sample, sizes)
    splits = SplitBed.splits(sample)
    for split in splits:
        do_prepare_genome_coverage(split, sizes)


def do_prepare_genome_coverage(sample, sizes):
    bed_raw = sample + "-raw.bed"
    bed_ignore_strand = sample + "-cov.bed"
    center_annotations(bed_raw, bed_ignore_strand)


def center_annotations(bed, output):
    '''Resize annotations to 1 positioned at the center.'''
    with open(bed, "r") as infile:
        with open(output, "w") as outfile:
            for line in infile:
                if line.startswith('track') or line.startswith('browser') or line.startswith('#'):
                    outfile.write(line)
                    continue
                columns = line.rstrip('\r\n').split('\t')
                if len(columns) >= 3:
                    start = int(columns[1])
                    end = int(columns[2])
                    length = end - start
                    start = start + int(length / 2)
                    end = start + 1
                    outfile.write(columns[0])
                    outfile.write("\t")
                    outfile.write(str(start))
                    outfile.write("\t")
                    outfile.write(str(end))
                    for i in range(3, len(columns)):
                        outfile.write("\t")
                        outfile.write(columns[i])
                    outfile.write("\n")


if __name__ == '__main__':
    main()