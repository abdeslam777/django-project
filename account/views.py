from django.shortcuts import render , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def user_profile(request):
    return render(request,'account/user_profile.html')


# def supervisor_profile(request ,supervisor_id):
#     supervisor = get_object_or_404(User, id=supervisor_id, groups__name='Supervisor')
#     return render(request, 'account/supervisor_profile.html', {'supervisor': supervisor,})
# Create your views here.
