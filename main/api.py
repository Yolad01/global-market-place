from django.http import HttpRequest
from ninja import Query
from ninja_extra import (
    NinjaExtraAPI, api_controller, http_delete, http_get, http_post, permissions, route, pagination, status,
    ControllerBase
)
from ninja.security import HttpBearer
from ninja.constants import NOT_SET

from .api_schema.user_schema import MessageSchema, UserSchema, NotFoundError, WalletSchema, SkillaProfileSchema, CreateMessageSchema
from .api_schema.brief_schema import BriefSchema
from .api_schema.skill_schema import GigsSchema, UserReviewSchema, CreateUserReviewSchema
from .api_schema.business_schema import OrderSchema, CreateOrderSchema
from .api_schema.blog_schema import BlogCategorySchema, BlogPostSchema, CreateBlogPostSchema

from .models import (
    Thread, User, Wallet, Brief, Skill, JobCategory, AboutSkilla, ProfilePicture, UserReview,
    SkillaProfile, ClientProfile, Order, SkillaReachoutToClient, Payment, Message, ContactList,
    BlogCategory, BlogPost
)
from django.contrib.auth import authenticate, login, logout
from ninja.errors import HttpError
#jwt auth imports
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth

from django.shortcuts import render, redirect, get_object_or_404, Http404
from . import search


# class AuthBearer(HttpBearer):
#     def authenticate(self, request, token):
#         try:
#             user = User.objects.get(auth_token=token)
#             return user
#         except User.DoesNotExist:
#             raise HttpError(401, "Invalid token")
        

api = NinjaExtraAPI(title="SKillaApi", description="By Yolad Global Services Limited")


@api_controller("/users", tags=["Users"], permissions=[], auth=JWTAuth())
class UserPath:
   
    @route.get("/", response=list[UserSchema])
    def get_users(self, request):
        print(request.user.id)
        return User.objects.all()


    @route.get("/user", response={200: UserSchema, 404: NotFoundError})
    def get_user(self, request):
        user = request.user
        try:
            user = User.objects.get(id=user.id)
            return user
        except User.DoesNotExist as e:
            return 404, {"message": "User not found"}
        



@api_controller("/skilla", tags=["Skilla"])
class Skilla:

    @route.get("/view-briefs", response={200: list[BriefSchema], 404: NotFoundError})
    def get_briefs(self, request):
        user = request.user
        try:
            brief = Brief.objects.all()
            return brief
        except Brief.DoesNotExist as e:
            return 404, {"message": "User not found"}
        

    @route.get("/wallet", response={200: WalletSchema, 404: NotFoundError}, auth=JWTAuth())
    def get_wallet(self, request):
        user = request.user
        try:
            wallet = Wallet.objects.get(user=user)
            return wallet
        except Wallet.DoesNotExist as e:
            return 404, {"message": "User not found"}
        

    @route.get("/user_gigs", response={200: list[GigsSchema], 404: NotFoundError}, auth=JWTAuth())
    def get_user_gigs(self, request):
        user = request.user
        try:
            gigs = Skill.objects.all().filter(skilla=user)
            return gigs
        except Skill.DoesNotExist as e:
            return 404, {"message": "User does not match any skill"}

    
    @route.get("/all_gigs", response={200: list[GigsSchema], 404: NotFoundError})
    def get_all_gigs(self):
        try:
            gigs = Skill.objects.all()
            return gigs
        except Skill.DoesNotExist as e:
            return 404, {"message": "Search came up empty"}
        

    @route.get("/profile", response={200: SkillaProfileSchema, 400: NotFoundError}, auth=JWTAuth())
    def get_user_profile(self, request):
        user = request.user
        try:
            profile = SkillaProfile.objects.get(user=user)
            return profile
        except SkillaProfile.DoesNotExist as e:
            return 400, {"message": "No profile found"}
        
    




@api_controller("/quote", tags=["Quote"])
class Quote:

    @http_get("/", auth=JWTAuth(), response={200: pagination.PaginatedResponseSchema[OrderSchema], 404: NotFoundError})
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=10)
    def get_quotes(self, request):
        user = request.user
        try:
            quotes = Order.objects.filter(skilla=user).order_by("-order_created")
            return quotes
        except Order.DoesNotExist as e:
            return 400, {"message": "No orders found"}

        
    @http_post("/create", auth=JWTAuth(), response={200: OrderSchema, 404: NotFoundError})
    def create_order(self, request, client, payload: CreateOrderSchema):
        user = request.user
        client = User.objects.get(username=client)
        try:
            quote = Order.objects.create(
                skilla=user,
                client=client,
                gig_desc=payload.gig_desc,
                delivery=payload.delivery,
                price=payload.price
            )
            return quote
        except Order.DoesNotExist as e:
            return 404, {"message": "error creating the user. Check your payload"}



@api_controller("/ratings", tags=["Ratings"])
class Rating:

    @http_get("/", response={200: list[UserReviewSchema], 401: NotFoundError}, auth=JWTAuth())
    def get_ratings(self, request, skilla: int | None = None):
        user = request.user
        user_id: int = user.id
        try:
            if skilla:
                reviews = UserReview.objects.filter(user=skilla)
                return reviews
            else:
                reviews = UserReview.objects.filter(rater=user_id)
            return reviews
        except UserReview.DoesNotExist as e:
            return 401, {"message": "No ratings found"}
        

    @http_post("/rate", response={200: list[UserReviewSchema], 401: NotFoundError}, auth=JWTAuth())
    def rate_user(self, request, rate: CreateUserReviewSchema):
        user = request.user
        try:
            create_rating = UserReview.objects.create(
                user=user.id,
                rater=rate.rater,
                rating=rate.rating,
                comment=rate.comment
            )
            return create_rating
        except Exception as e:
            return 401, {"message": "Nothing to return"}


