# encoding
import csv
import pywsd
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from pywsd import disambiguate
from pywsd.similarity import max_similarity

line = 0

with open('emoji_mapping.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        line += 1
        print >> sys.stderr, "processing line %d" % line
        emoji = row[0]
        text = row[1].replace(' ', '_').replace(';', ' ')
        tokens = disambiguate(text, algorithm=max_similarity, 
            similarity_option='wup', keepLemmas=True)
        syns = set([t[2].name() for t in tokens if t[2] is not None])
        text = text.replace(' ', ';').replace('_', ' ')
        print "%s,%s,%s" % (emoji, text, ";".join(syns))