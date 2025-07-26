#!/usr/bin/env python3
"""
GenCAD AI - Linux Desktop 3D Model Generator
A standalone desktop application that generates FreeCAD 3D models from text prompts using Google Gemini AI.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, PhotoImage
import requests
import subprocess
import os
import json
import tempfile
import sys
import threading
import re
import atexit
from datetime import datetime

# Constants
GEMINI_API_KEY = "AIzaSyCMU6n2ZHgJc-GmD7VWEyi3xnwyaml2t1c"  # Updated API key
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
FREECAD_COMMAND = "freecad"  # Assumes 'freecad' is in PATH

class GenCADApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("GenCAD AI")
        self.geometry("900x700")
        self.configure(bg="#FFFFFF")
        self.resizable(True, True)
        
        # Color scheme
        self.colors = {
            'bg_primary': '#FFFFFF',
            'bg_secondary': '#F8F8F8',
            'bg_input': '#FDFDFD',
            'fg_primary': '#000000',
            'fg_secondary': '#333333',
            'border': '#E0E0E0',
            'accent': '#000000',
            'button_bg': '#000000',
            'button_fg': '#FFFFFF',
            'button_active': '#333333'
        }
        
        # Initialize UI
        self.setup_ui()
        
        # Center the window
        self.center_window()
        
        # Set minimum window size
        self.minsize(600, 500)
        
    def center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_ui(self):
        """Setup the enhanced user interface"""
        # Main container with padding
        main_container = tk.Frame(self, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)
        
        # Header section
        header_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Main title
        title_label = tk.Label(
            header_frame,
            text="GenCAD AI",
            font=("Arial", 28, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['fg_primary']
        )
        title_label.pack(pady=(0, 8))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="AI-Powered 3D CAD Model Generator",
            font=("Arial", 14),
            bg=self.colors['bg_primary'],
            fg=self.colors['fg_secondary']
        )
        subtitle_label.pack(pady=(0, 5))
        
        # Separator line
        separator = tk.Frame(header_frame, height=2, bg=self.colors['border'])
        separator.pack(fill=tk.X, pady=(15, 0))
        
        # Input section
        input_section = tk.Frame(main_container, bg=self.colors['bg_primary'])
        input_section.pack(fill=tk.X, pady=(0, 25))
        
        # Prompt label
        prompt_label = tk.Label(
            input_section,
            text="Describe your 3D model:",
            font=("Arial", 13, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['fg_primary'],
            anchor='w'
        )
        prompt_label.pack(fill=tk.X, pady=(0, 8))
        
        # Prompt input frame with border
        input_frame = tk.Frame(
            input_section,
            bg=self.colors['border'],
            relief=tk.SOLID,
            bd=1
        )
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Multi-line text input for prompts
        self.prompt_text = tk.Text(
            input_frame,
            height=4,
            font=("Arial", 12),
            bg=self.colors['bg_input'],
            fg=self.colors['fg_primary'],
            relief=tk.FLAT,
            bd=10,
            wrap=tk.WORD,
            selectbackground="#0078D4",
            insertbackground=self.colors['fg_primary']
        )
        self.prompt_text.pack(fill=tk.X, padx=2, pady=2)
        
        # Example text
        example_text = 'Example: "Create a 50mm cube with a 10mm cylindrical hole through the center"'
        self.prompt_text.insert("1.0", example_text)
        self.prompt_text.bind("<FocusIn>", self.clear_example_text)
        self.example_cleared = False
        
        # Button frame
        button_frame = tk.Frame(input_section, bg=self.colors['bg_primary'])
        button_frame.pack(fill=tk.X)
        
        # Generate button with enhanced styling
        self.generate_button = tk.Button(
            button_frame,
            text="Generate CAD Model",
            font=("Arial", 13, "bold"),
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            activebackground=self.colors['button_active'],
            activeforeground=self.colors['button_fg'],
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.generate_cad_model
        )
        self.generate_button.pack(side=tk.LEFT)
        
        # Add hover effects
        self.generate_button.bind("<Enter>", self.on_button_enter)
        self.generate_button.bind("<Leave>", self.on_button_leave)
        
        # Status section
        status_section = tk.Frame(main_container, bg=self.colors['bg_primary'])
        status_section.pack(fill=tk.BOTH, expand=True)
        
        # Status label
        status_label = tk.Label(
            status_section,
            text="Status & Output:",
            font=("Arial", 13, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['fg_primary'],
            anchor='w'
        )
        status_label.pack(fill=tk.X, pady=(0, 8))
        
        # Status text frame with border
        status_frame = tk.Frame(
            status_section,
            bg=self.colors['border'],
            relief=tk.SOLID,
            bd=1
        )
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status text area
        self.status_text = scrolledtext.ScrolledText(
            status_frame,
            font=("Courier New", 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['fg_primary'],
            relief=tk.FLAT,
            bd=10,
            state=tk.DISABLED,
            wrap=tk.WORD,
            selectbackground="#0078D4"
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Initial status message
        self.update_status("GenCAD AI is ready. Enter a description and click 'Generate CAD Model'.")
        self.update_status("Tip: Be specific with dimensions and materials for better results.")
        
    def on_button_enter(self, event):
        """Handle button hover enter"""
        if self.generate_button['state'] != tk.DISABLED:
            self.generate_button.configure(bg=self.colors['button_active'])
            
    def on_button_leave(self, event):
        """Handle button hover leave"""
        if self.generate_button['state'] != tk.DISABLED:
            self.generate_button.configure(bg=self.colors['button_bg'])
        
    def clear_example_text(self, event):
        """Clear example text when user focuses on the text widget"""
        if not self.example_cleared:
            self.prompt_text.delete("1.0", tk.END)
            self.example_cleared = True
            
    def update_status(self, message):
        """Update the status text area with a timestamped message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, formatted_message)
        self.status_text.config(state=tk.DISABLED)
        self.status_text.see(tk.END)
        self.update_idletasks()
        
    def validate_freecad_script(self, script):
        """Enhanced validation for FreeCAD Python scripts with stronger checks"""
        if not script or not script.strip():
            return False, "Script is empty or contains only whitespace"
            
        # Check for essential FreeCAD imports - more specific validation
        required_imports = [
            r'import\s+FreeCAD',
            r'import\s+Part'
        ]
        
        for pattern in required_imports:
            if not re.search(pattern, script, re.IGNORECASE):
                return False, f"Missing required import matching pattern: {pattern}"
        
        # Check for document creation - this is a stronger validation
        if not re.search(r'FreeCAD\.newDocument\(\)', script, re.IGNORECASE):
            return False, "Script does not appear to be a valid FreeCAD Python script (missing FreeCAD.newDocument()). Possible hallucination or invalid response."
        
        # Check for basic FreeCAD operations
        freecad_patterns = [
            r'FreeCAD\.',
            r'Part\.',
            r'\.addObject\(',
            r'\.recompute\('
        ]
        
        pattern_found = False
        for pattern in freecad_patterns:
            if re.search(pattern, script, re.IGNORECASE):
                pattern_found = True
                break
                
        if not pattern_found:
            return False, "Script does not contain recognizable FreeCAD operations"
            
        # Check for potentially dangerous operations (enhanced security)
        dangerous_patterns = [
            r'import\s+os(?!\w)',
            r'import\s+subprocess',
            r'import\s+sys(?!\w)',
            r'import\s+shutil',
            r'import\s+urllib',
            r'import\s+socket',
            r'import\s+requests',
            r'\bos\.',
            r'\bsubprocess\.',
            r'\bsys\.',
            r'\bshutil\.',
            r'\burllib\.',
            r'\bsocket\.',
            r'\brequests\.',
            r'exec\s*\(',
            r'eval\s*\(',
            r'__import__',
            r'open\s*\(',
            r'file\s*\(',
            r'input\s*\(',
            r'raw_input\s*\(',
            r'compile\s*\(',
            r'globals\s*\(',
            r'locals\s*\(',
            r'setattr\s*\(',
            r'getattr\s*\(',
            r'delattr\s*\(',
            r'hasattr\s*\('
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, script, re.IGNORECASE):
                return False, f"Script contains potentially dangerous operation: {pattern}"
                
        return True, "Script validation passed"
        
    def generate_cad_model(self):
        """Generate CAD model from user prompt"""
        # Disable the generate button to prevent multiple simultaneous requests
        self.generate_button.config(state=tk.DISABLED)
        
        # Run the generation in a separate thread to keep UI responsive
        thread = threading.Thread(target=self._generate_cad_model_thread)
        thread.daemon = True
        thread.start()
        
    def _generate_cad_model_thread(self):
        """Thread function for CAD model generation"""
        try:
            # Get prompt text
            prompt_text = self.prompt_text.get("1.0", tk.END).strip()
            
            if not prompt_text or prompt_text.startswith("Example:"):
                self.update_status("Error: Please enter a valid model description.")
                return
                
            self.update_status("Generating model... Please wait.")
            self.update_status(f"Processing prompt: {prompt_text}")
            
            # Construct Gemini payload
            full_prompt = self._construct_freecad_prompt(prompt_text)
            
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": full_prompt}]
                    }
                ],
                "generationConfig": {
                    "responseMimeType": "text/plain",
                    "maxOutputTokens": 4096,
                    "temperature": 0.3
                }
            }
            
            # Call Gemini API
            self.update_status("Connecting to Gemini AI...")
            
            try:
                response = requests.post(GEMINI_API_URL, json=payload, timeout=60)
                response.raise_for_status()
                result = response.json()
                
                # Extract the generated script
                generated_script = self._extract_script_from_response(result)
                
                if not generated_script:
                    self.update_status("Error: Gemini API returned empty or invalid response.")
                    return
                    
                self.update_status("AI response received. Validating script...")
                
                # Enhanced validation with stronger checks
                is_valid, validation_message = self.validate_freecad_script(generated_script)
                
                if not is_valid:
                    self.update_status(f"Error: Script validation failed - {validation_message}")
                    self.update_status("Possible AI hallucination detected. Please try a different prompt.")
                    return
                    
                self.update_status("Script validation passed. Creating temporary file...")
                
                # Save script to temporary file
                script_path = self._save_script_to_temp_file(generated_script)
                
                if not script_path:
                    return
                    
                # Execute FreeCAD
                self._execute_freecad(script_path)
                
            except requests.exceptions.RequestException as e:
                if hasattr(e, 'response') and e.response is not None:
                    self.update_status(f"Error connecting to Gemini API: {e.response.status_code} {e.response.reason}")
                    try:
                        error_details = e.response.text
                        if error_details:
                            self.update_status(f"Gemini API Error Details: {error_details}")
                    except:
                        pass
                else:
                    self.update_status(f"Error connecting to Gemini API: {e}")
                return
            except ValueError as e:
                self.update_status(f"Error parsing Gemini response: {e}")
                return
            except Exception as e:
                self.update_status(f"An unexpected error occurred during API call: {e}")
                return
                
        finally:
            # Re-enable the generate button
            self.generate_button.config(state=tk.NORMAL)
            
    def _construct_freecad_prompt(self, user_prompt):
        """Construct the full prompt for Gemini AI"""
        return f"""Generate a complete and valid Python script for FreeCAD to create a 3D model based on the following description.

REQUIREMENTS:
- The script must be self-contained and runnable within FreeCAD
- Use only FreeCAD's built-in modules (FreeCAD, Part, Draft, etc.)
- Do NOT import os, subprocess, sys, or any external libraries
- Do NOT include user interaction, file saving, or file I/O operations
- Create a new document at the start
- Add all geometry to the document
- End with FreeCAD.ActiveDocument.recompute() and FreeCAD.Gui.ActiveDocument.ActiveView.fitAll()
- Use proper Python syntax and FreeCAD API calls
- Create realistic dimensions if not specified

EXAMPLE STRUCTURE:
```python
import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("Model")

# Create geometry using Part module
# ... your geometry creation code here ...

# Add objects to document
doc.addObject("Part::Feature", "Model").Shape = your_shape

# Finalize
doc.recompute()
FreeCAD.Gui.ActiveDocument.ActiveView.fitAll()
```

USER DESCRIPTION: {user_prompt}

Generate only the Python script code, no explanations or markdown formatting:"""
        
    def _extract_script_from_response(self, result):
        """Extract the generated script from Gemini API response"""
        try:
            if (result and 
                result.get('candidates') and 
                result['candidates'][0].get('content') and 
                result['candidates'][0]['content'].get('parts')):
                
                generated_text = result['candidates'][0]['content']['parts'][0].get('text', '').strip()
                
                # Remove markdown code blocks if present
                if '```python' in generated_text:
                    # Extract code between ```python and ```
                    start = generated_text.find('```python') + 9
                    end = generated_text.find('```', start)
                    if end != -1:
                        generated_text = generated_text[start:end].strip()
                elif '```' in generated_text:
                    # Extract code between ``` and ```
                    start = generated_text.find('```') + 3
                    end = generated_text.find('```', start)
                    if end != -1:
                        generated_text = generated_text[start:end].strip()
                        
                return generated_text
            else:
                raise ValueError("Unexpected response structure from Gemini API")
                
        except Exception as e:
            self.update_status(f"Error extracting script from API response: {e}")
            return None
            
    def _save_script_to_temp_file(self, script):
        """Save the generated script to a temporary file"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py', encoding='utf-8') as temp_file:
                temp_file.write(script)
                script_path = temp_file.name
                
            self.update_status(f"Script saved to: {script_path}")
            return script_path
            
        except IOError as e:
            self.update_status(f"Error saving temporary script: {e}")
            return None
            
    def _execute_freecad(self, script_path):
        """Execute FreeCAD with the generated script"""
        self.update_status("Opening FreeCAD with the generated model...")
        
        try:
            # Check if FreeCAD is available
            subprocess.run([FREECAD_COMMAND, "--version"], 
                         capture_output=True, timeout=10, check=True)
            
            # Launch FreeCAD with the script
            subprocess.Popen([FREECAD_COMMAND, script_path])
            
            self.update_status("FreeCAD launched successfully!")
            self.update_status("Check the FreeCAD window for your generated 3D model.")
            
            # Schedule cleanup of temporary file after delay
            self.after(30000, lambda: self._cleanup_temp_file(script_path))
            
        except subprocess.CalledProcessError:
            self.update_status(f"Error: FreeCAD command '{FREECAD_COMMAND}' failed to execute.")
            self.update_status("Please ensure FreeCAD is properly installed.")
            
        except FileNotFoundError:
            self.update_status(f"Error: FreeCAD command '{FREECAD_COMMAND}' not found.")
            self.update_status("Please ensure FreeCAD is installed and available in your system's PATH.")
            self.update_status("You can install FreeCAD using your system's package manager:")
            self.update_status("  Ubuntu/Debian: sudo apt install freecad")
            self.update_status("  Fedora: sudo dnf install freecad")
            self.update_status("  Arch: sudo pacman -S freecad")
            
        except subprocess.TimeoutExpired:
            self.update_status("Error: FreeCAD version check timed out.")
            
        except Exception as e:
            self.update_status(f"Error launching FreeCAD: {e}")
            
    def _cleanup_temp_file(self, file_path):
        """Clean up temporary script file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.update_status(f"Temporary file cleaned up: {file_path}")
        except Exception as e:
            self.update_status(f"Warning: Could not clean up temporary file: {e}")

def main():
    """Main application entry point"""
    try:
        app = GenCADApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
