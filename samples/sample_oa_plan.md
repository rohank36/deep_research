<thinking>
The query is about a specific new school founded in the 1990s by merging a girls' school and a boys' school in a town with a history dating back to the late 19th century. The new school was given a Latin name, and the question is what was the original name of the girls' school before the merger.

To answer this, I need to:
1. Identify notable cases where girls' and boys' schools merged in the 1990s to form a coeducational school with a Latin name.
2. Focus on towns with a history going back to the second half of the 19th century.
3. Find the name of the girls' school involved in such a merger.

Since this is a historical and somewhat specific educational question, I should first try to identify which new school with a Latin name was formed in the 1990s from a merger of gender-segregated schools. Then, figure out the girls' school name.

This appears to be a breadth-first-search type problem: I need to consider different plausible schools or places that match these criteria, then find the one that fits.

I will run multiple subagents in parallel to look for mergers of girls' and boys' schools in the 1990s with Latin names, also focusing on the historical town clue.

I will run three searches in parallel:
1. Search for notable coeducational schools founded in the 1990s from merging boys' and girls' schools that have a Latin name.
2. Search for girls' schools in towns with 19th-century history that merged with boys' schools in the 1990s.
3. Search for towns with Latin-named schools founded in the 1990s by merging gender-segregated schools.

This will help triangulate the correct girls' school name.

</thinking>
<text>
I am researching notable coeducational schools founded in the 1990s by merging girls' and boys' schools where the new school was given a Latin name. I will also consider the historical context of the town dating back to the second half of the 19th century to find the name of the original girls’ school.
</text>
<tool_use>
{
  "name": "run_subagents_parallel",
  "args": {
    "num_agents": 3,
    "prompts": [
      "Find notable coeducational schools founded in the 1990s by merging girls' and boys' schools that were given Latin names. Include the original names of the schools if possible.",
      "Find girls' schools in towns with a history dating back to the late 19th century that merged with boys' schools in the 1990s. Provide their names and any information on the merged schools.",
      "Find towns with schools named in Latin founded in the 1990s by merging boys' and girls' schools. Provide the names of the predecessor schools as well."
    ]
  }
}
</tool_use>