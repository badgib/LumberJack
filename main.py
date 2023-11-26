import os
import re
import tkinter as tk

from datetime import datetime
from tkinter import filedialog, Scrollbar, Entry, Toplevel, Text, END, VERTICAL, Button, scrolledtext

# What rolls down stairs
# alone or in pairs,
# and over your neighbor's dog?
# What's great for a snack,
# And fits on your back?

# It's log, log, log

# Create the main window
root = tk.Tk()
root.title("LumberJack(and he's okay!)")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate window size based on screen resolution
window_width = int(screen_width * 0.6)
window_height = int(screen_height * 0.7)

# Set the initial size and position of the main window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.geometry(f"{window_width}x{window_height}+{(screen_width - window_width) // 2}+{(screen_height - window_height) // 2}")

# Default directory path
directory_path = "C:/MUSHclient/logs/"
log_ext = "txt"
def_above = 0
def_below = 16

# Function to create a new window displaying the selected line
def show_selected_line(selected_line):
    sl = selected_line
    def show_lines():
        input_text = sl
        lines_above = int(lines_above_entry.get())
        lines_below = int(lines_below_entry.get())
        selected_line = int(re.search(r'Line (\d+)', input_text).group(1))
        filename = re.search(rf'(.+\.{log_ext})', input_text).group(1)
        with open(filename, 'r') as file:
            all_lines = file.readlines()
        start_line = max(selected_line - lines_above, 1)
        end_line = min(selected_line + lines_below, len(all_lines))
        result = ''.join(all_lines[start_line-1:end_line])
        output_textbox.delete("1.0", tk.END)
        output_textbox.insert(tk.END, result)

    root = tk.Tk()
    root.title("ContextMatters")

    # Calculate window size based on screen resolution
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.6)
    window_height = int(screen_height * 0.6)
    root.geometry(f"{window_width}x{window_height}")
    
    lines_frame = tk.Frame(root)
    lines_frame.pack(padx=10, pady=10)

    lines_label = tk.Label(lines_frame, text="Lines above:")
    lines_label.pack(side=tk.LEFT)

    lines_above_entry = tk.Entry(lines_frame)
    lines_above_entry.insert(0, def_above)
    lines_above_entry.pack(side=tk.LEFT)

    lines_label = tk.Label(lines_frame, text="Lines below:")
    lines_label.pack(side=tk.LEFT)

    lines_below_entry = tk.Entry(lines_frame)
    lines_below_entry.insert(0, def_below)
    lines_below_entry.pack(side=tk.LEFT)

    show_button = tk.Button(root, text="Gimme context!", command=show_lines)
    show_button.pack()

    output_textbox = scrolledtext.ScrolledText(root, width=80, height=20)
    output_textbox.pack(expand=True, fill=tk.BOTH)


# Function to search for lines matching the regex pattern in a file
def search_lines(file_path, pattern):
    matching_lines = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        for line_number, line in enumerate(lines, 1):
            if re.search(pattern, line):
                matching_lines.append(f"{file_path} - Line {line_number}: {line.strip()}")
    return matching_lines

# Function to handle the first query and display results
def search_first_query():
    query = query_entry.get()
    results_text.config(state=tk.NORMAL)
    results_text.delete(1.0, END)
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(f".{log_ext}"):
                file_path = os.path.join(root, file)
                matching_lines = search_lines(file_path, query)
                for line in matching_lines:
                    results_text.insert(tk.END, line + "\n")
    results_text.config(state=tk.DISABLED)

