from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth import login, authenticate, logout
from main.forms import (RegistrationForm, JobForm, SkillaProfileForm,
                        ClientProfileForm, CompanyProfileForm, AboutSkillaForm,
                        TrainingAndCertificationForm, ProfilePictureForm, BriefForm,
                        ChatMessageForm, OrderForm, AcceptQuoteForm, BriefAppForm,
                        DeclineQuoteForm, SkillForm, DeleteBriefForm, EditBriefForm,
                        SearchForm, PaymentForm, UserReviewForm, ComplianceForm
                        )

from main.models import ( AboutSkilla, TrainingAndCertification, JobCategory, Job, SkillaProfile,
                         ClientProfile, CompanyProfile, ProfilePicture, Brief,
                         SkillaReachoutToClient, Clients, Order, User,
                         Skill, JobCategory, ContactList, Thread, Message, Payment, Wallet,
                         get_unread_messages_count, UserReview, MessageReadStatus,
                        )

from main.payment import PayStackIt
from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError, OperationalError
from .search import search_brief_title, search_brief_category, search_skill_category, skill_search
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import PasswordResetRequestForm, SetPasswordForm
from django.db.models import Q
from . import functions

from itertools import chain
from operator import attrgetter

# Create your views here.

def home(request):

    job_form = JobForm(request.POST)
    user = request.user

    if user.is_authenticated:
        return redirect("main:skillas_gigs")
    
    if request.method == "POST":
        var = request.POST["var"]
        print(var)
        return redirect("main:skilla_search", param=var)
    return render(request=request, template_name="main/home.html",
                  context={"form": job_form}
                  )

def about(request):
    return render(
        request=request,
        template_name="main/about.html"
    )
    
def terms_condition(request):
    return render(
        request=request,
        template_name="main/terms_condition.html"
    )


def service_policy(request):
    return render(
        request=request,
        template_name="main/skilla/service_policy.html"
    )
    
def frequently_asked_questions(request):
    return render(
        request=request,
        template_name="main/faq.html"
    )

@login_required(login_url="main:sign_in")
def s_identity(request):

    try:
        unread_count = get_unread_messages_count(user)
    except Exception as e:
        unread_count = 0

    user = request.user
    if request.method == "POST":
        house_no = request.POST["house_no"]
        street_name = request.POST["street_name"]
        city_name = request.POST["city_name"]
        region = request.POST["region"]
        country = request.POST["country"]
        zip_code = request.POST["zip_code"]
        
        instance = SkillaProfile.objects.get(user=user)
        instance.country = country
        instance.house_address = house_no
        instance.street_name = street_name
        instance.region = region
        instance.city = city_name
        instance.Postal_code = zip_code
        instance.save()

        return redirect("main:identity_details")
    return render(
        request=request,
        template_name="main/skilla/kyc/s_identity.html",
        context={"unread_count":unread_count,}
    )
    
@login_required(login_url="main:sign_in")
def identity_details(request):

    try:
        unread_count = get_unread_messages_count(user)
    except Exception as e:
        unread_count = 0

    user = request.user
    if request.method == "POST":
        nin = request.POST["nin"]
        id_image = request.FILES["id_image"]
        passport = request.FILES["passport"]

        instance = SkillaProfile.objects.get(user=user)
        instance.nin = nin
        instance.id_card = id_image
        instance.passport_photo = passport
        instance.save()

        return redirect("main:review")
    return render(
        request=request,
        template_name="main/skilla/kyc/identity_details.html",
        context={"unread_count":unread_count,}
        
    )
    

@login_required(login_url="main:sign_in")
def review(request):
    user = request.user

    try:
        unread_count = get_unread_messages_count(user)
    except Exception as e:
        unread_count = 0

    review = SkillaProfile.objects.get(user=user)
    
    return render(
        request=request,
        template_name="main/skilla/kyc/review.html",
        context={
            "review": review,
            "unread_count":unread_count,
        }
    )


@login_required(login_url="main:sign_in")
def compliance(request):
    user = request.user

    try:
        unread_count = get_unread_messages_count(user)
    except Exception as e:
        unread_count = 0

    return render(
        request=request,
        template_name="main/skilla/compliance/compliance.html",
        context={"unread_count":unread_count,}
    )


