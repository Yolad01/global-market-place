import requests
import json



class PayStackIt:
    authorization_url: str = ""
    reference_code: str = ""
    status: str = ""
    message: str = ""
    access_code: str = ""
    time_of_payment: str = ""
    card_type: str = ""
    payment_channel: str = ""



    trans_total_url="https://api.paystack.co/transaction/totals"
    
    def __init__(
            self,
            api_key: str,
            callback_url: str = None,
            on_cancel_url: str = None
    ):
        self.SECRET_KEY = api_key
        self.callback_url = callback_url
        self.on_cancel_url = on_cancel_url
        self.headers = {
            "Authorization": f'Bearer {self.SECRET_KEY}',
            "Content-Type": "application/json"
        }


    def pay(self, amount: int, email: str):
        """Returns a dictionary object."""
        self.email = email
        self.amount = amount * 100
        url_initialize = "https://api.paystack.co/transaction/initialize"
        self.headers = self.headers
        self.data = {
            "email": self.email,
            "amount": self.amount,
            "callback_url": self.callback_url,
            "metadata": {
            "cancel_action": self.on_cancel_url
        }

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
    

    def verify_transaction(self, reference_code) -> dict:
        self.transaction_verification_url = f'https://api.paystack.co/transaction/verify/{reference_code}'
        self.headers = self.headers
        self.response = requests.get(
            url=self.transaction_verification_url,
            headers=self.headers,
        )
        self.response = self.response.json()

        self.status = self.response["data"]["status"]
        self.message = self.response["message"]
        self.time_of_payment = self.response["data"]["paid_at"]
        self.card_type = self.response["data"]["authorization"]["card_type"]
        self.payment_channel = self.response["data"]["channel"]

        return None
    
    

    def refund(self, reference_code: str):
        self.refund_url ="https://api.paystack.co/refund"
        self.reference_code = reference_code
        self.data = {
            "transaction": self.reference_code,
        }
        self.response = requests.post(
            url=self.refund_url,
            headers=self.headers,
            json=self.data
        )
        if self.response.status_code == 200:
            return self.response.json()
        else:
            return None

    






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