from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import models
from socialnetwork.models import Profile
MAX_UPLOAD_SIZE = 2500000

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
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    email      = forms.CharField(max_length=50,
                                widget = forms.EmailInput())
    password  = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput())
    confirm_password  = forms.CharField(max_length = 200, 
                                label='Confirm Password',  
                                widget = forms.PasswordInput())

# Customizes form validation for properties that apply to more
# than one field.  Overrides the forms.Form.clean function.
    def clean(self):
    # Calls our parent (forms.Form) .clean function, gets a dictionary
    # of cleaned data as a result
        cleaned_data = super().clean()

    # Confirms that the two password fields match
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
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

class AddPostForm(forms.Form):
    post_input_text = forms.CharField(max_length = 200)
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return cleaned_data
        
    def clean_post(self):
        new_post = self.cleaned_data.get("post_input_text")
        if not new_post:
            raise forms.ValidationError("Need to use a post method")
        if len(new_post) > 200 or len(new_post) == 0:
            raise forms.ValidationError("Need to stick to character count")
        return new_post

class CommentForm(forms.Form):
    new_comment = forms.CharField(max_length = 200)
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    def clean_post(self):
        new_comment = self.cleaned_data.get("new_comment")
        if not new_comment:
            raise forms.ValidationError("Need to use a post method")
        if len(new_comment) > 200 or len(new_comment) == 0:
            raise forms.ValidationError("Need to stick to character count")
        return new_comment

class ProfileForm(forms.Form):
    profile_picture = forms.ImageField()
    bio_input_text = forms.CharField(max_length=200,widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))


class ProfileItemForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ( 'bio', 'picture')
        widgets = {
            'bio':forms.Textarea(attrs={'id':'id_bio_input_text', 'rows':'3'}),
            'picture': forms.FileInput(attrs = {'id':'id_profile_picture'})
        }
        labels = {
            'bio': "",
            'picture': "Upload image"
        }

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture or not hasattr(picture, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture





        