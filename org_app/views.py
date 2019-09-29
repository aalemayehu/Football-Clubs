from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    errorsFromModelsValidator = User.objects.registration_validator(request.POST)
    if len(errorsFromModelsValidator) > 0:
        for key, value in errorsFromModelsValidator.items():
            messages.error(request, value)
        return redirect ('/main')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user=User.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'], email = request.POST['email'], password=hash1.decode() )
        request.session['id'] = user.id # Where Session ID was saved. 
    return redirect('/groups')

def login(request):
    errorsFromLoginValidator = User.objects.login_validator(request.POST)
    if len(errorsFromLoginValidator)>0:
        for key, value in errorsFromLoginValidator.items():
            messages.error(request, value)
        return redirect('/main')
    user = User.objects.filter(email = request.POST['email'])[0]
    request.session ['id']= User.objects.filter(email = request.POST['email'])[0].id
    return redirect('/groups')

def groups(request):
    loggedinuser = User.objects.get(id= request.session['id'])
    context = {
        'loggedinuser' : User.objects.get(id= request.session['id']),
        'all_groups' : Group.objects.all()
    }
    return render(request,'groups.html',context)

def addgroups(request):
    errorsFromGroupValidator = Group.objects.group_validator(request.POST)
    if len(errorsFromGroupValidator)>0:
        for key, value in errorsFromGroupValidator.items():
            messages.error(request, value)
        return redirect('/groups')
    loggedinuser = User.objects.get(id= request.session['id'])
    my_group = Group.objects.create(name = request.POST['name'],description=request.POST['description'], creator=loggedinuser)
    my_group.joiners.add(loggedinuser)
    return redirect('/groups')

def delete(request,group_id):
    group_to_delete =Group.objects.get(id=group_id)
    group_to_delete.delete()
    return redirect('/groups')

def showgroup(request, group_id):
    loggedinuser = User.objects.get(id= request.session['id'])
    context = {
        'loggedinuser' : User.objects.get(id= request.session['id']),
        'my_group' : Group.objects.filter(joiners=loggedinuser),
        'this_group' : Group.objects.get(id=group_id),
        'order_groups': Group.objects.all().order_by("count")
    }
    return render(request,'showgroups.html',context)

def joingroup(request,group_id):
    loggedinuser = User.objects.get(id= request.session['id'])
    group_to_join = Group.objects.get(id=group_id)
    group_to_join.joiners.add(loggedinuser)

    return redirect ('/groups')

def leavegroup (request,group_id):
    group_to_leave =Group.objects.get(id=group_id)
    loggedinuser = User.objects.get(id= request.session['id'])
    group_to_leave.joiners.remove(loggedinuser)
    return redirect('/groups')

def logout(request):
    request.session.clear()
    return redirect('/main')