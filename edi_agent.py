import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from edi_parser import EDIParser

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def analyze_request(edi_text):
    # 1. Parse the data
    parser = EDIParser(edi_text)
    codes = parser.get_codes()
    
    # 2. Ask the Agent to reason
    prompt = f"""
    You are a Medical Necessity Agent. 
    A provider submitted a Prior Auth (EDI 278) with:
    Diagnosis: {codes['diagnosis']}
    Procedure: {codes['procedure']}

    Explain:
    1. What is the patient's condition in plain English?
    2. What is the requested treatment?
    3. Based on standard medical policy, what 2 things must the clinical notes prove for approval?
    """

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Run it!
raw_edi = "HI*BK:M17.11~SVC*HC:73721*1~"
print(analyze_request(raw_edi))