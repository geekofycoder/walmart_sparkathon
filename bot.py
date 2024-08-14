from dotenv import load_dotenv
import os
load_dotenv()
from IPython.display import display, Image
from openai import OpenAI
import os
import pandas as pd
import json
import io
from PIL import Image
import requests
from prompts import BASE_PROMPT
import time

client = OpenAI()
#Lets import some helper functions for assistants from https://cookbook.openai.com/examples/assistants_api_overview_python
def show_json(obj):
    display(json.loads(obj.model_dump_json()))

def submit_message(assistant_id, thread, user_message,file_ids=None):
    params = {
        'thread_id': thread.id,
        'role': 'user',
        'content': user_message,
    }
    if file_ids:
        params['file_ids']=file_ids

    client.beta.threads.messages.create(
        **params
)
    return client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
)

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id)
sku_path=".\SKU_data_mul_encode\processed_data.csv"
sku_data=pd.read_csv(sku_path)
# print(sku_data.head(5))

file = client.files.create(
  file=open(sku_path,"rb"),
  purpose='assistants',
)
assistant = client.beta.assistants.create(
  instructions=BASE_PROMPT,
  model="gpt-4",
  tools=[{"type": "code_interpreter"}],
    tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
  }
)
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Provide what should be done in this quarter of sales.",
      "attachments": [
        {
          "file_id": file.id,
          "tools": [{"type": "code_interpreter"}]
        }
      ]
    }
  ]
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)
def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id)

# if run.status == 'completed': 
#   messages = client.beta.threads.messages.list(
#     thread_id=thread.id
#   )
#   print(messages.content.value)
# else:
#   print(run.status)
time.sleep(10)
response = get_response(thread)
bullet_points = response
#.data[0].content[0]
#.text.value
print(bullet_points)