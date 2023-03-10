![background](https://user-images.githubusercontent.com/34188200/224317301-48a0d7c9-169a-46a9-82b5-71fcf03d54d4.png)

# GerritDataAnalyser - GDA-1.0


## Description:
This Python application crawls code review data through Gerrit REST API from Android, OpenStack, and Chromium platforms and visualizes it using Matplotlib. The user-friendly GUI built with Tkinter allows users to select the platform and time period for analysis. All the data is then saved in JSON file called data.JSON. All the graphs and chart are also exported and stored in the PDF_Files directory. 

The tool helps developers, project managers, and stakeholders to identify trends, patterns, and bottlenecks in their code review process, optimizing their workflow and improving efficiency. 

This open-source project is available on Github for contributions to its continuous improvement and expansion.

#### Credits
The theme used for this application is developed by: https://github.com/rdbende/Azure-ttk-theme.git

## Installation:
- The application is compatible with all major operating systems (Windows, MacOS, Linux, etc.).
### Note! To run the application, you will need to have Python 3.7 or higher installed on your system.

### Linux:
1. Download the ZIP file and extract it.
2. Install pip and Tkinter using:
```sh
sudo apt install python3-pip
sudo apt install python3-tk
```
3. Install pil and pil.imagetk using:
```sh
sudo apt-get install python3-pil python3-pil.imagetk
```
4. Install the requiremetns.txt using:
```sh
pip install -r requirements.txt
```
5. To run the application go to the extracted folder and run the main.py
```sh
python3 main.py
```
6. Enjoy!

### Windows OS:
1. Download the ZIP file and extract it
2. Install the requiremetns.txt using:
```sh
pip install -r requirements.txt
```
3. To run the application open cmd, navigate to the folder and run
```sh
python3 main.py
```
4. Enjoy!