# Function to handle subsequent queries and display results in a new window
def search_next_query():
    query = next_query_entry.get()
    results = []
    for line in results_text.get(1.0, tk.END).splitlines():
        if re.search(query, line):
            results.append(line)
    if results:
        new_window = Toplevel(root)
        new_window.title("NittyGritty(kitty litter)")
        new_window.geometry(f"{window_width}x{window_height}")
        
        # Create a frame for organizing widgets in the popup window
        popup_frame = tk.Frame(new_window)
        popup_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        new_results_text = Text(popup_frame, wrap=tk.WORD, height=20, width=100)
        new_results_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        new_results_text.config(state=tk.NORMAL)
        
        scrollbar = Scrollbar(popup_frame, orient=VERTICAL, command=new_results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        new_results_text.config(yscrollcommand=scrollbar.set)

        for result in results:
            # Add a button for each line
            line_with_button = result + " "
            button = Button(new_results_text, text="Blammo!", command=lambda line=result: show_selected_line(line))
            new_results_text.window_create(tk.END, window=button)
            new_results_text.insert(tk.END, line_with_button + "\n")
        new_results_text.config(state=tk.DISABLED)

        # Subsequent query input and search button in the popup window
        popup_next_query_label = tk.Label(popup_frame, text="Next query:")
        popup_next_query_label.pack()

        popup_next_query_entry = Entry(popup_frame)
        popup_next_query_entry.pack()

        popup_next_search_button = tk.Button(popup_frame, text="Search", command=lambda: search_popup_next_query(popup_next_query_entry, new_results_text))
        popup_next_search_button.pack()


# Function to handle subsequent queries in the popup window
def search_popup_next_query(query_entry, results_text):
    query = query_entry.get()
    results = []
    for line in results_text.get(1.0, tk.END).splitlines():
        if re.search(query, line):
            results.append(line)
    if results:
        results_text.config(state=tk.NORMAL)
        results_text.delete(1.0, END)
        for result in results:
            
            button = Button(results_text, text="Blammo!", command=lambda line=result: show_selected_line(result))
            results_text.window_create(tk.END, window=button)
            results_text.insert(tk.END, result + "\n")
        results_text.config(state=tk.DISABLED)

def get_current_day():
    current_date = datetime.now()
    day_of_year = current_date.timetuple().tm_yday
    total_days = 366 if current_date.year % 4 == 0 and (current_date.year % 100 != 0 or current_date.year % 400 == 0) else 365
    return current_date.year, day_of_year, total_days

# Function to open a directory dialog and set the directory path
def browse_directory():
    global directory_path
    directory_path = filedialog.askdirectory()
    directory_label.config(text="Directory: " + directory_path)

# Create frames to organize widgets
directory_frame = tk.Frame(root)
directory_frame.pack(pady=10)

query_frame = tk.Frame(root)
query_frame.pack(pady=10)

results_frame = tk.Frame(root)
results_frame.pack(expand=True, fill=tk.BOTH, pady=10)

# Directory selection
directory_label = tk.Label(directory_frame, text="Directory: " + directory_path)
directory_label.pack(side=tk.LEFT)

browse_button = tk.Button(directory_frame, text="Change", command=browse_directory)
browse_button.pack(side=tk.RIGHT)

year, current_day, total_days = get_current_day()
day_display = tk.Label(root, text=f"Today is day {current_day} of {total_days}, year {year}")
day_display.pack()

# First query input and search button
query_label = tk.Label(query_frame, text="First query:")
query_label.pack(side=tk.LEFT)

query_entry = Entry(query_frame)
query_entry.pack(side=tk.LEFT)

search_button = tk.Button(query_frame, text="Search", command=search_first_query)
search_button.pack(side=tk.LEFT)

# Text widget to display results of first query (scrollable and line wrapping)
results_text = Text(results_frame, wrap=tk.WORD, height=20, width=100)
results_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

scrollbar = Scrollbar(results_frame, orient=VERTICAL, command=results_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_text.config(yscrollcommand=scrollbar.set)

# Subsequent query input and search button
next_query_label = tk.Label(root, text="Next query:")
next_query_label.pack()

next_query_entry = Entry(root)
next_query_entry.pack()

next_search_button = tk.Button(root, text="Search", command=search_next_query)
next_search_button.pack()

# Run the tkinter main loop
root.mainloop()
