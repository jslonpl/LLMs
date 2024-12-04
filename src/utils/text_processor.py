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

    @staticmethod
    def split_text_into_chanks(text: str, end_signs: str = "\n") -> list:
        """
        Split text into paragraphs based on cheking special sign on end of the line.
        Parameters:
            text (str) : Input text to splitting / chanking
            end_signs (str) : End line signs, base on which methode splitting the text

        Return: 
            List[str] : List of paragraphs / chanks

        Raises:
            ValueError: If input text is None or not a string
            Exception: For other unexpected errors during process
        """
        try:
            if not text:
                return []
            
            text = text.strip()
            chanks = text.split(end_signs)
            filtered_chanks = []
            for p in chanks:
                if p.strip():
                    filtered_chanks.append(p.strip())
            return filtered_chanks

        except ValueError as ve:
            logging.error(f"Invalid input data: {ve}")
            raise
        except Exception as e:
            logging.error(f"Error during text splitting: {e}")
            raise

    @staticmethod
    def check_text_contain(text: str, phrase: str) -> bool:
        """
        Check if the text containing given phrase

        Parameters:
            text (str) : Text for analysis
            phrase (str): Searched phrase

        Returns:
            bool: True if phrase has been found, False otherwise
        """
        return phrase.lower() in text.lower()
    
    @staticmethod
    def tokenize_text(text: str, delimiter: str = r",\s+") -> list:
        """
        Tokenize text into individual words using specified delimiter.

        ParametersL
            text (str): Input text to tokenize
            delimiters (str): Regular expression pattern for splitting text
                                Default splits on commas and whitespace

        Returns:
            List[str]: List of tokens/words

        Raises:
            ValuError: If input text is None or not a string
            Exception: For other unexpected errors during processing

        Examples related with delimiter pattern for text1 = "hello world, python, data science":
            - delimiter: r',\s+' : result= ['hello world', 'python', 'data science']
            - delimiter: r'[,\s]+' : result = ['hello', 'world', 'python', 'data', 'science']
        """
        try:
            if not text:
                return []
            
            # Split text using regex pattern 
            raw_tokens = re.split(delimiter, text)

            # Initialize empty list for cleaned tokens
            tokens = []

            for token in raw_tokens:
                # Remove whitespace from start and end
                cleaned_token = token.strip()

                # Only add non-empty tokens
                if cleaned_token:
                    tokens.append(cleaned_token)
            return tokens
        
        except ValueError as ve:
            logging.error(f"Invalid input format: {ve}")
            raise
        except Exception as e:
            logging.error(f"Error during text tokenization: {e}")
            raise
                          
        

