#!/bin/bash
# Enable error handling
set -e

# Create images directory if it doesn't exist
mkdir -p images

# Check if the URLs file exists
if [ ! -f "all_image_urls.txt" ]; then
    echo "Error: all_image_urls.txt not found!"
    exit 1
fi

# Download loop reading from the file
while IFS= read -r url || [ -n "$url" ]; do
    # Skip empty lines
    if [ -z "$url" ]; then
        continue
    fi

    filename=$(basename "$url")

    # Check if file already exists to avoid re-downloading
    if [ ! -f "images/$filename" ]; then
        echo "Downloading $filename..."
        # Using curl with -f to fail on HTTP errors
        if ! curl -L -f -o "images/$filename" "$url"; then
            echo "Failed to download $url"
            # Optional: Decide if you want to stop or continue.
            # For now, we continue but warn.
            rm -f "images/$filename" # remove empty/failed file
        fi
    else
        echo "Skipping $filename (already exists)"
    fi
done < all_image_urls.txt

echo "Download process complete."
