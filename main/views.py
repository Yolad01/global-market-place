from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth import login, authenticate, logout
from main.forms import (RegistrationForm, JobForm, SkillaProfileForm,
                        ClientProfileForm, CompanyProfileForm, AboutSkillaForm,
                        TrainingAndCertificationForm, ProfilePictureForm, BriefForm,
                        ChatMessageForm, OrderForm, AcceptQuoteForm, BriefAppForm,
                        DeclineQuoteForm, SkillForm, DeleteBriefForm, EditBriefForm,
                        SearchForm
                        )

from main.models import ( AboutSkilla, TrainingAndCertification, JobCategory, Job, SkillaProfile,
                         ClientProfile, CompanyProfile, ProfilePicture, Brief,
                         SkillaReachoutToClient, Clients, User, Order,
                         Skill, JobCategory, ContactList, Thread, Message
                        )
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views import View
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Max
from .search import search_brief_title, search_brief_category
from .functions import msg_count, orders_count
from django.core.paginator import Paginator


# Create your views here.



def home(request):
    job_form = JobForm(request.POST)
    user = request.user
    if user.is_authenticated:
        return redirect("main:skillas_gigs")
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


def register(request):
    if request.method == "POST":
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            username = registration_form.cleaned_data["username"]
            password = registration_form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            if user.role == "CLIENT":
                ClientProfile.objects.create(user_id=request.user.id)
                messages.success(request, f"Logged in as {username}")
                return redirect("main:client_profile")
            elif user.role == "SKILLAS":
                SkillaProfile.objects.create(user_id=request.user.id)
                messages.success(request, f"Logged in as {username}")
                return redirect("main:skilla_profile")
            elif user.role == "COMPANY":
                messages.success(request, f"Logged in as {username}")
                return redirect("main:company_profile")
        messages.error(request,
                        "Your password should not be less than 8 characters. the characters should include an uppercase, lowercase a symbol and a number."
                        )
        # return redirect("main:register")
    registration_form = RegistrationForm()
    return render(request=request, template_name="main/register.html",
                  context={
                        "reg_form": registration_form,
                      })
    


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
            if user != None:
                login(request, user)
                if user.role == "CLIENT": 
                    messages.success(request, f"Logged in as {username}") 
                    return redirect("main:client_dashboard")
                elif user.role == "SKILLAS":
                    messages.success(request, f"Logged in as {username}")
                    return redirect("main:skillas_dashboard")
        else:
            messages.error(request, "Wrong login credentials. Please enter a correct username and password to access your dashboard")
            # return redirect("main:sign_in")

            
    return render(request=request, template_name="main/sign_in.html",
                    context={"form": form})


@login_required
def client_dashboard(request):
    job_categories = JobCategory.objects.all()
    jobs = Job.objects.all()
    profile = ClientProfile.objects.all().filter(user=request.user)

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
                "client_profile_info": ClientProfile.objects.all().filter(user=request.user)
            }
        )
    

#### add @login_required decorator
@login_required
def skilla(request):

    user = request.user
    single_search = None

    count_of_message = msg_count(model=Thread, user=user)
    count_of_order = orders_count(Order, user)
    brief = Brief.objects.all().order_by("-title")

    if request.method == "POST":
        form = BriefAppForm(request.POST)
        search_form = SearchForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data["client"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            categories = form.cleaned_data["categories"]
            budget = form.cleaned_data["budget"]
            client = form.cleaned_data["client"]

            get_categories = JobCategory.objects.get(title=categories)
            get_client = Clients.objects.get(username=client)

            reachout = SkillaReachoutToClient(
                user=user,
                title=title,
                description=description,
                categories=get_categories,
                budget=budget,
                client=get_client
            )
            reachout.save()
            messages.success(request, "Request successfully sent to the client")
            return redirect("main:skillas_dashboard")
        if search_form.is_valid():
            search_input = search_form.cleaned_data["search_input"]
            # single_search = search_brief_title(Brief, search_input) or search_brief_category(Brief, search_input)
            # print(single_search)
            # print(type(single_search))
            return redirect("main:search_results", param=search_input)



    form = BriefAppForm()
    search_form = SearchForm()
    return render(
        request=request, template_name="main/skilla/skillas_dashboard.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
            "brief": brief,
            "form": form,
            "search_form": search_form,
            "single_search": single_search,
            "count":count_of_message,
            "count_of_order": count_of_order
        }
    )




#### add @login_required decorator
def company(request):
    return render(
        request=request,
        template_name="main/company/company_dashboard.html"
    )
    



def log_out(request):
    logout(request)
    return redirect("main:home")



def s_profile(request):
    try:
        about_skilla = AboutSkilla.objects.get(user=request.user)
        skilla_pp = ProfilePicture.objects.get(user=request.user)
    except (AboutSkilla.DoesNotExist, ProfilePicture.DoesNotExist):
        about_skilla = AboutSkilla(user=request.user)
        skilla_pp = ProfilePicture(user=request.user)

    if request.method == "POST":
        about_form = AboutSkillaForm(request.POST, instance=about_skilla)
        cert_form =TrainingAndCertificationForm(request.POST)
        skilla_pp_form = ProfilePictureForm(request.POST, request.FILES, instance=skilla_pp)
        
        if about_form.is_valid():
            about_form.save()
            messages.success(request, "Updated successfully")
            return redirect("main:s_profile")

        if skilla_pp_form.is_valid():
            skilla_pp_form.save() ## skilla__pp == skilla profile picture
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
            "profile_pic_form": skilla_pp_form
        }
    )



