from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^.*(?=.{4,10})(?=.*[a-z]).*$')


class Manager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) == 0 :
            errors['first_name']= "First name must not be empty"
        if len(postData['first_name']) > 255 :
            errors['first_name']= "Course name can not be more than 255 characters"

        if len(postData['last_name']) == 0 :
            errors['last_name']= "Last name must not be empty"
        if len(postData['last_name']) > 255 :
            errors['last_name']= "Last name can not be more than 255 characters"
        
        if len(postData['email']) == 0 :
            errors['email']= "Email must not be empty"
        if len(postData['email']) > 255 :
            errors['email']= "Email can not be more than 255 characters"

        if len(postData['password']) < 8 :
            errors['password']= "Password must be at least 8 characters"
        if len(postData['password']) > 255 :
            errors['password']= "Password can not be more than 255 characters"
        elif not postData['password'] == postData['confirmpassword']:
            errors['password']= "Password does not match with the confirmation"
        elif not PW_REGEX.match(postData['password']):             
            errors['password']= "Need at least one number and one capital letter for the password"   
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = Manager()

class Message(models.Model):
    messagecontext = models.TextField()
    author = models.ForeignKey(User, related_name="messages")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    commentcontext = models.TextField()
    user = models.ForeignKey(User, related_name="usercomments")
    message = models.ForeignKey(Message, related_name="messagecomments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

