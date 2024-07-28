import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def create_fasta_file(rna_sequence, fasta_file):
    rna_record = SeqRecord(Seq(rna_sequence), id="rna", description="")
    SeqIO.write(rna_record, fasta_file, "fasta")
    print(f"FASTA file {fasta_file} created.")

def create_params_file(rna_sequence, params_file):
    with open(params_file, 'w') as file:
        file.write("# FARFAR2 Parameter File\n")
        file.write("# This file contains parameters for running the FARFAR2 protocol in Rosetta\n\n")
        file.write(f"SEQUENCE: {rna_sequence}\n")
        file.write("NSTRUCT: 10\n")
        file.write("USE_FRAGMENT_LIBRARY: true\n")
        file.write("FRAGMENT_LIBRARY_PATH: /path/to/fragment/library\n")
        file.write("MAX_FRAGMENT_INSERTIONS: 200\n")
        file.write("ROSETTA_FLAGS: -minimize_bond_angles -relax:ramp_constraints false\n")
    print(f"Parameters file {params_file} created.")

def create_slurm_script(fasta_file, params_file, output_dir, slurm_script_file):
    rosetta_scripts_path = "/path/to/rosetta/main/source/bin/rosetta_scripts.default.linuxgccrelease"
    xml_script_path = "/path/to/farfar2.xml"  # Path to FARFAR2 XML script
    job_name = os.path.basename(fasta_file).split('.')[0]
    
    with open(slurm_script_file, 'w') as file:
        file.write("#!/bin/bash\n")
        file.write(f"#SBATCH --job-name={job_name}\n")
        file.write(f"#SBATCH --output={output_dir}/{job_name}_%j.out\n")
        file.write(f"#SBATCH --error={output_dir}/{job_name}_%j.err\n")
        file.write("#SBATCH --ntasks=1\n")
        file.write("#SBATCH --cpus-per-task=4\n")
        file.write("#SBATCH --mem=4G\n")
        file.write("#SBATCH --time=24:00:00\n")
        file.write("\n")
        file.write(f"{rosetta_scripts_path} -parser:protocol {xml_script_path} -in:file:fasta {fasta_file} -out:path:all {output_dir} -params {params_file} -nstruct 10\n")
    print(f"SLURM script {slurm_script_file} created.")

def submit_job(slurm_script_file):
    os.system(f"sbatch {slurm_script_file}")
    print(f"Job submitted with script {slurm_script_file}")

def process_fasta_files(fasta_dir, output_dir):
    for fasta_file in os.listdir(fasta_dir):
        if fasta_file.endswith(".fasta"):
            fasta_path = os.path.join(fasta_dir, fasta_file)
            job_output_dir = os.path.join(output_dir, os.path.splitext(fasta_file)[0])
            if not os.path.exists(job_output_dir):
                os.makedirs(job_output_dir)
            params_file = os.path.join(job_output_dir, "params.txt")
            slurm_script_file = os.path.join(job_output_dir, "run_farfar2.slurm")
            
            # Create parameters file
            rna_sequence = str(list(SeqIO.parse(fasta_path, "fasta"))[0].seq)
            create_params_file(rna_sequence, params_file)
            
            # Create SLURM script
            create_slurm_script(fasta_path, params_file, job_output_dir, slurm_script_file)
            
            # Submit job
            submit_job(slurm_script_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python submit_farfar2_jobs.py <fasta_directory> <output_directory>")
        sys.exit(1)

    fasta_directory = sys.argv[1]
    output_directory = sys.argv[2]

    process_fasta_files(fasta_directory, output_directory)

