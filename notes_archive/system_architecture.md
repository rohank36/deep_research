# Thoughts
- maybe mess around with a Thread class with an Events sub class. Have class functions like thread_to_prompt or event_to_prompt etc.
    - if you can label events like "bad_tool_call" later after it self-heals you can remove that from the context so it doesn't dilute it.
- when orhcestrator wants to give feedback/adjust trajectory of worker agent, it should take the agents most recent thought + tool call from memory and restart the agent from that context.
- worker agent conflict resolution, trajectory handling, feedback - all handled by the orchestrator agent by looking at the system memory?
    - When will orchestrator check memory? (every x seconds? every time a new entry is added? have to think whats best and economical)
- for worker agent system prompts, have a generic part then a specialized part set by the orhcestrator (is this a good idea? could backfire if you need to change the task for the agent based on the orhcestrator re-thinking something)
- Need to add a create_plan tool which saves the plan to memory
    - also need a read_memory_tool and a bunch of other tools LOL but those will make themselves apparent as you work.
- What are the orchestrators tasks?
    - Plan (including sub tasks), subtask assignment, task management, agent monitoring, conflict resolution, re-plan to recover from errors etc
- cost optimization (use appropriate models at right times, context compression etc)
- When building, initially first test the system separately, e.g. orchestrator agent can generate a good plan and extract the tasks etc and separately test the worker agent: give it a sample sub-task and see how well it does (This will be key)
- multi thread vs async system design.


# System Design: Centralized Planning + Decentralized execution

## Orchestration
- How to store overall system trajectory
    - DAG data structure
### Planning
- How to create plan
    - Explicit prompt asking LLM to generate well structured plan with subtasks in specific parseable format (e.g. json) added to user input 
- How to save plan
    - This plan can be saved as is in a JSON file locally that can be read. 
    - Alternatively, the plan could also be saved as a tree data structure where the main root node is the original plan
- How to execute plan
    - Parse generated plan, for each sub task (with uid), create worker agent with that specific task in its system prompt (this you have to think more about)
- How to update plan
    - read json, update subtask via id selection, save plan
- How to correct sub plan task trajectory
    - Look at subtask to update, find associated agent, compress agent context (maybe using cheap model here) and restart agent with new/updated task 
- How to assess if plan is done
    - use eval agent. Pass in plan + final result, see if eval accepts or rejects

## Agents
### Orchestrator Agent
- Tasks: Generate system plan with subtasks, assign sub tasks to worker agents, manage worker agents, aggregate/compile/compress worker agent results, return final result to user
### Worker Agent
- Tasks: Generate plan based on task given by orchestrator, execute plan - run(), return response to orchestrator
### Eval Agent
- Agent to evaluate worker performance and overall result. Output format using tags as well to parse and get decision.
- How to evaluate worker performance
    - Pass overall plan and worker subtask, and prompt eval agent to analyze whether the subgent is doing a good job
    - Goal: see if worker agent is doing the right thing
- How to evaluate overall result?
    - 
### Worker Agent management 
- How will the orchestrator agent check the agent trajectories?
    - Using a separate thread that runs a health monitoring loop.
- When will the orchestrator agent check the agent trajectories?
    - 

### Health
- How to calculate health
    - After each LLM call, the agent should divide its current input prompt count / model window count. 1 --> bad health because the context window is being full used. 
- How to check health
    - calling the agent heartbeat fn

## Citations
- How to know if the source is trusted and/or high quality? 

## Memory
- How to store thoughts + tool_use
    - Hybrid approach: 
        - Hashing for signature tracking: ensures no duplication of thoughts/tool_use because we can check for exact matches
        - Vector Embedding for trajectory similarity 
            - Embed thought/tool_use as vector (keep thought/tool_use hash + agent id in metadata)
            - ADD agent's sequential thoughts/tool_use so we're summing the vectors. This will encode the trajectory of the agent in linear space. 
            - Do ANN with a certain threshold to see which trajectories are similar. 
            - Orchestrator can conflict resolve all the similar trajectories by updating each and adjusting their course or terminating. 

## Observability
- Logger statements 

## System security
- Security again prompt injection from websites/mcp servers etc
- Guardrails (agents must assess actions for potential harm)

## Tools
- create_worker_agent(): creates a worker agent
- web_search()
- web_fetch(): get complete contents from web site 