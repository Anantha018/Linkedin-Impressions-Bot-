import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
import os
from PIL import Image, ImageTk
import subprocess, sys
from get_job_titles import LinkedInBotGUI

windows_command_to_copy = '''& "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\chrome-profile"'''
mac_command_to_copy = r'''/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222&'''

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def window_copy_command():
    # Clear the clipboard and append the command
    root.clipboard_clear()
    root.clipboard_append(windows_command_to_copy)
    
    # Provide feedback to the user
    windows_copied_label.config(text="Command copied to clipboard!", foreground="green")

def mac_copy_command():
    # Clear the clipboard and append the command
    root.clipboard_clear()
    root.clipboard_append(mac_command_to_copy)
    
    # Provide feedback to the user
    mac_copied_label.config(text="Command copied to clipboard!", foreground="green")

def show_zero_frame():
    windows_frame.grid_forget()  # Hide the current frame
    mac_frame.grid_forget()      
    bottom_frame1.grid_forget()  
    back_button_frame1.grid_forget()
    
    zero_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
    bottom_frame0.grid(row=2, column=0, padx=20, pady=20, sticky='se')

def show_first_frame():
    second_frame.grid_forget()  # Hide the current frame
    zero_frame.grid_forget()    # Hide the current frame
    bottom_frame0.grid_forget()
    
    windows_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')  # Show the initial frame
    mac_frame.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')
    bottom_frame1.grid(row=2, column=0, padx=20, pady=20, sticky='se')
    back_button_frame1.grid(row=2, column=0, padx=20, pady=20, sticky='sw')
    
def show_second_frame():
    windows_frame.grid_forget()  # Hide the current frame
    mac_frame.grid_forget()      # Hide the current frame
    bottom_frame1.grid_forget()  # Hide the Next button frame
    back_button_frame1.grid_forget()
    third_frame.grid_forget()    # Hide the current frame
    
    second_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')  # Show the next frame

def show_third_frame():
    second_frame.grid_forget()  # Hide the current frame
    third_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

def close_and_run_job_titles_app():
    try:
        print("Closing current app...")

        # Instead of destroying the root right away, use withdraw to hide it.
        root.withdraw()
        root.destroy()
         # Construct the relative path to the executable
        exe_path = os.path.join('Job_titles', 'get_job_titles.exe')
    
        # Run the executable
        os.startfile(exe_path)

    except Exception as e:
        print(f"An error occurred: {e}")
        

# Create the main window
root = ttkb.Window(themename="darkly")
root.title("LinkedIn Bot")
root.state('zoomed')

# Create and configure style
style = ttkb.Style()
style.configure("TLabel", font=("Roboto", 14))
style.configure("TButton", font=("Roboto", 14))
style.configure("primary.TButton", font=("Roboto", 14), foreground="white")

# Create a frame for the content
zero_frame = tk.Frame(root)
zero_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew') 

# Create a label for the heading with larger font size in its own row
heading_label = ttk.Label(zero_frame, text="LinkedIn Bot", font=("Helvetica", 26, "bold"))
heading_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), padx=10)
heading_label.configure(anchor="center")

linkedin_bot_image =  tk.PhotoImage(file=resource_path("Images/linkedin_logo.png"))

# Create a label with the image and place it in column 0 (left side), in the next row
linkedin_bot_image_label = tk.Label(zero_frame, image=linkedin_bot_image)
linkedin_bot_image_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

# Define the LinkedIn bot description text
linkedin_text = """
This bot increases the probability of engagement and impressions on your LinkedIn profile by automating profile visits and \n interactions based on the content of your posts.
\n
Key Features: \n\n
- Automated Connection Visits: The bot will visit and engage with your LinkedIn connections.\n
- Targeted Job Profile Visits: It will visit job profiles relevant to your post content.\n
- AI-Generated Titles: Using AI, the bot generates post titles aligned with your content to boost engagement.\n
\n
Important Requirements:\n\n
- A stable and fast internet connection is necessary for smooth automation.\n
- The latest version of Chrome should be installed and up-to-date.\n
- No other tasks or interruptions should occur during the automation process. Your screen window must remain active \n until the process completes.\n
                                                            Press 'Next' to begin!
"""

