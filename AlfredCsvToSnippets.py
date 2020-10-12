# AlfredCsvToSnippets.py
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


import argparse
import logging
import re
import shutil
import subprocess
import time
import uuid
from csv import DictReader
from json import dumps
from os import path, mkdir, walk, getcwd
from sys import exit

# Turning on logging
logging.basicConfig(level=logging.DEBUG)


class AlfredCsvToSnippets:

    def __init__(self):
        self.created_folders = []
        self.parser = argparse.ArgumentParser()
        self.args = None

    @staticmethod
    def str2bool(v) -> bool:
        """
        A method to get bool values from the command line
        :param v: The input from the command line argument
        :type v: str
        :rtype: bool
        """

        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    @staticmethod
    def error_msg(msg: str) -> None:
        """
        Just a little helper
        :param msg:
        :type msg: str
        :return: None
        """
        print("ERROR: ", msg)
        exit(2)

    @staticmethod
    def dd(msg: str) -> None:
        """
        Just a little helper
        :param msg: The text to display
        :type msg: str
        :return: None
        """
        logging.debug(msg)
        exit(2)

    @staticmethod
    def replace_embedded_snipptes(content: str, sc_left: str, sc_right: str, change: bool) -> str:
        """ In the provided snippets are embedded snippets placeholder. Those wont fit for Alfred. So it gets changed
            :param content: The text content of the snippet
            :type content: str
            :param sc_left: The left side symbol of the placeholder f.e. "%"
            :type sc_left: str
            :param sc_right: sc_right The right side symbol of the placeholder f.e. "%"
            :type sc_right: str
            :param change: If false there will be no changes
            :type: bool
            :return: The replaced text content
            :rtype: str
        """

        if change:
            # this regex will turn something like %snippet:foo% into something like {snippet:foo}
            content = re.sub(rf"{sc_left}(\w+:\w+){sc_right}", r"{\1}", content)

            # this line changes the cursor position placeholder (ONLY TEXTEXPANDER TESTED)
            content = re.sub(rf"{sc_left}\|", "{cursor}", content)

            return content

    def remove_temp_folders(self) -> None:
        """
        Deletes the folders with the json files in it
        """
        if self.args.deletefolders:
            time.sleep(2)
            for f in self.created_folders:
                shutil.rmtree(path.join(self.args.output, f))
                print(f"{self.args.output}/{f} was deleted")

    def parse_command_line_args(self) -> None:
        """
        Parses the command line arguments
        :return: None
        """
        self.parser.add_argument(
            "-i",
            "--input",
            help="(str) [default: .] The relative folder path with the csv files",
            default=getcwd()
        )
        self.parser.add_argument(
            "-o",
            "--output",
            help="(str) [default: .] The folder path for saving the *.alfredsnippets files",
            default=getcwd()
        )
        self.parser.add_argument(
            "-f",
            "--fieldorder",
            help="(str) [default: 'abbreviation, content, name'] A comma separated list for the order of the fields "
                 "of the csv files",
            default="abbreviation, content, name"
        )
        self.parser.add_argument(
            "-d",
            "--deletefolders",
            help="(bool) [default=False] Delete the folders that contains the json files",
            type=self.str2bool,
            nargs='?',
            const=True,
            default=False
        )
        self.parser.add_argument(
            "-l",
            "--lplaceholder",
            help="(str) [default: %] The left side placeholder for the embedded snippets.",
            default="%"
        )
        self.parser.add_argument(
            "-r",
            "--rplaceholder",
            help="(str) [default: %] The right side placeholder for the embedded snippets.",
            default="%"
        )

        self.parser.add_argument(
            "-c",
            "--changeplaceholders",
            help="(bool) [default=True] Set to false if the placeholder shouldn't get changed at all",
            type=self.str2bool,
            nargs='?',
            const=True,
            default=True
        )

        self.args = self.parser.parse_args()

    def validate_command_line_args(self) -> None:
        """
        Validates the command line arguments
        :return: None
        """
        if not path.isdir(self.args.input):
            self.error_msg("The provided input path does not exist or isn't a directory")

        if not path.isdir(self.args.output):
            self.error_msg("The provided output path does not exist or isn't a directory")

        replace = self.args.fieldorder.replace(",", " ").replace("'", "").split()

        if type(replace) != list:
            self.error_msg("Fields order is not a comma separated list")
        self.args.fieldorder = replace

    def convert_csv_to_alfed(self) -> None:
        """
        The main worker. Converts the csv files into *.alfredsnippets files
        :return: None
        """
        global output_path, file_name
        self.parse_command_line_args()
        self.validate_command_line_args()

        for _, _, files in walk(self.args.input):
            for output_file in files:
                if output_file.endswith(".csv"):
                    file_name, _ = path.splitext(output_file)
                    output_path = ""
                    output_path = path.join(self.args.output, file_name)

                    try:
                        mkdir(output_path)
                        print(f"Creating folder {output_path}...")
                    except OSError:
                        print(f"Creation of directory {output_path} failed")

                    with open(path.join(self.args.input, output_file), "rt") as csv_file:
                        reader = DictReader(csv_file, fieldnames=self.args.fieldorder)

                        for row in reader:
                            uid = str(uuid.uuid1()).upper()
                            row["content"] = self.replace_embedded_snipptes(row["content"], self.args.lplaceholder,
                                                                            self.args.rplaceholder, self.args.changeplaceholders)
                            output = dumps(
                                {
                                    "alfredsnippet": {
                                        "snippet": row['content'],
                                        "uid": uid,
                                        "name": row['name'],
                                        "keyword": row['abbreviation']
                                    }
                                },
                                sort_keys=False, indent=4,
                                separators=(',', ': ')
                            )

                            output_file = f"{row['name']}_[{uid}].json"
                            target = path.join(output_path, output_file)
                            f = open(target, "w")
                            f.write(output)
                            f.close()
                            print(f"Writing file {target}...")
                else:
                    self.error_msg("The files in the input folder are not with extension '*.csv'")

                subprocess.call(
                    [
                        'ditto',
                        '--norsrc',
                        '-ck',
                        output_path,
                        self.args.output + "/" + file_name + ".alfredsnippets"
                    ]
                )
                print(f"{self.args.output}/{file_name}.alfredsnippets was created")
                self.created_folders.append(file_name)

        self.remove_temp_folders()


if __name__ == "__main__":
    alfred_converter = AlfredCsvToSnippets()
    alfred_converter.convert_csv_to_alfed()
