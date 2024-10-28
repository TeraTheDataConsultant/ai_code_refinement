# Create a python script that automatically organizes the mac os desktop 
import os
import shutil
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the path to the desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Define folders to organize files into
folders = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Spreadsheets": [".xlsx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Music": [".mp3", ".wav"],
    "Others": []
}


def create_folders():
    for folder in folders.keys():
        folder_path = os.path.join(desktop_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logging.info(f"Created folder: {folder_path}")


def organize_files():
    for filename in os.listdir(desktop_path):
        file_path = os.path.join(desktop_path, filename)
        if os.path.isfile(file_path):
            moved = False
            for folder, extensions in folders.items():
                if any(filename.lower().endswith(ext) for ext in extensions):
                    shutil.move(file_path, os.path.join(desktop_path, folder, filename))
                    logging.info(f"Moved file: {filename} to folder: {folder}")
                    moved = True
                    break
            if not moved:
                shutil.move(file_path, os.path.join(desktop_path, "Others", filename))
                logging.info(f"Moved file: {filename} to folder: Others")


def main():
    create_folders()
    organize_files()


if __name__ == "__main__":
    main()


# TODO: Add error handling for file operations
# TODO: Consider adding a command-line interface for user customization
# TODO: Implement a dry-run mode to preview changes before applying
# TODO: Add unit tests for folder creation and file organization functions