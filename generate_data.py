from openai import OpenAI
import pandas as pd
import json

client = OpenAI()


def data_prompt():
    return client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.99,
        messages=[
            {"role": "user", "content": """
        Generate a random dataset that mimics that which would be recorded for a company filings report
        The data should be small spanning 4 - 12 dates of either quarterly or yearly. The data could span one or
         multiple of; divisions, financial indicators, geographies etc. 
         Output your data in json, with the 
         name of the data as the key and the value as data that can be read into a pandas dataframe with one call
         All columns of the dataframe have to be the same length: 
         json ``` {'name': {pandas friendly dataframe}} ```"""}])

def generate_dataframe():
    response = data_prompt()
    data = response.choices[0].message.content

    json_data = json.loads(data.split('```')[1].replace('json', '').replace('\n', ''))
    data_frame = pd.DataFrame(list(json_data.values())[0])

    return data_frame, list(json_data.keys())[0]

# if __name__ == '__main__':
#
#
#
#     print(data)
