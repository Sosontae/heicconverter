# HEIC-to-JPEG Bulk Converter
This Python script allows for easy and efficient conversion of HEIC images to JPEG format. It provides a command-line interface to navigate directories and convert all HEIC files within a selected folder.

## Prerequisites
Before running the script, ensure you have the following installed:

* Python 3.x
* Libraries: PIL, pyheif, tqdm, questionary
* Coverage

Install them using pip:

```
pip install pillow pyheif tqdm questionary coverage
```

## Installation
Clone this repository to your local machine:

```
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

## Usage
Run the script from the command line:

```
python heic_to_jpeg_converter.py
```

Follow the interactive prompts to:

1. Navigate to the directory containing your HEIC files.
2. Select the directory for conversion.
3. Converted JPEG files will be saved in a new folder within the selected directory.

## Features
Directory Navigation: Easily browse and select the folder containing HEIC files.
Bulk Conversion: Efficiently converts all HEIC files in the selected directory.
Progress Tracking: Monitor the conversion progress with a clear and informative display.
