# Import necessary packages
import numpy as np
import tkinter as tk
import pandas as pd
import docx
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_score, recall_score
from tkinter import Label, Text, Button, messagebox
from tkinter import filedialog
from PyPDF2 import PdfReader


# Training data is the most important part of the program
# A program could mechanically work (going over text, producing outputs, etc.)
# Without proper training data ("Here is what Human and AI text looks like") then it will lack proper functionality
# For the program to be truly efficient then it will most likely require hundreds examples and more detailed identification IDs
# Simple GUI built using Tkinter
class TextDetectorGUI:
    def __init__(self, master, model, vectorizer, base_training_data):
        self.master = master
        master.title("AI Text Detector")  # This will be the title of the GUI window

        self.label = Label(master, text="Input Suspected Text: ")  # Label to indicate what the below entry box is for
        self.label.pack()

        self.text_frame = tk.Frame(master)
        self.text_frame.pack()

        self.text_entry = Text(self.text_frame, height=20, width=100)  # What the label above points to, where text is input for analysis
        self.text_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_entry.yview)  # Adds a scrollbar to the text box for particularly long inputs
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_entry.config(yscrollcommand=self.scrollbar.set)

        self.upload_button = Button(master, text="Upload Document", command=self.upload_document)  # Button for uploading documents (word, txt, pdf...)
        self.upload_button.pack(side=tk.LEFT)

        self.replace_training_data_button = Button(master, text="Replace Training Data", command=self.replace_training_data)  # Button for uploading CSV file datasets
        self.replace_training_data_button.pack(side=tk.RIGHT)

        self.analyse_button = Button(master, text="Scan",
                                     command=self.analyse_text)  # Button will call the program to analyse whatever text is within the above input
        self.analyse_button.pack(side=tk.LEFT)  # Positions the button on the left of the GUI window

        self.exit_button = Button(master, text="Exit",
                                  command=self.exit_program)  # Button will exit the program, first calling a confirmation window beforehand just in case
        self.exit_button.pack(side=tk.RIGHT)  # Positions the button on the right of the GUI window

        self.result_label = Label(master, text="")  # This will display the result of the analysis
        self.result_label.pack()

        self.reference_var = tk.IntVar()  # Checkbox for if input text has references: (name, date)
        self.reference_checkbox = tk.Checkbutton(master, text="Has References", variable=self.reference_var, command=self.update_reference)
        self.reference_checkbox.pack(side=tk.LEFT)

        self.sources_var = tk.IntVar()  # Checkbox for if input has sources anywhere: Harvard referencing/real sources
        self.sources_checkbox = tk.Checkbutton(master, text="Has Sources", variable=self.sources_var, command=self.update_source)
        self.sources_checkbox.pack(side=tk.LEFT)

        # These store the model and vectorizer for usage with the GUI
        # model so that the probability is predicted and vectorizer to convert the input text before being passed to the model
        self.model = model
        self.vectorizer = vectorizer
        self.base_training_data = base_training_data
        self.highlight_colour = "yellow"

    # When the document upload button is pressed the program this function will automatically filter the file types when searching through files
    # A backup check in case an invalid file type does get through will display a message/warning and not accept the input
    # Otherwise the input file will have its contents displayed in the text input box
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

    # When the button to replace the training dataset is selected then an initial yes or no message to continue will display
    # Files are automatically filtered to CSV files, upon a successful insertion then a message will display and the dataset is replaced
    # A CSV with invalid structure (columns) will not replace and display a message saying what is missing
    def replace_training_data(self):
        response = messagebox.askyesno("Warning", "Changing base training data may cause errors or affect program outputs. Continue?")
        if not response:
            return

        file_path = filedialog.askopenfilename(filetypes=[("CSV file", "*.csv")])
        if file_path:
            try:
                new_training_data = load_training_data(file_path)
                self.model, self.vectorizer = train_model(new_training_data)
                self.base_training_data = new_training_data
                messagebox.showinfo("Success", "Dataset has been updated...")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading or training with new dataset:\n{str(e)}")

    # update_reference and update_source will check the ticked boxes
    # Depending on if the checkboxes being ticked or not will affect the corresponding reference and source values for the input data
    def update_reference(self):
        if self.reference_var.get() == 1:
            return 0
        else:
            return 1

    def update_source(self):
        if self.sources_var.get() == 1:
            return 0
        else:
            return 1

    def analyse_text(self):  # Method will receive the text to be analysed then updates the above label with the result
        input_text = self.text_entry.get("1.0", tk.END).strip()

        if not input_text:  # If the text box is empty then a message will display and not continue
            messagebox.showwarning("No text found", "Enter text to be analysed...")
            return

        # Get the previous function values for the input text
        reference_value = self.update_reference()
        source_value = self.update_source()

        # Vectorize the text in a way the model can understand, using the same one made during training
        # The values for reference and source (missing from the input) are assigned from the acquired update functions
        # the text, reference, and source values are then concatenated like in the training
        input_vector_text = self.vectorizer.transform([input_text]).toarray()
        reference_source_values = np.array([[reference_value, source_value]])
        input_vector = np.concatenate((input_vector_text, reference_source_values), axis=1)

        # The input and set values are put through the model with the probability percentage rounded to two and displayed in the GUI
        probability = self.model.predict_proba(input_vector)[0][1] * 100
        probability = round(probability, 2)  # Round the probability output down to two decimal points
        result_text = f"AI-generation probability: {probability}%"
        self.result_label.config(text=result_text)

        # For text highlighting, the input text will be split before going through its own probability check
        sentences = re.split(r"(?<!\w\.\w)(?<![A-Z][a-z]\.)(?<=[.?])\s", input_text)

        # This will clear anything in the text box prior, so that only the highlighted text is shown
        self.text_entry.delete("1.0", tk.END)

        # The probability of the sentence text, anything higher than 50% is highlighted but can be adjusted if necessary
        for sentence in sentences:
            sentence_vector = self.vectorizer.transform([sentence]).toarray()
            sentence_vector = np.concatenate((sentence_vector, reference_source_values), axis=1)
            sentence_probability = self.model.predict_proba(sentence_vector)[0][1] * 100
            if sentence_probability > 50:
                self.text_entry.insert(tk.END, sentence, 'highlighted')
            else:
                self.text_entry.insert(tk.END, sentence)
            self.text_entry.insert(tk.END, '\n')
        self.text_entry.tag_configure('highlighted', background='yellow')  # Highlighted text will be yellow

    def exit_program(self):  # Method will ask for confirmation before exiting the program
        if messagebox.askokcancel("Exit", "Are you sure?"):
            self.master.destroy()


