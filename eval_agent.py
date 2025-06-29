from agent import Agent

class EvalAgent(Agent):
    # to evaluate the progress of subagents and the final task output.
    # does not build up past evaluations in context window, only knows orchestrator plan and keeps context window free
    # only assess whats its immediately looking at.
    raise NotImplementedError