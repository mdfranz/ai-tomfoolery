# OLLAMA Configuration

See [Ollama](https://docs.litellm.ai/docs/providers/ollama)

```
export OLLAMA_API_BASE=http://x.x.x.x:11434
```

# CLI
```
(adk) mfranz@cros-x360:~/github/ai-tomfoolery/adk$ adk run hello
Log setup complete: /tmp/agents_log/agent.20250607_115723.log
To access latest log: tail -F /tmp/agents_log/agent.latest.log
Running agent fish, type exit to exit.
[user]: are you there 
11:58:17 - LiteLLM:INFO: utils.py:3064 - 
LiteLLM completion() model= qwen2.5:7b; provider = ollama_chat
11:58:18 - LiteLLM:INFO: cost_calculator.py:655 - selected model name for cost calculation: ollama_chat/qwen2.5:7b
[fish]: Yes, I'm here! How can I be useful for you today?
```
