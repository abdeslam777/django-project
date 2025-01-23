from django.shortcuts import render , get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect 
from django.contrib import messages
from .models import Offer ,OfferApplication 
from .forms import OfferApplicationForm , OfferForm 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , authenticate ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group



def is_supervisor(user):
    return user.groups.filter(name='Supervisor').exists()

def is_student(user):
    return user.groups.filter(name='Student').exists()

def loginPage(request):
    # if request.user.is_authenticated:
    #     return redirect('offer')
    page ='login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'user does not exist !!' )
        
        user = authenticate(request, username=username , password=password)
        if user is not None:
            login(request,user)
            return redirect('offer')
        else:
            messages.error(request,'username OR password does not exist !!' )

    context = {'page': page}
    return render(request, 'auth/login.html',context)


def logoutUser(request):
    return redirect('login')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            student_group, created = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
            login(request,user)
            return redirect('login')
        else:
            messages.error(request,'an error accured during registration')
    return render(request,'auth/login.html',{'form': form})

def home(request):
    return render(request,'offer/home.html')

@login_required(login_url='login')
def offer(request):
    return render(request,'offer/offer.html')


@login_required(login_url='login')
def offer_list(request):
    # Determine the user's role
    supervisor_mode = is_supervisor(request.user)
    student_mode = is_student(request.user)

    if supervisor_mode:
        # Supervisors should see only the offers they created
        offers = Offer.objects.filter(supervisor=request.user.username).order_by('-created_at')
        count_offer = offers.filter(is_active=True).count()
        nbrOfferClosed = offers.filter(is_active=False).count()
    elif student_mode:
        # Students should see only active offers
        offers = Offer.objects.filter(is_active=True).order_by('-created_at')
        count_offer = offers.count()  # Total active offers
        nbrOfferClosed = 0  # Students don't see closed offers
    else:
        # If the user is neither a supervisor nor a student, deny access
        offers = Offer.objects.all().order_by('-created_at')  # Empty queryset
        count_offer = offers.filter(is_active=True).count()
        nbrOfferClosed = offers.filter(is_active=False).count()

    # Apply search filters if a query is provided
    query = request.GET.get('q', '')
    if query:
        offers = offers.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(supervisor__icontains=query) |
            Q(skills_required__icontains=query)
        )

    filtered_offer_count = offers.count()

    # Split skills into a list for each offer
    for offer in offers:
        offer.skills_list = offer.skills_required.split(',')

    return render(request, 'offer/offer_list.html', {
        'offers': offers,
        'count_offer': count_offer,
        'nbrOfferClosed': nbrOfferClosed,
        'filtered_offer_count': filtered_offer_count,
        'query': query,
        'supervisor_mode': supervisor_mode,  # Indicates supervisor role
        'student_mode': student_mode,        # Indicates student role
    })

# def offer_list(request):
#     offers = Offer.objects.all().order_by('-created_at')
#     for offer in offers:
#         # Split skills into a list
#         offer.skills_list = offer.skills_required.split(',')
#     count_offer=Offer.objects.filter(is_active=True).count()
#     nbrOfferClosed = Offer.objects.filter(is_active=False).count()
#     return render(request,'offer/offer_list.html',{'offers':offers ,'count_offer':count_offer ,'nbrOfferClosed':nbrOfferClosed})



# def offer_detail(request , pk):
#     offer = get_object_or_404(offer , pk=pk)
#     return render(request,'offer/offer_detail.html', {'offer': offer})
@login_required(login_url='login')
def offer_detail(request, pk):
    try:
        offer = Offer.objects.get(pk=pk)  # Fetch the offer based on the primary key
    except Offer.DoesNotExist:
        return render(request, '404.html')  # Optional custom 404 page
    return render(request, 'offer/offer_detail.html', {'offer': offer})




# def apply_offer(request, pk):
#     offer = get_object_or_404(Offer, pk=pk)

#     if request.method == 'POST':
#         form = OfferApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             application = form.save(commit=False)
#             application.offer = offer  # Link the application to the offer
#             application.save()
#             return redirect('offer_list')
#             # return HttpResponseRedirect('/success/')  # Redirect to a success page
#     else:
#         form = OfferApplicationForm()

#     return render(request, 'offer/apply_offer.html', {'form': form, 'offer': offer})



@login_required(login_url='login')
def create_offer(request):
    form = OfferForm()
    if request.method =='POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('offer_list')
    context = {'form': form}
    return render(request, 'offer/offer_form.html',context)

