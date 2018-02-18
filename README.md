
============
Political Playing Cards
============

First, scrape data from OpenSecrets.org. If you do not specify "--file" then the script will try every
possible ID. Specifying --file from an existing set of IDs speeds up the process immensely.
   * python ScrapeData.py --type contributors
   * python ScrapeData.py --file OpenSecretsIDs.csv --type contributors
   * python ScrapeData.py --file OpenSecretsIDs.csv --type industries

Note that "--type contributors" should be run first. Then "--type industries".

Next, scrape photos from congress.gov:
   * python ScrapePhotos.py

TODO: save the correct names for these files, to connect them to the right person!

Finally, run the MasterScript:
   * python MasterScript.py

This loops over all entries in OpenSecretsIDs.csv and produces the output file.

