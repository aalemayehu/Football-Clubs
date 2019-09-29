from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def registration_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['fname']) < 2:
            errors["fname"] = "Name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "Name should be at least 2 characters"
        if len(postData['email']) <1:#email
            errors['emailBlank'] = 'Email is required'
        usersWithEmail = User.objects.filter(email=postData['email'])
        if len(usersWithEmail)>0:#email
            errors['emailTaken'] = "Email is taken already" 
        if not EMAIL_REGEX.match(postData['email']):#email
            errors['emailPattern'] = ('Invalid email address!')
        if len(postData['password']) < 8:
            errors['passwordlength'] = 'Password must be at least 8 characters'
        print(errors)
        return errors
    def login_validator(self, postData):
        usersWithEmail = User.objects.filter(email=postData['email'])
        print('printing usersWithEmail below:')
        print(usersWithEmail)
        errors = {}
        if len(postData['email'])<1:
            errors['emailrequired'] = 'You must enter email'
        if len(postData['password'])<1:
            errors['passwordrequired'] = 'You must enter password'
        if len(usersWithEmail)<1:
            errors['emailnotregisterd'] = 'Email not registered'
        else:
            user = usersWithEmail[0]
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print("password match")
            else:
                print("failed password")
                errors['passwordincorrect']='Password not correct'
        return errors
class GroupManager(models.Manager):
    def group_validator(self, postData):
        errors = {}
        if len(postData['name'])<5:
            errors['OrgnameRequired'] = 'You must enter a proper Org Name with 5 characters minimum'
        if len(postData['description'])<10:
            errors['description'] = 'You must enter a description 10 or more characters long'
        print(errors)
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    creator = models.ForeignKey(User,related_name='groups_created', on_delete=models.CASCADE, null=True)
    joiners = models.ManyToManyField(User, related_name="groups_joined")
    objects = GroupManager()