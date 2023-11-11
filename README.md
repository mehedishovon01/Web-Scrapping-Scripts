# Introduction
This is a web scrapping with Selenium script. When data is located in a hidden table that is revealed when click on a specific tab with `ex: data-test-tab-id="1," it may require a different approach. Need to simulate the click action on the tab and then scrape the data from the revealed table.

_This often involves using libraries like Selenium to interact with the web page._
<br />

# Setup
To use this script to your own machine follow this steps

## Requirments

_You_ must have to need the following components to you machine
* Python3.10

### Python3.10

_Python 3.10_ is provided by Official _Ubuntu 22.04 LTS_ repositories and is preinstalled by default. To see which version of Python your machine have installed.

    python3 --version

If you have not install _pyhton3.10_ please follow this installation instructions

Just click here, [installation instructions](https://www.python.org/downloads/)
    

## Prepare the Script to Execute

### Clone repository from github

First of all, clone this repository using this command

    git clone https://github.com/mehedishovon01/Web-Scrapping-Scripts.git

### Create a virtualenv

Make a virtual environment to your project directory. Let's do this,

If you have already an existing python3 virtualenv then run this

    virtualenv venv

Or if virtualenv is not install in you machine then run this

    python3 -m venv venv
    
Activate the virtual environment and verify it

    . venv/bin/activate

### Install the dependencies

Most of the projects/scripts have dependency name like requirements.txt file which specifies the requirements of that projects/sripts. So, let’s install the requirements of it from the txt file.

    pip install -r requirements.txt

Boooooom! Setup is done.

## Execute the Script

### Run the Script
We are almost done. Let's run the command from terminal and get output,

    python3 scrapping.py

That’s it! Now your script is already running into the console.

After successfully execute the script it will show a message like, **_This script took X.X seconds to generate the results_**
#### _Note:_ This _Script_ will take few minutes or may be more depending on data range.
<br/>
<sub> Thanks for reading. </sub>
