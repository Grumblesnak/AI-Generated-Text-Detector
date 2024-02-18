# Import necessary packages
import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score


# Training data is the most important part of the program
# A program could mechanically work (going over text, producing outputs, etc.)
# Without proper training data ("Here is what Human and AI text looks like") then it will lack proper functionality
def analyze_text(input_text):
    # Training data for checking against input text (0 for human, 1 for AI)
    training_data = [
        ("The sun rose slowly, as if it wasn't sure it was worth all the effort.", 0),
        ("Grinning like a necrophiliac in a morgue.", 0),
        ("He moved in a way that suggested he was attempting the world speed record for the nonchalant walk.", 0),
        ("Then the storm broke, and the dragons danced.", 0),
        ("The seeds of war are oft planted during times of peace.", 0),
        ("Only you could have won me away from the sea. I came back from the ends of the earth for you.", 0),
        ("In a hole in the ground there lived a hobbit.", 0),
        ("So comes snow after fire, and even dragons have their endings.", 0),
        ("May the wind under your wings bear you where the sun sails and the moon walks.", 0),
        (
        "In the whimsical realm of Discworld, Rincewind finds himself entangled in comical misadventures, a true testament to Pratchett's unique narrative.",
        1),
        (
        "As the inept wizard Rincewind stumbles through absurd scenarios, Pratchett's humor shines, creating a delightful blend of fantasy and satire.",
        1),
        (
        "Terry Pratchett's second Discworld novel continues to captivate with its witty prose and clever exploration of fantastical elements.",
        1),
        (
        "In the intricate tapestry of Westeros' history, Martin weaves a compelling saga, chronicling the rise of House Targaryen and their dragons.",
        1),
        (
        "George R.R. Martin's meticulous storytelling delves into the political intrigues and power struggles that shaped the Targaryen dynasty.",
        1),
        (
        "Dragons soar and empires crumble in Martin's masterful narrative, bringing to life the epic history of the fiery-blooded rulers of Westeros.",
        1),
        (
        "Bilbo Baggins' unexpected journey unfolds with Tolkien's enchanting prose, whisking readers away to the heart of Middle-earth.",
        1),
        (
        "J.R.R. Tolkien's classic tale of adventure and self-discovery follows Bilbo on a quest filled with dwarves, dragons, and the allure of the One Ring.",
        1),
        (
        "In the Shire and beyond, Tolkien's vivid descriptions and rich world-building create a timeless fantasy that continues to captivate readers.",
        1),
    ]

    # These will be used for the X and y training data using the human and AI examples, later be updated to use files
    # Feature extraction
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([data[0] for data in training_data])

    # Split training data into features and labels
    y = np.array([data[1] for data in training_data])

    # Train the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Analyse input text
    input_vector = vectorizer.transform([input_text])
    prediction = model.predict(input_vector)

    # Return the AI likelihood prediction probability
    return model.predict_proba(input_vector)[0][1] * 100


# Input text for analysis, will be updated to be taken in by a GUI at a later stage
# input_text = "Amidst the celestial tapestry, dragons soared and empires crumbled, a dance of fire and chaos in the realm of fantasy."
input_text = "I am not a damn AI, what would make you think I am a goddamm AI? are you mad!"
probability = analyze_text(input_text)
print(f"AI-generation probability: {probability}%")
