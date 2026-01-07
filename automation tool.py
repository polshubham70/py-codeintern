"""
File Automation Tool
--------------------
Organizes files in a directory by type into subfolders.
Features:
- Scans and sorts files (images, docs, videos, PDFs, etc.)
- Moves files to categorized folders
- Logs actions with timestamps
- CLI or GUI mode (using Tkinter)
- Handles file conflicts

Author: Your Name (for internship)
Date: January 2026
"""

import os
import shutil
import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# File type categories (extendable)
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".doc", ".docx", ".txt", ".rtf", ".odt"],
    "PDFs": [".pdf"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".bat"],
    "Others": []  # Catch-all for uncategorized
}

def get_category(extension: str) -> str:
    """Determine category based on file extension"""
    extension = extension.lower()
    for cat, exts in CATEGORIES.items():
        if extension in exts:
            return cat
    return "Others"

def organize_directory(dir_path: str, log_file: str = "file_organizer_log.txt"):
    """Main organization logic"""
    dir_path = Path(dir_path).resolve()
    
    if not dir_path.exists() or not dir_path.is_dir():
        raise ValueError(f"'{dir_path}' is not a valid directory.")
    
    with open(log_file, "a", encoding="utf-8") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"\n--- Session started: {timestamp} | Directory: {dir_path} ---\n")
        print(f"Organizing '{dir_path}'...")
        
        moved_count = 0
        for item in dir_path.iterdir():
            if item.is_file():  # Skip directories
                ext = item.suffix
                category = get_category(ext)
                
                target_dir = dir_path / category
                target_dir.mkdir(exist_ok=True)
                
                target_path = target_dir / item.name
                
                # Handle name conflicts
                counter = 1
                while target_path.exists():
                    target_path = target_dir / f"{item.stem}_{counter}{ext}"
                    counter += 1
                
                try:
                    shutil.move(str(item), str(target_path))
                    action = f"MOVED: '{item.name}' -> '{category}/{target_path.name}'"
                    log.write(f"{timestamp} - {action}\n")
                    print(action)
                    moved_count += 1
                except Exception as e:
                    error = f"ERROR moving '{item.name}': {str(e)}"
                    log.write(f"{timestamp} - {error}\n")
                    print(error)
        
        summary = f"Organization complete. {moved_count} files moved. Log: {log_file}"
        log.write(f"{timestamp} - {summary}\n--- Session ended ---\n")
        print(summary)
        return summary

# CLI Mode
def cli_mode():
    """Command-line interface"""
    print("File Automation Tool")
    print("--------------------")
    dir_path = input("Enter directory path to organize (or Enter for current): ").strip()
    if not dir_path:
        dir_path = "."
    
    try:
        organize_directory(dir_path)
    except ValueError as e:
        print(f"Error: {e}")

# GUI Mode (Optional - Uncomment to use as default)
def gui_mode():
    """Graphical user interface with Tkinter"""
    def select_and_organize():
        dir_path = filedialog.askdirectory(title="Select Directory to Organize")
        if dir_path:
            try:
                summary = organize_directory(dir_path)
                messagebox.showinfo("Success", summary)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    
    root = tk.Tk()
    root.title("File Organizer")
    root.geometry("300x150")
    tk.Label(root, text="File Automation Tool", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Select Folder & Organize", command=select_and_organize).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    # Run CLI by default; uncomment below for GUI
    cli_mode()
    # gui_mode()  # Uncomment this line to use GUI instead