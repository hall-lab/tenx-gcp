#!/usr/bin/env perl

use strict;
use warnings 'FATAL';

use TestEnv;

use File::Compare;
use File::Temp;
use File::Slurp 'slurp';
use Test::Exception;
use Test::More tests => 4;

my %test;
subtest 'setup' => sub{
    plan tests => 2;

    $test{class} = 'Tenx::Assembly::Command::Stats::Quick';
    use_ok($test{class}) or die;
    $test{data_dir} = TestEnv::test_data_directory_for_class($test{class});
    ok(-d $test{data_dir}, 'data dir exists');


};

subtest 'success print to STDOUT' => sub{
    plan tests => 3;

    my $output;
    open local(*STDOUT), '>', \$output or die $!;
    lives_ok(sub{ $test{class}->execute(fasta_file => $test{data_dir}->file('fasta')->stringify); }, 'execute'); 
    
    my $expected_output = slurp($test{data_dir}->file('fasta.stats')->stringify);
    ok($expected_output, 'loaded expected output');
    is($output, $expected_output, 'output matches');

};

subtest 'success zero length scaffold print to stats_file' => sub{
    plan tests => 2;

    my ($fh, $stats_file) = File::Temp::tempfile();
    $fh->close;
    lives_ok(sub{ $test{class}->execute(fasta_file => $test{data_dir}->file('zero-length-scaffold.fasta')->stringify, stats_file => $stats_file); }, 'execute');
    is(File::Compare::compare($stats_file, $test{data_dir}->file('zero-length-scaffold.fasta.stats')->stringify), 0, 'stats file matches');
    
};

subtest 'fails' => sub{
    plan tests => 1;

    throws_ok(sub{ $test{class}->execute(fasta_file => $test{data_dir}->stringify); }, qr/Fasta file does not exist/, 'execute fails w/ non existing fasta file'); 

};

done_testing();
