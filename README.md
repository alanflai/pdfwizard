# pdfwizard 
---
![Alt pdfwizard logo](./Media/pdfwizard-logo-sm.png)


**pffwizard** is a Python application tool for dealing with pdf file. 


The main functionalities of this tool are the following:
- Read pdf file's metatada informations
- Add images and/or texts into the pdf file's pages
- Extract annotation texts withe the page's reference. The information can be ecported to an external powerpoint file or excel files

### Installation
---
The application needs Python 3.11 installed on your system. 

Download from Github the zip file of the
project.

Then unzip in a folder of your choice in your system (we refear to it as [app_dir]).

Create a python virtualenvironmnet in the chose directory

    [app_dir]\python -m venv venv  
    [app_dir]\venv\Scripts\activate

Install python libraries dependencies with [pip](https://pip.pypa.io/en/stable/)

    [app_dir]\python -m pip install --upgrade pymupdf
    [app_dir]\pip install python-pptx


### Usage
---


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
