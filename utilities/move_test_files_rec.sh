#!/bin/bash

# Define the input directory
input_dir="$1"

# Function to move files and delete test directories
function move_test_files {
  local dir="$1"
  # Loop through all subdirectories of the input directory
  for subdir in "$dir"/*/; do
    # Check if the subdirectory is named "test"
    if [ "$(basename "$subdir")" = "test" ]; then
      # Move all files from the "test" subdirectory to the input directory
      mv "$subdir"/* "$dir"
      # Remove the "test" subdirectory
      rmdir "$subdir"
    elif [ -d "$subdir" ]; then
      # Recursively call the function for all subdirectories
      move_test_files "$subdir"
    fi
  done
}

# Call the function to move files and delete test directories
move_test_files "$input_dir"
