# Projeto-IA
Project for the Artificial Intelligence University Class

## Setup Guide

### 1. Clone the Repository

First, clone the Projeto-IA repository to your local machine. You can do this by running the following command in your terminal or command prompt:

```bash
git clone https://github.com/Zane-dev16/Projeto-IA.git
```

### 2. Install Python

Ensure that Python is installed on your system. If Python is not installed, you can download and install it from the official Python website: [Python Downloads](https://www.python.org/downloads/)

### 3. Navigate to Projeto-IA Folder

Open a terminal or command prompt and navigate to the Projeto-IA folder:

```bash
cd /path/to/Projeto-IA
```

### 4. Create Virtual Environment

Create a virtual environment named `projenv` using Python's built-in `venv` module:

```bash
python -m venv projenv
```

5. Activate Virtual Environment
Activate the projenv virtual environment. Activation steps depend on your operating system:

**On Windows**:

```bash
projenv\Scripts\activate
```

**On Unix or MacOS**:
```bash
source projenv/bin/activate
```

6. Install Dependencies
Install project dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

## How to Test

To run the program, follow these steps:

1. Ensure you are in the Projeto-IA directory in the terminal.

2. Use the following syntax to run the program:

```bash
python proj2324base/pipe.py < test_folder_name/test_file_name
```

For example:
```bash
python proj2324base/pipe.py < custom-tests/mytest1.txt
```
