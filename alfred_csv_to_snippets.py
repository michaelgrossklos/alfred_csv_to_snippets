# alfred_csv_to_snippets.py
# Generates Alfred 4 json snippet files from a csv file
# Written for python 3.8.5
# 
# Based on the script by derickfey (https://github.com/derickfay/import-alfred-snippets)
#
# Author: Michael Großklos (https://github.com/michaelgrossklos)
#
# Published under MIT license
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software 
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from csv import DictReader
from json import dumps
from os import urandom, path, mkdir, walk   
from binascii import b2a_hex
from sys import exit, argv

import subprocess
import uuid
import logging
import shutil
import time

logging.basicConfig(level=logging.DEBUG)

def dd(msg):
    logging.debug(msg)
    exit()

def errorMsg(message):
    print('ERROR: ' + message)
    exit()  
    

print("Specify the path where the CSV files are located:")
inputPath = input()
if not path.isdir(inputPath):
        errorMsg("The path you provided does not exist or isn't a directory:\n" + inputPath) 

print("Is this the order in which the content in your csv files is sorted: 'keyword, content, name'? (Y/n):")
isSorted = input()
if isSorted == "y" or isSorted =="":
    fieldNames = ["keyword", "content", "name"]
else:
    print("Specify the order in which the content is sorted (f.e.: 'name, content, keyword'):")
    inputSorting = input()  
    fieldNames = inputSorting.replace(",", " ").replace("'", "").split()
    if type(fieldNames) != list:
        errorMsg("Your provided order is not a list like: 'keyword, content, name'")  

print("Where to save the converted files?")
targetPath = input()
if not path.isdir(targetPath):
        errorMsg("The path you provided does not exist or isn't a directory:\n" + targetPath) 

print("In order to convert the csv files into *.alfredsnippets files,\n this script generates one subfolder per file into which the single snippet files get saved.\n Do you want to keep those folders, otherwise they get deleted? (y/N)")
keepFolders = input()

createdFolders = []

for root, dirs, files in walk(inputPath):
    for outputFile in files:
        if outputFile.endswith('.csv'): 

            fileName, fileExtension = path.splitext(outputFile)
            outputPath=""
            outputPath = targetPath + "/" + fileName

            try:
                mkdir(outputPath)
                print(f'Making folder {outputPath}...')
            except OSError:
                print ("Creation of the directory %s failed" % path)


            with open (path.join(inputPath, outputFile), 'rt') as csvfile:
                reader = DictReader(csvfile, fieldnames=fieldNames)
                
                for row in reader:    
                    uid = str(uuid.uuid1()).upper()

                    output = dumps({"alfredsnippet" : {"snippet" : row['content'], "uid": uid, "name" : row['name'], "keyword" : row['keyword']}}, sort_keys=False, indent=4, separators=(',', ': '))
                    outputFile = row['name']+" ["+uid+"].json"
                    target = outputPath + "/" + outputFile              
                    f = open(target, 'w')
                    f.write(output)
                    f.close()
                    print(f"Writing file {target}...")    
        else:
            errorMsg("The files in the provided folder are not *.csv files.")

        subprocess.call(['ditto', '--norsrc', '-ck', outputPath, targetPath + "/" + fileName + ".alfredsnippets"])
        print(f"{targetPath}/{fileName}.alfredsnippets was created")
        createdFolders.append(fileName)

if keepFolders == "n" or keepFolders == "":
    time.sleep(2)
    for f in createdFolders:
        shutil.rmtree(targetPath + "/" + f)
        print(f"{targetPath}/{f} was deleted")





