from django.shortcuts import render, redirect
from datetime import datetime, date
from mysite.forms import LoginForm, StudentProfileForm, EmployeeProfileForm, AddFriendForm
from mysite.models import Person, Student, Employee, Message

def welcome(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if 'newMessage' in request.GET and request.GET['newMessage'] != '':
            newMessage = Message(author = logged_user, content = request.GET['newMessage'], publication_date = date.today())
            newMessage.save()
        friendMessages = Message.objects.filter(author__friends = logged_user).order_by('-publication_date')
        return render(request, 'welcome.html', { 'logged_user' : logged_user, 'friendMessages': friendMessages })
    else:
        return redirect('/login')

def login(request):
    if len(request.POST) > 0:
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            logged_user = Person.objects.get(email = user_email)
            request.session['logged_user_id'] = logged_user.id
            return redirect('/welcome')
        else:
            return render(request, 'login.html', { 'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', { 'form': form })

def register(request):
    if len(request.GET) > 0 and 'profileType' in request.GET:
        studentForm = StudentProfileForm(prefix='st')
        employeeForm = EmployeeProfileForm(prefix='em')
        if request.GET['profileType'] == 'student':
            studentForm = StudentProfileForm(request.GET, prefix='st')
            if studentForm.is_valid():
                studentForm.save()
                return redirect('/login')
        elif request.GET['profileType'] == 'employee':
            employeeForm = EmployeeProfileForm(request.GET, prefix='em')
            if employeeForm.is_valid():
                employeeForm.save()
                return redirect('/login')
        return render(request, 'user_profile.html', {'studentForm': studentForm, 'employeeForm': employeeForm})
    else: 
        studentForm = StudentProfileForm(prefix='st')
        employeeForm = EmployeeProfileForm(prefix='em')
        return render(request, 'user_profile.html', {'studentForm': studentForm, 'employeeForm': employeeForm})

def get_logged_user_from_request(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']
        if len(Student.objects.filter(id=logged_user_id)) == 1:
            return Student.objects.get(id= logged_user_id)
        elif len(Employee.objects.filter(id=logged_user_id)) == 1:
            return Employee.objects.get(id= logged_user_id)
        else:
            return None
    else:
        return None

def add_friend(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if len(request.GET) > 0:
            form = AddFriendForm(request.GET)
            if form.is_valid():
                new_friend_email = form.cleaned_data['email']
                newFriend = Person.objects.filter(email = new_friend_email)
                logged_user.friends.add(newFriend)
                logged_user.save()
                return redirect('/welcome')
            else: 
                return render(request, 'add_friend.html',{ 'form': form })
        else:
            form = AddFriendForm()
            return render(request, 'add_friend.html', { 'form': form})
    else:
        return redirect('/login')

def show_profile(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if 'userToShow' in request.GET and request.GET['userToShow'] != '':
            user_to_show_id = int(request.GET['userToShow'])
            results = Person.objects.filter(id=user_to_show_id)
            if len(results) == 1:
                if Student.objects.filter(id=user_to_show_id):
                    user_to_show = Student.objects.filter(id=user_to_show_id)
                else:
                    user_to_show = Employee.objects.get(id=user_to_show_id)
                return render(request, 'show_profile.html', {'user_to_show': user_to_show})
            else:
                return render(request, 'show_profile.html', {'user_to_show': logged_user})
        else:
            return render(request, 'show_profile.html', {'user_to_show': logged_user})
    else:
        return redirect('/login') 