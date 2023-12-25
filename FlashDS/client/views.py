# Using Python Libraries in Django
import stripe
import requests
import firebase_admin
from firebase_admin import credentials, auth, messaging
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from FlashDS.client import forms
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from FlashDS.models import Request,Transaction,Courier
#stripe_Api_key
stripe.api_key = settings.STRIPE_API_SECRET_KEY
# Create your views here.
cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIAL)
firebase_admin.initialize_app(cred)
# -------------------------------------------------------------------------------------
@login_required()
def home(request):
    return redirect(reverse('client:profile'))
# -------------------------------------------------------------------------------------
# client Profile
@login_required(login_url="/sign-in/?next=/client/")
def client_profile(request):
    # function for changing profile information
    # ----------------------------------------------------
    change_pass_form = PasswordChangeForm(request.user)
    client_form = forms.clientForm(instance=request.user)
    Profile_Pic_Form = forms.ClientCustomForm(instance=request.user.client)
    if request.method == "POST":
        # if action is update information
        # run this function
        if request.POST.get('action') == 'update_information':
            # update first&lastname form
            client_form = forms.clientForm(request.POST, instance=request.user)
            # update profile picture form
            Profile_Pic_Form = forms.ClientCustomForm(
                request.POST, request.FILES, instance=request.user.client,)
            if client_form.is_valid():
                client_form.save()
                Profile_Pic_Form.save()
                messages.success(request, 'Profile Updated Successfully')
                return redirect(reverse('client:profile'))
# function for changing profile information
# ---------------------------------------------------
        elif request.POST.get('action') == 'update_user_password':
            # if action is update Password
            # run this function
            change_pass_form = PasswordChangeForm(request.user, request.POST)
            if change_pass_form.is_valid():
                user = change_pass_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password Updated Successfully')
                return redirect(reverse('client:profile'))
# if action is update phone
# run this function
        elif request.POST.get('action') == 'update_user_phone':
            firebase_user = auth.verify_id_token(request.POST.get('id_token'))
            request.user.client.phone_number = firebase_user['phone_number']
            request.user.client.save()
            return redirect(reverse('client:profile'))
    context = {
        'client_form': client_form,
        'Profile_Pic_Form': Profile_Pic_Form,
        'change_pass_form': change_pass_form
    }
    return render(request, 'client/profile.html', context)
# ------------------------------------------------------------------------------------
@login_required(login_url="/sign-in/?next=/client/")
def client_Payment(request):
    current_client = request.user.client
    #changing current card
    if request.method == "POST":
        stripe.PaymentMethod.detach(current_client.stripe_payment_id)
        current_client.stripe_payment_id = ""
        current_client.stripe_card_last_octet = ""
        current_client.save()
        return redirect(reverse('client:payment.html'))
    # Check if the current client has a Stripe ID
    if not current_client.stripe_client_id:
    # If not, create a new Stripe customer and save the ID to the client model
        client = stripe.Customer.create()
        current_client.stripe_client_id = client['id']
        current_client.save()
    # Get the payment methods associated with the current client
    payment_method = stripe.PaymentMethod.list(
        customer=current_client.stripe_client_id,
        type="card",
    )
    # Update the client model with payment information if a payment method is available
    if payment_method and len(payment_method.data) > 0:
        payment_method = payment_method.data[0]
        current_client.stripe_payment_id = payment_method.id
        current_client.stripe_card_last_octet = payment_method.card.last4
        current_client.save()
    else:
        # If no payment method is available, clear the payment information
        current_client.stripe_payment_id = ""
        current_client.stripe_card_last_octet = ""
        current_client.save()
    # Create a SetupIntent for setting up future payments
    if not current_client.stripe_payment_id:  
        intent = stripe.SetupIntent.create(
            customer=current_client.stripe_client_id
        )
        # Prepare context data for rendering the payment.html template
        context = {
            "client_secret": intent.client_secret,
            "STRIPE_API_PUBLISH_KEY": settings.STRIPE_API_PUBLISH_KEY,
        }
        # Render the payment.html template with the context data
        return render(request,'client/payment.html',context)
    else:
        return render(request,'client/payment.html')
# -------------------------------------------------------------------------------------
@login_required(login_url="/sign-in/?next=/client/")
def job_request(request):
    current_image = Request.objects.all()
    current_client = request.user.client
    if not request.user.client.stripe_payment_id:
        return redirect(reverse('client:payment'))
    has_current_task = Request.objects.filter(
        client = current_client,
        status__in = [
            Request.PROCESSING_STATUS,
            Request.DELIVERING_STATUS,
            Request.PICKING_STATUS,  
        ]
    ).exists()
    if has_current_task:
        messages.warning(request,'You still have a processing Tasks')
        return redirect(reverse('client:current_task'))
    creating_request = Request.objects.filter(client=current_client,status=Request.CREATING_STATUS).last()
    # This line retrieves the last request in the creating status associated with the current client.
    request_form_1 = forms.Create_Request_form_1(instance=creating_request)
    request_form_2 = forms.Create_Request_form_2(instance=creating_request)
    request_form_3 = forms.Create_Request_form_3(instance=creating_request)
    #The form is initialized with the instance of the creating request. This allows the form to be pre-filled with the existing data if it exists
    if request.method == "POST":
        #Handling the form submission
