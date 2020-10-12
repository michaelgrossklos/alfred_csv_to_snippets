# A Small Converter Script for Alfred Snippets

This script converts export files (*.csv) from other snippet tools like TextExpander into *.alfredsnippets archives, which than easally can be imported into Alfred 4. With limitation the script replaces the placeholders for embedded snippets. It is inspired by the script by derickfay https://github.com/derickfay/import-alfred-snippets. In fact small snippets of his code is still in this one. 

## Dependencies
There is one dependency which the script needs to convert the files. It is `Ditto` [https://ss64.com/osx/ditto.html](https://ss64.com/osx/ditto.html). Most likely, it's already installed on your machine. You can find out by simply typing `which ditto` in the terminal. If you get something like this `/usr/bin/ditto`, you are good to go.

If `ditto` isn't installed on your machine, you should be able to install it via `Homebrew Casks` [https://github.com/Homebrew/homebrew-cask/blob/master/Casks/ditto.rb](https://github.com/Homebrew/homebrew-cask/blob/master/Casks/ditto.rb). 

`Ditto` is used to pack the snippets folders into the actual `*.alfredsnippets` archives.

## Usage 
Using this script is as simple as typing the following in the terminal:
`python3 AlfredCsvToSnippets.py [args]`  

**_*<span style="color: #ff0000">CAUTION: Using this script is on your own risk.</span> Not that it could be more dangerous than loosing all the `*.csv` files. I did not deep testing this script and it is more like an quick and dirty aproach even thou, I tried to put in some error handling. So you've be warned ;)*_**

### Folder Structure 
It doesn't matter where to put this script or the exported `*.csv` files from the other snippet tool. But I recomment creating a dedicated folder on your Desktop. In this folder you should put this very script and creating a subfolder where you can place the `*.csv` files. And also create a subfolder where the converted files can be saved. The names of the folders doesn't matter. The folder structure could look like this.

![Bildschirmfoto 2020-10-12 um 17 53 59](https://user-images.githubusercontent.com/6610580/95774830-7b319300-0cc1-11eb-9a1a-15f231aa9abc.png)

### Command line arguments 
The script uses command line agruments which you can specify behind the script call. The argument `-h` or `--help` shows all the arguments one can set. Basically all arguments are opional. 

#### `-i` or `--input` (str) [default: current working directory]
`Example: AlfredCsvToSnippets.py -i "./input_folder"`<br>
This is the path to the folder where all the csv files are in. If you're following my advice, this path could be look like above.

**Notice:** *This path **must** be relativ to the `AlfredCsvToSnippets.py`. 

#### `-o` or `--output` (str) [default: current working directory]
`Example: AlfredCsvToSnippets.py -o "./output_folder"`<br>
The `*.alfredsnippets` files need to be stored. Here you can tell the `AlfredCsvToSnippets.py`, where this place should be. Like the `--input` path, this one should be relativ to the script too. According to my recomendation this path could be like the example above. 

**Notice:** *The folder you specify here, must already exist. The Script does not create one.*

#### `-f` or `--fieldorder` (str) [default: abbreviation, content, name]
`Example: AlfredCsvToSnippets.py -f "abbreviation, name, content"`<br>
The `*.csv` files must contain exactly three fields: the snippet abbreviation, the snippet name and the snippet content/text. The `*.csv` files don't need a first line with header names. Such a file could look somethings along the lines like:
```
"xseldriv","from selenium import webdriver","Python import Selenium webdriver"
"xsel","from selenium.webdriver.common.keys import Keys","Python Selenium Keys"
"xfebxp","driver.find_element_by_xpath()","Python find XPath"
"xfebcss","driver.find_element_by_css_selector()","Python find CSS"
``` 

In the case above, the order of the elements are: abbreviation, content, name. If you've exported snippets from TextExpander it is likely possible that this order is allready correct. In that case, you don't need to use this argument.

### Embedded snippets
There may be already some embedded snippets in your snippets. In case of TextExpander they look like this `%snippet:foobar%`. Well, gues what?! In Alfred they look like this `{snippet:foobar}`. Not a huge difference but still a difference. If you would import your snippets with the `%snippet:foobar%` placeholders and you use this snippet, the placeholder would not be replaced with the embedded snippet. Instead you'd see just the text `%snippet:foobar%`.

Well, with the `AlfredCsvToSnippets.py` script those placeholderd get replaced. At least some of them. Because some snippet tool have some more snippet features than Alfred actually has. There are all kinds of placeholders. Since Alfred does not have the functionality that your actual snippet tool provides, we aren't be able to change these placeholders. The script is only be able to change two kind of placeholders which are `%snippet:foobar%` and `%|`. The last one is used (at least in TextExpander) as the placeholder for the cursor. In Alfred this is represented by `{cursor}`.

Because I don't know all the different placeholders in all the tools, I decided to make the symbols changeable. With symbol I mean this `%`. Since most of the tools uses a left and a right symbol, you can set two different symbols. Below you can read how to use this feature.

#### `-l`or `--lplaceholder` (str) [default: %]
`Example: AlfredCsvToSnippets.py -l "{{"`<br>
Just provide the symbol that is on the left hand side of the placeholder code. As you can see it don't need to be just one character.

#### `-r`or `--rplaceholder` (str) [default: %]
`Example: AlfredCsvToSnippets.py -r "}}"`<br>
Just provide the symbol that is on the right hand side of the placeholder code. As you can see it don't need to be just one character.

#### `-c`or `--changeplaceholders` (bool) [default: true]
`Example: AlfredCsvToSnippets.py -c false`<br>
If you do not want to have the placeholders changed at all, set this to false. If you are using this agument, the placeholders will be remain untouched. In that case obviously, you don't need to set the `--lplaceholder` nor the `--rplaceholder`.

#### `-d`or `--deletefolders` (bool) [default: false]
`Example: AlfredCsvToSnippets.py -d false`<br>
In order to convert the `*.csv` files into `*.alfredsnippets` files, this script generates one subfolder per `*.csv` file, into which the single snippet files will be saved. Usually one `*.csv` file consists of multible snippets. Therfore the file represends the snippets group. During the conversion, these files are getting turned into subfolders in which the single files will be placed. For each row (record) of that `*.csv`, one `*.json` file will be created. These files are the single snippet files. Their names are looking someting like this: `EN Screencast Site [2F6C090A-0BEA-11EB-80EF-002332307138].json`. Don't worry about the gibberish between the brackets. It's just a unique identifyer that Alfred requires.

These automatically created subfolders, can be automatically deleted. But if you wish to keep them you use the argument below. In the end you will have the `*.alfredsnippets` files and smome folders named after the `*.csv` files. 


### Importing the files into Alfred 4
To import the `*.alfredsnippets` files into Alfred 4, just double click them. Alfred Preferences will then open and you can verfy that you are willing to import these snippets. Each file gets stored as a seperate group in Alfred 4.
