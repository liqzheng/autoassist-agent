from rag import search_documents as rag_search

def search_documents(query: str) -> str:
    return rag_search(query)

def analyze_data(task: str, data: str = "") -> str:
    return f"[Data Analysis] Task received: {task}"

def web_search(query: str) -> str:
    return f"[Web Search] Results for: {query}"

TOOLS = [
    {
        "name": "search_documents",
        "description": "Search uploaded documents and knowledge base for relevant information",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "The search query"}},
            "required": ["query"]
        }
    },
    {
        "name": "analyze_data",
        "description": "Perform data analysis, calculate statistics, or derive insights",
        "input_schema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "The analysis task"},
                "data": {"type": "string", "description": "Optional data context"}
            },
            "required": ["task"]
        }
    },
    {
        "name": "web_search",
        "description": "Search the web for current information and recent events",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "The search query"}},
            "required": ["query"]
        }
    }
]

def execute_tool(name: str, inputs: dict) -> str:
    if name == "search_documents":
        return search_documents(inputs["query"])
    elif name == "analyze_data":
        return analyze_data(inputs["task"], inputs.get("data", ""))
    elif name == "web_search":
        return web_search(inputs["query"])
    else:
        return f"Unknown tool: {name}"
