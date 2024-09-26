from openai import OpenAI
import pandas as pd
import json

client = OpenAI()

def compare_prompt(original_data, extracted_data):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.001,
        messages=[
            {"role": "user", "content": f"""
            Original Data: {original_data}
            Extracted Data: {extracted_data}
            You are creating a python function that compares the numerical values of the two datasets above. You
            are trying to join these datasets together to then evaluate if the extracted data is the same as the original
            data
            For each numerical value in original_data you need to evaluate if it has the correct corresponding value 
            in the extracted data, this includes for every date
            the function should take original_data and extracted data and return a dictionary with a name for the
            data point in original and a bool for if it has been extracted,
             plus the combined dataset used to evaluate
            python ```data_compare(original_data, extracted_data) -> Dict[str, bool], pd.DataFrame(): ```
            """}])



if __name__ == '__main__':
    import os
    from graph_vision import build_url, url_response, load_response_data

    all_files = os.listdir('./data/')
    all_uids = [i.replace('.jpg', '') for i in all_files if i[-3:] == 'jpg']
    all_acc = {}
    for uid in all_uids[:10]:
        try:
            url = build_url(uid + '.jpg')
            response = url_response(url)
            new_data = load_response_data(response)
            original_data = pd.read_csv("./data/" + uid + '.csv')

            python_response = compare_prompt(original_data, new_data)
            data = python_response.choices[0].message.content
            python_func = data.split('```')[1].replace('python', '')
            exec(python_func)
            accuracy, combined_data = data_compare(original_data = original_data, extracted_data = new_data)

            all_acc[uid] = accuracy

            # id_avg_error.append(sum(errors)/len(errors))
        except Exception as e:
            print(e)
            print(uid)



    all_acc_df = pd.DataFrame(all_acc).T.reset_index().melt(id_vars = 'index').dropna()
    acc = all_acc_df['value'].mean()
    group_acc = all_acc_df.groupby('index')['value'].mean().mean()
    print(all_acc)