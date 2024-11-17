from src.api.openai_api import OpenAIClient

def test_generate_text():
    client = OpenAIClient()
    prompt = "Who are you? Response in two short phrases."

    try:
        response = client.generate_response(prompt, model="gpt-4", max_tokens=100)
        assert  isinstance(response, str), "Opdpowiedz nie jest tekstem"
        assert len(response)>0, "Odpowiedz jest pusta"
        print(f"Odpowiedz modelu: {response}")
    except Exception as e:
        print(f"Błąd podczas testu: {e}")
        


if __name__ == "__main__":
    test_generate_text()