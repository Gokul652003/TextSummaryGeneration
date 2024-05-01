import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import PyPDF2
import speech_recognition as sr

# Initialize NLTK
nltk.download('punkt')

def summarize_text_content(text, sentence_count):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LsaSummarizer()
    summarized_text = ''
    for sentence in summarizer(parser.document, sentence_count):
        summarized_text += str(sentence) + ' '
    return summarized_text

def summarize_pdf_content(pdf_file, sentence_count):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return summarize_text_content(text, sentence_count)

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

def main():
    st.title("Text Summarization Web App")
    st.sidebar.header("Navigation")
    selected_option = st.sidebar.radio("", ["Home", "Summarize Text", "Summarize PDF", "Summarize Audio"])

    if selected_option == "Home":
        st.write("Welcome to the Text Summarization Web App!")
        st.write("Please select an option from the sidebar.")

    elif selected_option == "Summarize Text":
        st.subheader("Summarize Text")
        text = st.text_area("Enter text:")
        sentence_count = st.number_input("Number of sentences in summary:", min_value=1, value=3)
        if st.button("Summarize"):
            summarized_text = summarize_text_content(text, sentence_count)
            st.write("Summarized Text:")
            st.write(summarized_text)

    elif selected_option == "Summarize PDF":
        st.subheader("Summarize PDF")
        pdf_file = st.file_uploader("Upload a PDF file:")
        if pdf_file is not None:
            sentence_count = st.number_input("Number of sentences in summary:", min_value=1, value=3)
            if st.button("Summarize"):
                summarized_text = summarize_pdf_content(pdf_file, sentence_count)
                st.write("Summarized Text:")
                st.write(summarized_text)

    elif selected_option == "Summarize Audio":
        st.subheader("Summarize Audio")
        audio_file = st.file_uploader("Upload an audio file:", type=["mp3", "wav"])
        if audio_file is not None:
            sentence_count = st.number_input("Number of sentences in summary:", min_value=1, value=3)
            if st.button("Summarize"):
                text = transcribe_audio(audio_file)
                summarized_text = summarize_text_content(text, sentence_count)
                st.write("Summarized Text:")
                st.write(summarized_text)

if __name__ == "__main__":
    main()