@login_required(login_url="main:sign_in")
def guide_one(request):
    return render(
        request=request,
        template_name="main/skilla/compliance/guide_one.html"
    )


@login_required(login_url="main:sign_in")
def guide_two(request):
    return render(
        request=request,
        template_name="main/skilla/compliance/guide_two.html"
    )


@login_required(login_url="main:sign_in")
def guide_three(request):
    return render(
        request=request,
        template_name="main/skilla/compliance/guide_three.html"
    )


@login_required(login_url="main:sign_in")
def guide_four(request):
    return render(
        request=request,
        template_name="main/skilla/compliance/guide_four.html"
    )


@login_required(login_url="main:sign_in")
def guide_five(request):
    user = request.user
    if request.method == "POST":
        form = ComplianceForm(request.POST)
        if form.is_valid():
            compliance_form = form.save(commit=False)
            compliance_form.user = user
            compliance_form.save()

    form = ComplianceForm()

    return render(
        request=request,
        template_name="main/skilla/compliance/guide_five.html",
        context={
            "form": form
        }
    )
    


def register(request):
    if request.method == "POST":
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            username = registration_form.cleaned_data["username"]
            password = registration_form.cleaned_data["password1"]
            email = registration_form.cleaned_data["email"]
            user = authenticate(username=username, password=password)
            # wallet, _ = Wallet.objects.create(user=user)

            subject = "Welcome to Skillas. You know what time it is"
            message = f'Hi {username}, we are happy to have you here'
            email_from = settings.EMAIL_HOST_USER
            recipient = [email]
            send_mail_to_user = send_mail(
                subject=subject,
                message=message,
                from_email=email_from,
                recipient_list=recipient
            )

            login(request, user)
            if user.role == "CLIENT":
                ClientProfile.objects.create(user_id=request.user.id)
                send_mail_to_user
                messages.success(request, f"Welcome {username}")
                return redirect("main:client_dashboard")
            elif user.role == "SKILLAS":
                SkillaProfile.objects.create(user_id=request.user.id)
                send_mail_to_user
                messages.success(request, f"Welcome {username}")
                return redirect("main:skillas_dashboard")
        else:
            for field, errors in registration_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    print(error)

        return redirect("main:register")
    registration_form = RegistrationForm()
    return render(request=request, template_name="main/register.html",
                  context={
                        "reg_form": registration_form,
                      })
    



