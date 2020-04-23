import click, jinja2, json, os, re, yaml
from Bio import SeqIO

@click.command(help="generate assembly stats")
@click.option("--fasta-fn", "-i", type=click.STRING, required=True, help="Fasta file name")
@click.option("--gap-ns", "-n", type=click.INT, help="Minimum number of Ns for scaffolded assembly gaps")
@click.option("--output-fn", "-o", type=click.STRING, required=True, help="Output file name")
@click.option("--output-format", "-f", type=click.Choice(["quick", "yaml", "json"]), default="quick", help="Output format")
def asm_stats_cmd(fasta_fn, gap_ns, output_fn, output_format):
    """
    Generate Assembly Stats
    """
    if not os.path.exists(fasta_fn):
        raise Exception("Fasta file does not exist: {}".format(fasta_fn))

    stats = {}
    if gap_ns is None:
        contigs = get_contig_lengths(fasta_fn)
        stats["contigs"] = get_stats(contigs)
    else:
        scaffolds, contigs = get_scaffold_and_contig_lengths(fasta_fn, gap_ns)
        stats["scaffolds"] = get_stats(scaffolds)
        stats["contigs"] = get_stats(contigs)

    if output_format == "json":
        output = json.dumps(stats)
    elif output_format == "yaml":
        output = yaml.dump(stats)
    else: # quick
        template_fn = os.path.join(os.path.dirname(__file__), "templates", "stats.quick.jinja")
        with open(template_fn, 'r') as f:
            template = jinja2.Template(f.read())
        output = template.render(stats=stats, length_buckets=length_buckets())+"\n"

    with open (output_fn, "w") as f:
        f.write(output)

#-- asm_stats_cmd

def get_contig_lengths(fasta_fn):
    contigs = []
    for seq in SeqIO.parse(fasta_fn, "fasta"):
        contigs.append(len(seq))
    contigs.sort()
    return contigs

#-- get_contig_lengths

def get_scaffold_and_contig_lengths(fasta_fn, ns):
    scaffolds = []
    contigs = []
    gap_splitter = re.compile(r"N{{{},}}".format(ns))
    for seq in SeqIO.parse(fasta_fn, "fasta"):
        scaffold_l = 0
        prev_start = 0
        for gap in re.finditer(gap_splitter, str(seq.seq)):
            contig_l = gap.span()[0] - prev_start
            prev_start = gap.span()[1]
            scaffold_l += contig_l
            contigs.append(contig_l)
        if scaffold_l == 0 or prev_start != len(seq):
            contig_l = len(seq) - prev_start
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
    length = sum(lengths)
    count = len(lengths)
    stats = {
        "total": length,
        "count": count,
        "mean": int(length/count),
        "max": lengths[-1],
        "genome_n50": int(length/2),
        "n50_length": 0,
    }

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
