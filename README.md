![Alt pdfwizard logo](./media/pdfwizard-logo-sm.png)
# pdfwizard 
---



**pffwizard** is a Python application tool for dealing with pdf file. 


The main functionalities  are the following:
- Read pdf file's metatada informations
- Add images and/or texts into pages of the input pdf file according to an input layout as json file
- Extract annotation texts and export to a powerpoint or excel file with reference to pdf file pages

The application use the following external python library:

- [pymupdf](https://pymupdf.readthedocs.io/en/latest/intro.html): for PDF file managment
- [python-pptx](https://python-pptx.readthedocs.io/en/latest/): for Powerpoint management

### Installation
---
The application needs Python 3.11 installed on your system. 

Download from Github the zip file of the
project.

Then unzip in a folder of your choice in your system (we refear to it as [app_dir]).

Create a python virtualenvironment in the chosen directory

    [app_dir]\python -m venv venv  
    [app_dir]\venv\Scripts\activate

Install python libraries dependencies with [pip](https://pip.pypa.io/en/stable/)

    [app_dir]\python -m pip install --upgrade pymupdf
    [app_dir]\pip install python-pptx


### Usage
---
For **metadata** information extraction from an input pdf file give the following command: 

    [app_dir]\python pdfwiz.py <pdf_file_name>.pdf  
    
The comand for annotation extraction from the input pdf file is:

    [app_dir]\python pdfwiz.py <pdf_file_name>.pdf -annotatio  

While, the command to elaborate the pdf input file (adding images and/or texts) is:

    [add_dir]\python pdfwiz.py <configuration_file.name>.json  


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
