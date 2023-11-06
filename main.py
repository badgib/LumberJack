import os
import re
import tkinter as tk
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

    lines_label = tk.Label(root, text="Lines above:")
    lines_label.pack()

    lines_above_entry = tk.Entry(root)
    lines_above_entry.insert(0, def_above)
    lines_above_entry.pack()

    lines_label = tk.Label(root, text="Lines below:")
    lines_label.pack()

    lines_below_entry = tk.Entry(root)
    lines_below_entry.insert(0, def_below)
    lines_below_entry.pack()

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
        new_results_text = Text(new_window, wrap=tk.WORD, height=20, width=100)
        new_results_text.pack(expand=True, fill=tk.BOTH)
        new_results_text.config(state=tk.NORMAL)
        for result in results:
            # Add a button for each line
            line_with_button = result + " "
            button = Button(new_results_text, text="Blammo!", command=lambda line=result: show_selected_line(line))
            new_results_text.window_create(tk.END, window=button)
            new_results_text.insert(tk.END, line_with_button + "\n")
        new_results_text.config(state=tk.DISABLED)

        # Subsequent query input and search button in the popup window
        popup_next_query_label = tk.Label(new_window, text="Next query:")
        popup_next_query_label.pack()
        popup_next_query_entry = Entry(new_window)
        popup_next_query_entry.pack()
        popup_next_search_button = tk.Button(new_window, text="Search", command=lambda: search_popup_next_query(popup_next_query_entry, new_results_text))
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
            # results_text.insert(tk.END, result + "\n")
            button = Button(results_text, text="Blammo!", command=lambda line=result: show_selected_line(result))
            results_text.window_create(tk.END, window=button)
            results_text.insert(tk.END, result + "\n")
        results_text.config(state=tk.DISABLED)

# Function to open a directory dialog and set the directory path
def browse_directory():
    global directory_path
    directory_path = filedialog.askdirectory()
    directory_label.config(text="Directory: " + directory_path)

# Directory selection
directory_label = tk.Label(root, text="Directory: " + directory_path)
directory_label.pack()
browse_button = tk.Button(root, text="Change", command=browse_directory)
browse_button.pack()

# First query input and search button
query_label = tk.Label(root, text="First query:")
query_label.pack()
query_entry = Entry(root)
query_entry.pack()
search_button = tk.Button(root, text="Search", command=search_first_query)
search_button.pack()

# Text widget to display results of first query (scrollable and line wrapping)
results_text = Text(root, wrap=tk.WORD, height=20, width=100)
results_text.pack(expand=True, fill=tk.BOTH)
results_text.config(state=tk.DISABLED)
scrollbar = Scrollbar(results_text, orient=VERTICAL, command=results_text.yview)
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
