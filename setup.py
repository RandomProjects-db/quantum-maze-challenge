#!/usr/bin/env python3
"""
Quantum Maze - Enhanced Edition
AWS Build Games Challenge Entry

Setup script for easy installation and deployment
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="quantum-maze-challenge",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A quantum physics-enhanced retro maze game built with Amazon Q Developer CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/quantum-maze-challenge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Arcade",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "quantum-maze=quantum_maze:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.wav", "*.ogg", "sounds/*"],
    },
    keywords="game, quantum, physics, retro, arcade, maze, pygame, aws, challenge",
    project_urls={
        "Bug Reports": "https://github.com/your-username/quantum-maze-challenge/issues",
        "Source": "https://github.com/your-username/quantum-maze-challenge",
        "Documentation": "https://github.com/your-username/quantum-maze-challenge#readme",
    },
)
