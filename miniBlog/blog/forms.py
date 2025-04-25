from django.forms import ModelForm,PasswordInput,CharField,Form
from .models import userDetail,Post,Comment
from django.contrib.auth.models import User
from django.core.validators  import RegexValidator

class RegisterUserForm(ModelForm):
    class Meta:
        model = userDetail
        fields = ['hobby']


class CustopmloginForm(Form):
    username=CharField(label='Your username', max_length=100,validators=[RegexValidator(regex="^[A-Za-z1-9_-]*$"
    ,message="Username invalid : must not contain spection charcters"),])
    password=CharField(widget=PasswordInput(),label='Your password', max_length=100)

class EditPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title","text"]
        labels = {
            'title': 'Title :',
            'text': 'Please enter your post text :',
        }

class EditCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {
            'text': 'Please type your comment :',
        }