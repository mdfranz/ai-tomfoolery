import os
import logging
from datetime import datetime
from strands import Agent
from strands.models.ollama import OllamaModel


# Assumes  OLLAMA_HOST=127.0.0.1:11434 (or other portk)

logging.getLogger("strands").setLevel( logging.DEBUG)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Generate a single timestamp for all files
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")

models_list = ['gemma3:12b', 'cogito:14b']
# models_list = ['qwen2.5:7b', 'gemma3:12b', 'olmo2:13b', 'phi4-mini:3.8b', 'deepseek-r1:14b']
for m in models_list:
    logging.debug(f"Processing model: {m}")
    try:
        ollama_model = OllamaModel(
            host=f"http://{os.environ['OLLAMA_HOST']}",
            model_id=m,streaming=False)
        agent = Agent(model=ollama_model)
        logging.debug(f"Agent created for model: {m}")

        response = agent("Tell me a scary story about America")



        print("\n",type(response))
        print(f"Response from model {m}: {response}")

        # Create a safe filename and save the response
        safe_model_name = m.replace(':', '-')
        filename = f"output/{timestamp}-{safe_model_name}.txt"
        with open(filename, "w") as f:
            f.write(str(response))
        logging.info(f"Response from model {m} saved to {filename}")

    except Exception as e:
        logging.error(f"An error occurred while processing model {m}: {e}")
