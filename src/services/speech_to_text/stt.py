import whisper
from typing import Dict, Optional

class SpeechToTextModel:
    """ ABS base class for speach to text models implementation. """

    def transcribe(self, file_path: str, language: Optional[str] = None) -> Dict:
        """ Transcribe selected audio file. """
        raise NotImplementedError(" Method transcribe() must be implemented in a subclass. ")
    

class WhisperModel(SpeechToTextModel):
    """ Implementation local Whisper model for transcription speach to text. """

    _instance = {}

    def __new__(cls, model_size: str = "base"):
        """ Application of the Singleton pattern for each model size. """
        if model_size not in cls._instance:
            cls._instance[model_size] = super(WhisperModel, cls).__new__(cls)
            return cls._instance[model_size]
        
    def __init__(self, model_size : str = "base" ) -> None:
        """
        Initialzation of Whisper model.

        :param model_size: Size of Whisper model that will be loading. Available sizes: 'tiny' , 'base' , 'small' , 'medium' , 'large'
        """
        if not hasattr(self, 'inilialized'):
            self.model_size = model_size
            self.model = whisper.load_model(self.model_size)
            self.inilialized = True # Prevent re-initialization
    

    def transcribe(self, file_path: str, language: Optional[str] = None) -> Dict:
        """
        Transcibe selected audio file with using Whisper model.

        :param file_path: path describes audio file location.
        :param language: Language code, ex. 'pl' for polish
        :return: Transcription result returned as dictionary.
        """
        try:
            result = self.model.transcribe(file_path, language=language)
            return result
        except Exception as e:
            raise RuntimeError(f"Error during transcription: {e}")


class STTService:
    """ Speach-to-text conversion service using any model compatible with SpeechToTextModel ABS class.  """

    def __init__(self, model: SpeechToTextModel) -> None:
        """
        Initialize STT service with the given model.

        :param model: an instance of the class inheriting from SpeechToTextModel.
        """
        self.model = model

    def transcription(self, file_path: str, language: Optional[str] = None) -> Dict:
        """
        Transcibe selected audio file with using configured model.

        :param file_path: path describes audio file location.
        :param language: Language code, ex. 'pl' for polish
        :return: Transcription result returned as dictionary.
        """
        return self.model.transcribe(file_path, language)