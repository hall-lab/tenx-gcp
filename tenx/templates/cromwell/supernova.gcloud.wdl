# Supernova Pipeline

workflow supernova {

  String sample_name

  call localize_reads {
    input:
      sample_name = sample_name
  }

  call assemble {
    input:
      sample_name = localize_reads.output_sample_name
  }

  call mkoutput {
    input:
      sample_name = assemble.output_sample_name
  }

  call upload {
    input:
      sample_name = mkoutput.output_sample_name
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

task assemble {

  String sample_name

  command {
    tenx asm assemble ${sample_name}
  } 
  
  output {
    String output_sample_name = sample_name
  }
}

task mkoutput {

  String sample_name

  command {
    tenx asm mkoutput ${sample_name}
  }

  output {
    String output_sample_name = sample_name
  }
}

task upload {

  String sample_name

  command {
    tenx asm upload ${sample_name}
  } 
}
