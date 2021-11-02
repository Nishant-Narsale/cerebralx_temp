from django.shortcuts import redirect, render
from rest_framework import viewsets
from .models import Blog
from .serializers import BlogSerializer
from django.contrib import messages
from .models import MailchimpEmail


# Create your views here.
def index(request):
    return render(request,'index.html')

# Blog Api
class BlogViewset(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()


#Subscription code
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError


# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID

def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))


def subscription(request):
    if request.method == "POST":
        email = request.POST['email']
        em , created = MailchimpEmail.objects.get_or_create(email=email)
        messages.success(request, "Email received. thank You! ")
        subscribe(email)
        return redirect('api:index')

    return redirect('api:index')
