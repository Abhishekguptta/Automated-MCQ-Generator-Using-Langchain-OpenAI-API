import os 
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback

from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


#loading json file

with open(r'H:\Automated-MCQ-Generator-Using-Langchain-OpenAI-API\Response.json','r') as file:
    RESPONSE_JSON =  json.load(file)

#creating a form using st.form 
with st.form("user_inputs"):
    #file upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")

    #Input fields
    mcq_count = st.number_input("No. of MCQs", min_value=3,max_value = 50)

    #Subject
    subject = st.text_input("Insert Subject", max_chars=20)

    #quiz tone
    tone = st.text_input("Comlexity Level of Questions", max_chars=20, placeholder= "Simple" )

    #add button
    button = st.form_submit_button("Create MCQs")

    #check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)

                #count takens and the const of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_josn": json.dumps(RESPONSE_JSON)
                            }
                    )
                #st.write(response)

            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"completion Tokens:{cb.completion_tokens}")
                print(f"Totalcost:{cb.total_cost}")

                if isinstance(response, dict):
                    #extract the quiz data from the response
                    quiz = response.get("quiz",None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #display the review in atext box as well
                            st.text_area(label="Review",value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)            

#d