def load_training_data(file_path):
    # Pandas is used to read in the CSV file and encoded, if not encoded then an error will occur
    df = pd.read_csv(file_path, encoding="latin-1")
    return df


def train_model(training_data):
    # The returned above data is sent here with 'CountVectorizer' to convert the text
    vectorizer = CountVectorizer()

    # Separate the text and numeric X data
    # Convert the text into a way the model is capable of understanding
    # Put all the X data together
    X_text = vectorizer.fit_transform(training_data["TEXT"]).toarray()
    X_numeric = np.array(training_data[["REFERENCE", "SOURCE"]], dtype=float)
    X = np.concatenate((X_text, X_numeric), axis=1)

    # Take the y data from the dataset (target value)
    y = np.array(training_data["ID"])

    # 80% of data is used for training and 20% for testing, a random state is set to 0 for consistent outputs
    # The model is also created and fitted with the training data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    trained_model = MultinomialNB()
    trained_model.fit(X_train, y_train)

    # Evaluate/test the model's accuracy, F1 score, precision, recall, and prediction outcome (TP, TN, FP, FN)
    y_prediction = trained_model.predict(X_test)
    acc = round(accuracy_score(y_test, y_prediction), 2)
    f1 = round(f1_score(y_test, y_prediction), 2)
    precision = round(precision_score(y_test, y_prediction), 2)
    recall = round(recall_score(y_test, y_prediction), 2)
    confusion = confusion_matrix(y_test, y_prediction)

    # Print out the inbuilt tests
    print(f"Accuracy: {acc}")
    print(f"F1: {f1}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"Confusion Matrix: ")
    print(confusion)

    # The newly trained Multinomial model and vectorizer for transforming the text are returned
    return trained_model, vectorizer


if __name__ == "__main__":
    # The new training method is deferred to a function with the name of the CSV file that will use pandas
    # The training data, when broken down and returned is sent to the model to be trained
    training_data = load_training_data("TextData.csv")
    model, vectorizer = train_model(training_data)

    # Ensures the script is actually being run correctly, if it is then the GUI will run properly in a Tk event loop
    root = tk.Tk()
    app = TextDetectorGUI(root, model, vectorizer, training_data)
    root.mainloop()