@login_required(login_url="main:sign_in")
def skilla_profile(request):
    try:
        skilla_profile = request.user.skillaprofile
    except SkillaProfile.DoesNotExist:
        skilla_profile = SkillaProfile(user=request.user)
    if request.method == "POST":
        form = SkillaProfileForm(request.POST, instance=skilla_profile)
        if form.is_valid():
            form.save()
            profile = SkillaProfile.objects.get(user=request.user)
            profile.activate_user()
            profile.save()
            messages.success(request, "profile updated successfully")
            return redirect("main:skillas_dashboard")
    
    form = SkillaProfileForm()
    
    return render(
        request=request,
        template_name="main/skilla/skilla_profile.html",
        context={
            "form": form,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )
        


@login_required(login_url="main:sign_in")
def client_profile(request):
    try:
        client_profile = request.user.clientprofile
    except ClientProfile.DoesNotExist:
        client_profile = ClientProfile(user=request.user)
    if request.method == "POST":
        form = ClientProfileForm(request.POST, request.FILES, instance=client_profile)
        if form.is_valid():
            form.save()
            # profile = ClientProfile.objects.get(user=request.user)
            client_profile.activate_user()
            client_profile.save()
            messages.success(request, "Updated Successfully")
            return redirect("main:client_dashboard")
        
    form = ClientProfileForm(instance=client_profile)
    
    return render(
        request=request,
        template_name="main/client/client_profile.html",
        context={
            "form": form,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
        }
    )
    


@login_required(login_url="main:sign_in")
def company_profile(request):
    try:
        company_profile = request.user.companyprofile
    except CompanyProfile.DoesNotExist:
        company_profile = CompanyProfile(user=request.user)
    
    if request.method == "POST":
        form = CompanyProfileForm(request.POST, instance=company_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "profile saved successfully")
            profile = CompanyProfile.objects.get(user=request.user)
            profile.activate_user()
            profile.save()
            return redirect("main:company_dashboard")
    form = CompanyProfileForm()
    
    return render(
        request=request,
        template_name="main/company/company_profile.html",
        context={
            "form": form,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )
    
    

def sign_in(request):
    user = request.user
    if user.is_authenticated:
        return redirect("main:home")
    form = AuthenticationForm(request, data=request.POST)
    if request.method =="POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            print(user)
            if user != None:
                login(request, user)
                if user.role == "CLIENT": 
                    messages.success(request, f"Welcome {username}") 
                    return redirect("main:client_dashboard")
                elif user.role == "SKILLAS":
                    messages.success(request, f"Welcome {username}")
                    return redirect("main:skillas_dashboard")
        else:
            messages.error(request, "Wrong login credentials. Please enter a correct username and password to access your dashboard")

    return render(request=request, template_name="main/sign_in.html",
                    context={"form": form})


@login_required(login_url="main:sign_in")
def client_dashboard(request):
    user = request.user
    try:
        job_categories = JobCategory.objects.all()
        jobs = Job.objects.all()
        profile = ClientProfile.objects.all().filter(user=request.user)
        unread_count = get_unread_messages_count(user)
    except Exception as e:
        pass

    try:
        client_pp = ProfilePicture.objects.get(user=request.user)
    except ProfilePicture.DoesNotExist:
        client_pp = ProfilePicture(user=request.user)

    if request.method == "POST":
        client_pp_form = ProfilePictureForm(request.POST, request.FILES, instance=client_pp)

        if client_pp_form.is_valid():
            client_pp_form.save()
            return redirect("main:client_dashboard")
        
    client_pp_form = ProfilePictureForm()
    
    return render(
            request=request, template_name="main/client/client_dashboard.html",
            context={
                "job_categories": job_categories,
                "jobs": jobs,
                "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
                "profile": profile,
                "profile_pic_form": client_pp_form,
                "client_profile_info": ClientProfile.objects.all().filter(user=request.user),
                "unread_count": unread_count,
            }
        )
    


@login_required(login_url="main:sign_in")
def skilla(request):

    user = request.user
    single_search = None

    user = User.objects.get(username=user.username)

    try:
        wallet, _ = Wallet.objects.get_or_create(user=user)
        unread_count = get_unread_messages_count(user)
        brief = Brief.objects.all().order_by("-title")
        trans_count = Payment().get_skilla_order_count(user=user)
    except Exception as e:
        unread_count = None
        brief = None
        trans_count = None

    if request.method == "POST":
        form = BriefAppForm(request.POST)
        # search_form = SearchForm(request.POST)
        search_input = request.POST.get("search_input")
        if form.is_valid():
            client = form.cleaned_data["client"]
            title = form.cleaned_data["title"]
            # description = form.cleaned_data["description"]
            categories = form.cleaned_data["categories"]
            budget = form.cleaned_data["budget"]
            client = form.cleaned_data["client"]

            get_categories = JobCategory.objects.get(title=categories)
            get_client = Clients.objects.get(username=client)

            reachout = SkillaReachoutToClient(
                user=user,
                title=title,
                # description=description,
                categories=get_categories,
                budget=budget,
                client=get_client
            )
            reachout.save()
            messages.success(request, "Request successfully sent to the client")
            return redirect("main:skillas_dashboard")
        # if search_form.is_valid():
        #     search_input = search_form.cleaned_data["search_input"]
        if search_input:
            return redirect("main:search_results", param=search_input)

    form = BriefAppForm()
    search_form = SearchForm()
    return render(
        request=request, template_name="main/skilla/skillas_dashboard.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
            "brief": brief,
            "form": form,
            # "search_form": search_form,
            "single_search": single_search,
            "unread_count":unread_count,
            "count_of_order": trans_count,
            "wallet": wallet,
        }
    )


@login_required(login_url="main:sign_in")
def company(request):
    return render(
        request=request,
        template_name="main/company/company_dashboard.html"
    )
    


def log_out(request):
    logout(request)
    return redirect("main:home")



@login_required(login_url="main:sign_in")
def s_profile(request):
    user = request.user
    try:
        about_skilla = AboutSkilla.objects.get(user=user)
        unread_count = get_unread_messages_count(user)
        trans_count = Payment().get_skilla_order_count(user=user)
    except (AboutSkilla.DoesNotExist):
        about_skilla = AboutSkilla(user=user)
        unread_count = 0
        trans_count = 0


    try:
        skilla_pp = ProfilePicture.objects.get(user=user)
    except  ProfilePicture.DoesNotExist:
        skilla_pp = None

    if request.method == "POST":
        about_form = AboutSkillaForm(request.POST, instance=about_skilla)
        cert_form =TrainingAndCertificationForm(request.POST)
        skilla_pp_form = ProfilePictureForm(request.POST, request.FILES, instance=skilla_pp)
        
        if about_form.is_valid():
            about_form.save()
            messages.success(request, "Updated successfully")
            return redirect("main:s_profile")

        if skilla_pp_form.is_valid():
            skilla_pp_instance = skilla_pp_form.save(commit=False)
            skilla_pp_instance.user = request.user  # Set the user
            skilla_pp_instance.save()
            messages.success(request, "Profile Picture updated successfully")

        if cert_form.is_valid():
            cert_instance = cert_form.save(commit=False)
            cert_instance.user = request.user
            cert_instance.save()
            messages.success(request, "Info saved successfully")
            return redirect("main:s_profile")
    

    about_form = AboutSkillaForm()
    cert_form = TrainingAndCertificationForm()
    skilla_pp_form = ProfilePictureForm()
    search_form = SearchForm()

    return render(
        request=request,
        template_name="main/skilla/s_profile.html",
        context={
            "profile": SkillaProfile.objects.all().filter(user=request.user),
            "about_skilla": AboutSkilla.objects.all().filter(user=request.user),
            "train_and_cert": TrainingAndCertification.objects.all().filter(user=request.user),
            "about_form": about_form,
            "cert_form": cert_form,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
            "profile_pic_form": skilla_pp_form,
            "search_form": search_form,
            "unread_count":unread_count,
            "count_of_order": trans_count,
        }
    )



@login_required(login_url="main:sign_in")
def wallet(request):
    user = request.user
    wallet, _ = Wallet.objects.get_or_create(user=user)
    try:
        unread_count = get_unread_messages_count(user)
        trans_count = Payment().get_skilla_order_count(user=user)
    except Exception as e:
        unread_count = 0
        trans_count = 0
    
    return render(
        request=request,
        template_name="main/skilla/wallet/wallet.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
            "search_form": SearchForm(),
            "wallet": wallet,
            "unread_count":unread_count,
            "count_of_order": trans_count,
        }
    )



