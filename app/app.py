import streamlit as st
from summarizer import summarizeBartLarge
from advance import summ
from extractive import summarize_text_content,summarize_pdf_content,transcribe_audio
from PyPDF2 import PdfReader
import speech_recognition as sr
import os
import tempfile

st.title("Text Summarization using :rainbow[GenAI] :pencil:")

with st.sidebar:
    st.title("Navigation.")
    selected_option = st.radio("Select Option", ["Text", "PDF", "Audio"], key='selected_option')

if selected_option == "Text":
    st.title("_Text_ _Summarization_")
    selected_model = st.selectbox("Select model",
                                  [None, 'Extractive Method', 'Abstractive Method','Advance Method'],
                                  key='selected_model',
                                  help='Select appropriate model to compute')
    max_words = st.slider("Maximum Words in Summary:", 20, 200, 100)
    min_words = st.slider("Minimum Words in Summary:", 10, 50, 20)

    text_input = st.text_area("Enter Text to Summarize:", height=350, disabled=False)

    if st.button("Summarize", key='button', type='secondary'):
        if not text_input:
            st.warning("Please enter the text above")
        else:
            if selected_model == 'Extractive Method':
                summary = summarize_text_content(text_input,3)
            
                st.write(summary)
            elif selected_model == 'Abstractive Method':
                summary = summarizeBartLarge(text_input, max_words, min_words)
                st.subheader(":green[Summary:]")
                st.write(summary)
            elif selected_model == 'Advance Method':
                a=summ(text_input,5)
                st.write(a)
                
            else:
                st.warning("Please select any model!", icon='⚠️')

elif selected_option == "PDF":
    st.title("PDF Summarizer")
    selected_model = st.selectbox("Select model",
                                  [None, 'Extractive Method', 'Abstractive Method','Advance Method'],
                                  key='selected_model',
                                  help='Select appropriate model to compute')
    
    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
    
    if selected_model == 'Extractive Method':
        ns = st.slider("Number of Sentences in Summary:", 0, 10, 3)
        if uploaded_file is not None:
            pdf_reader = PdfReader(uploaded_file)
        text_input = ""
        for page_num in range(len(pdf_reader.pages)):
            text_input += pdf_reader.pages[page_num].extract_text()
        st.text_area("Extracted Text from PDF:", value=text_input, height=350, disabled=False)
        if st.button("Summarize", key='button', type='secondary'):
            if not text_input:
                st.warning("Please upload a PDF file")
            else:
                summary = summarize_text_content(text_input,ns)
                st.subheader(":green[Summary:]")
                st.write(summary)
    elif selected_model == 'Abstractive Method':
        max_words = st.slider("Maximum Words in Summary:", 20, 200, 100)
        min_words = st.slider("Minimum Words in Summary:", 10, 50, 20)
        if uploaded_file is not None:
            pdf_reader = PdfReader(uploaded_file)
        text_input = ""
        for page_num in range(len(pdf_reader.pages)):
            text_input += pdf_reader.pages[page_num].extract_text()
        st.text_area("Extracted Text from PDF:", value=text_input, height=350, disabled=False)
        if st.button("Summarize", key='button', type='secondary'):
            if not text_input:
                st.warning("Please upload a PDF file")
            else:
                summary = summarizeBartLarge(text_input, max_words, min_words)
                st.subheader(":green[Summary:]")
                st.write(summary)
    elif selected_model == 'Advance Method':
        if uploaded_file is not None:
            pdf_reader = PdfReader(uploaded_file)
        text_input = ""
        for page_num in range(len(pdf_reader.pages)):
            text_input += pdf_reader.pages[page_num].extract_text()
        st.text_area("Extracted Text from PDF:", value=text_input, height=350, disabled=False)
        if st.button("Summarize", key='button', type='secondary'):
            if not text_input:
                st.warning("Please upload a PDF file")
            else:
                summary = summ(text_input,6)
                st.subheader(":green[Summary:]")
                st.write(summary)
    else:
      st.warning("Please select any model!", icon='⚠️')


        
    

elif selected_option == "Audio":
    st.title("Audio Summarizer")
    selected_model = st.selectbox("Select model",
                                  [None, 'Extractive Method', 'Abstractive Method','Advance Method'],
                                  key='selected_model',
                                  help='Select appropriate model to compute')
    if selected_model=='Extractive Method':
        with st.sidebar:
            uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3"])
        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
                tmpfile.write(uploaded_file.read())
                tmpfile_name = tmpfile.name
                # Convert audio bytes to text using speech recognition
                recognizer = sr.Recognizer()
                with sr.AudioFile(tmpfile_name) as source:
                    audio_text = recognizer.listen(source)
                text_input = recognizer.recognize_google(audio_text)
                st.text_area("Transcribed Text from Audio:", value=text_input, height=350, disabled=False)
                max_words = st.slider("Maximum Words in Summary:", 20, 200, 100)
                min_words = st.slider("Minimum Words in Summary:", 10, 50, 20)
                if st.button("Summarize", key='button', type='secondary'):
                    if not text_input:
                        st.warning("Please upload an audio file")
                    else:
                        summary = summarizeBartLarge(text_input, max_words, min_words)
                        st.subheader(":green[Summary:]")
                        st.write(summary)
            os.unlink(tmpfile_name)  # Delete the temporary file after use
    elif selected_model=='Abstractive Method':
            with st.sidebar:
             uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3"])
            if uploaded_file is not None:
                with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
                    tmpfile.write(uploaded_file.read())
                    tmpfile_name = tmpfile.name
                    # Convert audio bytes to text using speech recognition
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(tmpfile_name) as source:
                        audio_text = recognizer.listen(source)
                    text_input = recognizer.recognize_google(audio_text)
                    st.text_area("Transcribed Text from Audio:", value=text_input, height=350, disabled=False)
                    max_words = st.slider("Maximum Words in Summary:", 20, 200, 100)
                    min_words = st.slider("Minimum Words in Summary:", 10, 50, 20)
                    if st.button("Summarize", key='button', type='secondary'):
                        if not text_input:
                            st.warning("Please upload an audio file")
                        else:
                            summary = summarizeBartLarge(text_input, max_words, min_words)
                            st.subheader(":green[Summary:]")
                            st.write(summary)
                os.unlink(tmpfile_name)
    elif selected_model=='Advance Method':
        with st.sidebar:
            uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3"])
        
        if uploaded_file is not None:
                    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
                        tmpfile.write(uploaded_file.read())
                        tmpfile_name = tmpfile.name
                        # Convert audio bytes to text using speech recognition
                        recognizer = sr.Recognizer()
                        with sr.AudioFile(tmpfile_name) as source:
                            audio_text = recognizer.listen(source)
                        text_input = recognizer.recognize_google(audio_text)
                        st.text_area("Transcribed Text from Audio:", value=text_input, height=350, disabled=False)
                        max_words = st.slider("Maximum Words in Summary:", 20, 200, 100)
                        min_words = st.slider("Minimum Words in Summary:", 10, 50, 20)
                        if st.button("Summarize", key='button', type='secondary'):
                            if not text_input:
                                st.warning("Please upload an audio file")
                            else:
                                summary = summarizeBartLarge(text_input, max_words, min_words)
                                st.subheader(":green[Summary:]")
                                st.write(summary)
                    os.unlink(tmpfile_name)
    else:
        st.warning("Please select any model!", icon='⚠️')
            

                