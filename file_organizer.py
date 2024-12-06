import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as ctk

def organize_files_in_path(folder_path, progress_var, progress_bar, app):
    # convert the folder path to a Path object
    folder = Path(folder_path)
    # get all files in a folder
    files = [f for f in folder.iterdir() if f.is_file()]
    total_files = len(files)
    
    # when no files are found, show a message and return
    if total_files == 0:
        messagebox.showinfo("Info", "No files to organize in the selected folder.")
        return
    
    # loop through each file and organize based on file extension
    for i, item in enumerate(files, start=1):
        # extract file extension (or use "no_extension" if none)
        file_extension = item.suffix[1:] if item.suffix else "no_extension"
        # Create or confirm the folder for this extension
        new_folder = folder / file_extension
        new_folder.mkdir(exist_ok=True)
        
        # Move the file into the corresponding extension folder
        destination = new_folder / item.name
        item.rename(destination)
        
        # Update the progress bar based on how many files are processed
        progress_percentage = (i / total_files) * 100
        progress_var.set(progress_percentage)
        progress_bar.update()

        # success 
        messagebox.showinfo("Success", "Files organized by file extensions!")

        progress_var.set(0)  # reset progress bar
        progress_bar.update()


def browse_folder(entry_widget):
    # Open a directory selection dialog
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        # Clear any existing text and insert the chosen path
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, selected_directory)

def start_organization(path_entry, progress_var, progress_bar, app):
    # Get the folder path from the entry field
    folder_path = path_entry.get().strip()
    # Check if a valid folder was provided
    if not folder_path:
        messagebox.showerror("Error", "Please select a valid folder.")
        return
    
    # Check if the folder exists
    if not Path(folder_path).exists():
        messagebox.showerror("Error", f"Path {folder_path} does not exist.")
        return

    # Call the function to organize the files
    organize_files_in_path(folder_path, progress_var, progress_bar, app)

def show_help():
    # Display a help message dialog explaining how to use the app
    messagebox.showinfo("Help", "Select a folder, then click 'Organize Files' to sort files into folders by their extensions.")

def on_close():
    # Cleanly close the application window
    app.destroy()

# Set the UI to dark mode for visual consistency
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Create the main application window using a dark theme
app = ttk.Window(themename="superhero")  
app.title("Advanced File Organizer")
app.resizable(False, False)

# Create the main frame with padding
frame = ttk.Frame(app, padding=20)
frame.pack(expand=True, fill="both")

# Label and Entry for folder path selection
path_label = ttk.Label(frame, text="Folder Path:", font=("Segoe UI", 10))
path_label.grid(row=0, column=0, sticky="w", padx=(0,10), pady=5)

path_entry = ttk.Entry(frame, width=40, bootstyle="info")
path_entry.grid(row=0, column=1, sticky="ew", pady=5)

# Browse button to open directory dialog
browse_button = ttk.Button(frame, text="Browse", bootstyle="secondary", command=lambda: browse_folder(path_entry))
browse_button.grid(row=0, column=2, padx=10, pady=5)

# Make the middle column expand if window resized
frame.grid_columnconfigure(1, weight=1)

# Progress bar setup to show organization progress
progress_var = tk.DoubleVar(value=0)
progress_bar = ttk.Progressbar(frame, variable=progress_var, length=300, bootstyle="info-striped")
progress_bar.grid(row=1, column=0, columnspan=3, pady=20, sticky="ew")

# bold-font for buttons and styling purposes
bold_font = ("Segoe UI", 11, "bold")

# "Organize Files" button
start_button = ctk.CTkButton(
    master=frame,
    text="Organize Files",
    corner_radius=20,
    fg_color="#2fa572",
    text_color="white",
    command=lambda: start_organization(path_entry, progress_var, progress_bar, app),
    width=120,
    height=30,
    font=bold_font
)
start_button.grid(row=2, column=0, columnspan=3, pady=10)

# small help button for instructions
help_button = ctk.CTkButton(
    master=frame,
    text="?",
    corner_radius=15,
    fg_color="#2fa572",
    text_color="white",
    width=30,
    height=30,
    command=show_help,
    font=bold_font
)
help_button.grid(row=3, column=2, sticky="e", pady=(5,0))

# Set the protocol for closing the window to our on_close function
app.protocol("WM_DELETE_WINDOW", on_close)

# Center the window on the screen
app.update_idletasks()
width = app.winfo_reqwidth()
height = app.winfo_reqheight()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)
app.geometry(f"{width}x{height}+{x}+{y}")

app.mainloop()
