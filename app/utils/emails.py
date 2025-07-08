from mailjet_rest import Client
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("MAILJET_API_KEY")
api_secret = os.getenv("MAILJET_SECRET_KEY")
sender_email = os.getenv("MAILJET_SENDER_EMAIL")
sender_name = os.getenv("MAILJET_SENDER_NAME")

mailjet = Client(auth=(api_key, api_secret), version = 'v3.1')
def send_email(subject : str , to: str, body: str):
        data = {
            'Messages': [
                {
                    "From": {
                        "Email" : sender_email,
                        "Name": sender_name
                    },
                    "To": [
                        {
                            "Email": to,
                            "Name" : to.split("@")[0]
                        }
                    ],

                        "Subject": subject,
                        "HTMLPart" : body
                }
            ]

          
        }

        result = mailjet.send.create(data = data)
        if result.status_code != 200:
            print(" Erreur d'envoi :" , result.status_code , result.json())
        else:
            print(f"Email envoyé à {to}")
