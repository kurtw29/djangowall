from django.shortcuts import render, HttpResponse, redirect

from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, ("thewall/index.html"))

def wall(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        id=request.session["user_id"]
        themessages = Message.objects.all()

        # print('Messages:', themessages)
        msg=[]
        for x in themessages:
            c = Comment.objects.filter(message=x)
            msgid= x.id
            author_id = x.author_id
            
            u = User.objects.get(id=author_id)
            c = Comment.objects.filter(message=x)
            print("#"*30)
            print(User.objects.filter(messages__id=1).values())
            for g in c:
                n = 
            mix = {
                "id": x.id,
                "messagecontext":x.messagecontext,
                "author_id":x.author_id,
                "created_at":x.created_at,
                "updated_at":x.updated_at,
                "first_name":u.first_name,
                "last_name":u.last_name,
                "comment":c
            }
            msg.append(mix)
            # print(c)
        data={
            'userinfo' : User.objects.get(id=id),
            'msg' : msg
        }
        # print(msg)
        return render(request, "thewall/wall.html", {"data": data} )

def register(request):
    if request.method =="POST":
        errors = User.objects.validator(request.POST)
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']

        EmailExists= User.objects.filter(email=request.POST['email'])
        if not len(EmailExists) == 0:
            print("email exists error")
            messages.error(request, "Email " + request.POST['email'] + " is already registered")
            return redirect('/')

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            pwhashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

            User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pwhashed) 
            messages.success(request, "Successfully added")
            request.session.clear()
            return redirect('/')
    return redirect("/")

def login(request):
    if request.method =="POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email = email)
            if user:
                if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                    id= user.id
                    messages.success(request, "Login Success")
                    request.session['user_id'] = id
                    return redirect('/wall')
                else:
                    messages.error(request, "Login Fail")
                    return redirect("/")
        except:
            messages.error(request, "Login Fail")
            return redirect("/")
    return redirect("/")

def clear(request):
    request.session.clear()
    print("Session Cleared")
    messages.success(request, "Session Cleared")
    return redirect ("/")


def message(request):
    if "user_id" not in request.session:
        return redirect('/')
    else: 
        if request.method == "POST":
            content= request.POST["content"]
            if len(content) == 0:
                messages.error(request, "Message can not be empty you fuck")
                return redirect("/wall")
            else:
                id= request.session['user_id']
                this_author= User.objects.get(id=id)
                Message.objects.create(messagecontext=content, author=this_author)
                return redirect("/wall")

def comment(request,id):
    if "user_id" not in request.session:
        return redirect('/')
    else: 
        if request.method == "POST":
            content= request.POST["content"]
            if len(content) == 0:
                messages.error(request, "Message can not be empty you fuck")
                return redirect("/wall")
            else:
                user_id= request.session['user_id']
                this_message= Message.objects.get(id=id)
                this_user= User.objects.get(id=user_id)
                Comment.objects.create(commentcontext=content, user=this_user, message=this_message)
                return redirect("/wall")