@login_required(login_url="main:sign_in")
def fund_withdrawal(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/fund_withdrawal.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )



@login_required(login_url="main:sign_in")
def continue_to_withdrawal(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/continue_to_withdrawal.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )



@login_required(login_url="main:sign_in")
def create_brief(request):
    if request.method =="POST":
        form = BriefForm(request.POST, request.FILES)
        if form.is_valid():
            brief_form = form.save(commit=False)
            brief_form.user = request.user
            brief_form.save()
            ##### messages
            return redirect("main:view_brief")
            
    form = BriefForm()
    return render(
        request=request,
        template_name="main/client/brief/create_brief.html",
        context={
            "form": form
            
        }
    )
    
    


@login_required(login_url="main:sign_in")
def applications(request):
    skilla_client = SkillaReachoutToClient.objects.all().filter(client=request.user)
    
    return render(
        request=request,
        template_name="main/client/application.html",
        context={
            "skilla_client": skilla_client,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
        }
    )




@login_required(login_url="main:sign_in")
def profile_view(request, pk):

    try:
        skilla = User.objects.get(id=pk)
        user_profile = SkillaProfile.objects.get(user=skilla.id)
        picture = ProfilePicture.objects.get(user=skilla.id)
        trans_count = Payment().get_skilla_order_count(user=skilla.id)
        average_rating, ratings = UserReview().get_rating(user_id=skilla.id)

        view_about_skilla = AboutSkilla.objects.get(user__id=pk)
        view_T_and_cert = TrainingAndCertification.objects.filter(user__id=pk)
        
    except (ObjectDoesNotExist, OperationalError, ProfilePicture.DoesNotExist):
        view_about_skilla = None
        view_T_and_cert = None
        picture = None

        # skilla = None
        # user_profile = None
        # picture = None

        trans_count = None
        average_rating["average_rating"] = 0
        ratings = None

    print(user_profile)
    
    return render(
        request=request,
        template_name="main/client/view_skilla_profile.html",
        context={
            "skilla": skilla,
            "user_profile": user_profile,
            "picture": picture,
            "total_order": trans_count,
            "average_rating": average_rating["average_rating"],
            "ratings":ratings,
            "view_about_skilla": view_about_skilla,
        }
    )



