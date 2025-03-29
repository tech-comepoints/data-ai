from setuptools import setup, find_packages

setup(
    name="data-dashboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'pandas',
        'plotly',
        'jinja2',
        'python-multipart',
        'sqlalchemy',
        'pyyaml',
        'requests',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'black',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A configurable data analytics dashboard",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/data-dashboard",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
) 