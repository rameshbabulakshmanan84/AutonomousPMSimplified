WBS_GENERATION_PROMPT = """

Charter:
{charter_content}

You are a project planner. Generate a Work Breakdown Structure (WBS) aligned with delivery gates.

For each work package: WBS_ID, name, description, owner, hours, acceptance_criteria.

OUTPUT FORMAT:
Return a hierarchical text outline of work packages and tasks.

Use this format:
1.0 Phase Name (Gate 1)
  1.1 Work Package Name
    - Owner: [name]
    - Hours: [number]
    - Acceptance Criteria: [description]
  1.2 Another Package
    - Owner: [name]
    - Hours: [number]
    - Acceptance Criteria: [description]

2.0 Next Phase (Gate 2)
  2.1 Work Package
    ...

CRITICAL REMINDER: Do NOT use JSON. Do NOT use markdown code blocks. Just plain text outline.

"""

DETAILED_PLAN_PROMPT = """
You are an expert project planner. Your job: create a detailed task plan from an approved WBS.
 
INPUT:
- Approved WBS (hierarchical work packages with characteristics)
- Budget allocated
- Total Timeline is 12 weeks
 
OUTPUT: Detailed task plan with dates, dependencies, and costs.
 
CONSIDERATIONS BY DOMAIN:
- Cloud Migration: include data validation, cutover windows, rollback contingencies
- Software Development: include code review, UAT, deployment staging
- Infrastructure: include capacity testing, failover testing, security hardening
- Compliance: include audit checkpoints, document sign-offs, traceability tasks
 
STRICT RULES:
- Each task has: task_id (T1, T2...), wbs_id (link to package), name, owner, duration_hours (1-40), 
  cost, start_date, end_date, predecessors, gate_number, gate_blocking
- Task cost = duration_hours × $60/hour (default rate)
- Total cost must NOT exceed budget
- Tasks must fit within charter timeline
- Gate-blocking tasks must complete before gate exit
- Milestones align with gate exits
- If urgency=high, compress timelines (parallel work, overlap phases where safe)
- If risk_profile=high, add explicit risk mitigation tasks and review gates
- If customer_facing=true, add UAT, communication, and rollback planning tasks
 

Using the WBS & characteristics, generate a detailed task level plan.Apply domain specific best practices.
OUTPUT FORMAT populate in TABLE FORMAT :

- Domain consideration inferred
Return a task list with:
- Task ID (T1, T2, T3...)
- Task name
- Owner (from charter team)
- Duration (hours)
- Cost (hours × $60)
- Gate mapping (which gate this belongs to)
- Dependencies (which tasks must finish first)
- Status (Not Started, In Progress, Completed)
- Start date
- End date 


Example:
T1 - Requirements Gathering
  Owner: Project Manager
  Duration: 20 hours
  Cost: $1,200
  Gate: 1
  Dependencies: None
  status : Not Started
  Start date : 03-07-2026
  End date : 10-07-2026 

T2 - Design Review
  Owner: Architect
  Duration: 30 hours
  Cost: $1,800
  Gate: 1
  Dependencies: T1
  status : Not Started


Continue for all WBS packages...

CONSTRAINTS:
- Total cost must not exceed ${budget}
- Each task 1-40 hours max
- All tasks must map to a gate
- Keep it simple and realistic

Budget allocation : ${budget}
WBS: {wbs}

Do NOT use JSON. Do NOT use markdown. Just plain text task list.
"""
