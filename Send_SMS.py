
import vonage

def send():
  client = vonage.Client(key="13021f24", secret="26BiHdvLMW1XRWFZ")
  sms = vonage.Sms(client)

  responseData = sms.send_message(
    {
      "from": "Vonage APIs",
      "to": "420737887369",
      "text": "test",
    }
  )

  if responseData["messages"][0]["status"] == "0":
    print("Message sent successfully.")
  else:
    print(f"Message failed with error: {responseData['messages'][0]['error-text']}")


