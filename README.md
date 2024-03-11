# AI-Generated-Text-Detector
Machine learning Python program for detecting AI-generated text

If you are downloading the main file (for whatever reason) then run it on the latest instance of JetBrains Pycharm Community Edition for simplicities sake as that is what I wrote it on, and also install the required packages when prompted if needed. Couldn't add the other files alongside the main code so may need to create a new project then copy and paste the code into a new main.py file. Attempted to reinstall Pycharm Edu but all links lead to Community Edition instead, seems to work fine though.

Initial 0.5 Build: 
  No GUI, 
  Inbuilt text input, 
  Console outputs, 
  Small training dataset.

Update 1.0 Changes: 
  Simple GUI, 
  Can exit program from GUI, 
  Text input on GUI, replaces previous inbuilt text input, 
  Outputs on GUI, replaces previous console outputs, 
  Slightly expanded training dataset, 
  (Minor) Renamed some things that used American spelling (z) to British spelling (s). 

Update 1.5 Changes: 
  Program has switched from the previous inbuilt training data to using a CSV file, 
  Code has been added (using pandas) to extract data from the file, train the X and y, train the model, and then work as intended, 
  Structure of dataset file is identical to formerly inbuilt structure ("blah blah blah", 0 or 1). 

Update 2.0 Changes: 
  Program allows for alternative uploading of a file instead of typing/copy-pasting text, accepts and should auto filte for txt, docx (word), and pdf files, 
  Any files that are invalid and not one of the above three are refused. 

Update 2.5 Changes: 
  Allows replacement of default provided training dataset through a button on GUI, 
  Warning before changing training dataset appears as popup, 
  (Minor) Highlighting moved to planned 3.0 changes after training dataset configuration, 
  (Minor) Included text files with code potentially for 3.0: One using current model that needs heavy modifying to work, and one using a RNN Neural Model with potential issue of not having enough in training dataset. 

Planned 3.0 Changes: 
  Improve GUI, make more user friendly/appealing to look at, 
  Improve dataset contents (Either significantly increase quantity or expand classification of texts (more 0 and 1 columns)), 
  Highlight text that triggers probability result above 20%, 
  Update code to handle updated dataset if neccessary, 
  Expand training dataset.
  
