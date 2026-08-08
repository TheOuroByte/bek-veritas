from setuptools import setup, find_packages

setup(
    name="bek-veritas",
    version="9.0.0",
    packages=find_packages(),
    install_requires=["pydantic>=2.0", "httpx>=0.25.0"],
    author="The Fulcrum Initiative",
    description="Zero-Training Thermodynamic Logic Coprocessor for LLMs",
    python_requires=">=3.8",
)