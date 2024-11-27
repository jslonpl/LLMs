from dataclasses import dataclass
from typing import Dict, Optional, List
import uuid
from bs4 import BeautifulSoup

@dataclass
class MediaPlaceholder:
    type: str # "image" or "audio"
    name: str
    src: str
    caption: Optional[str] = None
    position: int = 0
    unique_id: str = str(uuid.uuid4())
    ai_description : Optional[str] = None


class HTMLParser:
    def __init__(self):
        self.images_data: Dict[str, MediaPlaceholder] = {}
        self.audio_data: Dict[str, MediaPlaceholder] = {}
        self._position_counter = 0

    def _create_placeholder(self, media_type: str, name: str, src: str, caption: str = None):
        """ Create new media placeholder. """
        self._position_counter += 1
        return MediaPlaceholder(
            type=media_type,
            name=name,
            src=src,
            caption=caption,
            position=self._position_counter
        )
    
    def _process_figure(self, figure_element) -> Optional[str]:
        """
        Process figure elements and return placeholder if image has been found.

        Args:
            figure_element: Figure HTML element to process

        Returns:
            Optional[str]: Placeholder for founded image or None
        """
        img = figure_element.find("img")
        if not img:
            return None
        
        src = img.get("src", "")
        name = src.split("/")[-1]
        caption = figure_element.find("figcaption")
        caption_text = caption.get_text().strip() if caption else None

        placeholder = self._create_placeholder('image', name, src, caption_text)
        self.images_data[name] = placeholder
        return f"__MEDIA_{placeholder.unique_id}__"
    
    def _process_audio(self, audio_element) -> Optional[str]:
        """
        Process audio elements and return placeholder if audio has been found.

        Args:
            audio_element : Audio element for processing

        Returns:
            Optional[str]: Placeholder for dounded audio element or None
        """
        src = audio_element.get('src',"")
        if not src:
            source = audio_element.find("source")
            if source:
                src = source.get("src","")
        
        if not src:
            return None
        
        name = src.split("/")[-1]
        placeholder = self._create_placeholder("audio", name, src)
        self.audio_data[name] = placeholder
        return f"__MEDIA_{placeholder.unique_id}__"
    
    def _process_text_node(self, element) -> Optional[str]:
        """
        Process text node

        Args:
            element: Text element to processing

        Returns:
            Optional[str]: Processed text or None
        """
        if element.parent.name in ["figcaption", "script", "style"]:
            return None
        text = element.strip()
        return text if text else None
    
    def parse_html_to_text(self, html_content: str) -> str:
        """
        Parse HTML content, extract text and media

        Args:
            html_content: HTML text for parse

        Returns:
            Parsed text with plaseholders for media
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content : List[str] = []

        for element in soup.body.descendants:
            content = None

            if element.name == 'figure':
                content = self._process_figure(element)
            elif element.name == "audio":
                content = self._process_audio(element)
            elif element.name is None:
                content = self._process_text_node(element)

            if content:
                text_content.append(content)
        
        return '\n'.join(filter(None, text_content))
    
    def get_image_data(self) -> Dict[str, MediaPlaceholder]:
        """ Return dictionary containg images data"""
        return self.images_data
    
    def get_audio_data(self) -> Dict[str, MediaPlaceholder]:
        """ Returns dictionary containg audio data """
        return self.audio_data
    
    def replace_media_placeholders(self, text: str, replacements: Dict[str, str]) -> str:
        """
        Replace media placeholders with actual content

        Args:
            text: Text with placeholders
            replacements: Dictionary mapping unique_id with placeholders content

        Returns:
            Text with replaced placeholders
        """

        result = text
        for media_id, replacement in replacements.items():
            placeholder = f"__MEDIA_{media_id}__"
            result = result.replace(placeholder, replacement)
        return result


