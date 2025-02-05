import os
import json
import traceback
import pandas as pd 
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

#import necessary packages from langchain

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

#load environment variables from the .env file
load_dotenv()
KEY = os.getenv("OPENAI_API_KEYS")


llm = ChatOpenAI(openai_api_key = KEY,model_name="gpt-3.5-turbo",temperature=0.3)
