from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .models import Trainer, Moderator

def home(request):
    return render(request, 'trainerapp/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            mylist = request.POST.getlist('make_moderator')
            if mylist:
                m = Moderator(user=request.user, is_moderator=True)
                m.save()

            return redirect('read') 
    else:       
        form = UserCreationForm()
    return render(request, 'trainerapp/signup.html', {'form':form})

def login_user(request):
    errors={}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('read')
        else:
            if not username:
                errors['empty_username'] = 'Please enter username'
            elif not password:
                errors['empty_password'] = 'Please enter password'
            elif user is None:
                errors['invalid'] = 'Username and Password do not match. If you do not have an account sign up.'
    return render(request, 'trainerapp/login.html', errors)

def log_out(request):
    logout(request)
    return redirect('login_user')

def read(request):
    all_trainers = Trainer.objects.order_by("lastname")
    context = {"all_trainers": all_trainers}
    return render(request, "trainerapp/read.html", context)

def create(request):
    errors = {}
    # tr = Trainer.objects.all()
    if request.method == "POST":
        trainer = Trainer()
        trainer.firstname = request.POST["firstname"]
        trainer.lastname = request.POST["lastname"]
        trainer.subject = request.POST["subject"]
        

        if not trainer.firstname:
            errors["empty_firstname"] = "first name can't be null"
        elif not trainer.firstname.isalpha():
            errors["invalid_firstname"] = "first name can't contain numeric characters"
        elif not trainer.lastname:
            errors["empty_lastname"] = "last name can't be null"
        elif not trainer.lastname.isalpha():
            errors["invalid_lastname"] = "lastname can't contain numeric characters"
        elif not trainer.subject:
            errors["empty_subject"] = "subject can't be null"
        elif not trainer.subject.isalpha() or not trainer.subject:
            errors["invalid_subject"] = "subject can't contain numeric characters"
        elif Trainer.objects.filter(firstname = trainer.firstname, lastname = trainer.lastname, subject = trainer.subject).exists():
            errors["already_exists"] = "trainer already exists"
        elif trainer is not None:
            trainer.save()
            context = {"firstname": trainer.firstname, "lastname": trainer.lastname, "subject": trainer.subject}
            return render(request, "trainerapp/create.html", context)
    return render(request, "trainerapp/create.html", errors)

def update(request, id):
    trainerToUpdate = Trainer.objects.get(id=id)
    context = {"trainer" : trainerToUpdate}
    if request.method == "POST":
        newFirstname = request.POST["update_firstname"]
        newLastname = request.POST["update_lastname"]
        newSubject = request.POST["update_subject"]
        
        if request.user.moderator.is_moderator:
            trainerToUpdate.firstname = newFirstname
            trainerToUpdate.lastname = newLastname
            trainerToUpdate.subject = newSubject
            trainerToUpdate.save()

        return redirect('read')

    return render(request, 'trainerapp/update.html', context)


def delete(request, id):
    trainerToDelete = Trainer.objects.get(id=id)
    if request.method == "POST":
        trainerToDelete.delete()
        return redirect('read')
    return render(request,"trainerapp/delete.html")