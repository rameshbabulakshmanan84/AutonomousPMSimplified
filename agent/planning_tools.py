import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
load_dotenv()
from agent.planning_prompt import WBS_GENERATION_PROMPT,DETAILED_PLAN_PROMPT

#First write WBS from charter
def generate_wbs(charter_text:str)->dict:
    "Generate WBS from charter"
    #print("This is the charter text",charter_text)

    client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview"
)


    try:
        response = client.chat.completions.create(
            model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            max_tokens=2000,
            messages=[{"role": "user", "content": WBS_GENERATION_PROMPT.format(charter_content=charter_text)}]
        )

        wbs_text = response.choices[0].message.content.strip()

        #print("Generated WBS text:", wbs_text)
        return {
            "wbs": wbs_text,
            "success": True
        }
    except Exception as e:
        print(f"Error generating WBS: {e}")
        return {
            "error": str(e),
            "success": False
        }

#Use the WBS & the budget to generate a detailed plan
def generate_detailed_plan(wbs:str, budget:float)->dict:
    "Generate detailed plan from WBS and budget"

    client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview"
)


    try:
        response = client.chat.completions.create(
            model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            max_tokens=2000,
            messages=[{"role": "user", "content": DETAILED_PLAN_PROMPT.format(wbs=wbs, budget=budget)}]
        )

        detailed_plan_text = response.choices[0].message.content.strip()
        return {
            "plan": detailed_plan_text,
            "success": True
        }
    except Exception as e:
        print(f"Error generating detailed plan: {e}")
        return {
            "error": str(e),
            "success": False
        }



