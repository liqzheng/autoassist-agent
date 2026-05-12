import os
from dotenv import load_dotenv

load_dotenv()  # 先读 .env 文件

import anthropic
from tools import TOOLS, execute_tool

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are AutoAssist Agent, a smart AI assistant with access to tools.
Always use at least one tool to answer questions — never reply from memory alone.
Think step by step before acting."""

def run_agent(message: str, history: list = []) -> dict:
    messages = history + [{"role": "user", "content": message}]
    steps = []
    iteration = 0
    max_iterations = 5

    while iteration < max_iterations:
        iteration += 1
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            final_answer = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_answer += block.text
            return {"answer": final_answer, "steps": steps}

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    steps.append({"tool": block.name, "input": block.input})
                    result = execute_tool(block.name, block.input)
                    steps[-1]["output"] = result
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            messages.append({"role": "user", "content": tool_results})

    return {"answer": "Max iterations reached.", "steps": steps}