@login_required(login_url="main:sign_in")
def inbox(request):

    user = request.user.id
    inbox = None
    mssg = None
    profile_picture = None

    try:
        mssg_thread = Message.objects.filter(sender=user) ### try except this shit
        
        for msg in mssg_thread:
            mssg: list = []
            mssg.append(msg.text)
    except Message.DoesNotExist:
        mssg_thread = None

    try:
        contact_list = ContactList.objects.get_or_create(user=user)[0]
        inbox = contact_list.contacts.all()
        
        for pic in inbox:
            profile_picture_sec = ProfilePicture.objects.get(user=pic)
        

    except ValueError:
        contact_list = None
        inbox = None
        profile_picture_sec = None
    try:
        profile_picture = ProfilePicture.objects.get(user=user)
        read_messages = MessageReadStatus.objects.all().filter(user=user)

        for message in read_messages:
            MessageReadStatus.objects.get(pk=message.pk)
            message.is_read = True
            message.save()

    except (ProfilePicture.DoesNotExist, MessageReadStatus.DoesNotExist, UnboundLocalError):
        profile_picture = None

    return render(
        request=request,
        template_name="main/messaging/inbox.html",
        context={
            "inbox": inbox,
            "profile_picture": profile_picture,
            'me': user,
            # 'messages': msg,
            "mssg":mssg,
            "profile_picture_sec": profile_picture_sec,
        }
    )


@login_required(login_url="main:sign_in")
def quotes(request):

    user = request.user

    try:
        display_order = Order.objects.filter(
            skilla=user,
        ).order_by("-created_at")
        print(display_order)
    except Exception as e:
        display_order = None

    try:
        unread_count = get_unread_messages_count(user)
        trans_count = Payment().get_skilla_order_count(user=user)
    except Exception as e:
        unread_count = None
        trans_count = None

    return render(
        request=request,
        template_name="main/skilla/quotes_and_orders/sent_quotes.html",
        context={
            "display_order": display_order,
            "search_form": SearchForm(),
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
            "unread_count":unread_count,
            "count_of_order": trans_count,
        }
    )


@login_required(login_url="main:sign_in")
def orders(request):
    user = request.user

    try:
        display_order = Order.objects.all().filter(
            client=user,
        ).order_by("-created_at")
        print(display_order)
    except Exception as e:
        display_order = None

    if request.method == "POST":
        accept_form = AcceptQuoteForm(request.POST)
        decline_form = DeclineQuoteForm(request.POST)
        
        if accept_form.is_valid():
            order_id = accept_form.cleaned_data["form_id"]
            order = Order.objects.get(client=user, id=order_id)
            order.accepted = True
            order.save()
            return redirect("main:orders")
        
        if decline_form.is_valid():
            order_id = decline_form.cleaned_data["form_id"]
            order = Order.objects.get(client=user, id=order_id)
            order.decline = True
            order.save()
            return redirect("main:orders")
        
        order_id = request.POST["mark_order_as_complete"]
        if order_id:
            order = Order.objects.get(id=order_id)
            order.completed = True
            order.save()
            ##### Using session to store data to be used on order page
            skilla = order.skilla.username
            request.session["skilla"] = skilla
            # Using session to store data to be used on order page #####

            user_wallet = Wallet.objects.get(user=order.skilla)
            user_wallet.pending -= order.price
            user_wallet.main += order.price
            user_wallet.save()
            return redirect("main:rate_user")

        
    accept_form = AcceptQuoteForm()
    decline_form = DeclineQuoteForm()
   
    return render(
        request=request,
        template_name="main/client/orders.html",
        context={
            "display_order": display_order,
            "accept_form": accept_form,
            "decline_form": decline_form,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),

        }
    )

