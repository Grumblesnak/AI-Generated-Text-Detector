# Import necessary packages
# Unused imports and such will be commented out for now to reduce warnings until they are or are confirmed not needed
import numpy as np
# import tensorflow as tf
import tkinter as tk
import pandas as pd
import docx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
# from sklearn.metrics import accuracy_score
from tkinter import Label, Text, Button, messagebox
from tkinter import filedialog
from PyPDF2 import PdfReader


# Training data is the most important part of the program
# A program could mechanically work (going over text, producing outputs, etc.)
# Without proper training data ("Here is what Human and AI text looks like") then it will lack proper functionality
# For the program to be truly efficient then it will most likely require hundreds examples and more detailed identification IDs
def analyse_text(input_text, model, vectorizer):
    input_vector = vectorizer.transform([input_text])
    probability = model.predict_proba(input_vector)[0][1] * 100  # Return the AI likelihood prediction probability
    return probability


# Simple GUI built using Tkinter
class TextDetectorGUI:
    def __init__(self, master, model, vectorizer):
        self.master = master
        master.title("AI Text Detector")  # This will be the title of the GUI window

        self.label = Label(master, text="Input Suspected Text: ")  # Label to indicate what the below entry box is for
        self.label.pack()

        self.text_entry = Text(master, height=5,
                               width=50)  # What the label above points to, where text is input for analysis
        self.text_entry.pack()

        self.upload_button = Button(master, text="Upload Document", command=self.upload_document)
        self.upload_button.pack()

        self.analyse_button = Button(master, text="Scan",
                                     command=self.analyse_text)  # Button will call the program to analyse whatever text is within the above input
        self.analyse_button.pack(side=tk.LEFT)  # Positions the button on the left of the GUI window

        self.exit_button = Button(master, text="Exit",
                                  command=self.exit_program)  # Button will exit the program, first calling a confirmation window beforehand just in case
        self.exit_button.pack(side=tk.RIGHT)  # Positions the button on the right of the GUI window

        self.result_label = Label(master, text="")  # This will display the result of the analysis
        self.result_label.pack()

        # These store the model and vectorizer for usage with the GUI
        # model so that the probability is predicted and vectorizer to convert the input text before being passed to the model
        self.model = model
        self.vectorizer = vectorizer

    def upload_document(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt;*.docx;*.pdf")])
        if file_path:
            with open(file_path, "rb") as file:
                if file_path.lower().endswith(".txt"):
                    content = file.read().decode("utf-8")
                elif file_path.lower().endswith(".docx"):
                    doc = docx.Document(file)
                    content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                elif file_path.lower().endswith(".pdf"):
                    pdf_reader = PdfReader(file)
                    content = ""
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        content += page.extract_text()
                else:
                    messagebox.showwarning("Invalid File", "Upload a valid text, Word, or PDF document...")
                    return

            self.text_entry.delete("1.0", tk.END)
            self.text_entry.insert(tk.END, content)

    def analyse_text(self):  # Method will receive the text to be analysed then updates the above label with the result
        input_text = self.text_entry.get("1.0", tk.END).strip()
        probability = analyse_text(input_text, self.model, self.vectorizer)
        probability = round(probability, 2)  # Round the probability output down to two decimal points
        result_text = f"AI-generation probability: {probability}%"
        self.result_label.config(text=result_text)

    def exit_program(self):  # Method will ask for confirmation before exiting the program
        if messagebox.askokcancel("Exit", "Are you sure?"):
            self.master.destroy()


def load_training_data(file_path):
    # Pandas is used to read in the CSV file and encoded, if not encoded then an error will occur
    # The columns 'TEXT' and 'ID' alongside their contents (example text and what that texts corresponding ID is) are returned
    df = pd.read_csv(file_path, encoding="latin-1")
    return df["TEXT"].tolist(), df["ID"].tolist()


def train_model(training_data):
    # The returned above data is sent here with 'CountVectorizer' to convert the text
    # X and y are set with the corresponding 0 and 1 data from the ID column with their matching text examples
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(training_data[0])
    y = np.array(training_data[1])

    # 80% of data is used for training and 20% for testing, a random state is set to 0 for consistent outputs
    # The model is also created and fitted with the training data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    trained_model = MultinomialNB()
    trained_model.fit(X_train, y_train)

    # The newly trained Multinomial model and vectorizer for transforming the text are returned
    return trained_model, vectorizer


if __name__ == "__main__":
    # The new training method is deferred to a function with the name of the CSV file that will use pandas
    # The training data, when broken down and returned is sent to the model to be trained
    training_data = load_training_data("TextData.csv")
    model, vectorizer = train_model(training_data)

    # Ensures the script is actually being run correctly, if it is then the GUI will run properly in a Tk event loop
    root = tk.Tk()
    app = TextDetectorGUI(root, model, vectorizer)
    root.mainloop()
