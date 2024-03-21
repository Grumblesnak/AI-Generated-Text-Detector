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
  (Minor) Included text files with code potentially for 3.0: One using current model that needs heavy modifying to work, and one using a RNN Neural Model with potential issue of not having enough in training dataset, 
  (Minor) Included beta training dataset for potential 3.0 update. Currently is short in examples that may be affecting RNN model. 

Update 3.0 Changes: 
  Slightly Improved GUI, made input box larger, 
  Suspicious text will be highlighted and displayed in input box after scan, not 100% as has demonstrated highlighting text with 0.12% AI probability, 
  Dataset expanded with two new columns: REFERENCE and SOURCE. 0 for possession (Human) and 1 for lack thereof (AI), 
  GUI updated to include two checkboxes for assigning values to the input text for the aforementioned columns, by default value is 1 if left unticked, 
  Dataset itself has been remade with different examples that are more professional.
  (Minor) Removed beta training dataset, 
  (Minor) Removed text files from previous update. 

Update 3.5 Changes:
  Included a check to ensure the text input box isn't empty, if it is then a message is displayed, 
  Expanded training dataset, 
  (Minor) Added more comments to code in an attempt to describe some things. 
