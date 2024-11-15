import logging
import sympy


class Calculator:
    """
    Handles safe evaluation and validation of mathematical expressions.
    """

    @staticmethod
    def evaluate_expression(expression_str):
        """
        Safely evaluates a mathematical expression string.

        Args:
            expression_str (str): The mathematical expression as a string

        Returns:
            float: The evaluated result, or None is a error occurs
        """
        try:
            expression = sympy.sympify(expression_str)
            result = float(expression.evalf())
            return result
        except Exception as e:
            logging.error(f"Error evaluating expression '{expression_str}': {e}")
            return None

    @staticmethod
    def is_correct_answer(question, provided_answer):
        """
        Check if the provided answer is correct for the given question

        Args:
            question (str): The mathematical question.
            provided_answer (str): The answer to validate.

        Returns:
        bool: True if the answer is correct, False otherwise.
        """
        expected_answer = Calculator.evaluate_expression(question)
        if expected_answer is None:
            return False
        try:
            provided_answer = float(provided_answer)
            return abs(provided_answer-expected_answer) < 1e-6
        except ValueError:
            logging.error(f"Invalid answer format: {provided_answer}")
            return False