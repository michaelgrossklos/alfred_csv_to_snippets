# A Small Converter Script for Alfred Snippets

This script converts export files (*.csv) from other snippet tools like TextExpander into *.alfredsnippets archives, which than easaly can be importet into Alfred 4.

## Dependencies
There is one dependency which the script needs to convert the files. It is `Ditto` [https://ss64.com/osx/ditto.html](https://ss64.com/osx/ditto.html). Most likely, it's already installed on your machine. You can find out by simply typing `which ditto` in the terminal. If you get something like this `/usr/bin/ditto`, you are good to go.

If `ditto` isn't installed on your machine, you should be able to install it via `Homebrew Casks` [https://github.com/Homebrew/homebrew-cask/blob/master/Casks/ditto.rb](https://github.com/Homebrew/homebrew-cask/blob/master/Casks/ditto.rb). 

`Ditto` is used to pack the snippets folders into the actual `*.alfredsnippets` archives.

## Usage ##
Using this script is as simple as typing the following in the terminal:
`python3 alfred_csv_to_snippets.py`  

**_*<span style="color: #ff0000">CAUTION: Using this script is on your own risk.</span> Not that it could be more dangerous than loosing all the `*.csv` files. I did not deep testing this script and it is more like an quick and dirty aproach even thou, I tried to put in some error handling. So you've be warned ;)*_**

### Saving the files ###
It doesn't matter where to put this script or the exported `*.csv` files. Because during the process, you can specify all needed paths. I recomment making a dedicated folder on your Desktop. In ths folder you should put this script and make subfolder where you can place the exported `*.csv` files. And also make a subfolder, where the converted files can be saved to. The names of the folders doesn't matter. But as I said, you can put them where ever you please.

### The questions ###
No, it is not a questioneer. But during the processing of the script you get asked some questions.

#### #1. Specify the path where the CSV files are located: ####
If you're following my advice, this path could be `./csvfolder`. 

**Notice:** *this path must be relativ to the script. If you (for example) have put the script in a folder on your Desktop named `AlfredSnippets` and in that folder you created a subfolder named `csvfolder`, the relative path to that subfolder would be as shown above.* 

#### #2. Is this the order in which the content in your csv files is sorted: 'keyword, content, name'? (Y/n): ####

The `*.csv` files must contain exactly three fields: the snippet abriviation, the snippet name and the snippet content/text. They don't need a first line with header names. Such a file could look somethins along the lines like this:
```
"xseldriv","from selenium import webdriver","Python import Selenium webdriver"
"xsel","from selenium.webdriver.common.keys import Keys","Python Selenium Keys"
"xfebxp","driver.find_element_by_xpath()","Python find XPath"
"xfebcss","driver.find_element_by_css_selector()","Python find CSS"
``` 

In the case above, the order of the elements are: keyword, content, name. Ff you exported snippets from TextExpander it is likely possible that this order is matching. in this case, you just can press Enter.

If the fileds doesn't match, just type `n`and press Enter.

#### #3. Specify the order in which the content is sorted (f.e.: 'name, content, keyword'): ####
In case you answered the question before with `n`, here is the place to specify the order that matches your `*.csv`files. Just type the order of the fields seperated by commas, f.e.: `name, keyword, content`. **Notice:** it is important that you stick to the field names. They have to be `name`, `content` and `keyword`. You just need to putit in the right order.

#### #4. Where to save the converted files? ####
The `*.alfredsnippets` files need a place to be stored. Here you can tell the script, where this place should be. Like the prior mentioned path, this one should be relativ to the script too. I comem back to my recomendation: this path could be something like this: `./export`.

#### #5. Deleting subfolders? ####
In order to convert the `*.csv` files into `*.alfredsnippets` files, this script generates one subfolder per file, into which the single snippet files get saved. Usually one `*.csv` file consists of multible snippets. therfore the file represends the snippets group. During the convertion, these files are getting turned into subfolders in which single files will be placed. These files are the single snippet files. Their names are someting like this: `EN Screencast Site [2F6C090A-0BEA-11EB-80EF-002332307138].json`. Don't worry about the gibberish between the brackets.

These automatically created subfolders, with the `*.json` files in them, can be deleted by the script, after the `*.alfredsnippets` files have been created. but if you wish, you just can type `y` on this question and the folders wont get deleted. Eather way... in the end you will have the `*.alfredsnippets`files. These are alongside the subfolders in the export folder that you specified earlier.  

### Importing the files into Alfred App ###
To import the `*.alfredsnippets`files into Alfred 4, just double click them. Alfred Preferences will then open and you can verfy that you are willing to import these snippets. Each file gets stored as a seperate group in Alfred 4.

## Remarks ##
### Embedded snippets support ###
Since Alfred 4.1 supports embedded snippets, which adds even more power to the tool, there is a little scatch to this script. If you are using other snippet tools that are allready suttporting embeded snippets, the possibility is very high that the placeholders do not match. For example the embeded snippet placeholders of TextExpander are looking like this `%snippet:xmailsid%` or in case of the placeholder where the cursor should be placed `%|`. 

This scipt does not change the contents inside the snippets. So maybe you have to do a little work to change these placeholders. Mainly it is just a matter of changing the `%%` with `{}`.

Maybe in the future I add the functionality to change these placeholders automatically. But for now it is what it is. If one is in mood to add that functionality, please feel free to do so.

### My apologies ###
Since english is not my first langage (I am German), I ple to apologise all the typos and missspellings and gramar failures. Not just here but also in the script. If you want to fix them, feel free to do so.