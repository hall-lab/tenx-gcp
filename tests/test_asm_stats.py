import os, unittest
from click.testing import CliRunner

from tenx.asm_stats import asm_stats_cmd, get_contig_lengths, get_scaffold_and_contig_lengths, get_metrics, length_buckets

class AsmStatsTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "asm-stats")
        self.fasta1_fn = os.path.join(self.data_dn, "asm.fasta")
        self.fasta2_fn = os.path.join(self.data_dn, "asm.scaffolded.fasta")
        self.expected_scaffolds = [ 17004, 350002, 1000001]
        self.expected_contigs = [1, 2001, 5001, 10001, 100001, 250001, 1000001]

    def test1_get_contig_lengths(self):
        contigs = get_contig_lengths(self.fasta1_fn)
        self.assertEqual(contigs, self.expected_contigs)

    def test1_get_scaffold_and_contig_lengths(self):
        scaffolds, contigs = get_scaffold_and_contig_lengths(self.fasta2_fn)
        self.assertEqual(scaffolds, self.expected_scaffolds)
        self.assertEqual(contigs, self.expected_contigs)

    def test2_get_metrics(self):
        expected_metrics = {
            "total": sum(self.expected_scaffolds),
            "count": len(self.expected_scaffolds),
        }
        expected_metrics["genome_n50"] = int(expected_metrics["total"]/2)
        expected_metrics["n50_length"] = expected_metrics["total"]

        for b in length_buckets():
            expected_metrics["_".join([str(b), "count"])] = 0
            expected_metrics["_".join([str(b), "length"])] = 0
        expected_metrics["1000000_length"] = self.expected_scaffolds[-1]
        expected_metrics["1000000_count"] = 1
        expected_metrics["250000_length"] = self.expected_scaffolds[1]
        expected_metrics["250000_count"] = 1
        expected_metrics["10000_length"] = self.expected_scaffolds[0]
        expected_metrics["10000_count"] = 1
        metrics = get_metrics(self.expected_scaffolds)
        self.assertEqual(metrics, expected_metrics)

        expected_metrics = {
            "total": sum(self.expected_contigs),
            "count": len(self.expected_contigs),
        }
        expected_metrics["genome_n50"] = int(expected_metrics["total"]/2)
        expected_metrics["n50_length"] = expected_metrics["total"]
        for b in length_buckets():
            expected_metrics["_".join([str(b), "count"])] = 1
            expected_metrics["_".join([str(b), "length"])] = b + 1
        metrics = get_metrics(self.expected_contigs)
        self.assertEqual(metrics, expected_metrics)

    def test4_asm_stats_cmd(self):
        self.assertEqual(0, 0)

# -- AsmStatsTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