#### create apis for getting messages
@api_controller("/messages", tags=["messages"])
class Messages:

    @http_get("/chats", auth=JWTAuth(), response={200: list[MessageSchema], 401: NotFoundError})
    def view_chats(self, request, user_counterpart: int):
        user = request.user
        try:
            messages = Message.get_messages_between_users(user1=user, user2=user_counterpart)
            return messages
        except Message.DoesNotExist as e:
            return 401, {"message": "No messages found"}
        

    @http_post("/create", auth=JWTAuth(), response={200: MessageSchema, 401: NotFoundError})
    def create_message(self, request, mssg_reciever: int, payload: CreateMessageSchema):
        user = request.user
        if mssg_reciever:
            mssg_reciever = User.objects.get(id=mssg_reciever)

        try:
            user_contacts, _ = ContactList.objects.get_or_create(user=user)
            mssg_reciever_contact, _ = ContactList.objects.get_or_create(user=mssg_reciever)

            user_contacts.add_contact(mssg_reciever)
            mssg_reciever_contact.add_contact(user)
        except Exception as e:
            pass

        thread = Thread.objects.get_or_create_personal_thread(user, mssg_reciever)
        if thread is None:
            raise Http404
        # messages = thread.message_set.all()

        try:
            mssg_created = Message.objects.create(
                sender=user,
                thread=thread,
                text=payload.text
            )
            return 200, mssg_created
        except Exception as e:
            return 401, {"message": "Nothing to create"}


#### Create api for the users message contact
@api_controller("/contact", tags=["Contacts"])
class Contacts:
    
    @http_get("/", auth=JWTAuth(), response=list[UserSchema])
    def get_contacts(self, request):
        user = request.user
        contact_list = ContactList.objects.get_or_create(user=user)[0]
        contact_list = contact_list.contacts.all()
        return contact_list
    


#### create apis for searching for users
@api_controller("/search", tags=["Search"])
class Search:
    
    @route.post("/user", response={200: UserSchema, 404: NotFoundError})
    def search_user(self, request, user_id: int):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist as e:
            return 404, {"message": "User not found"}
        

    @route.post("/gigs", response={200: list[GigsSchema], 404: NotFoundError})
    def search_gigs(self, keyword):
        try:
            skill = search.skill_search(Skill, keyword)
            return skill
        except Skill.DoesNotExist as e:
            return 404, {"message": "gigs matching query not found"}
        

    @route.post("/buyers_requests", response={200: list[BriefSchema], 404: NotFoundError})
    def search_buyers_requests(self, keyword):
        try:
            briefs = search.search_brief_title(Brief, keyword)
            return briefs
        except Brief.DoesNotExist as e:
            return 404, {"message": "brief matching query not found"}
        


#### Create the Blog APIs
@api_controller("/blogs", tags=["Blog"])
class Blogs:

    @http_get("", response={200: pagination.PaginatedResponseSchema[BlogPostSchema], 401: NotFoundError})
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=10)
    def get_blogs(self, author_id: int | None = None):
        if not author_id:
            try:
                blog_post = BlogPost.objects.all()
                return blog_post
            except BlogPost.DoesNotExist as e:
                return 401, {"message": "No blog post found"}
        else:
            try:
                author = User.objects.get(id=author_id)
                blog_post = BlogPost.objects.filter(author=author)
                return blog_post
            except BlogPost.DoesNotExist as err:
                return 401, {"message": "Nothing to see here"}
                
    
    
    @http_get("/get_blog_category", response={200: pagination.PaginatedResponseSchema[BlogCategorySchema], 401: NotFoundError})
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=10)
    def get_blogs_category(self):
        try:
            category = BlogCategory.objects.all()
            return category
        except BlogPost.DoesNotExist as e:
            return 401, {"message": "No blog post found"}


    @http_post("/create_blog", response={200: BlogPostSchema, 401: NotFoundError}, auth=JWTAuth())
    def create_blog(self, request, category_id: int, payload: CreateBlogPostSchema):
        user = request.user
        try:
            category = BlogCategory.objects.get(id=category_id)
            blog_post = BlogPost.objects.create(
                title=payload.title,
                content=payload.content,
                author=user,
                category=category
            )
            return blog_post
        except BlogCategory.DoesNotExist as e:
            return 401, {"message": "This is not a blog category"}
        
    @http_delete("/delete", auth=JWTAuth())
    def delete_blog(self, blog_id: int, request):
        # user = request.user
        try:
            blog = BlogPost.objects.get(id=blog_id)
            blog.delete()
            return {"message": "Blog deleted"}
        except BlogCategory.DoesNotExist as err:
            return 401, {"message": "Nothing to delete here"}


            
        




api.register_controllers(
    UserPath,
    NinjaJWTDefaultController,
    Skilla,
    Quote,
    Rating,
    Messages,
    Contacts,
    Search,
    Blogs,
)

