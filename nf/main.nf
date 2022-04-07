#!/usr/bin/env nextflow
nextflow.enable.dsl=2 

process preprocessing_get_proteins {
  input: 
    val x
  output:
    stdout
  script:
    """
    echo '${x} | get_proteins'
    """
}

process preprocessing_get_angles {
  input: 
    val x
  output:
    stdout
  script:
    """
    echo '${x} | get_angles'
    """
}

process preprocessing_angle_data_prep {
  input: 
    val x
  output:
    stdout
  script:
    """
    echo '${x} | angle_data_prep'
    """
}

workflow {
  Channel.of('file-1.txt') | preprocessing_get_proteins | preprocessing_get_angles | preprocessing_angle_data_prep | view
}
