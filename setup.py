from setuptools import setup, find_packages

setup(
    name="netVEN0M",
    version="1.0",
    author="root0emir",
    description="A Wi-Fi network scanning and brute-force tool.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/root0emir/netVEN0M",  
    packages=find_packages(),
    install_requires=[
        'scapy',  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Supported Python versions
)