# Create a label for the text with left margin (padx) and text wrapping (wraplength), in the same row as the image
linkedin_window_label = ttk.Label(zero_frame, text=linkedin_text, justify="left", style="TLabel")
linkedin_window_label.grid(row=1, column=1, pady=10, padx=(30, 10), sticky='nw')

bottom_frame0 = tk.Frame(root)
bottom_frame0.grid(row=2, column=0, padx=20, pady=20, sticky='se')

# Add a Next button to the second frame
next_button0 = ttk.Button(bottom_frame0, text="Next", style="primary.TButton", command=show_first_frame)
next_button0.grid(row=8, column=4, pady=2, sticky='se')


# First frame
# Create the initial frames and widgets
windows_frame = tk.Frame(root)
windows_frame.grid(row=0, column=0, padx=20, pady=20, sticky='ew')
windows_frame.grid_forget()

windows_label = ttk.Label(windows_frame, text="For Windows Users: Open the Start menu and search for Command Prompt, PowerShell, or Terminal. Then, run the command below.", style="TLabel")
windows_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))

windows_command_text = tk.Text(windows_frame, height=1, width=70, font=("Roboto", 12))
windows_command_text.insert(tk.END, windows_command_to_copy)
windows_command_text.config(state=tk.DISABLED)
windows_command_text.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='ew')

windows_copy_button = ttk.Button(windows_frame, text="Copy", command=window_copy_command)
windows_copy_button.grid(row=2, column=0, pady=10, sticky='e')

windows_copied_label = tk.Label(windows_frame, text="")
windows_copied_label.grid(row=2, column=1, pady=5, sticky='e')

windows_terminal_image = tk.PhotoImage(file=resource_path("Images/windows_command.png"))
windows_image_label = tk.Label(windows_frame, image=windows_terminal_image)
windows_image_label.grid(row=3, column=0, columnspan=2, pady=10)

mac_frame = tk.Frame(root)
mac_frame.grid(row=1, column=0, padx=20, pady=20, sticky='ew')
mac_frame.grid_forget()

mac_label = ttk.Label(mac_frame, text="For Mac OS users: Press Cmd + Space and type Terminal or navigate to Applications > Utilities > Terminal, then run the command below.", style="TLabel")
mac_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))

mac_command_text = tk.Text(mac_frame, height=1, width=70, font=("Roboto", 12))
mac_command_text.insert(tk.END, mac_command_to_copy)
mac_command_text.config(state=tk.DISABLED)
mac_command_text.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 12), sticky='ew')

mac_copy_button = ttk.Button(mac_frame, text="Copy", command=mac_copy_command)
mac_copy_button.grid(row=2, column=0, pady=(0, 10), sticky='e')

mac_copied_label = tk.Label(mac_frame, text="")
mac_copied_label.grid(row=2, column=1, pady=5, sticky='e')

mac_terminal_image = tk.PhotoImage(file=resource_path("Images/mac_terminal_window.png"))
mac_image_label = tk.Label(mac_frame, image=mac_terminal_image)
mac_image_label.grid(row=3, column=0, columnspan=2, pady=10)

bottom_frame1 = tk.Frame(root)
bottom_frame1.grid(row=2, column=0, padx=20, pady=20, sticky='se')
bottom_frame1.grid_forget()

back_button_frame1 = tk.Frame(root)
back_button_frame1.grid(row=2, column=0, padx=20, pady=20, sticky='sw')
back_button_frame1.grid_forget()

next_button1 = ttk.Button(bottom_frame1, text="Next", style="primary.TButton", command=show_second_frame)
next_button1.grid(row=0, column=0, pady=(10, 0), sticky='se')

back_button1 = ttk.Button(back_button_frame1, text="Back", command=show_zero_frame)
back_button1.grid(row=2, column=0, pady=(10, 0), sticky='sw')

# Second Frame
# Create the next frame to show after clicking the Next button
second_frame = tk.Frame(root)
second_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
second_frame.grid_forget()  # Initially hide this frame


