import click, os, re
from Bio import SeqIO

@click.command(help="generate assembly stats")
@click.option("--fasta-fn", type=click.STRING, help="Fasta file name.")
@click.option("--min-gap-size", type=click.STRING, help="Minimum gap size")
@click.option("--output-fn", type=click.STRING, help="Output file name")
def asm_stats_cmd(fasta_fn, min_gap_size, outout_fn):
    """
    Generate Assembly Stats
    """
    if not os.path.exists(fasta_fn):
        raise Exception("Fasta file does not exist: {}".format(fasta_fn))

    if min_gap_size is not None:
        contigs = get_contig_lengths(fasta_fn)
        scaffolds = contigs
    else:
        scaffolds, contigs = get_scaffold_and_contig_lengths(fasta_fn)

    scaffold_stats = get_stats(scaffolds)
    contig_stats = get_stats(contigs)
    #with open (output_fn, "w") as f:

#-- asm_stats_cmd

def get_contig_lengths(fasta_fn):
    contigs = []
    for seq in SeqIO.parse(fasta_fn, "fasta"):
        contigs.append(len(seq))
    contigs.sort()
    return contigs

#-- get_contig_lengths

def get_scaffold_and_contig_lengths(fasta_fn):
    scaffolds = []
    contigs = []
    scaffold_splitter = re.compile(r"[ATGCatgc]+")
    for seq in SeqIO.parse(fasta_fn, "fasta"):
        scaffold_l = 0
        for m in re.finditer(scaffold_splitter, str(seq.seq)):
            contig_l = len(m.group(0))
            scaffold_l += contig_l
            contigs.append(contig_l)
        scaffolds.append(scaffold_l)
    scaffolds.sort()
    contigs.sort()
    return scaffolds, contigs

#-- get_scaffold_and_contig_lengths

def length_buckets():
    return (1000000, 250000, 100000, 10000, 5000, 2000, 0)

#-- length_buckets

def get_stats(lengths):
    # TODO
    # n50
    # max length id ?
    stats = {
        "total": sum(lengths),
        "count": len(lengths),
        "n50_length": 0,
    }
    stats["genome_n50"] = int(stats["total"]/2)

    buckets = length_buckets()
    for b in buckets:
        stats[str(b) + "_length"] = 0
        stats[str(b)+ "_count"] = 0

    for l in lengths:
        if stats["n50_length"] < stats["genome_n50"]:
            stats["n50_length"] += l
        for b in buckets:
            if l >= b:
                stats[str(b) + "_length"] += l
                stats[str(b)+ "_count"] += 1
                break

    return stats

#-- get_stats
