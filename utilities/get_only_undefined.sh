#!/bin/bash

# Define the source directory where the files currently reside
src_dir="plotted_tensors"

# Define the destination directory where the files will be moved
dest_dir="undefined_tensors"

# Check if the destination directory exists; if not, create it
if [ ! -d "$dest_dir" ]; then
  mkdir -p "$dest_dir"
fi

# Loop through each line in the filestomove.txt file and move the corresponding file
while read filename; do
  if [ -f "$src_dir/$filename.png" ]; then
    mv "$src_dir/$filename.png" "$dest_dir"
    echo "Moved $filename to $dest_dir"
  else
    echo "File $filename.png not found in $src_dir"
  fi
done < filestomove.txt
