import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
import sklearn
import mpld3
import csv

infile = '/data/20150814_security_tender_data.csv'
outfilename = '/data/cluster_output.csv'

with open(infile, 'rb') as fp_in, open(outfile, 'wb') as fp_out:
    reader = csv.reader(fp_in, delimiter=",")
    headers = next(reader)  # read first row

    writer = csv.writer(fp_out, delimiter=",")
    writer.writerow(headers + ['inits'])

    for row in reader:
         print row