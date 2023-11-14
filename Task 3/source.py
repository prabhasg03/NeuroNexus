from tkinter import filedialog

import numpy as np
import tkinter as tk
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, Embedding, LSTM, RepeatVector, Concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from PIL import Image
import matplotlib.pyplot as plt

# Load pre-trained ResNet50 model without the top layer
base_model = ResNet50(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)


# Function to preprocess and extract features from an image
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array)
    features = np.reshape(features, features.shape[1])
    return features


# Example usage of feature extraction
img_features = extract_features('path/to/your/image.jpg')

# Dummy captions (replace with your dataset)
captions = [
    "A cat sitting on a mat",
    "A dog playing in the park",
    "A bird perched on a branch"
]

# Tokenize captions
tokenizer = Tokenizer()
tokenizer.fit_on_texts(captions)
vocab_size = len(tokenizer.word_index) + 1

# Create sequences of tokens from captions
sequences = tokenizer.texts_to_sequences(captions)

# Pad sequences to ensure they have the same length
max_len = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')


# Function to define the captioning model
def define_model(vocab_size, max_len):
    input_image = Input(shape=(2048,))
    fe1 = Dense(256, activation='relu')(input_image)
    input_caption = Input(shape=(max_len,))
    se1 = Embedding(vocab_size, 256, mask_zero=True)(input_caption)
    se2 = LSTM(256)(se1)
    decoder1 = Concatenate()([fe1, se2])
    decoder2 = Dense(256, activation='relu')(decoder1)
    output = Dense(vocab_size, activation='softmax')(decoder2)
    model = Model(inputs=[input_image, input_caption], outputs=output)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model


# Define the model
caption_model = define_model(vocab_size, max_len)


# Function to generate data for training
def data_generator(captions, images, tokenizer, max_len, vocab_size):
    while True:
        for i in range(len(captions)):
            img_features = extract_features(images[i])
            in_seq = tokenizer.texts_to_sequences([captions[i]])[0]
            in_seq = pad_sequences([in_seq], maxlen=max_len, padding='post')[0]
            in_seq = to_categorical([in_seq], num_classes=vocab_size)[0]
            yield ([img_features, in_seq], in_seq)


# Example usage of the data generator
gen = data_generator(captions, ['path/to/your/image.jpg'], tokenizer, max_len, vocab_size)
x, y = next(gen)

# Train the captioning model
epochs = 10
steps = len(captions)
for i in range(epochs):
    generator = data_generator(captions, ['path/to/your/image.jpg'], tokenizer, max_len, vocab_size)
    caption_model.fit(generator, epochs=1, steps_per_epoch=steps, verbose=1)

# Save the model
caption_model.save('image_caption_model.h5')

# Load the trained model
caption_model = load_model('image_caption_model.h5')


# Function to generate captions for a given image
def generate_caption(model, photo):
    in_text = 'startseq'
    for i in range(max_len):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_len)
        yhat = model.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = word_for_id(yhat, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    return in_text


# Function to map an integer to a word
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


# Example usage of caption generation
img_path = filedialog.askopenfilename()
img_features = extract_features(img_path)
caption = generate_caption(caption_model, img_features)
print(caption)
