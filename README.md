![background](https://user-images.githubusercontent.com/34188200/224317301-48a0d7c9-169a-46a9-82b5-71fcf03d54d4.png)

# GerritDataAnalyser - GDA-1.0


## Description:
This Python application crawls code review data through Gerrit REST API from Android, OpenStack, and Chromium platforms and visualizes it using Matplotlib. The user-friendly GUI built with Tkinter allows users to select the platform and time period for analysis. All the data is then saved in JSON file called data.json in the Storage directory. All the graphs and chart are also exported and stored in the Storage/PDF_Files directory (Check Storage/PDF_Files for examples). 

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


## How to use the application
1. Open the sidebar:

![one](https://user-images.githubusercontent.com/34188200/224417281-5c9e832c-0b04-4675-ba3b-058a21f00c3b.png)

2. Choose your platform and choose a time period:

![two](https://user-images.githubusercontent.com/34188200/224417309-99d017e5-1a96-43e1-8689-847f37ad06f8.png)

3. It takes some time to crawl data depending on your time period. So be patient!






## Found bugs or having some advice/tips (or even problems)?
- You can reach me here: f.asadi2002@gmail.com


