
# Remove the accession number after taxonomy lacking species assignment
def remove_accession(tsv_file, output_file):
    with open(tsv_file, 'r') as input_file, open(output_file, 'w') as output:
        for line in input_file:
            # Split the line into columns using tab as the delimiter
            columns = line.strip().split('\t')
            if len(columns) >= 2:  # Ensure there are at least two columns
                entry = columns[1]  # Get the entry from the second column
                if 'sp.' in entry:  # Check if 'sp.' is present in the entry
                    # Split the entry at 'sp.' and take the first part, then append 'sp.' to it
                    entry = entry.split('sp.', 1)[0] + 'sp.'
                # Write the modified line to the output file
                output.write(f"{columns[0]}\t{entry}\n")
            else:
                # Preserve the line as it is if there are fewer than two columns
                output.write(line)


# Merge the fasta and the modified tsv
def merge_fasta_tsv(fasta_file, tsv_file, output_file):
    fasta_sequences = {}  # Initialize empty dictionary

    # Make ID:sequence dictionary
    with open(fasta_file, 'r') as fasta:
        sequence_id = ""  # Initialize empty string to store each ID
        for line in fasta:
            line = line.strip()

            # In the header
            if line.startswith('>'):
                sequence_id = line[1:]  # Start at index 1 to skip the >
                # Make an empty entry in the dict for each unique ID
                fasta_sequences[sequence_id] = ""

            # In the sequence, fill in the empty entries when for loop is in the sequence
            else:
                fasta_sequences[sequence_id] += line

    # Merge
    with open(tsv_file, 'r') as tsv, open(output_file, 'w') as output:
        for line in tsv:
            # Split the line by delimiter; assign first column as ID and second as taxon
            identifier, taxonomic_assignment = line.strip().split('\t')
            if identifier in fasta_sequences:  # For each line, check if ID is in dictionary
                sequence = fasta_sequences[identifier]  # Retrieve the sequence
                # Add > to taxon header, new line, add sequence, new line
                output.write(f'>{taxonomic_assignment}\n{sequence}\n')
