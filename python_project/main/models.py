from django.db import models
from django.db.models import Model
from datetime import datetime, date
import re

# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        NAME_REGEX = re.compile(r'^[a-zA-Z]')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')
        
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name needs at least 2 characters.'
        if not NAME_REGEX.match(post_data['first_name']):
            errors['first_name_char'] = 'First name should contain only letters'
            
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name needs at least 2 characters.'
        if not NAME_REGEX.match(post_data['last_name']):
            errors['last_name_char'] = 'Last name should contain only letters'
            
        if len(post_data['email']) < 8:
            errors['email_length'] = "Email too short!!"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['invalid_email'] = "Invalid email! Try again!"            
        
        if len(post_data['password']) < 8:
            errors['pass_length'] = "Password needs to be 8 characters"
        if post_data['password'] != post_data['confirm_password']:
            errors['invalid_password'] = "Password and confirm doesn't match!"
        
        if len(post_data['street_address']) < 2:
            errors['street_address'] = 'Your address needs at least 2 characters.'
        
        if len(post_data['city']) < 2:
            errors['city'] = "Please enter your city address."

        if len(post_data['state']) < 2:
            errors['state'] = "Please enter your state."

        if len(post_data['zip_code']) < 4:
            errors['zip_code'] = "Please enter your 5 digit zip code."
            
        if len(post_data['phone']) > 0 and len(post_data['phone']) < 10:
            errors['phone'] = 'Please enter your phone number with the area code.'
        if len(post_data['phone']) > 0 and not PHONE_REGEX.match(post_data['phone']):
            errors['invalid_phone'] = 'Please enter valid phone number.'
        return errors

    def login_validation(self, post_data):
        errors = {}
        NAME_REGEX = re.compile(r'^[a-zA-Z]')
        PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['invalid_email'] = 'Invalid email! Try Again!'
        return errors

    def project_validation(self, post_data):
        errors={}
        if len(post_data['title']) < 2:
            errors['title'] = 'Title needs at least 2 characters.'
        if not post_data['class']:
            errors['class'] = 'Please include a class.'
        if post_data['due_date'] < date.today().strftime("%Y-%m-%d"):
            errors['due_date'] = "Deadline cannot be in the past"
        return errors
    
    def class_validation(self, post_data):
        errors={}
        if len(post_data['subject']) < 2:
            errors['subject'] = 'Subject needs at least 2 characters.'
        if not post_data['schedule_day']:
            errors['schedule_day'] = 'Please include a day for class to be held.'
        if not post_data['schedule_time']:
            errors['schedule_day'] = 'Please include a time for class to be held.'
        return errors
    
    def update_class_validation(self, post_data):
        errors={}
        NAME_REGEX = re.compile(r'^[a-zA-Z]')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')
        if post_data['subject'] and len(post_data['subject']) < 2:
            errors['subject'] = 'Subject needs at least 2 characters.'
        return errors

    def edit_account_validation(self, post_data):
        errors={}
        NAME_REGEX = re.compile(r'^[a-zA-Z]')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')
        if len(post_data['first_name']) != 0 and len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name needs at least 2 characters.'
        if len(post_data['first_name']) != 0 and not NAME_REGEX.match(post_data['first_name']):
            errors['first_name_char'] = 'First name should contain only letters'
        
        if len(post_data['last_name']) != 0 and len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name needs at least 2 characters.'
        if len(post_data['last_name']) != 0 and not NAME_REGEX.match(post_data['last_name']):
            errors['last_name_char'] = 'Last name should contain only letters'
        
        if len(post_data['email']) != 0 and not EMAIL_REGEX.match(post_data['email']):
            errors['invalid_email'] = 'Invalid email! Try Again!'
        
        if len(post_data['password']) != 0 and len(post_data['password']) < 8:
            errors['password_length'] = 'Passwords need at least 8 characters.'
        if post_data['password'] != post_data['confirm_password']:
            errors['invalid_password'] = 'Password does not match with Confirm Password.'
        
        if len(post_data['street_address']) != 0 and len(post_data['street_address']) < 2:
            errors['street_address'] = 'Your address needs at least 2 characters.'
        if len(post_data['street_address']) != 0 and not ADDRESS_REGEX.match(post_data['street_address']):
            errors['invalid_street_address'] =  'Please enter a valid Address.'
        
        if len(post_data['city']) != 0 and len(post_data['city']) < 2:
            errors['city'] = "Please enter your city address."

        if len(post_data['state']) != 0 and len(post_data['state']) < 2:
            errors['state'] = "Please enter your state."

        if len(post_data['zip_code']) != 0 and len(post_data['zip_code']) < 4:
            errors['zip_code'] = "Please enter your 5 digit zip code."
        
        if len(post_data['phone']) != 0 and len(post_data['phone']) < 10:
            errors['phone'] = 'Please enter your phone number with the area code.'
        if len(post_data['phone']) != 0 and not PHONE_REGEX.match(post_data['phone']):
            errors['invalid_phone'] = 'Please enter valid phone number.'
        # if len(post_data["related_user"]) != 0 and User.objects.filter(id=post_data["related_user"]).exists() == False:
        #     errors["related_user"] = "The parent's you put in does not exsit!"
        return errors

    def new_project_validation(self, post_data):
        errors={}
        if len(post_data['title']) < 2:
            errors['title'] = 'Title needs at least 2 characters.'
        if not post_data['due_date']:
            errors['no_due_date'] = "Please include a due date."
        if post_data['due_date'] and post_data['due_date'] < date.today().strftime("%Y-%m-%d"):
            errors['due_date'] = "Deadline cannot be in the past."
        if len(post_data['desc']) < 2:
            errors['desc'] = 'Description needs at least 2 characters.'

        return errors

    def edit_project_validation(self,post_data):
        errors={}
        if len(post_data['title']) != 0 and len(post_data['title']) < 2:
            errors['title'] = 'Title needs at least 2 characters.'
        if len(post_data['due_date']) !=0 and post_data['due_date'] < date.today().strftime("%Y-%m-%d"):
            errors['due_date'] = "Deadline cannot be in the past."
        if len(post_data['desc']) != 0 and len(post_data['desc']) < 2:
            errors['desc'] = 'Description needs at least 2 characters.'

        return errors

    def upload_image_validation(self, post_data):
        errors ={}
        if len(post_data['title']) < 2:
            errors['title'] = 'Title needs at least 2 characters.'
        return errors
    
    def related_person_validator(self, post_data):
        errors={}
        logged_user_email = post_data['logged_user_email']
        if logged_user_email == post_data['email']:
                errors['email'] = "You cannot enter your own email"
        return errors
    
    def add_student_validation(self, post_data):
        errors={}
        if 'list_of_students' not in post_data:
            errors['student'] = "No more available students."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length = 255)
    street_address = models.CharField(max_length = 255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    phone = models.IntegerField(blank=True, null=True)
    access_level = models.CharField(max_length = 255)
    profile_image = models.ImageField(upload_to='profile_image', blank=True, null=True, default="profile1.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to')
    def __unicode__(self):
        return self.first_name + " " + self.last_name
    
RELATIONSHIP_PARENT = 1
RELATIONSHIP_GUARDIAN = 2
RELATIONSHIP_STUDENT = 3
RELATIONSHIP_SIBLING = 4
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_PARENT, 'Parent'),
    (RELATIONSHIP_GUARDIAN, 'Guardian'),
    (RELATIONSHIP_STUDENT, 'Student'),
    (RELATIONSHIP_SIBLING, 'Sibling'),
)

