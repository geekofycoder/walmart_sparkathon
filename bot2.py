import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from prompts import generate_prompt
load_dotenv(override=True)

# sku_path="data_mul_encode\processed_data.csv"
# df=pd.read_csv(sku_path)

client=OpenAI()
def get_responses(prompt):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"system","content":prompt}],
    top_p=0.001,
    temperature=0.01
    )
    return response.choices[0].message.content

def create_rec_csv(df):
    recommendations = []

    for index, row in df.iterrows():
        prompt = generate_prompt(row)
        recommendation = get_responses(prompt)
        recommendations.append({
            'SKU_ID': row['SKU_ID'],
            'Product_Name': row['Product_Name'],
            'Recommendations': recommendation
        })
    recommendations_df = pd.DataFrame(recommendations)
    output_file_path = 'path_to_save_recommendations.csv'
    recommendations_df.to_csv(output_file_path, index=False)
    return recommendations_df

