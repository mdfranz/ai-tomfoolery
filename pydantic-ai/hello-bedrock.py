#!/usr/bin/env python

# import logging,os

from pydantic_ai import Agent
from pydantic_ai_bedrock.bedrock import BedrockModel

# logging.basicConfig(level=logging.DEBUG)


# See https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html 

bedrock_models = ["anthropic.claude-3-5-sonnet-20241022-v2:0","cohere.command-r-plus-v1:0",
                  "us.meta.llama3-3-70b-instruct-v1:0","us.amazon.nova-pro-v1:0"]

if __name__ == "__main__":
    for m in bedrock_models:

        print (f"Testing {m}")
        model = BedrockModel( model_name=m)
        agent = Agent(model=model, system_prompt='Be verbose, reply with at least 3 sentences with elaboration')
        result = agent.run_sync('Where does "hello world" come from?')
        print(result.data)
        print(result.usage())
