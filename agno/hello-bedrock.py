#!/usr/bin/env python

# import logging,os

from agno.agent import Agent
from agno.models.aws import AwsBedrock


# logging.basicConfig(level=logging.DEBUG)
# See https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html 

bedrock_models = ["anthropic.claude-3-5-sonnet-20241022-v2:0","cohere.command-r-plus-v1:0",
                  "us.meta.llama3-3-70b-instruct-v1:0","us.amazon.nova-pro-v1:0"]

if __name__ == "__main__":
    for m in bedrock_models:

        agent = Agent( 
            model=AwsBedrock(id=m), 
            description="You are an amazing full stack technology historian",
            instructions=["Be verbose, reply with at least 3 sentences with elaboration"], 
            markdown=False,
            debug_mode=True,
            exponential_backoff=True,
            telemetry=True
        )

        agent.system_prompt="Be verbose, reply with at least 3 sentences with elaboration"

        try:
            agent.print_response('Where does "hello world" come from?')
        except:
            print (f"{m} FAILED")

