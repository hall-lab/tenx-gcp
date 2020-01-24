package Tenx::Assembly::Command::Stats::Quick;

use strict;
use warnings 'FATAL';

use Bio::SeqIO;
use List::Util;

class Tenx::Assembly::Command::Stats::Quick {
    is => 'Command::V2',
    has_input => {
        fasta_file => {
            is => 'Text',
            doc => 'Fasta file to derive assembly stats.',
        },
    },
    has_optional_input => {
        min_gap_size => {
            is => 'Number',
            default_value => 1,
            doc => 'Minimum ',
        },
    },
    has_output => {
        stats_file => {
            is => 'Text',
            default_value => '-',
            doc => 'File to output stats. Deafults to STDOUT.',
        },
    },
    doc => 'produce "quick" stats for assemblies',
};

sub help_detail { __PACKAGE__->__meta__->doc }

sub execute {
    my ($self) = @_;

    my $fasta_file = $self->fasta_file;
    $self->fatal_message('Fasta file does not exist! %s', $fasta_file) if not -f $fasta_file or not -s $fasta_file;
    my $reader = Bio::SeqIO->new(
        -format => 'fasta',
        -file   => $fasta_file,
    );

    my $min_Ns_for_gap = $self->min_gap_size;
    my %metrics;
    my @scaf_lengths;
    my @ctg_lengths;
    my $max_scaffold_length = -1;
    my $max_contig_length = -1;
    while( my $seq = $reader->next_seq ) {
        my $sequence = $seq->seq || '';
        my $scaffold_length = $seq->length || 0;
        my $bd_length = get_breakdown_length($scaffold_length);
        $metrics{'BD'}{'SCAF'}{$bd_length}{'len'} += $scaffold_length;
        $metrics{'BD'}{'SCAF'}{$bd_length}{'ct'}++;
        $metrics{'SCAFFOLD_LENGTHS'} += $scaffold_length;
        $metrics{'SCAFFOLD_COUNT'}++;
        push @scaf_lengths, $scaffold_length;
        if( $scaffold_length > $max_scaffold_length ) {
            $metrics{'MAX_SCAFFOLD_LENGTH'} = $scaffold_length;
            $max_scaffold_length = $scaffold_length;
            $metrics{'MAX_SCAFFOLD_ID'} = $seq->id;
            $sequence =~ s/N//ig;
            $metrics{'MAX_SCAFFOLD_BASES_LENGTH'} = length $sequence;
        }
        my @contigs = ( $scaffold_length > 0 )
        ? split( /N{$min_Ns_for_gap,}+/i, ($sequence || '') )
        : '';
        #my @contigs = split( /N{$min_Ns_for_gap,}+/i, ($seq->seq || '') );
        for my $contig( @contigs ) {
            my $contig_length = length $contig;
            my $bd_length = get_breakdown_length($contig_length);
            $metrics{'BD'}{'CTG'}{$bd_length}{'len'} += $contig_length;
            $metrics{'BD'}{'CTG'}{$bd_length}{'ct'}++;
            push @ctg_lengths, $contig_length;
            $metrics{'CONTIG_LENGTHS'} += $contig_length;
            $metrics{'CONTIG_COUNT'}++;
            if( $contig_length > $max_contig_length ) {
                $metrics{'MAX_CONTIG_LENGTH'} = $contig_length;
                $max_contig_length = $contig_length;
            }
        }
    }

    @scaf_lengths = sort {$b<=>$a} @scaf_lengths;
    my $n50_length = 0;
    my $total_lengths;
    for( 0 .. $#scaf_lengths ) {
        my $length = $scaf_lengths[$_];
        $total_lengths += $length;
        if( $total_lengths > ( $metrics{'SCAFFOLD_LENGTHS'} * 0.5 ) ) {
            $n50_length = $scaf_lengths[ $_ - 1].' ('.$scaf_lengths[$_].') '.$scaf_lengths[ $_ + 1 ];
            last;
        }
    }

    @ctg_lengths = sort {$b<=>$a} @ctg_lengths;
    my $n50_ctg_length = 0;
    $total_lengths = 0;
    for( 0 .. $#ctg_lengths ) {
        my $length = $ctg_lengths[$_];
        $total_lengths += $length;
        if( $total_lengths > ( $metrics{'CONTIG_LENGTHS'} * 0.5 ) ) {
            $n50_ctg_length = $ctg_lengths[ $_ - 1 ].' ('.$ctg_lengths[$_].') '.$ctg_lengths[ $_ + 1 ];
            last;
        }
    }

	# Open the output file
	my $stats_file = $self->stats_file;
	my $stats_fh = ( $stats_file eq '-' )
	? 'STDOUT'
	: IO::File->new($stats_file, 'w');
    $self->fatal_message('Failed to open stats stats file: %s', $stats_file) if not $stats_fh;

    $stats_fh->print("SCAFFOLDS\n");
    $stats_fh->printf("  %-10s%-15s\n", 'COUNT', $metrics{'SCAFFOLD_COUNT'});
    $stats_fh->printf("  %-10s%-15s\n", 'LENGTH', $metrics{'SCAFFOLD_LENGTHS'});
    $stats_fh->printf("  %-10s%-15s\n", 'AVG', int( $metrics{'SCAFFOLD_LENGTHS'} / $metrics{'SCAFFOLD_COUNT'}));
    $stats_fh->printf("  %-10s%-15s\n", 'N50', $n50_length);
    $stats_fh->printf("  %-10s%-15s\n", 'LARGEST', $metrics{'MAX_SCAFFOLD_LENGTH'});
    $stats_fh->printf(" (ID: %s, BASES_ONLY_LENGTH: %s)\n", $metrics{'MAX_SCAFFOLD_ID'}, $metrics{'MAX_SCAFFOLD_BASES_LENGTH'});
    print_length_bd($stats_fh, \%metrics, 'SCAF');
    $stats_fh->print("\nCONTIGS\n");
    $stats_fh->printf("  %-10s%-15s\n", 'COUNT', $metrics{'CONTIG_COUNT'});
    $stats_fh->printf("  %-10s%-15s\n", 'LENGTH', $metrics{'CONTIG_LENGTHS'});
    $stats_fh->printf("  %-10s%-15s\n", 'AVG', int( $metrics{'CONTIG_LENGTHS'} / $metrics{'CONTIG_COUNT'}));
    $stats_fh->printf("  %-10s%-15s\n", 'N50', $n50_ctg_length);
    $stats_fh->printf("  %-10s%-15s\n", 'LARGEST', $metrics{'MAX_CONTIG_LENGTH'});
    print_length_bd($stats_fh, \%metrics, 'CTG');
}

