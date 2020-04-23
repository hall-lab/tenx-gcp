import filecmp, os, tempfile, unittest
from click.testing import CliRunner

from tenx.asm_stats import asm_stats_cmd, get_contig_lengths, get_scaffold_and_contig_lengths, get_stats, length_buckets

class AsmStatsTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "asm-stats")
        self.fasta1_fn = os.path.join(self.data_dn, "asm.fasta")
        self.fasta2_fn = os.path.join(self.data_dn, "asm.scaffolded.fasta")
        self.fasta2_stats_fn = os.path.join(self.data_dn, "asm.scaffolded.fasta.stats")
        self.expected_scaffolds = [ 17004, 350002, 1000001]
        self.expected_contigs = [1, 2001, 5001, 10001, 100001, 250001, 1000001]

        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_get_contig_lengths(self):
        contigs = get_contig_lengths(self.fasta1_fn)
        self.assertEqual(contigs, self.expected_contigs)

    def test1_get_scaffold_and_contig_lengths(self):
        scaffolds, contigs = get_scaffold_and_contig_lengths(self.fasta2_fn, 2)
        self.assertEqual(scaffolds, self.expected_scaffolds)
        self.assertEqual(contigs, self.expected_contigs)

    def test2_get_stats(self):
        total = sum(self.expected_scaffolds)
        count = len(self.expected_scaffolds)
        expected_stats = {
            "total": total,
            "count": count,
            "mean": int(total/count),
            "max": self.expected_scaffolds[-1],
            "genome_n50": int(total/2),
            "n50_length": total,
        }
        for b in length_buckets():
            expected_stats["_".join([str(b), "count"])] = 0
            expected_stats["_".join([str(b), "length"])] = 0
        expected_stats["1000000_length"] = self.expected_scaffolds[-1]
        expected_stats["1000000_count"] = 1
        expected_stats["250000_length"] = self.expected_scaffolds[1]
        expected_stats["250000_count"] = 1
        expected_stats["10000_length"] = self.expected_scaffolds[0]
        expected_stats["10000_count"] = 1
        stats = get_stats(self.expected_scaffolds)
        self.assertEqual(stats, expected_stats)

        total = sum(self.expected_contigs)
        count = len(self.expected_contigs)
        expected_stats = {
            "total": total,
            "count": count,
            "mean": int(total/count),
            "max": self.expected_contigs[-1],
            "genome_n50": int(total/2),
            "n50_length": total,
        }
        for b in length_buckets():
            expected_stats["_".join([str(b), "count"])] = 1
            expected_stats["_".join([str(b), "length"])] = b + 1
        stats = get_stats(self.expected_contigs)
        self.assertEqual(stats, expected_stats)

    def test4_asm_stats_cmd(self):
        runner = CliRunner()
        result = runner.invoke(asm_stats_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_stats_cmd, [])
        self.assertEqual(result.exit_code, 2)

        stats_fn = os.path.join(self.temp_d.name, "stats.txt")
        result = runner.invoke(asm_stats_cmd, ["-i", self.fasta2_fn, "-n", 2, "-o", stats_fn, "-f", "quick"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertEqual(filecmp.cmp(stats_fn, self.fasta2_stats_fn), True)

        result = runner.invoke(asm_stats_cmd, ["-i", self.fasta2_fn, "-n", 2, "-o", stats_fn, "-f", "json"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_stats_cmd, ["-i", self.fasta2_fn, "-n", 2, "-o", stats_fn, "-f", "yaml"])
        self.assertEqual(result.exit_code, 0)

# -- AsmStatsTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
