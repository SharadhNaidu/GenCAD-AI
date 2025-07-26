# GenCAD AI - Linux Desktop 3D Model Generator

GenCAD AI is a standalone Linux desktop application that generates FreeCAD 3D models from natural language text prompts using Google Gemini AI. The application features a simple, black-and-white user interface and requires no sign-in.

## Features

- **Text-to-3D Model Generation**: Convert natural language descriptions into FreeCAD 3D models
- **No Sign-in Required**: Works immediately upon launch
- **Simple UI**: Clean, minimalistic black-and-white interface
- **AI-Powered**: Uses Google Gemini AI for intelligent script generation
- **Safety First**: Built-in validation to prevent malicious code execution
- **Cross-Distribution**: Compatible with any Linux distribution

## Prerequisites

### Required Software
1. **Python 3.6+** (usually pre-installed on most Linux distributions)
2. **FreeCAD** - The open-source 3D CAD software
3. **Internet Connection** - For Google Gemini API access

### Installing FreeCAD

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install freecad
```

#### Fedora:
```bash
sudo dnf install freecad
```

#### Arch Linux:
```bash
sudo pacman -S freecad
```

#### openSUSE:
```bash
sudo zypper install FreeCAD
```

### Installing Python Dependencies
```bash
cd "Gen CAD AI"
pip3 install -r requirements.txt
```

Or install manually:
```bash
pip3 install requests
```

## Installation

1. **Clone or download** this project to your preferred directory
2. **Install dependencies** as shown above
3. **Ensure FreeCAD is in your PATH** by running:
   ```bash
   freecad --version
   ```
   If this command fails, you may need to add FreeCAD to your PATH or install it.

## Usage

### Running the Application
```bash
cd "Gen CAD AI"
python3 gencad_ai.py
```

### How to Use
1. **Launch the application** using the command above
2. **Enter a description** of the 3D model you want to create in the text input area
3. **Click "Generate CAD Model"** to start the generation process
4. **Wait for processing** - the status area will show progress updates
5. **FreeCAD will open** automatically with your generated 3D model

### Example Prompts
- "Create a 50mm cube with a 10mm cylindrical hole through the center"
- "Design a simple bottle opener with a handle"
- "Make a bracket with two mounting holes"
- "Generate a gear with 20 teeth and 5mm thickness"
- "Create a hexagonal nut with M8 thread"

## Application Features

### User Interface
- **Title Area**: Displays "GenCAD AI" and subtitle
- **Prompt Input**: Multi-line text area for entering model descriptions
- **Generate Button**: Triggers the AI model generation process
- **Status Area**: Shows real-time progress updates and error messages

### Safety Features
- **Script Validation**: Automatically validates generated code for safety
- **Hallucination Prevention**: Detects and prevents execution of invalid or malicious code
- **Error Handling**: Comprehensive error handling for network, API, and system issues
- **Timeout Protection**: Prevents hanging on long-running API requests

### Technical Implementation
- **GUI Framework**: Tkinter (built-in with Python)
- **API Integration**: Google Gemini AI via REST API
- **CAD Integration**: FreeCAD Python scripting
- **Threading**: Non-blocking UI during AI processing

## Troubleshooting

### Common Issues

#### "FreeCAD command not found"
- Ensure FreeCAD is installed: `sudo apt install freecad` (Ubuntu/Debian)
- Verify installation: `freecad --version`
- Check if FreeCAD is in your PATH

#### "Error connecting to Gemini API"
- Check your internet connection
- Verify the API key is valid
- Check if you've exceeded API quota limits

#### "Script validation failed"
- The AI generated invalid or potentially unsafe code
- Try rephrasing your prompt with more specific details
- Use simpler geometric descriptions

#### Application won't start
- Ensure Python 3 is installed: `python3 --version`
- Install missing dependencies: `pip3 install requests`
- Check for error messages in the terminal

### Getting Better Results
- **Be specific**: Include dimensions, materials, and details
- **Use simple geometry**: Start with basic shapes and combinations
- **Specify units**: Include measurements in mm, cm, or inches
- **Describe purpose**: Mention what the object is for

## File Structure
```
Gen CAD AI/
├── gencad_ai.py          # Main application file
├── requirements.txt      # Python dependencies
├── README.md            # This documentation
└── examples/            # Example prompts and outputs (optional)
```

## Security Notes

- The application validates all AI-generated code before execution
- Only FreeCAD-specific Python modules are allowed
- Network operations and file I/O are blocked in generated scripts
- Temporary files are automatically cleaned up

## API Configuration

The application uses the Google Gemini API key provided in the prompt. For production use, consider:
- Storing the API key in environment variables
- Implementing user-configurable API settings
- Adding API usage monitoring

## Contributing

This is a standalone project implementation. For modifications:
1. Ensure all changes maintain the security validation features
2. Test with various prompt types and edge cases
3. Maintain the simple, black-and-white UI design
4. Follow the existing error handling patterns

## License

This project is provided as-is for educational and personal use. Please ensure compliance with:
- Google Gemini API terms of service
- FreeCAD licensing requirements
- Local regulations regarding AI-generated content

## Support

For issues with:
- **FreeCAD**: Check the official FreeCAD documentation
- **Google Gemini API**: Refer to Google's AI documentation
- **Linux Installation**: Consult your distribution's package manager documentation
