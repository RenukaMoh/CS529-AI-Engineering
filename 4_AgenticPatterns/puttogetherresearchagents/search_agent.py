from agents import Agent, WebSearchTool, ModelSettings, function_tool

# Do it on the terminal - uv pip install openai-agents duckduckgo-search or uv add openai-agents duckduckgo-search
#from duckduckgo_search import DDGS # Free version of websearch and no key required
from ddgs import DDGS

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)
@function_tool
def duckduckgo_search_tool(query:str):
    """
    Performs a DuckDuckGo web search for a given query.
    Args:
        query: The search query string.
    Returns:
        The search results (e.g., in a string format for the agent).
    """
    ddgs = DDGS()
    results = ddgs.text(keywords=query, max_results=3) # Example: limit to 5 results
    formatted_results = "\n".join([f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}" for r in results])
    return formatted_results

# Register the search tool with the OpenAI Agents SDK
#search_tool = function_tool(duckduckgo_search_tool)

# Create your agent with the registered tool
search_agent = Agent(
    name="Search Agent",
    instructions=INSTRUCTIONS,
    tools=[duckduckgo_search_tool], 
   # tools=[search_tool],
    model="gpt-4o-mini"
)


# If you are interested to pay the amount using OpenAI Websearch, current .25$ per query
"""search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)"""