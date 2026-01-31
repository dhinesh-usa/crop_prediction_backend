#!/usr/bin/env python3
"""
Setup script for Crop Prediction Backend
This script helps initialize the project and install dependencies
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"SUCCESS: {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("ERROR: Python 3.8 or higher is required")
        return False
    print(f"SUCCESS: Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create a virtual environment"""
    if not os.path.exists("venv"):
        return run_command("python -m venv venv", "Creating virtual environment")
    else:
        print("SUCCESS: Virtual environment already exists")
        return True

def activate_and_install():
    """Activate virtual environment and install dependencies"""
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate && pip install -r requirements.txt"
    else:  # Unix/Linux/MacOS
        activate_cmd = "source venv/bin/activate && pip install -r requirements.txt"
    
    return run_command(activate_cmd, "Installing dependencies")

def create_data_directory():
    """Create data directory structure"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print("SUCCESS: Data directory created")
    return True

def main():
    """Main setup function"""
    print("Crop Prediction Backend Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("ERROR: Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not activate_and_install():
        print("ERROR: Failed to install dependencies")
        sys.exit(1)
    
    # Create data directory
    if not create_data_directory():
        print("ERROR: Failed to create data directory")
        sys.exit(1)
    
    print("\nSetup completed successfully!")
    print("\nTo run the application:")
    if os.name == 'nt':  # Windows
        print("1. Activate virtual environment: venv\\Scripts\\activate")
    else:  # Unix/Linux/MacOS
        print("1. Activate virtual environment: source venv/bin/activate")
    print("2. Run the application: python app.py")
    print("\nThe API will be available at: http://localhost:5000")

if __name__ == "__main__":
    main()