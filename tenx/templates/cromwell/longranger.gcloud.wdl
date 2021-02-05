# Longranger Pipeline

workflow longranger {
  String sample_name
  String ref_name

  call localize_reads {
    input:
      sample_name = sample_name
  }

  call localize_ref {
    input:
      ref_name = ref_name
  }

  call align {
    input:
      sample_name = localize_reads.output_sample_name,
      ref_name = localize_ref.output_ref_name
  }

  call upload {
    input:
      sample_name = align.output_sample_name
  }
}

task localize_reads {
  String sample_name

  command {
    tenx reads download ${sample_name}
  }

  output {
    String output_sample_name = sample_name
  }
}

task localize_ref {
  String ref_name

  command {
    tenx ref download ${ref_name}
  }

  output {
    String output_ref_name = ref_name
  }
}

task align {
  String sample_name
  String ref_name

  command {
    tenx aln align ${sample_name} ${ref_name}
  } 
  
  output {
    String output_sample_name = sample_name
  }
}

task upload {
  String sample_name

  command {
    tenx aln upload ${sample_name}
  } 
}
