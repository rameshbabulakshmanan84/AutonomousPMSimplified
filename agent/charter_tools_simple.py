import os
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()
from agent.charter_prompt_simple import CHARTER_SYSTEM_PROMPT

client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview"
)


def generate_charter(brd_content:str)->dict:
    "Generate charter from BRD content"
    print("Inside generate_charter function with BRD content:", brd_content)
    try:
        response = client.chat.completions.create(
            model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            max_tokens=2000,
            messages=[
                {"role": "system", "content": CHARTER_SYSTEM_PROMPT.format(brd=brd_content)},
                
            ]
        )
        charter_text = response.choices[0].message.content.strip()
        return {
            "charter_text": charter_text,
            "success": True
        }
    except Exception as e:
        print(f"Error generating charter: {e}")
        return {
            "error": str(e),
            "success": False
        }