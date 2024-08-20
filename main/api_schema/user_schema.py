from ninja import Schema, ModelSchema, Form
from main.models import (
    User, Wallet, SkillaProfile, ProfilePicture, Message, MessageReadStatus, TrackingModel,
    Thread
)


class UserSchema(ModelSchema):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["password", "user_permissions"]


class LoginSchema(Schema):
    username: Form[str]
    password: Form[str]


class NotFoundError(Schema):
    message: str


class WalletSchema(ModelSchema):
    class Meta:
        model = Wallet
        fields = "__all__"


class SkillaProfileSchema(ModelSchema):
    class Meta:
        model = SkillaProfile
        exclude = [
            "nin",
            "id_card",
            "passport_photo"
        ]
    

class ProfilePictureSchema(ModelSchema):
    class Meta:
        model = ProfilePicture
        fields = "__all__"



class MessageSchema(ModelSchema):
    class Meta:
        model = Message
        exclude = ["id"]
