from api_client import APIClient

def main():
    api_url = 'https://xyz.ag3nts.org/verify'
    client = APIClient(api_url)

    # first request with instance
    payload = client.get_payload("READY", "0")
    text, msg_id = client.get_question(payload)

    if text and msg_id:
        # Generate answer to the question
        response = client.generate_response(text)
        if response:
            # Getting resposne to the question and sending next request
            payload = client.get_payload(response, msg_id)
            answer, msg_id_resp = client.get_question(payload)
            if answer and msg_id_resp:
                print(f'Final answer: {answer}')
            else:
                print(f'Final answer could not be obtained.')
        else:
            print('Answer could not be generated.')
    else:
        print("API failed to respond. ")


if __name__ == "__main__":
    main()