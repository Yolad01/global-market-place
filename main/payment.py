import requests
import json



class PayStackIt:
    authorization_url = ""
    trans_total_url="https://api.paystack.co/transaction/totals"
    
    def __init__(
            self,
            email: str,
            amount: int,
            api_key: str,    
    ):
        self.SECRET_KEY = api_key
        self.email = email
        self.amount = amount * 100


    def pay(self) -> dict:
        """Returns a dictionary object"""
        url_initialize = "https://api.paystack.co/transaction/initialize"
        self.headers = {
            "Authorization": f'Bearer {self.SECRET_KEY}',
            "Content-Type": "application/json"
        }
        self.data = {"email": self.email, "amount": self.amount}
        self.response = requests.post(
            url=url_initialize,
            headers=self.headers,
            json=self.data
        )
        self.response = dict(self.response.json())
        self.status = self.response["status"]
        self.message = self.response["message"]
        self.authorization_url = self.response["data"]["authorization_url"]
        self.access_code = self.response["data"]["access_code"]
        # self.reference_code = self.response["data"]["reference"]

        return {
            "status": self.status,
            "message": self.message,
            "authorization_url": self.authorization_url,
            "access_code": self.access_code
        }
    
    def verify_transaction(self, reference_code):
        self.verify_transaction = f'https://api.paystack.co/transaction/verify/{reference_code}'