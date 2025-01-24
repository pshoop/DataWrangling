#!python
# -*- coding: utf-8 -*-
### RU MOD dictionary assembler

#This is a simple bit of code to parse data scraped from the RU MOD website.

#This data is in single HTML webpages and is parsed using BeautifulSoup

#This will read in all .html files in whatever directory the script happens to be in

#The resulting dictionary will be output as dictionary.csv to a new directory called 
#'output'
###

# Import all the things

import pandas as pd
from bs4 import BeautifulSoup as BS
import glob
import os

# use glob to create a list[] of all .html files in the directory
file_list = glob.glob('*.html')

# initialize an empty list
# this will be used to build a dataframe
big_list = []

# iterate through each file in the list
for f in file_list:
    
    # initiate an empty holder list[]
    small_list = []
    
    # open each file for parsing
    with open(f, 'rb') as fp:
        
        # parse the .html file with BeautifulSoup
        soup = BS(fp, features='html.parser')
        h1s = soup.h1

        # if the number of 'h1' tags in the .html is greater than 1,
        # assign the text from the 2nd 'h1' tag to a holder variable
        if len(h1s) > 1:
            h1_2 = h1s.find_next('h1')
            h1_str = h1_2.get_text()
        # Otherwise just assign the text from the lone 'h1' tag to the holder    
        else:
            h1_str = h1s.get_text()

        # grab the text from the 'p' tag in the parsed html 
        # assign text to a holder variable
        def_text = soup.p.get_text()
        
        # append both holder variables to the holder list
        small_list.append(h1_str)
        small_list.append(def_text)
    
    # Create the big list by appending the holder list
    big_list.append(small_list)

# Create a pandas dataframe from the big list and give it column headers
df = pd.DataFrame(big_list, columns = ['Word', 'Definition'])

# Setup output filename and directory
outname = 'dictionary.csv'
outdir = './output'

# Use os to create the directory if it doesn't already exist
if not os.path.exists(outdir):
    os.mkdir(outdir)

fullname = os.path.join(outdir, outname)    

# Output the final file without the pandas index
df.to_csv(fullname,index=False)
