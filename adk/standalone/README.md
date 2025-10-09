# Model Testing Script

## Overview

This Python script, `tmp-runner.py`, is designed to test and interact with multiple large language models (LLMs) sequentially. It uses the Google ADK (Agent Development Kit) and the LiteLLM library to create, run, and query agents for a predefined list of models.

## Purpose

The primary purpose of this script is to provide a simple and efficient way to:

-   **Verify Model Availability:** Quickly check if a list of specified models are accessible and responsive.
-   **Compare Model Outputs:** Send the same prompts to different models to compare their responses, personalities, and capabilities.
-   **Automate Repetitive Testing:** Automate the process of setting up and querying models, which can be tedious to do manually.

This is particularly useful for developers who are experimenting with different models and need a consistent way to evaluate them.

## Features

-   **Multi-Model Testing:** The script iterates through a list of model IDs and runs the same set of queries on each one.
-   **Structured Logging:** All interactions and potential errors are logged to a file (`tmp-runner.log`), making it easy to review the results. It also cleanly separates the script's logs from the underlying libraries' logs.
-   **Object-Oriented Design:** The logic for handling a single model is encapsulated in a `ModelTester` class, which makes the code clean, organized, and easy to extend.
-   **Error Handling:** The script includes error handling to prevent a failure with one model from crashing the entire process.

## How to Use

1.  **Install Dependencies:** Make sure you have the necessary libraries installed. You can typically do this by running:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Models:** Open `tmp-runner.py` and modify the `MODEL_IDS` list to include the models you want to test.

3.  **Run the Script:** Execute the script from your terminal:
    ```bash
    python tmp-runner.py
    ```

4.  **Check the Output:** The script will print the models' responses to the console. A detailed log of the session will be saved in `tmp-runner.log`.

## Code Structure

-   **`ModelTester` Class:** This class is the core of the script. An instance of `ModelTester` is created for each model. It handles the creation of the agent, the runner, and the session, and it provides a `query` method to interact with the model.
-   **`test_model()` Function:** This function orchestrates the testing process for a single model. It creates an instance of `ModelTester` and calls its `query` method with predefined prompts.
-   **Main Execution Block:** The `if __name__ == "__main__":` block contains the list of `MODEL_IDS` and iterates through them, calling `test_model()` for each one.
