#!/bin/bash

# Directories
FASTA_DIR="fasta_files"
SS_DIR="secondary_structure"
OUTPUT_DIR="output"

# Run the Python script to prepare FARFAR2 jobs
python prepare_farfar2_jobs.py $FASTA_DIR $SS_DIR $OUTPUT_DIR

# Submit each SLURM script in the output directories
for job_dir in $OUTPUT_DIR/*; do
  if [ -d "$job_dir" ]; then
    slurm_script="$job_dir/run_farfar2.slurm"
    if [ -f "$slurm_script" ]; then
      sbatch $slurm_script
      echo "Submitted job with script $slurm_script"
    else
      echo "SLURM script not found in $job_dir"
    fi
  fi
done