sub lengths_and_labels {
    {
        1000000 => '> 1M',
        250000 => '250K--1M',
        100000 => '100K--250K',
        10000 => '10K--100K',
        5000 => '5K--10K',
        2000 => '2K--5K',
        0 => '0--2K',
    }
}
sub bd_lengths {
    my $lengths_and_labels = lengths_and_labels();
    sort { $b <=> $a } keys %$lengths_and_labels;
}
sub get_label_for_bd_length {
    my ($bd_length) = @_;
    die "No bd_length given to get_label_for_bd_length!" if not defined $bd_length;
    my $lengths_and_labels = lengths_and_labels();
    $lengths_and_labels->{$bd_length};
}

sub print_length_bd {
    my ($stats_fh, $metrics, $type) = @_;
    my $subject = ( $type eq 'SCAF' )
    ? 'Scaffolds'
    : 'Contigs' ;
    for my $bd_length ( bd_lengths() ) {
       my $length = ( exists $metrics->{'BD'}{$type}{$bd_length}{'len'} )
	   ? $metrics->{'BD'}{$type}{$bd_length}{'len'}
           : 0 ;
       my $count = ( exists $metrics->{'BD'}{$type}{$bd_length}{'ct'} )
	   ? $metrics->{'BD'}{$type}{$bd_length}{'ct'}
           : 0 ;
       $stats_fh->printf("  $subject %s: $count ( $length bp )\n", get_label_for_bd_length($bd_length));
    }
}

sub get_breakdown_length {
    my ($length) = @_;
    die "No length given to get_breakdown_length" if not defined $length;
    List::Util::first { $length >= $_ } bd_lengths();
}

1;
