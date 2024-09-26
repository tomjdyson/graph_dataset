import os
from graph_vision import build_url
import pandas as pd


def create_single_jsonl(image_url, df):
    return {"messages": [{"role": "system", "content": [{"type": "text", "text": """You are an extraction agent that is extracting data from graphs"""}]},
                         {"role": "user", "content": [{"type": "text", "text": """extract the data that is contained in this image. Output your data in json, with the 
           name of the data as the key and the value as data that can be read into a pandas dataframe with one call
           All columns of the dataframe have to be the same length: 
           json ``` {'name': {pandas friendly dataframe}} ```"""}, {"type": "image_url", "image_url": {"url": image_url}},
                                                  ]},
                         {"role": "assistant", "content": [{"type": "text", "text": df.to_json(orient='records')}]}]}

def build_jsonl(dir):
    all_files = os.listdir(dir)
    all_uids = [i.replace('.jpg', '') for i in all_files if i[-3:] == 'jpg']
    all_jsonl = []
    for uid in all_uids:
        graph_url = build_url("/data/train/", uid + '.jpg')
        data = pd.read_csv(dir + uid + '.csv')
        single_jsonl = create_single_jsonl(graph_url, data)
        all_jsonl.append(single_jsonl)

    return all_jsonl

if __name__ == '__main__':
    import json
    data = build_jsonl("./data/train/")

    with open('graph_finetuning_v0.jsonl', 'w') as file:
        for entry in data:
            # Dump each dictionary as a JSON object and write it to a new line
            file.write(json.dumps(entry) + '\n')

