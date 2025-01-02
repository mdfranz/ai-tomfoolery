import random
from loguru import logger
import ollama

# From https://medium.com/@smrati.katiyar/ollama-tool-function-calling-e02f81bd9d41

def get_lucky_number(min_number: int, max_number: int) -> int:
    """
    Generate Lucky number to use in your calculations

    Args:
         min_number: Minimum integer value
         max_number: Maximum integer value

    Returns:
        int: Randomly generated number between minimum and maximum limit
    """
    lucky_number = random.randint(int(min_number), int(max_number))
    logger.info(f"Lucky Number: {lucky_number}")
    return lucky_number

def this_is_dummy_function_to_confuse_llm(min_number: int, max_number: int) -> int:
    """
    This is a dummy function to confuse llm

    Args:
         min_number: Minimum integer value
         max_number: Maximum integer value

    Returns:
        int: a static integer value
    """
    logger.info("I am a dummy function to confuse llm tool calling")
    return 5

available_functions = {
    'get_lucky_number': get_lucky_number,
    'this_is_dummy_function_to_confuse_llm': this_is_dummy_function_to_confuse_llm,
}

if __name__ == '__main__':
    response = ollama.chat(
        'llama3.2',
        messages=[
            {
                'role': 'user',
                'content': 'Generate a lucky number between 13 and 20'
            }
        ],
        tools=[get_lucky_number, this_is_dummy_function_to_confuse_llm]
    )
    logger.info(response.message.tool_calls)
    for tool in response.message.tool_calls or []:
        function_to_call = available_functions.get(tool.function.name)
        if function_to_call:
            print('Function output:', function_to_call(**tool.function.arguments))
        else:
            print('Function not found:', tool.function.name)

