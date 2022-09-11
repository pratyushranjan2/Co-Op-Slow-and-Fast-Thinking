import pandas as pd
import sys

if len(sys.argv) != 2:
	print "Incorrect parameters"
	sys.exit(0)

df = pd.read_csv(sys.argv[1])
print df.shape
