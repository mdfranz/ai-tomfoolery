import asyncio, os, logging, textwrap

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=f"{os.path.splitext(os.path.basename(__file__))[0]}.log",
)

# Redirect LiteLLM logs to the file by removing its default handlers
litellm_logger = logging.getLogger("LiteLLM")
litellm_logger.handlers = []
litellm_logger.propagate = True
#
# See https://github.com/koverholt/adk-runtime-example
#

APP_NAME = "ollama"
USER_ID = "user"
SESSION_ID = "session"


class ModelTester:
    """A class to test a single model."""

    def __init__(self, model_id: str):
        """Initialize the ModelTester.

        Args:
            model_id: The ID of the model to test using LiteLLM format - https://docs.litellm.ai/docs/
        """
        self.model_id = model_id
        self.agent = self._create_agent()
        self.runner = self._create_runner()
        self.session = self._create_session()

    def _create_agent(self) -> Agent:
        """Create an agent for the model."""
        return Agent(
            name=self.model_id.replace("/", "").replace(":", "").replace("-", ""),
            model=LiteLlm(model=self.model_id),
            description=f"Agent for {self.model_id}",
            instruction=textwrap.dedent(
                """
               You are a silly 3rd grader that says inappropriate things all the time
            """
            ).strip(),
        )

    def _create_runner(self) -> InMemoryRunner:
        """Create an in-memory runner for the agent."""
        return InMemoryRunner(
            agent=self.agent,
            app_name=APP_NAME,
        )

    def _create_session(self):
        """Create a session for the runner."""
        return asyncio.run(
            self.runner.session_service.create_session(
                app_name=APP_NAME, user_id=USER_ID
            )
        )

    def query(self, prompt: str):
        """Query the agent with the given prompt.

        Args:
            prompt: The prompt to send to the agent.
        """
        logging.info("** User: %s", prompt)

        responses = []
        response = self.runner.run(
            new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
            user_id=USER_ID,
            session_id=self.session.id,
        )

        for message in response:
            if message.content.parts and message.content.parts[0].text:
                logging.info(
                    "** %s: %s\n", message.author, message.content.parts[0].text
                )
                print(f"\n{message.author} said  {message.content.parts[0].text}")
                responses.append(response)

        return responses


if __name__ == "__main__":
    MODEL_IDS = [
        "ollama/granite4:latest",
        "ollama/cogito:14b",
        "ollama/granite4:micro",
        "ollama/granite4:tiny-h",
    ]

    # Iterate through each model
    for model_id in MODEL_IDS:
        try:
            logging.info("=" * 60)
            logging.info("Testing model: %s", model_id)
            logging.info("=" * 60)

            tester = ModelTester(model_id)
            print(tester.query("Tell me a joke"))
            print(tester.query("Tell me a story"))

        except Exception as e:
            logging.error("Error testing model %s: %s", model_id, e)
