import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
    requirements = f.read().splitlines()

setup(
    name="bek-veritas",
    version="8.0.0", 
    packages=find_packages(),
    install_requires=requirements,
    author="J. Bravo - The Fulcrum Initiative",
    description="Zero-Training Thermodynamic Logic Coprocessor for LLMs",
    python_requires=">=3.8",
)