@login_required(login_url='login')
def update_offer(request, pk):
    offer = Offer.objects.get(id=pk)
    form = OfferForm(instance=offer)
    if request.method =='POST':
        form = OfferForm(request.POST,instance=offer)
        if form.is_valid():
            form.save()
            return redirect('offer_list')
    context = {'form': form}
    return render(request,'offer/update_offer.html',context)

@login_required(login_url='login')
def delete_offer(request ,pk):
    offer = Offer.objects.get(id=pk)
    if request.method == "POST":
        offer.delete()
        return redirect('offer_list')
    return render(request, 'offer/confirm_delete.html', {'offer': offer})


@login_required(login_url='login')
def application_list(request):
    # Determine the user's role
    supervisor_mode = is_supervisor(request.user)
    student_mode = is_student(request.user)

    if supervisor_mode:
        # Supervisors should see applications for their posted offers
        applications = OfferApplication.objects.filter(offer__supervisor=request.user.username).order_by('-applied_at')
    elif student_mode:
        # Students should see only their own applications
        applications = OfferApplication.objects.filter(email=request.user.email).order_by('-applied_at')
    else:
        # If the user is neither a supervisor nor a student, deny access
        applications = OfferApplication.objects.all().order_by('-applied_at')  # Empty queryset

    return render(request, 'offer/application_list.html', {
        'applications': applications,
        'supervisor_mode': supervisor_mode,  # Indicates supervisor role
        'student_mode': student_mode,        # Indicates student role
    })

# def application_list(request):

#     if request.user.groups.filter(name="Student").exists():
#         # For students: show offers they've applied to
#         applications = OfferApplication.objects.filter(student=request.user)
#     elif request.user.groups.filter(name="Supervisor").exists():
#         # For supervisors: show applications to their offers
#         applications = OfferApplication.objects.filter(offer__supervisor=request.user)
#     else:
#         applications = None  # Default if no role matches

#     return render(request, 'offer/application_list.html', {
#         'applications': applications,
#     })

    # if offer_id:
    #     applications = OfferApplication.objects.filter(offer_id=offer_id)
    # else:
    #     applications = OfferApplication.objects.all().order_by('-applied_at')
    # return render(request, 'offer/application_list.html', {'applications': applications})


@login_required(login_url='login')
def apply_offer(request, pk):
    # Fetch the offer object based on the primary key
    offer = get_object_or_404(Offer, pk=pk)

    if request.method == 'POST':
        form = OfferApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.offer = offer
            application.save()
            return redirect('offer_list')
    else:
        form = OfferApplicationForm()

    return render(request, 'offer/apply_offer.html', {'form': form, 'offer': offer})



# @login_required
# def view_watchlist(request):
#     watchlist_offers = request.user.user_watchlist.all()
#     return render(request, 'offer/offer_watchlist.html', {'watchlist_offers': watchlist_offers})


# @login_required
# def add_to_watchlist(request, offer_id):
#     offer = get_object_or_404(Offer, id=offer_id)
#     if offer in request.user.user_watchlist.all():
#         messages.info(request, "This offer is already in your watchlist.")
#     else:
#         request.user.watchlist.add(offer)
#         messages.success(request, f"Offer '{offer.title}' has been added to your watchlist.")
#     return redirect('offer_list')  # Redirect to the offer list or desired page

# def remove_from_watchlist(request,watchlist_id):
#     watchlist_entry = get_object_or_404(Watchlist, user=request.user, id=watchlist_id)
#     watchlist_entry.delete()
#     return redirect('watchlist-page')



# def submissions_view(request):
#     # Get all applications for the logged-in student
#     applications = OfferApplication.objects.all()

#     context = {
#         'applications': applications
#     }
#     return render(request, 'submissions.html', context)


# def change_status(request, pk):
#     application = get_object_or_404(Application, pk=pk)
    
#     if request.method == 'POST':
#         status = request.POST.get('status')
#         if status in ['pending', 'accepted', 'rejected']:
#             application.status = status
#             application.save()
#             return redirect('submissions')  # or redirect to an admin view
#     return render(request, 'change_status.html', {'application': application})



# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Automatically log in the user after registration
#             messages.success(request, 'Registration successful! You are now logged in.')
#             return redirect('offer_list')  # Redirect to the offers list
#     else:
#         form = UserCreationForm()
    
#     return render(request, 'auth/register.html', {'form': form})