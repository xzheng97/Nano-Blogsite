from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from socialnetwork.models import Post, Profile, Comment

MAX_UPLOAD_SIZE = 2500000

class EntryForm(forms.Form):
    last_name     = forms.CharField(max_length=20)
    first_name    = forms.CharField(max_length=20)
    birthday      = forms.DateField(required=False)
    children      = forms.IntegerField(required=False, label='# of children')
    address       = forms.CharField(required=False, max_length=200)
    city          = forms.CharField(required=False, max_length=30)
    state         = forms.CharField(required=False, max_length=20)
    zip_code      = forms.CharField(required=False, max_length=10)
    country       = forms.CharField(required=False, max_length=30)
    email         = forms.CharField(required=False, max_length=32)
    phone_number  = forms.CharField(required=False, max_length=16, label='Phone #')


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


class RegisterForm(forms.Form):
    username   = forms.CharField(max_length = 20)
    password  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    confirm_password  = forms.CharField(max_length = 200, 
                                 label='Confirm',  
                                 widget = forms.PasswordInput())
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
    first_name = forms.CharField(max_length=20)
    
    last_name  = forms.CharField(max_length=20)
    
    
   

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        exclude = (
            'post_author',
            'post_time',
        )
        labels = {
            "post_input_text": "New Post"
        }


class CreateProfile(forms.ModelForm):
    bio_input_text = forms.CharField(widget=forms.Textarea(attrs={"rows":2,"class":"profile_bio"}))
    class Meta:
        model = Profile
        fields = ('bio_input_text', 'profile_picture')

    def clean_profile_picture(self):
        picture = self.cleaned_data['profile_picture']
        if not picture or not hasattr(picture, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture