from django.shortcuts import render,redirect,reverse
from django.views.generic import TemplateView,FormView,ListView,DetailView,DeleteView
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm,CustopmloginForm,EditPostForm,EditCommentForm
from django.contrib.auth import authenticate, login , logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post,Comment
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Create your views here.
#logout(request)

class lgoutView(View):
    def get(self, request):
        if (request.method=="GET"):
            logout(request)
            return redirect("blog:login")

class register(View):
    template_name = "blog/register.html"

    def get(self, request):
        if (self.request.user.is_authenticated ):
            return redirect("blog:listPost")
        if (request.method=="GET"):
            return render(request,"blog/register.html",context={"UserForm": UserCreationForm() 
            , "UserDetail": RegisterUserForm()})

    def post(self, request):
        result=None
        if (request.method=="POST"):
            _user=UserCreationForm(request.POST)
            _userDetail=RegisterUserForm(request.POST)

            if (_user.is_valid() and _userDetail.is_valid() ):
                user=_user.save()
                userD=_userDetail.save(commit=False)
                userD.user=user
                userD.save()
                result="User created succesfully"
        return render(request,"blog/register.html",context={"UserForm": _user 
            , "UserDetail": _userDetail , "result": result })
    
class loginPage(FormView):
    template_name = 'blog/login.html'
    form_class = CustopmloginForm
    success_url = '/listPost'
    result=None

    def get(self, request):
        if (self.request.user.is_authenticated ):
            return redirect("blog:listPost")
        return super().get(request)
        #return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        user=form
        if (self.request.user.is_authenticated ):
            return redirect("blog:listPost")
        if (self.request.method=="POST"):
            if (user.is_valid()):
                username=user.cleaned_data["username"]
                password=user.cleaned_data["password"]
                user = authenticate(self.request, username=username, password=password)
                if user is not None:
                    login(self.request, user)
                    self.result="Auth succesfull"
                    return super().form_valid(form)
                else:
                    self.result="Login failed"
                    return super().form_invalid(form)


    def get_context_data(self,**kwargs):
        super()
        if 'result' not in kwargs:
            kwargs['result'] = self.result
        return super().get_context_data(**kwargs)

class editPost(LoginRequiredMixin,FormView):
    template_name = 'blog/editPost.html'
    form_class = EditPostForm
    success_url = '/listPost'
    result=None
    login_url="/login"

    def get(self, request):
        if ( not self.request.user.is_authenticated ):
            return redirect("blog:login")
        return super().get(request)
        #return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        post=form
        if ( not self.request.user.is_authenticated ):
            return redirect("blog:login")
        if (self.request.method=="POST"):
            if (post.is_valid()):
                _post=post.save(commit=False)
                _post.user=self.request.user
                _post.save()
                return super().form_valid(form)

class listPost(ListView):
    paginate_by = 20
    model = Post
    template_name="blog/listPost.html"
    ordering="-id"

    def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            context["forward"]=range(context["page_obj"].number+1,context["page_obj"].number+4)
            context["backward"]=range(context["page_obj"].number-4,context["page_obj"].number)
            return context


def postDetailx(request):
    return render(request,'blog/postDetail.html')

class postDetail(DetailView):
    template_name='blog/postDetail.html'
    model = Post
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"]=self.object.comment_set.all()
        for i in context["comments"]:
            print( i.user.id )
        return context



class deletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:listPost')
    template_name="blog/deletePost.html"

    def get(self, request,**kwargs):
        if (self.request.user==self.get_object().user ):
            return super().get(request,**kwargs)
        elif (  self.request.user.is_superuser ) :
            return super().get(request,**kwargs)
        else:
            return redirect(reverse("blog:postDetail",kwargs={"pk":self.get_object().id}))


class editComment(LoginRequiredMixin,FormView):
    template_name="blog/editComment.html"
    form_class=EditCommentForm
    success_url = None
    result=None
    login_url="/login"

    def form_valid(self, form):
        comment=form
        if ( not self.request.user.is_authenticated ):
            return redirect("blog:login")
        if (self.request.method=="POST"):
            if (comment.is_valid()):
                _comment=comment.save(commit=False) 
                _comment.user=self.request.user
                #_post.Post=Post.objects.filter(pk=self.kwargs['post_id']).get()
                post=Post.objects.filter(pk=self.kwargs['npost']).get()
                _comment.Post=post
                print(_comment.user)
                _comment.save()
                self.success_url="/postDetail/"+ str(_comment.Post.id)+"/"
                return super().form_valid(form)

class deleteComment(DeleteView):
    model = Comment
    template_name="blog/deleteComment.html"

    def get(self, request , pk):
        self.object=self.get_object()
        if ( not self.request.user.is_superuser ):
            return redirect("blog:login")
        elif (self.request.user!= self.object.user and ( not self.request.user.is_superuser)):
            return redirect("blog:login")
        return super().get(request)

    def get_success_url(self):
        self.success_url=reverse_lazy("blog:postDetail",kwargs={"pk":self.object.Post.id})
        return super().get_success_url()