@login_required(login_url="main:sign_in")
def create_gigs(request):
    user = request.user
    if request.method =="POST":
        form = SkillForm(request.POST, request.FILES)
        if form.is_valid():
            skill_form = form.save(commit=False)
            skill_form.skilla = user
            skill_form.save()
            return redirect("main:skillas_dashboard")
            
    form = SkillForm()
    return render(
        request=request,
        template_name="main/skilla/create_gigs.html",
        context={
            "form": form
        }
    )


@login_required(login_url="main:sign_in")
def skillas_gigs(request):

    skills = Skill.objects.all()
    paginator = Paginator(skills, 16)

    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_input = search_form.cleaned_data["search_input"]
            print(search_input)
            return redirect("main:skilla_search", param=search_input)
        
    if request.method == "POST":
        var = request.POST["var"]
        return redirect("main:skilla_search", param=var)
    

    search_form = SearchForm()
    
    return render(
        request=request,
        template_name="main/skillas_gigs.html",
        context={
            "page_object": page_object,
            # "skills": skills,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
            "search_form": search_form,
        }
        
    )

@login_required(login_url="main:sign_in")
def skillas_gigs_details(request, id):
    gig = Skill.objects.get(id=id)

    search_form = SearchForm()

    # return redirect("main:skillas_gigs_details", pk=gig)
    return render(
        request=request,
        template_name="main/skilla/skill_detail.html",
        context={
            "gig": gig,
            "search_form": search_form,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
        }
        
    )

@login_required(login_url="main:sign_in")
def view_skills(request):

    try:
        user=request.user
        skills = Skill.objects.all().filter(skilla=user)
        profile_pic = ProfilePicture.objects.get(user=user)
    except (Skill.DoesNotExist, ProfilePicture.DoesNotExist):
        skills = None
        profile_pic = None
    return render(
        request=request,
        template_name="main/skilla/view_skills.html",
        context={
            "skills": skills,
            "profile_pics": profile_pic
        }
        
    )
    
@login_required(login_url="main:sign_in")
def view_brief(request):

    user=request.user
    try:
        brief = Brief.objects.all().filter(user=user).order_by("-date")
        profile_pic = ProfilePicture.objects.get(user=user)
    except ObjectDoesNotExist:
        profile_pic = None

    if request.method == "POST":
        delete_form = DeleteBriefForm(request.POST)
        if delete_form.is_valid():
            form_id = delete_form.cleaned_data.get("delete_brief")
            get_brief = Brief.objects.get(id=form_id)
            get_brief.delete()
            return redirect("main:view_brief")
            
    return render(
        request=request,
        template_name="main/client/brief/view_brief.html",
        context={
            "briefs": brief,
            "profile_pics": profile_pic,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
        }
        
    )
    
@login_required(login_url="main:sign_in")
def edit_brief(request, id):
    user = request.user
    get_object_for_edit = Brief.objects.get(user=user, id=id)
    job_category = JobCategory.objects.all()

    if request.method == "POST":
        form = EditBriefForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            attach_files = form.cleaned_data["attach_files"]
            categories = form.cleaned_data["categories"]
            budget = form.cleaned_data["budget"]
            budget_flexible = form.cleaned_data["budget_flexible"]
            date = form.cleaned_data["date"]
            
            get_object_for_edit.title=title
            get_object_for_edit.description=description
            get_object_for_edit.attach_files=attach_files
            get_object_for_edit.categories=categories
            get_object_for_edit.budget=budget
            get_object_for_edit.budget_flexible=budget_flexible
            get_object_for_edit.date=date
            
            get_object_for_edit.save()

            return redirect("main:view_brief")
        
    form = EditBriefForm()


    return render(
        request=request,
        template_name="main/client/brief/edit_brief.html",
        context={
            "form": form,
            "edit_brief": get_object_for_edit,
            "job_categories": job_category

        }
    )


