from openai import OpenAI
import json
import pandas as pd

client = OpenAI()


def build_url(dir, uid):
    return f"https://github.com/tomjdyson/graph_dataset/blob/main/{dir}{uid}?raw=true"


def url_response(url):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": """extract the data that is contained in this image. Output your data in json, with the 
           name of the data as the key and the value as data that can be read into a pandas dataframe with one call
           All columns of the dataframe have to be the same length: 
           json ``` {'name': {pandas friendly dataframe}} ```"""},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response


def load_response_data(response):
    string_data = response.choices[0].message.content
    cleaned_str = string_data.split('```')[1].replace('json', "").replace("\n", "")
    cleaned_json = json.loads(cleaned_str)
    return pd.DataFrame(list(cleaned_json.values())[0])


if __name__ == '__main__':
    import os

    current_dir = "/data/test/"
    all_files = os.listdir(f'.{current_dir}')
    all_uids = [i.replace('.jpg', '') for i in all_files if i[-3:] == 'jpg']
    for uid in all_uids:
        url = build_url(current_dir, uid + '.jpg')
        response = url_response(url)
        new_data = load_response_data(response)
        original_data = pd.read_csv("./data/" + uid + '.csv')
        print(new_data)
        print(original_data)
        break
