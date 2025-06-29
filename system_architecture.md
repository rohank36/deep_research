# Thoughts
- when orhcestrator wants to give feedback/adjust trajectory of worker agent, it should take the agents most recent thought + tool call from memory and restart the agent from that context.
- what is the better system design for trajectory communication?
    1. Centralized: Orchestrator controls trajectory
    2. Decentralized: Agents control their own trajectory and can see what all other agents are doing
- worker agent conflict resolution, trajectory handling, feedback - all handled by the orchestrator agent by looking at the system memory?
    - When will orchestrator check memory? (every x seconds? every time a new entry is added? have to think whats best and economical)
- for worker agent system prompts, have a generic part then a specialized part set by the orhcestrator (is this a good idea? could backfire if you need to change the task for the agent based on the orhcestrator re-thinking something)
- How will the memory be structued. Probably vector db for semantic search...
    - what do agents send to memory? 
- Need to add a create_plan tool which saves the plan to memory
    - also need a read_memory_tool and a bunch of other tools LOL but those will make themselves apparent as you work.
- What are the orchestrators tasks?
    - Plan (including sub tasks), subtask assignment, task management, agent monitoring, conflict resolution, re-plan to recover from errors etc
- Have to think more about memory and how that will work. How can we best represent an agent's trajectory and ensure there are no conflicts?
- cost optimization (use appropriate models at right times, context compression etc)
- security again prompt injection from websites/mcp servers etc
- guardrails (agents must assess actions for potential harm)


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
- How to evaluate overall result?
### Worker Agent management 
- trajectory handling, 
### Health
- How to calculate health
- How to check health

## Communication 

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