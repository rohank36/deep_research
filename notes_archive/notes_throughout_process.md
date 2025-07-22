# Observations

## July 5th 2025
- Corrects itself well when it gets the correct format wrong. Though gpt-4.1-nano often gets the format wrong, still recovers well which means feedback loop is working.
    - update: it messes up the format quite a bit.
- When given 5 links, it was able to tell that the first link (etsy) wasn't something factual. Was looking for newspaper articles and archive/databases. **Shows that the agent was able to reason about which links to select**
- is able to accurately use the links provided by the search result.
- When it was terminated, it reasoned about the information it had and gave an answer (non-hallucinated) which is hopeful.
- tough to get quality search results on DuckDuckGo. re: etsy always coming up first. Very diff results when tested with google search
    - future soln: source quality checker.
- the raw fetch_content is noisy and long. Might be useful to extract key information anchored on the task using another cheap llm?
- not sure if the trajectory of its reasoning and process is good enough
    - may require further prompt eng
- It doesn't go through all the links in a search result. not even 2. always just 1 then fetches the content.
    - prompt eng worker agent instructions more.
    - fixed wa sys prompt. works better now.
        - fetched link it wanted, but the site was blocked, so it acknowledged that and tried another link from the same search results. then tried the last reasonable link from the search results. Prompt eng fixed it. good.
- maybe for general instructions give few shot examples that are relevant to search?
- the search component of the MAS is hard lol
- tried w/ gpt-4.1 and it overall felt a bit better but still made mistakes. 
    - notably it kept messing up the dictionary brackets for the tool_use. it missed the final closing bracket across 2 calls.
- 4.1-mini
    - good answer formatting. good reasoning about links. doesn't just auto try new search after 1 link (seems that the prompt eng rlly was the key to fixing this). 
    - when it tried all relevant links and none worked out, it tried a new search. Exactly what i wanted it to do.
    - when it found a reasonable answer it followed the proper protocol (e.g. proper formatting with no tool call)
    - answer it found was reasonable given the search results it got.
    - happy with it.
- ### Summary:
    - 4.1-nano really gets the format wrong a lot of times. wastes a lot of steps being told its missing a tag and making the same mistake repeatedly
        - need to make format simpler? or is it cause the model isn't that good?
        - maybe think about a way to remove preivous error traces? this might posion the context and confuse the model.
        - 4.1-mini on one run worked exactly as expected.
    - **quality of sources is an issue (duckduckgo surfacing bad sites, e.g. crosswords and etsy)**
        - possible soln: brave search api
    - **site content not having anything good is an issue**
    - **site content just being rlly noisy is also an issue**
    - models tested:
        - 4.1-nano: not great, not bad. makes a lot of formatting mistakes but still works-ish.
        - 4.1: works well when it works, but makes formatting mistakes as well. most $$ out of the 3.
        - 4.1-mini: worked exactly as wanted. On 1 run, it completed the task well with no formatting errors and is a good price. 
        - **tldr. Use 4.1-mini for worker agent**
    - I wonder if you run it for wayyy more steps, how it will adjust its search trajectory. will it just keep searching for roughly the same thing? just with a few things changed? thus yielding similar search results and it the agent just hitting a wall? will have to test and see i guess.

- ### Learnings:
    - have to test and play around a lot to craft a good prompt. a good prompt is essential as it powers the brain of the agent.
    - ai engineering is rlly just a new paradigm of swe. instead of if-else control flow, the program control flow is done by the LLM and the conditional statements are defined in plain english by your prompt.
    - sometimes the best model isn't always best for the job, try diff models (re: 4.1-mini working better than 4.1, while being cheaper)
        - most general open source models (e.g. llama) aren't that good for agent brains.

## July 6th 2025
- Right now ur working with hard queries. lets try a simple query and see how the agent performs.
    - tried with "How many Ballon d'Ors does Lionel Messi have?"
        - it answered correctly with one tool call. Too easy. try harder task.
        - in the system prompts its important to include the current date, because if the user asks a query in regards to time (explicitly or implicitly) like this one, the agent needs to be aware.
    - "Which American president had a vice president who later became president, and also signed a major civil rights act during their own presidency?"
        - Exhibited strong reasoning aligned with the prompt.  
        - Came up with a correct answer. Question was badly worded, but it did what it could.
        - Followed the prompt and built its factual knowledge based on the task and continued searching so it could fill its gaps.
- gpt-4.1-mini is so good with the formatting, the workflow goes smoothly with it.
- right now oa run code == wa run code. see if you need to make any modifications to oa code. if not then implement run in Agent. same for terminate_agent. 
- gpt-4.1-mini, for fn args that are more not just str, when it goes through json.loads() it turns to the correct objects like int and List[str]. Refer to sample_oa_plan.md. The tool call types are correct after json.loads()
- ### Summary
    - rewrote oa prompt and run(). Now need to implement the functions to run the subagents then can test full pipeline.
    - need to be thoughtful about how to execute the subagents in parallel.
    - you should try asking it AskMcGill type questions (e.g. list all currently available 1 credit computer science courses at McGill)
        - easily verifiable 
- ### Learnings
    - when building from scratch, start as simple as possible and build from there. This is especially true for prompts.
    - gpt-4.1-mini is good

## July 21st 2025
- Refactored a ton of the code to make it way simpler. 
- You fell into the classic trap of building top down, building for things you thought you'd need making it way more complex then it needed to be. Build lean then add later if needed. Don't try to overcompliate things.
- Tried prompt injecting and the agent new it was bad stuff. Continued properly
- Huge bottleneck is how bad your search tools are. Low quality sources + hard to scrape a lot of times. 
- orchestrator showed signs of good reasoning. Ran 2 subagents in parallel then thought a bit more info needed to be found so ran one subagent. Good.
- for production would also need a citations agent, context engineering/trajectory management

- ### Summary
    - 
- ### Learnings
    - 