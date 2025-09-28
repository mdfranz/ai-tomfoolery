import os
import logging
from strands import Agent
from strands.models.ollama import OllamaModel

logging.getLogger("strands").setLevel( logging.DEBUG) 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
                                          
models_list = ['qwen2.5:7b', 'gemma3:12b', 'olmo2:13b', 'phi4-mini:3.8b', 'deepseek-r1:14b']                                                                                                       
for m in models_list:
    logging.debug(f"Processing model: {m}") 
    try:
        ollama_model = OllamaModel(
            host=f"http://{os.environ['OLLAMA_HOST']}",
            model_id=m,streaming=False)
        agent = Agent(model=ollama_model)
        logging.debug(f"Agent created for model: {m}")
                                          
        response = agent("Tell me a scary story about America")
        print(type(response))
        print(f"Response from model {m}: {response}")  
    except Exception as e:                                                                                                                                               
        logging.error(f"An error occurred while processing model {m}: {e}")   
