# User Reports
The user exports found in the admin panel of the Startup Colorado page is nearly impossible to read and extract useful information from in it's original state. The goal of this repo is to generate readable pdf reports from the raw user exports. 
#
### Generating Reports
The main file in this repository is the 'generate_reports.py'. If you would like to create a packaged executable application of the script, use pyinstaller (downloadable pip package) with the following command:

pyinstaller --onefile --console .\generate_reports.py

This executable should appear in a 'dist' folder in the directory you reside in. 
NOTE: If you have many packages/libraries installed, all of those get included in the bundled application. This can cause the size of the generated executable to skyrocket and hard to transfer. To avoid this, create a virtual environment with python and only installed the needed packages/libraries to run the script.
