# Article Renamer

--------------------------------
### PROBLEM and MOTIVATION: 
Downloaded scientific papers and books usually come with unreadable/weird file names. Yes, Mendeley or EndNote are able identify the files, but do so only inside their own interface, the folder in which the files actually are usually still look like a mess. Since renaming each file manually is a pain, and python is fun, we tried to mitigate the problem.

### SOLUTION: 
Based on each file's doi (Digital Object Identifier), the python scripts attempt to rename all .pdf files included in the folder from which they are executed. Renaming is done following the format 'Title, Year' or 'Year, Title', depending on which script was used. Doi codes are searched in each file's metadata and inside the text. 

The scripts were proven to work for most scientific articles and books, falling when:
	- file is old, therefore, does not have an assigned doi
	- .pdf file is encrypted or protected
	- doi is really mixed with other strings or placed in unusual position, e.g. in the 3th page footer aside a logo.
	- .pdf file is cursed.

### ATENTION: 
If you have suggestions in how to improve these scripts, please comment about it on github or open an issue over it; credit will, of course, be shared. Keep in mind that the idea is to make something simple, that does not require the download of huge python libraries or support software, for example, the Microsoft Visual Tools required by the pdftotext python library.

--------------------------------
## INSTALATION:

Everything required to execute these scripts occupy around 150 MB. 
 
1. Install the most recent version of Python from 'https://www.python.org/downloads/'. The python version used here was 3.7.4.

2. The pip should have already been installed from the previous step. If not follow the procedures from one of the recommended links:
	- https://phoenixnap.com/kb/install-pip-windows
	- https://pip.pypa.io/en/stable/installing/

3. Download all files from this github repository.

4. Install the python libraries required, for such run in Windows command prompt the following:
	
	`pip install requests==2.22.0 PyPDF2==1.26.0 glob2==0.7`
	
	Alternatively, use the requirements file by running the command line from the same directory:

	`pip install -r requirements.txt`


## USAGE:

1. Make a copy of the Article_Renamer_Title_Year.py or the Article_Renamer_Year_Title.py and drag it to the desired folder containing the .pdf files to be renamed.

2. Right click over the copied script and select 'Edit with IDLE'

3. Once it opens, Press F5

4. Wait

5. When you see the 'DONE!', well its done.

## NOTES:

1. The script does not affect subfolders

2. Repeated files are renamed with a -RPT after them

3. Running the script twice will add -RPT to all file names.




Writen by Adriano.S.P.P and Denise.A.G. - 09/07/2020; inpired by NECESSITY and user "Pu Du" from Researchgate.net
