from ninja import Schema, ModelSchema, Form
from main.models import BlogCategory, BlogPost
from .user_schema import UserSchema
from datetime import datetime



class BlogCategorySchema(ModelSchema):
    class Meta:
        model = BlogCategory
        fields = "__all__"


class BlogPostSchema(Schema):
    id: int
    title: str
    content: str
    author: UserSchema
    category: BlogCategorySchema


class CreateBlogPostSchema(Schema):
    title: Form[str]
    content: Form[str]