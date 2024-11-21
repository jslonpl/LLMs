import re
import logging

class TextProcessor:
    """
    Class for text processing and analysis.

    Main functionalities:
    - Extract content between special tags
    - (future features)
    """

    @staticmethod
    def extract_text_between_tags(text: str, tag: str) -> str:
        """
        Extract content between specific tags in a given text.

        Parameters:
            text (str) - Input text containing tags
            tag (str) - The tag name to extract content from (e.g., 'answer').

        Return
            str: Content between the tags, or an empty string if not found.
        """
        try:
            pattern = rf"<{tag}>(.*?)</{tag}>"
            match = re.search(pattern, text, re.DOTALL)
            return match.group(1).strip() if match else ""
        except Exception as e:
            logging.error(f"Error during tag extraction: {e}")
            raise
