import requests
import json



class PayStackIt:
    authorization_url: str = ""
    reference_code: str = ""
    status: bool
    message: str = ""
    access_code: str = ""

    trans_total_url="https://api.paystack.co/transaction/totals"
    
    def __init__(
            self,
            email: str,
            amount: int,
            api_key: str,
            callback_url: str = None
    ):
        self.SECRET_KEY = api_key
        self.email = email
        self.amount = amount * 100
        self.callback_url = callback_url

    def pay(self):
        """Returns a dictionary object."""
        url_initialize = "https://api.paystack.co/transaction/initialize"
        self.headers = {
            "Authorization": f'Bearer {self.SECRET_KEY}',
            "Content-Type": "application/json"
        }
        self.data = {
            "email": self.email,
            "amount": self.amount,
            "callback_url": self.callback_url
        }
        self.response = requests.post(
            url=url_initialize,
            headers=self.headers,
            json=self.data
        )
        self.response = self.response.json()

        self.authorization_url = self.response["data"]["authorization_url"]
        self.reference_code = self.response["data"]["reference"]
        self.message = self.response["message"]
        self.status =  self.response["status"]
        self.access_code = self.response["data"]["access_code"]

        return None
    
    def verify_transaction(self, reference_code):
        self.transaction_verification_url = f'https://api.paystack.co/transaction/verify/{reference_code}'
        self.response = requests.get(
            url=self.transaction_verification_url,
            headers=self.headers,
        )
        return self.response.json()
    






    #  return {
    #         "status": self.status,
    #         "message": self.message,
    #         "authorization_url": self.authorization_url,
    #         "access_code": self.access_code,
    #         "reference_code": self.reference_code,
    #         "full_response": self.response
    #     }


        # self.status = self.response["status"]
        # self.message = self.response["message"]
        # self.authorization_url = self.response["data"]["authorization_url"]
        # self.access_code = self.response["data"]["access_code"]
        # self.reference_code = self.response["data"]["reference"]