def wallet(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/wallet.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )



def fund_withdrawal(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/fund_withdrawal.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )



def continue_to_withdrawal(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/continue_to_withdrawal.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )


def withdraw_success(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/success_page.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )
    
    
def create_brief(request):
    if request.method =="POST":
        form = BriefForm(request.POST, request.FILES)
        if form.is_valid():
            brief_form = form.save(commit=False)
            brief_form.user = request.user
            brief_form.save()
            ##### messages
            return redirect("main:client_dashboard")
            
    form = BriefForm()
    return render(
        request=request,
        template_name="main/client/brief/create_brief.html",
        context={
            "form": form
            
        }
    )
    
    
def applications(request):
    skilla_client = SkillaReachoutToClient.objects.all().filter(client=request.user)
    
    return render(
        request=request,
        template_name="main/client/application.html",
        context={
            "skilla_client": skilla_client
        }
    )



def profile_view(request, pk): #Use the id for the querries or make the username foreignkey or unique
    view_profile = SkillaProfile.objects.get(user__id=pk)
    view_profile_picture = ProfilePicture.objects.get(user__id=pk)
    view_about_skilla = AboutSkilla.objects.get(user__id=pk)
    view_T_and_cert = TrainingAndCertification.objects.filter(user__id=pk)
    skilla = User.objects.get(id=pk)
    
    return render(
        request=request,
        template_name="main/client/view_skilla_profile.html",
        context={
            "view_profile": view_profile,
            "view_profile_picture": view_profile_picture,
            "view_about_skilla": view_about_skilla,
            "view_T_and_cert": view_T_and_cert,
            "skilla": skilla
        }
    )




def inbox(request):
    user = request.user.id
    inbox = None
    profile_picture = None

    try:
        contact_list = ContactList.objects.get_or_create(user=user)[0]
        inbox = contact_list.contacts.all()
    except ValueError:
        pass
    # except UnboundLocalError:
    #     pass
    

    msg = Message.objects.all().filter(sender=user)

    try:
        profile_picture = ProfilePicture.objects.get(
            user=user
        )
    except ProfilePicture.DoesNotExist:
        pass

    return render(
        request=request,
        template_name="main/messaging/inbox.html",
        context={
            "inbox": inbox,
            "profile_picture": profile_picture,
            'me': user,
            'messages': msg,
        }
    )




def quotes(request):

    user = request.user

    display_order = Order.objects.filter(
        skilla=user,
    ).order_by("-order_created")

    return render(
        request=request,
        template_name="main/skilla/quotes_and_orders/sent_quotes.html",
        context={
            "display_order": display_order,
        }
    )



def orders(request):
    user = request.user.id

    display_order = Order.objects.all().filter(
        client=user,
    ).order_by("-order_created")

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
        
        
    accept_form = AcceptQuoteForm()
    decline_form = DeclineQuoteForm()
    
    return render(
        request=request,
        template_name="main/client/orders.html",
        context={
            "display_order": display_order,
            "accept_form": accept_form,
            "decline_form": decline_form
        }
    )


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


def skillas_gigs(request):

    search_form = SearchForm()
    skills = Skill.objects.all()
    paginator = Paginator(skills, 12)

    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    return render(
        request=request,
        template_name="main/skillas_gigs.html",
        context={
            "page_object": page_object,
            # "skills": skills,
            "search_form": search_form
        }
        
    )


def skillas_gigs_details(request, id):
    gig = Skill.objects.get(id=id)

    # return redirect("main:skillas_gigs_details", pk=gig)
    return render(
        request=request,
        template_name="main/skilla/skill_detail.html",
        context={
            "gig": gig
        }
        
    )


def view_skills(request):

    user=request.user
    skills = Skill.objects.all().filter(skilla=user)
    profile_pic = ProfilePicture.objects.get(user=user)
    return render(
        request=request,
        template_name="main/skilla/view_skills.html",
        context={
            "skills": skills,
            "profile_pics": profile_pic
        }
        
    )
    
    
def view_brief(request):

    user=request.user
    brief = Brief.objects.all().filter(user=user).order_by("-date")
    profile_pic = ProfilePicture.objects.get(user=user)

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
            "profile_pics": profile_pic
        }
        
    )
    

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



def thread_view(request, username):
    template_name = 'main/messaging/chat.html'

    user = request.user
    message_receiver = User.objects.get(username=username)

    profile_picture = ProfilePicture.objects.get(user=user)

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

    form = ChatMessageForm()
    order_form = OrderForm()

    context = {
        'me': user,
        'thread': thread,
        'user': other_user,
        'messages': messages,
        'form': form,
        "order_form": order_form
    }
    return render(request, template_name, context=context)



def search_results(request, param):

    single_search = param
    single_search = search_brief_title(Brief, single_search) or search_brief_category(Brief, single_search)

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
        }
    )