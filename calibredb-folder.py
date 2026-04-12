#!/usr/bin/env python3
"""
Create .driveinfo.calibre and .metadata.calibre for a folder device.
Uses the same code path as the Calibre GUI.
Usage: calibre-debug -e create_device_info.py -- /path/to/folder
"""

import os
import sys

# Import calibre modules
from calibre.devices.folder_device.driver import FOLDER_DEVICE

def create_driveinfo(folder_path):
    """Create .driveinfo.calibre file using device's internal method."""
    print(f"Creating .driveinfo.calibre for: {folder_path}")
    dev = FOLDER_DEVICE(folder_path)
    # Set up progress reporter (required by device)
    dev.set_progress_reporter(lambda percent, msg: print(f"  [{int(percent*100):>3}%] {msg}"))

    # Simulate device connection - this creates driveinfo via _update_driveinfo_file
    dev.current_library_uuid = None
    dev.open(None, None)
    return dev

def create_metadata_from_device(folder_path):
    """Create .metadata.calibre file using device's internal methods."""
    print(f"Scanning {folder_path} for ebooks and creating metadata...")

    # Create device instance
    dev = FOLDER_DEVICE(folder_path)
    dev.current_library_uuid = None
    # Set up progress reporter (required by device)
    dev.set_progress_reporter(lambda percent, msg: print(f"  [{int(percent*100):>3}%] {msg}"))
    dev.open(None, None)

    # Get books from device - this scans and creates booklist
    print(f"Scanning for books...")
    booklist = dev.books(oncard=None, end_session=False)

    # Sync booklists - this writes .metadata.calibre
    print(f"Writing metadata cache...")
    dev.sync_booklists((booklist, None, None), end_session=False)

    print(f"Found {len(booklist)} books")
    return booklist

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 create_device_info.py /path/to/folder")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a directory")
        sys.exit(1)

    print(f"Processing folder: {folder_path}\n")

    # Create driveinfo file
    dev = create_driveinfo(folder_path)

    # Create metadata file using device's built-in methods
    create_metadata_from_device(folder_path)

    # Clean up device connection
    dev.eject()

    print(f"\nDevice info files created for: {folder_path}")
    print("\nCreated files:")
    print(f"  - {os.path.join(folder_path, '.driveinfo.calibre')}")
    print(f"  - {os.path.join(folder_path, '.metadata.calibre')}")

if __name__ == "__main__":
    main()