@login_required(login_url="main:sign_in",)
def thread_view(request, username):
    template_name = 'main/messaging/chat.html'
    mssg = None
    user = request.user
    counterpart = User.objects.get(username=username).id

    display_order = Order.objects.filter(
        skilla=user, client=counterpart
    ).order_by("-created_at")

    message_receiver = User.objects.get(username=username)

    try:
        contact_list = ContactList.objects.get_or_create(user=user)[0]
        inbox = contact_list.contacts.all()

        for pic in inbox:
            profile_picture_sec = ProfilePicture.objects.get(user=pic)

    except ValueError:
        contact_list = None
        inbox = None
        profile_picture_sec = None

    other_user = get_object_or_404(get_user_model(), username=username)

    try:
        add_to_contacts, _ = ContactList.objects.get_or_create(user=user)
        add_to_other_contact, _ = ContactList.objects.get_or_create(user=other_user)

        add_to_other_contact.add_contact(user)
        add_to_contacts.add_contact(other_user)

    except IntegrityError:
        pass

    thread = Thread.objects.get_or_create_personal_thread(user, other_user)
    if thread is None:
        raise Http404

    messages = thread.message_set.all()

    display_order = Order.objects.filter(
        (Q(skilla=user) & Q(client=counterpart)) | (Q(skilla=counterpart) & Q(client=user))
    ).order_by("-created_at")

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        order_form = OrderForm(request.POST)
        if form.is_valid():
            # Save the message
            text = form.cleaned_data["msg_body"]
            Message.objects.create(sender=user, thread=thread, text=text)
            return redirect('main:chat', username=other_user.username)

        if order_form.is_valid():
            order_form = order_form.save(commit=False)
            order_form.skilla = user
            order_form.client = message_receiver
            # order_form.paid = False
            order_form.save()

    mssg_thread = Message.objects.filter(sender=user)
    
    for msg in mssg_thread:
        mssg: list = []
        mssg.append(msg.text)

    form = ChatMessageForm()
    order_form = OrderForm()

    context = {
        'user': user,
        'thread': thread,
        'other_user': other_user,
        'messages': messages,
        'form': form,
        "order_form": order_form,
        "inbox": inbox,
        "display_order": display_order,
        "profile_picture_sec": profile_picture_sec,
        "mssg":mssg,
        # "combined_data": combined_data
    }
    return render(request, template_name, context=context)

@login_required(login_url="main:sign_in")
def search_results(request, param):
    user = request.user
    single_search = param
    single_search = search_brief_title(Brief, single_search) or search_brief_category(Brief, single_search)

    try:
        unread_count = get_unread_messages_count(user)
        trans_count = Payment().get_skilla_order_count(user=user)
    except Exception as e:
        unread_count = None
        trans_count = None

    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_input = search_form.cleaned_data["search_input"]

            single_search = search_brief_title(Brief, search_input) or search_brief_category(Brief, search_input)
            print(single_search)
    
    search_form = SearchForm()
    return render(
        request=request, template_name="main/search.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
            "single_search": single_search,
            "search_form": search_form,
            "unread_count":unread_count,
            "count_of_order": trans_count,
        }
    )

@login_required(login_url="main:sign_in")
def skilla_search(request, param):

    single_search = param
    print(single_search)
    skilla = skill_search(Skill, single_search) or search_skill_category(Skill, single_search)

    paginator = Paginator(skilla, 12)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_input = search_form.cleaned_data["search_input"]
            print(search_input)
            skilla = skill_search(Skill, search_input)
            print(skilla)

    search_form = SearchForm()
    return render(
        request=request, template_name="main/skilla_search.html",
        context={
            "search_form": search_form,
            "page_object": page_object,
        }
    )



def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(
                    reverse("main:password_reset_confirm", kwargs={"uidb64": uid, "token": token})
                )
                send_mail(
                    "Password Reset Request",
                    f"Use the link below to reset your password:\n{reset_link}",
                    # settings.EMAIL_HOST_USER,
                    "admin@example.com",
                    [user.email],
                    fail_silently=False,
                )
                return redirect("main:password_reset_done")
    else:
        form = PasswordResetRequestForm()

    return render(request, template_name="main/password_reset_request.html", context={"form": form})


def password_reset_confirm(request, uidb64=None, token=None):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                password_1 = form.cleaned_data["new_password1"]
                user.set_password(password_1)
                user.save()

                return redirect("main:password_reset_complete")
        else:
            form = SetPasswordForm()
    else:
        form = None

    return render(request, template_name="main/password_reset_confirm.html", context={"form": form})



def password_reset_done(request):
    return render(request, template_name="main/password_reset_done.html")



