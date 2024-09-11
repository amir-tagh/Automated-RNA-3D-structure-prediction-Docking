#!/bin/bash

# Function to display help information
display_help() {
    echo "Usage: $0 [OPTION]"
    echo "Process directories to remove carriage returns from .dbn and .fasta files"
    echo "and convert the second line of .fasta files to lowercase."
    echo
    echo "Options:"
    echo "  -h, --help     Display this help message and exit"
    echo
    echo "Run this script without any options to process the current directory."
}

# Function to process files in a directory
process_directory() {
    local dir=$1

    echo "Processing directory: $dir"

    # Look for .dbn file and remove carriage returns
    dbn_file=$(find "$dir" -type f -name "*.dbn" 2>/dev/null)
    if [ -n "$dbn_file" ]; then
        echo "Removing carriage returns from $dbn_file"
        tr -d '\r' < "$dbn_file" > "${dbn_file}.tmp" && mv "${dbn_file}.tmp" "$dbn_file"
    fi

    # Look for .fasta file, remove carriage returns, and convert the second line to lowercase
    fasta_file=$(find "$dir" -type f -name "*.fasta" 2>/dev/null)
    if [ -n "$fasta_file" ]; then
        echo "Removing carriage returns from $fasta_file"
        tr -d '\r' < "$fasta_file" > "${fasta_file}.tmp" && mv "${fasta_file}.tmp" "$fasta_file"
        
        echo "Converting second line to lowercase in $fasta_file"
        awk 'NR==2{print tolower($0)} NR!=2{print}' "$fasta_file" > "${fasta_file}.tmp" && mv "${fasta_file}.tmp" "$fasta_file"
    fi
}

# Check for help option
if [[ $1 == "-h" || $1 == "--help" ]]; then
    display_help
    exit 0
fi

# Sort directories and process each one
for dir in $(ls -d */ | sort); do
    process_directory "$dir"
done
