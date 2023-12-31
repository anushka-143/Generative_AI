import openai
import pandas as pd

from secret_key import openai_api_key
import json

openai.api_key = openai_api_key

def extract_financial_data(text):
    prompt = get_prompt_financial() + text
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role":"user", "content":prompt}]

    )
    content = response.choices[0]['message']["content"]
    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["Measure","Value"])
    except (json.JSONDecodeError, IndexError):
        pass
    return pd.DataFrame({
        "Measure": ["Comapny name","Stock symbol","Revenue","Net income","Value"],
        "Value":["","","","",""]
    })

def get_prompt_financial():
    return'''please retrieve company name, revenue, net income and earning per share (a.k.a EPS)
    from following article. If you can't find the information in this article then return " ". DO not make up things. 
    Then retrieve a stock symbol corresponding to that company. for this you can use your general knowledge (it doesn't have to be from this article).
    Always return the respone as a valid JSON string. the format of that string should be this,
    {
        "Company Name": "Walmart",
         "Stock symbol":"WMT",
         "Revenue":"12.34 million",
         "Net income":"34.78 million",
         "EPS":"2.1 $"
    }
    Article:
    =========
    '''
if __name__== '__main__':
    text = '''Tesla, Inc. engages in the design, development, manufacture, and sale of fully electric vehicles, energy generation and storage systems. It also provides vehicle service centers, supercharger station, and self-driving capability. The company operates through the following segments: Automotive and Energy Generation and Storage. The Automotive segment includes the design, development, manufacture and sale of electric vehicles. The Energy Generation and Storage segment includes the design, manufacture, installation, sale, and lease of stationary energy storage products and solar energy systems, and sale of electricity generated by its solar energy systems to customers. It develops energy storage products for use in homes, commercial facilities and utility sites. The company was founded by Jeffrey B. Straubel, Elon Reeve Musk, Martin Eberhard, and Marc Tarpenning on July 1, 2003 and is headquartered in Palo Alto, CA. '''
    df = extract_financial_data(text)
    print(df.to_string())
