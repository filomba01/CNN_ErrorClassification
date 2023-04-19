#!/bin/bash

# Define the source directory where the files currently reside
# shellcheck disable=SC1007
src_dir=$1

# Define the destination directory where the files will be moved
# shellcheck disable=SC1007
dest_dir=$2

# shellcheck disable=SC1068
# shellcheck disable=SC2034
content_file=$3

echo "Number of arguments: $#"


# Check if the destination directory exists; if not, create it
if [ ! -d "$dest_dir" ]; then
  mkdir -p "$dest_dir"
fi

# Loop through each line in the filestomove.txt file and move the corresponding file
while read filename; do
  if [ -f "$src_dir/$filename.png" ]; then
    cp "$src_dir/$filename.png" "$dest_dir"
    echo "Moved $filename to $dest_dir"
  else
    echo "File $filename.png not found in $src_dir"
  fi
done < $content_file
