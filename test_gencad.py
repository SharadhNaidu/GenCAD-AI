#!/usr/bin/env python3
"""
Test script for GenCAD AI
Tests basic functionality without actually calling the API or launching FreeCAD
"""

import sys
import os

# Add the parent directory to the path to import gencad_ai
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_script_validation():
    """Test the script validation function"""
    print("Testing script validation...")
    
    # Import the validation function
    from gencad_ai import GenCADApp
    app = GenCADApp()
    
    # Test valid script
    valid_script = """
import FreeCAD
import Part

doc = FreeCAD.newDocument("Test")
box = Part.makeBox(10, 10, 10)
doc.addObject("Part::Feature", "Box").Shape = box
doc.recompute()
FreeCAD.Gui.ActiveDocument.ActiveView.fitAll()
"""
    
    is_valid, message = app.validate_freecad_script(valid_script)
    print(f"Valid script test: {'PASS' if is_valid else 'FAIL'} - {message}")
    
    # Test invalid script (missing imports)
    invalid_script1 = """
doc = FreeCAD.newDocument("Test")
box = Part.makeBox(10, 10, 10)
"""
    
    is_valid, message = app.validate_freecad_script(invalid_script1)
    print(f"Invalid script test 1: {'PASS' if not is_valid else 'FAIL'} - {message}")
    
    # Test dangerous script
    dangerous_script = """
import FreeCAD
import Part
import os
os.system("rm -rf /")
"""
    
    is_valid, message = app.validate_freecad_script(dangerous_script)
    print(f"Dangerous script test: {'PASS' if not is_valid else 'FAIL'} - {message}")
    
    # Test empty script
    empty_script = ""
    
    is_valid, message = app.validate_freecad_script(empty_script)
    print(f"Empty script test: {'PASS' if not is_valid else 'FAIL'} - {message}")
    
    app.destroy()  # Clean up the tkinter window

def test_imports():
    """Test that all required modules can be imported"""
    print("\nTesting imports...")
    
    try:
        import tkinter
        print("✓ tkinter imported successfully")
    except ImportError as e:
        print(f"✗ tkinter import failed: {e}")
        return False
    
    try:
        import requests
        print("✓ requests imported successfully")
    except ImportError as e:
        print(f"✗ requests import failed: {e}")
        return False
    
    try:
        import threading
        print("✓ threading imported successfully")
    except ImportError as e:
        print(f"✗ threading import failed: {e}")
        return False
    
    try:
        import tempfile
        print("✓ tempfile imported successfully")
    except ImportError as e:
        print(f"✗ tempfile import failed: {e}")
        return False
    
    return True

def test_freecad_availability():
    """Test if FreeCAD is available in the system"""
    print("\nTesting FreeCAD availability...")
    
    import subprocess
    
    try:
        result = subprocess.run(['freecad', '--version'], 
                              capture_output=True, 
                              timeout=10, 
                              text=True)
        if result.returncode == 0:
            print("✓ FreeCAD is available in PATH")
            print(f"  Version info: {result.stdout.strip()}")
            return True
        else:
            print("✗ FreeCAD command failed")
            return False
    except FileNotFoundError:
        print("✗ FreeCAD not found in PATH")
        print("  Install FreeCAD using your system's package manager:")
        print("  Ubuntu/Debian: sudo apt install freecad")
        print("  Fedora: sudo dnf install freecad")
        print("  Arch: sudo pacman -S freecad")
        return False
    except subprocess.TimeoutExpired:
        print("✗ FreeCAD version check timed out")
        return False
    except Exception as e:
        print(f"✗ Error checking FreeCAD: {e}")
        return False

def main():
    """Run all tests"""
    print("GenCAD AI Test Suite")
    print("===================")
    
    tests_passed = 0
    total_tests = 3
    
    # Test imports
    if test_imports():
        tests_passed += 1
    
    # Test script validation
    try:
        test_script_validation()
        tests_passed += 1
        print("✓ Script validation tests completed")
    except Exception as e:
        print(f"✗ Script validation tests failed: {e}")
    
    # Test FreeCAD availability
    if test_freecad_availability():
        tests_passed += 1
    
    print(f"\nTest Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! GenCAD AI should work correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
