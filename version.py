#!/usr/bin/env python3
"""
Version information for Macro Recorder Tool
"""

__version__ = "1.0.0"
__author__ = "Macro Recorder Development Team"
__email__ = "support@macrorecorder.com"
__license__ = "MIT"
__copyright__ = "Copyright 2024, Macro Recorder Tool"

# Build information
BUILD_DATE = "2024-12-19"
BUILD_NUMBER = "1"

# Application metadata
APP_NAME = "Macro Recorder Tool"
APP_DESCRIPTION = "🎯 Tool ghi lại và phát lại các hành động chuột và bàn phím"
APP_URL = "https://github.com/macrorecorder/tool"

# Version components
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0

def get_version():
    """Get formatted version string"""
    return f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

def get_version_info():
    """Get detailed version information"""
    return {
        "version": get_version(),
        "build_date": BUILD_DATE,
        "build_number": BUILD_NUMBER,
        "python_version": None,  # Will be filled at runtime
        "platform": None,       # Will be filled at runtime
    }

def print_version():
    """Print version information"""
    print(f"{APP_NAME} v{get_version()}")
    print(f"Build: {BUILD_DATE}.{BUILD_NUMBER}")
    print(f"Author: {__author__}")
    print(f"License: {__license__}")

if __name__ == "__main__":
    print_version() 