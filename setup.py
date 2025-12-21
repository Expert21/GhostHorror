from setuptools import setup, find_packages

setup(
    name="ghost-horror",
    version="1.0.0",
    description="A spooky fullscreen experience for launching Ekphos",
    author="Isaiah",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.0",
        "python-xlib>=0.33",
    ],
    entry_points={
        "console_scripts": [
            "ghost-horror=ghost_horror.main:main",
        ],
    },
    python_requires=">=3.8",
)