#step 1--------------
        if request.POST.get('step') == '1':
            request_form_1 = forms.Create_Request_form_1(request.POST,request.FILES, instance=creating_request)
            if request_form_1.is_valid():
                creating_request = request_form_1.save(commit=False)
                creating_request.client = current_client
                creating_request.save()
                return redirect (reverse('client:job_request'))
#step 2--------------
        elif request.POST.get('step') == '2':
            request_form_2 = forms.Create_Request_form_2(request.POST,instance=creating_request)
            if request_form_2.is_valid():
                creating_request = request_form_2.save()
                return redirect (reverse('client:job_request'))
# step 3 ------------
        elif request.POST.get('step') == '3':
            request_form_3 = forms.Create_Request_form_3(request.POST,instance=creating_request)
            if request_form_3.is_valid():
                creating_request = request_form_3.save()
                try:
                    Req = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&mode=transit&key={}".format( 
                        creating_request.pickup_address,
                        creating_request.delivery_address,
                        settings.GOOGLE_MAP_API_KEY,
                    ))
                    print(Req.json()['rows'])
                    distance = Req.json()['rows'][0]['elements'][0]['distance']['value']
                    duration = Req.json()['rows'][0]['elements'][0]['duration']['value']
                    creating_request.distance = round(distance/1000,2)
                    creating_request.duration = int(duration/60)
                    #per 5el per km
                    creating_request.price = round(creating_request.distance * 5, 2) 
                    creating_request.save()
                except Exception as statement :
                    print(statement)
                    messages.error(request,"We are sorry this Area out of Zone Of our Shipping")
                return redirect (reverse('client:job_request'))
# Step 4
        elif request.POST.get('step') == '4':
            if creating_request.price:
                try:
                    payment_intent = stripe.PaymentIntent.create(
                        amount=int(round(creating_request.price * 100)),
                        currency='EGP',
                        # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
                        customer = current_client.stripe_client_id,
                        payment_method= current_client.stripe_payment_id,
                        off_session=True,
                        confirm=True,
                    )

                    Transaction.objects.create(
                        stripe_request_payment_id = payment_intent['id'],
                        task_request = creating_request,
                        payment_amount = creating_request.price,
                    )

                    creating_request.status  = Request.PROCESSING_STATUS
                    creating_request.save()
                    # Notifications
                    courier = Courier.objects.all()
                    register_tokens = [i.fcm_token for i in courier if i.fcm_token]
                    message = messaging.MulticastMessage(
                        notification=messaging.Notification(
                            title=creating_request.name,
                            body=creating_request.description,
                        ),
                        webpush=messaging.WebpushConfig(
                            notification=messaging.WebpushNotification(
                                icon=creating_request.picture.url,  
                            ),
                            fcm_options=messaging.WebpushFCMOptions(
                                link=settings.NOTIFICATION_URL + reverse('courier:available_task'),
                            ),
                        ),
                        tokens=register_tokens  
                    )
                    response = messaging.send_multicast(message)
                    print('{0} messages delivered successfully'.format(response.success_count))
                    messages.success(request,'Your Payment has been added Sucssefuly')
                    return redirect(reverse('client:home'))
                except stripe.error.CardError as e:
                    err = e.error
                    # Error code will be authentication_required if authentication is needed
                    print("Code is: %s" % err.code)
                    payment_intent_id = err.payment_intent['id']
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
# Check the steps
    if not creating_request:
        current_step = 1
    elif creating_request.delivery_name:
        current_step = 4
    elif creating_request.pickup_name:
        current_step = 3
    else:
        current_step = 2
    context = {
        'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY,
        'request_form_1':request_form_1,
        'request_form_2':request_form_2,
        'request_form_3':request_form_3,
        'creating_request':creating_request,
        'current_image':current_image,
        'current_step':current_step,
    }
    return render(request,'client/job_request.html',context)
# ---------------------------------------------------------------------------------
@login_required(login_url="/sign-in/?next=/client/")
def current_task(request):
    task_status = Request.objects.filter(
        client = request.user.client,
        status__in=[
            Request.PROCESSING_STATUS,
            Request.PICKING_STATUS,
            Request.DELIVERING_STATUS,
        ]
    )
    context = {
        "task_status":task_status,
    }
    return render(request,'client/task.html',context)
# -----------------------------------------------------------------------------------
@login_required(login_url="/sign-in/?next=/client/")
def done_task(request):
    task_status = Request.objects.filter(
        client = request.user.client,
        status__in=[
            Request.COMPLETED_STATUS,
            Request.CANCELED_STATUS,
        ]
    )
    context = {
        "task_status":task_status,
    }
    return render(request,'client/task.html',context)
#-----------------------------------------------------------------------------------
@login_required(login_url="/sign-in/?next=/client/")
def task_info(request,task_id):
    task_status = Request.objects.get(id=task_id)
    if request.method == "POST" and task_status.status == task_status.PROCESSING_STATUS:
        task_status.status = task_status.CANCELED_STATUS
        task_status.save()
        messages.success(request,'Your Task has been Canceled Sucssefuly')
        return redirect(reverse('client:done_task'))
    context ={
        "task_status":task_status,
        "GOOGLE_MAP_API_KEY":settings.GOOGLE_MAP_API_KEY,

    }
    return render(request,'client/task_info.html',context)