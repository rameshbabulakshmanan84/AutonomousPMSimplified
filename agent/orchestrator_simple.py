#from sympy import re

from agent.charter_tools_simple import generate_charter
from agent.planning_tools import generate_wbs, generate_detailed_plan

#Initalize global variables to store intermediate results
#global charter_text_global, wbs_global, plan_global
charter_text_global = None
wbs_global = None
plan_global = None

#from tabulate import tabulate
#formyat helper function to return a structured response


'''
def format_plan_table(plan_text: str) -> str:
    rows = []
    for line in plan_text.split("\n"):
        if not line.strip() or not line.strip().startswith("T"):
            continue  # skip headers or invalid lines

        try:
            # Example: "T1 - Conduct Stakeholder Analysis Owner: Project Manager Duration: 20 hours ..."
            parts = line.split("Owner:")
            task_info = parts[0].strip()
            rest = parts[1] if len(parts) > 1 else ""

            # Safer split
            if "-" in task_info:
                task_id, task_name = task_info.split("-", 1)
            else:
                task_id, task_name = task_info, ""

            owner = rest.split("Duration:")[0].strip() if "Duration:" in rest else ""
            duration = rest.split("Duration:")[1].split("Cost:")[0].strip() if "Duration:" in rest else ""
            cost = rest.split("Cost:")[1].split("Gate:")[0].strip() if "Cost:" in rest else ""
            gate = rest.split("Gate:")[1].split("Dependencies:")[0].strip() if "Gate:" in rest else ""
            dependencies = rest.split("Dependencies:")[1].strip() if "Dependencies:" in rest else ""

            rows.append([task_id.strip(), task_name.strip(), owner, duration, cost, gate, dependencies])
        except Exception as e:
            print("Skipping line due to parse error:", line, e)

    headers = ["Task ID", "Task Name", "Owner", "Duration", "Cost", "Gate", "Dependencies"]
    return tabulate(rows, headers=headers, tablefmt="grid")

'''
#format helper function to return a structured response
def format_output(text:str,output_type:str)->str:
    #text = clean_markdown(text)
    lines=text.strip().split("\n")
    formatted=[]

    for line in lines:
        if not line.strip():
            continue
        if output_type == "plan":
            formatted.append(f"- {line.strip()}")
        elif output_type == "wbs":
            if line.strip()[0].isdigit():
                formatted.append(f"\n{line.strip()}")
            else:
                formatted.append(f"    {line.strip()}")
        elif output_type == "charter":
            if ":" in line:
                key, val = line.split(":", 1)
                formatted.append(f"**{key.strip()}**: {val.strip()}")
            else:
                formatted.append(line.strip())
        else:
            formatted.append(line.strip())

    return "\n".join(formatted)


def run_orchestrator(user_message:str, budget:float=250000)->dict:
    global charter_text_global, wbs_global, plan_global
    msg_lower = user_message.lower().strip()
    print(f"Orchestrator received message: {user_message}")
   
   #Button action: Generate Charter
    if "generate charter" in msg_lower: 
        result= generate_charter(user_message)
        if result.get("success"):
            charter_text_global = result.get("charter_text")
            #print("Generated Charter Text:", charter_text_global)
            return {"success": True, "content":format_output(charter_text_global,"charter"),"type": "charter"}
        return {"success": False, "error": result.get("error")}
          
   #Button action: Generate WBS
    elif "generate" in msg_lower and "wbs" in msg_lower:
        print("Generating WBS from charter text:", charter_text_global)
        result = generate_wbs(charter_text_global)
        if result.get("success"):
            wbs_global = result.get("wbs")
            #print("Generated WBS Text inside orchestrator:", wbs_global)
            return {"success": True, "content":format_output(wbs_global,"wbs"),"type": "wbs"}
        return {"success": False, "error": result.get("error")}
   #Button action: Generate Detailed Plan 
    elif "generate" in msg_lower and "plan" in msg_lower and wbs_global and budget:
        result = generate_detailed_plan(wbs_global, budget)
        if result.get("success"):
            plan_global = result.get("plan")
            return {"success": True,"content":format_output(plan_global,"plan"),"type": "plan"}
        return {"success": False, "error": result.get("error")}
    else:
        return {
            "success": False,
            "error": "Invalid request or missing required inputs (charter_text for WBS, wbs and budget for plan)."
        }

        
