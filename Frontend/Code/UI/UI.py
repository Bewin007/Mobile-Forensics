import tkinter as tk
from tkinter import ttk
import subprocess

class AndroidTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Android Tool")
        
        # Create dark mode theme
        self.root.configure(bg="#1e1e1e")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background='#1e1e1e', foreground='#d8d8d8')
        self.style.configure('TButton', background='#333', foreground='#d8d8d8', font=('Arial', 12))
        self.style.map('TButton', background=[('active', '#666')])
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create start page
        self.start_page = ttk.Frame(self.notebook)
        self.notebook.add(self.start_page, text='Start')
        self.create_start_page_widgets()
        
        # Create functions page
        self.functions_page = ttk.Frame(self.notebook)
        self.notebook.add(self.functions_page, text='Functions')
        self.create_functions_page_widgets()
        
        # Hide functions page initially
        self.notebook.hide(1)
        
        # Create terminal-like display
        self.terminal_frame = ttk.Frame(root)
        self.terminal_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.create_terminal()
        
    def create_start_page_widgets(self):
        # Add widgets to the start page
        start_label = ttk.Label(self.start_page, text="Welcome to Android Tool!", background='#1e1e1e', foreground='#d8d8d8')
        start_label.pack(pady=10)
        
        # Button to reveal functions page
        start_button = ttk.Button(self.start_page, text="Start", command=self.show_functions_page)
        start_button.pack(pady=5)
        
    def create_functions_page_widgets(self):
        # Create buttons for the functions page
        self.create_buttons()
        
    def create_buttons(self):
        # Button texts
        button_texts = ["Call logs", "SMS logs", "Contacts", "Accounts", "Bluetooth", 
                        "Calendar", "Current Running Process", "Recovery", 
                        "Log Extraction", "Media Extraction", "Packages", 
                        "Ram Capture", "Reboot", "Telegram Media", 
                        "WhatsApp Media", "WhatsApp Logs", "Wifi History"]
        
        # Create and place buttons in rows of three
        row = 0
        column = 0
        for text in button_texts:
            button = ttk.Button(self.functions_page, text=text, command=lambda t=text: self.button_clicked(t))
            button.grid(row=row, column=column, padx=10, pady=5, sticky="ew")
            column += 1
            if column == 3:
                column = 0
                row += 1
                
    def button_clicked(self, text):
        # Execute corresponding script based on button text
        command = f"python {text.lower().replace(' ', '_')}.py"
        output = self.execute_command(command)
        self.update_terminal(output)
    
    def execute_command(self, command):
        # Execute command and capture output
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)
    
    def show_functions_page(self):
        # Show functions page
        self.notebook.select(1)
        
    def create_terminal(self):
        # Create terminal-like display using a text widget with scrollbar
        self.terminal_text = tk.Text(self.terminal_frame, wrap=tk.WORD, background='#1e1e1e', foreground='#d8d8d8', insertbackground='#d8d8d8')
        self.terminal_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.terminal_scroll = ttk.Scrollbar(self.terminal_frame, orient=tk.VERTICAL, command=self.terminal_text.yview)
        self.terminal_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.terminal_text.config(yscrollcommand=self.terminal_scroll.set)
        self.terminal_text.insert(tk.END, "Terminal Output:\n")
        self.terminal_text.config(state=tk.DISABLED)  # Disable text editing
    
    def update_terminal(self, output):
        # Enable text editing and insert output
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.insert(tk.END, f"\n\n{output}\n")
        self.terminal_text.config(state=tk.DISABLED)  # Disable text editing

if __name__ == "__main__":
    root = tk.Tk()
    app = AndroidTool(root)
    root.mainloop()
