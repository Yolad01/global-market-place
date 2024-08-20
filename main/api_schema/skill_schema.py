from ninja import ModelSchema, FilterSchema, Schema
from main.models import Skill, UserReview
from .user_schema import UserSchema
from main.utils import options


class GigsSchema(ModelSchema):
    class Meta:
        model = Skill
        fields = "__all__"


class UserReviewSchema(Schema):
    user: UserSchema
    rater: UserSchema
    rating: options.Rate
    comment: str


class CreateUserReviewSchema(Schema):
    user: UserSchema | None = None
    rater: UserSchema
    rating: int
    comment: str



class AverageRatingSchema(Schema):
    average_rating: float