def password_reset_complete(request):
    return render(request, template_name="main/password_reset_complete.html")



def make_payment(request, order_no, price):
    user = request.user
    order = Order.objects.get(order_no=order_no)
    try:
        skilla_img = ProfilePicture.objects.get(user=order.skilla)
    except ProfilePicture.DoesNotExist:
        skilla_img = None
    # print(skilla_img)
    # print(price)

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            send_fund = PayStackIt(
                api_key=settings.PAYSTACK_API_KEY,
                callback_url="http://127.0.0.1:8000/success_page"
            )

            send_fund.pay(email=user.email, amount=amount)

            payment, _ = Payment.objects.get_or_create(
                user=user,
                email=user.email,
                amount=amount,
                pending=amount,
                reference=send_fund.reference_code,
                skilla=order.skilla,
                skilla_image=skilla_img.image,
                order_no=order_no
            )
            return redirect(send_fund.authorization_url)

    form = PaymentForm()
    return render(
        request=request,
        template_name="main/payment/make_payment.html",
        context={
            "form": form,
            "price": price
        }
    )


def payment_success(request):
    user = request.user
    payment = Payment.objects.filter(user=user).last()
    verify = PayStackIt(
        api_key=settings.PAYSTACK_API_KEY,
        callback_url="http://127.0.0.1:8000/success_page",
        on_cancel_url="http://127.0.0.1:8000/success_page"
    )
    verify.verify_transaction(payment.reference)
    # print(json.dumps(verify, indent=3))
    timestamp = verify.time_of_payment
    timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    payment.status = verify.status
    payment.message = verify.message
    payment.time_of_payment = timestamp
    payment.card_type = verify.card_type
    payment.channel = verify.payment_channel
    if verify.status == "success":
        payment.completed = True
    payment.save()
    ##### Marking order as paid
    order = Order.objects.get(order_no=payment.order_no)
    order.paid = True
    order.save()
    ##### Adding to user pending balance
    user_wallet = functions.user_wallet(payment.skilla)
    
    return render(
        request=request,
        template_name="main/skilla/wallet/success_page.html",
        context={
        }
    )


@login_required(login_url="main:sign_in")
def paid_order_history(request):
    user = request.user
    payment = Payment.objects.filter(user=user).order_by("-pk")

    paginator = Paginator(payment, 5)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    try:
        profile_pic = ProfilePicture.objects.all().filter(user=request.user)
        user_profile_pic =  ProfilePicture.objects.get(user=request.user)
    except ObjectDoesNotExist:
        profile_pic = None
        user_profile_pic = None

    return render(
        request=request,
        template_name="main/client/paid_order_history.html",
        context={
            "profile_pic": profile_pic,
            "user_profile_pic": user_profile_pic,
            # "payment": payment,
            "payment": page_object,
        }
    )


@login_required(login_url="main:sign_in")
def rate_user(request):
    user = request.user.id
    skilla = request.session.get("skilla")
    try:
        skilla = User.objects.get(username=skilla)
        user_profile = SkillaProfile.objects.get(user=skilla.id)
        picture = ProfilePicture.objects.get(user=skilla.id)
        trans_count = Payment().get_skilla_order_count(user=skilla.id)
        average_rating, ratings = UserReview().get_rating(user_id=skilla.id)
    except (SkillaProfile.DoesNotExist, Payment.DoesNotExist, UserReview.DoesNotExist, User.DoesNotExist):
        skilla = None
        user_profile = None
        picture = None
        trans_count = 0
        average_rating = None
        ratings = 0
        


    form = UserReviewForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user_review = form.save(commit=False)
            user_review.user = skilla
            user_review.rater = request.user
            user_review.save()
            return redirect("main:orders")
        
    return render(
        request=request,
        template_name="main/rate_user.html",
        context={
            "skilla": skilla,
            "user_profile": user_profile,
            "picture": picture,
            "total_order": trans_count,
            "average_rating": average_rating["average_rating"],
            "ratings":ratings,
            "form": form,
        }
    )

@login_required(login_url="main:sign_in")
def manage_gigs(request):

    search_form = SearchForm()
    return render(
        request=request,
        template_name="main/skilla/manage_gigs.html",
        context={
            "search_form": search_form,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
        }
    )
