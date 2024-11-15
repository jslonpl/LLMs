import json
import logging

from src.api.openai_api import OpenAIClient
from src.services.s01e03.calculator import Calculator


class DataProcessor:
    """
    Manages data loading, processing and saving
    """
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.data = None
        self.openai_client = OpenAIClient()


    def load_json_data(self):
        """
        Loads data from the input JSON file.
        """
        try:
            with open(self.input_file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            logging.info(f"Data loaded from {self.input_file_path}")
        except Exception as e:
            logging.error(f"Error loading data from {self.input_file_path}: {e}")

    
    def save_json_data(self):
        """
        Saves processed data to the output JSON file.
        """
        try:
            with open(self.output_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)
                logging.info(f"Data saved to {self.output_file_path}")
            logging.info(f"Data saved to {self.output_file_path}")
        except Exception as e:
            logging.error(f"Error saving data to {self.output_file_path}: {e}")


    def process_data(self):
        """
        Processes the loaded data, handling both test and calculation items.
        """
        if self.data is None:
            logging.error("No data loaded to process.")
            return
        
        for item in self.data.get("test-data", []):
            if "test" in item:
                self._process_test_item(item)
            else:
                self._process_calc_item(item)

    
    def _process_test_item(self, item):
        """
        Processes a test requiring OpenAI API interaction.

        Args:
            item(dict): The item to process.
        """
        question = item.get("test",{}).get("q")
        if question:
            answer = self.generate_openai_response(question)
            item["test"]["a"] = answer
            logging.info(f"Processed OpenAI response for question: {question}")
        else:
            logging.warning("No question found in test item.")


    def _process_calc_item(self, item):
        """
        Processes a calculation item by validating or correcting the answer.

        Args:
            item(dict): The calculation to process
        """
        question = item.get("question")
        answer = item.get("answer")
        if question and answer is not None:
            if not Calculator.is_correct_answer(question, answer):
                correct_answer = Calculator.evaluate_expression(question)
                item["answer"] = correct_answer
                logging.info(f"Correct answer for question '{question}': {correct_answer}")
            else:
                logging.info(f"Answer for quesiton: '{question}' is correct.")
        else:
            logging.warning("Incomplete data in calibration item.")

    
    def generate_openai_response(self, question):
        """
        Generates a reponse from the OpenAI API for a given question.

        Args:
            question (str): The question to send to OpenAI.

        Returns:
            str: The reponse from OpenAI, or None if an error occurs.
        """

        prompt = f"Use the shortest possible phrase to answer. {question}"
        try:
            response = self.openai_client.generate_response(
                prompt,
                model = 'gpt-4',
                max_tokens = 50
            )
            return response
        except Exception as e:
            logging.error(f"Error generating OpenAI response: {e}")
            return None

