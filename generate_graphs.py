from openai import OpenAI
import random

client = OpenAI()


def graph_prompt(data, name, url_location ):
    columns = list(data)

    data_labels = random.choice(["Use Data labels in the plot", "Do not use data labels in the plot"])
    plot_types = random.choice(["bar", "line", "pie", "scatter", "area"])


    return client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.99,
        messages=[
            {"role": "user", "content": f"""
            You are trying to create python code to plot a simple pandas dataframe which will be called df
            The plot must have a title, x axis, y axis but apart from that decide on what the plot should look like yourself
            the name of the dataset is {name}, the columns of the dataset are {columns}
            Presume matplotlib is imported as plt, pandas is imported as pd and seaborn is imported as sns, use whichever
            youd like
            do not show the plot
            Use random colours as youd like
            The plot should be a {plot_types} chart
            {data_labels}
            the image can be any size you like
            Create your python as a function that takes df & uid, saves the plot as '{url_location}uid.jpg' and 
            saves the data that could be extracted from the plot in '{url_location}uid.csv'
            python ```data_plotter(df, uid): ```
            """}])


if __name__ == '__main__':
    from generate_data import generate_dataframe
    from uuid import uuid4
    import matplotlib as plt
    import pandas as pd
    import seaborn as sns
    import os

    print(len(os.listdir('./data/test')))

    while len(os.listdir('./data/test')) < 100:

        try:
            df, name = generate_dataframe()

            python_response = graph_prompt(df, name, './data/test/')
            data = python_response.choices[0].message.content
            python_func = data.split('```')[1].replace('python', '')
            # data_plotter = lambda data, uid: ass
            exec(python_func)
            picked_uid = uuid4()
            data_plotter(df, uuid4())
        except Exception as e:
            print(e)