chrome_window_label = ttk.Label(second_frame, text="A new Chrome window will open if the command is successfully executed!", style="TLabel")
chrome_window_label.grid(row=0, column=0, pady=20)

# Load and resize the image
chrome_image = Image.open(resource_path("Images/new_chrome_window.png"))
chrome_image = chrome_image.resize((700, 400), Image.LANCZOS)

# Convert the image to a format tkinter can use
chrome_window_image = ImageTk.PhotoImage(chrome_image)

# Create a label with the resized image
chrome_window_image_label = tk.Label(second_frame, image=chrome_window_image)
chrome_window_image_label.grid(row=1, column=0, pady=10, sticky='n')


# Linkedin label and Image
linkedin_window_label = ttk.Label(second_frame, text="Now login into your Linkedin account and make sure to not close this logged in Chrome window!", style="TLabel")
linkedin_window_label.grid(row=2, column=0, pady=20)

# Load and resize the image
linkedin_image = Image.open(resource_path("Images/linkedin_page_window.png"))
linkedin_image = linkedin_image.resize((700, 400), Image.LANCZOS)

# Convert the image to a format tkinter can use
linkedin_window_image = ImageTk.PhotoImage(linkedin_image)

# Create a label with the resized image
linkedin_window_image_label = tk.Label(second_frame, image=linkedin_window_image)
linkedin_window_image_label.grid(row=3, column=0, pady=10, sticky='n')

# Add a Next button to the second frame
next_button2 = ttk.Button(second_frame, text="Next", style="primary.TButton", command=show_third_frame)
next_button2.grid(row=8, column=0, pady=2, sticky='se')

# Add a Back button to the second frame to go back to the first frame
back_button2 = ttk.Button(second_frame, text="Back", command = show_first_frame)
back_button2.grid(row=8, column=0, pady=2, sticky='sw')



# Third Frame
third_frame = tk.Frame(root)
third_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
third_frame.grid_forget()  # Initially hide this frame

settings_window_label = ttk.Label(third_frame, text="Now, go to your settings page and click on Visibility", style="TLabel")
settings_window_label.grid(row=0, column=0, pady=20)

# Load and resize the image
settings_image = Image.open(resource_path("Images/settings_page.png"))
settings_image = settings_image.resize((800, 400), Image.LANCZOS)

settings_window_image = ImageTk.PhotoImage(settings_image)

settings_window_image_label = tk.Label(third_frame, image=settings_window_image)
settings_window_image_label.grid(row=1, column=0, pady=10, sticky='n')

visibility_window_label = ttk.Label(third_frame, text="Make sure to select the option 'Your name and headline'", style="TLabel")
visibility_window_label = visibility_window_label.grid(row=2, column=0, pady=20)

visibility_image = Image.open(resource_path("Images/profile_viewing_options.png"))
visibility_image = visibility_image.resize((850, 350), Image.LANCZOS)


visibility_window_image = ImageTk.PhotoImage(visibility_image)

visibility_window_image_label = tk.Label(third_frame, image=visibility_window_image)
visibility_window_image_label.grid(row=3, column=0, pady=10, sticky='n')

caution_label = ttk.Label(third_frame, text="After pressing Next, a new window will open in a few seconds!", style="TLabel")
caution_label = caution_label.grid(row=8, column=0, pady=2, sticky='s')

back_button3 = ttk.Button(third_frame, text="Back", command = show_second_frame)
back_button3.grid(row=8, column=0, pady=2, sticky='sw')

next_button2 = ttk.Button(third_frame, text="Next", style="primary.TButton", command=close_and_run_job_titles_app)
next_button2.grid(row=8, column=0, pady=2, sticky='se')



second_frame.grid_rowconfigure(1, weight=1)
second_frame.grid_columnconfigure(0, weight=1)

# Ensure the image stays within the label's dimensions
second_frame.update_idletasks()  

third_frame.grid_rowconfigure(1, weight=1)
third_frame.grid_columnconfigure(0, weight=1)

# Ensure the image stays within the label's dimensions
third_frame.update_idletasks()  

# Configure row and column weights to make sure the frames expand correctly
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)
root.grid_columnconfigure(0, weight=1)


# get_job_titles

# Run the main loop
root.mainloop()
