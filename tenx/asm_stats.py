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

    scaffold_metrics = get_metrics(scaffolds)
    contig_metrics = get_metrics(contigs)
    #with open (output_fn, "w") as f:

def get_contig_lengths(fasta_fn):
    contigs = []
    for seq in SeqIO.parse(fasta_fn, "fasta"):
        contigs.append(len(seq))
    contigs.sort()
    return contigs

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

def length_buckets():
    return (1000000, 250000, 100000, 10000, 5000, 2000, 0)

def get_metrics(lengths):
    # TODO
    # n50
    # max length id ?
    metrics = {
        "total": sum(lengths),
        "count": len(lengths),
        "n50_length": 0,
    }
    metrics["genome_n50"] = int(metrics["total"]/2)

    buckets = length_buckets()
    for b in buckets:
        metrics[str(b) + "_length"] = 0
        metrics[str(b)+ "_count"] = 0

    for l in lengths:
        if metrics["n50_length"] < metrics["genome_n50"]:
            metrics["n50_length"] += l
        for b in buckets:
            if l >= b:
                metrics[str(b) + "_length"] += l
                metrics[str(b)+ "_count"] += 1
                break

    return metrics

#    $stats_fh->print("SCAFFOLDS\n");
#    $stats_fh->printf("  %-10s%-15s\n", 'COUNT', $metrics{'SCAFFOLD_COUNT'});
#    $stats_fh->printf("  %-10s%-15s\n", 'LENGTH', $metrics{'SCAFFOLD_LENGTHS'});
#    $stats_fh->printf("  %-10s%-15s\n", 'AVG', int( $metrics{'SCAFFOLD_LENGTHS'} / $metrics{'SCAFFOLD_COUNT'}));
#    $stats_fh->printf("  %-10s%-15s\n", 'N50', $n50_length);
#    $stats_fh->printf("  %-10s%-15s\n", 'LARGEST', $metrics{'MAX_SCAFFOLD_LENGTH'});
#    $stats_fh->printf(" (ID: %s, BASES_ONLY_LENGTH: %s)\n", $metrics{'MAX_SCAFFOLD_ID'}, $metrics{'MAX_SCAFFOLD_BASES_LENGTH'});
#    print_length_bd($stats_fh, \%metrics, 'SCAF');
#    $stats_fh->print("\nCONTIGS\n");
#    $stats_fh->printf("  %-10s%-15s\n", 'COUNT', $metrics{'CONTIG_COUNT'});
#    $stats_fh->printf("  %-10s%-15s\n", 'LENGTH', $metrics{'CONTIG_LENGTHS'});
#    $stats_fh->printf("  %-10s%-15s\n", 'AVG', int( $metrics{'CONTIG_LENGTHS'} / $metrics{'CONTIG_COUNT'}));
#    $stats_fh->printf("  %-10s%-15s\n", 'N50', $n50_ctg_length);
#    $stats_fh->printf("  %-10s%-15s\n", 'LARGEST', $metrics{'MAX_CONTIG_LENGTH'});
#    print_length_bd($stats_fh, \%metrics, 'CTG');