class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='from_users', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_users', on_delete=models.CASCADE)
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Class(models.Model):
    # teacher = models.ManyToManyField(Teacher, related_name="teacher_classes")
    # student = models.ManyToManyField(Student, related_name="student_classes")
    user = models.ManyToManyField(User, related_name="parent_classes")
    subject = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    schedule_day  = models.CharField(max_length=255) #checkbox or dropdown
    schedule_time = models.TimeField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Project(models.Model):
    course = models.ForeignKey(Class, related_name="project_classes", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    reviewed_by_user = models.ManyToManyField(User, related_name="user_has_reviewed")
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    

class Image(models.Model):
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to="main/static/img")
    submission = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    submitter = models.ForeignKey(User, related_name='submitted_images', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    # parent_id = models.ForeignKey(Teacher, related_name="parent_messages", on_delete=models.CASCADE)
    # student_id = models.ForeignKey(Teacher, related_name="student_messages", on_delete=models.CASCADE)
    # access_level = models.IntegerField()
    image_comment = models.ForeignKey(Image, related_name="messages", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Comment(models.Model):
    comment = models.TextField()
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    # parent_id = models.ForeignKey(Parent, related_name="parent_comments", on_delete=models.CASCADE)
    # student_id = models.ForeignKey(Student, related_name="student_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Bulletin_board(models.Model):
    bulletin = models.TextField()
    user = models.ForeignKey(User, related_name="bulletins", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()