#!/usr/bin/env python

import logging
import os
import sys
import json
from datetime import datetime, timezone

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.mcp import MCPServerSSE
from pydantic_ai.providers.ollama import OllamaProvider

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="agent.log",
)

logging.info("Starting agent...")


class K8sAgent:
    def __init__(self, model_name: str):
        self.model_name = model_name
        logging.info(f"Initializing K8sAgent with model: {model_name}")

        self.server = MCPServerSSE(
            os.getenv("MCP_URL", "http://127.0.0.1:8000/sse"),max_retries=5
        )
        logging.info("MCP Server initialized.")

        self.agent = Agent(
            model_name,
            toolsets=[self.server],
            retries=5,
            instructions=(
                "You are a Kubernetes administrator. You will be asked to manage and inspect a Kubernetes cluster."
                "You can use the Kubernetes MCP Server to perform actions."
                "Provide concise summaries of the actions taken or information retrieved."
            ),
        )
        logging.info("Pydantic AI Agent created.")

    def run_task(self, task_string: str):
        logging.info(f"Running task: {task_string}")
        result = self.agent.run_sync(task_string)
        logging.info(f"Agent run complete. Result output: {result.output}")
        logging.info(f"Agent run complete. Usage output: {result.usage()}")
        self.log_interaction(task_string, result)
        return result

    def log_interaction(self, task: str, result):
        """Logs the interaction details to a JSONL file."""
        usage = result.usage()
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": self.model_name,
            "task": task,
            "response": result.output,
            "usage": {
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "total_tokens": usage.input_tokens + usage.output_tokens,
            }
        }

        with open("agent_history.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python k8s-loop.py <model_name>", file=sys.stderr)
        print("\t\t models: ollama:qwen3:14b gpt-5-mini gemini-2.5-pro")
        print("\nSee https://ai.pydantic.dev/models/overview/ for examples")
        sys.exit(1)

    model_name = sys.argv[1]

    if model_name.find("ollama") > -1:
        if "OLLAMA_BASE_URL" not in os.environ:
            print("Set OLLAMA_BASE_URL to http://1.2.3.4:11434/v1")
            sys.exit(1)

    k8s_agent_instance = K8sAgent(model_name)

    print("Enter your tasks. Type 'exit' or 'quit' to end the session.")
    while True:
        try:
            user_task = input("K8s Task (or 'exit'/'quit'): ")
            if user_task.lower() in ["exit", "quit"]:
                print("Exiting session.")
                break
            if not user_task.strip():
                print("Task cannot be empty. Please enter a task.")
                continue

            result = k8s_agent_instance.run_task(user_task)
            print("\n" + result.output)
            print(result.usage())
        except Exception as e:
            logging.error(f"An error occurred during task execution: {e}")
            print(f"An error occurred: {e}")
