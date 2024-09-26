from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o-mini",
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
            "url": "https://github.com/tomjdyson/graph_dataset/blob/main/data/013f7a63-f164-41e6-8eb8-d7b47b7d578f.png",
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])