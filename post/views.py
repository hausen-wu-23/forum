from django.shortcuts import redirect, render
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User, AnonymousUser
from django.views import View
from .forms import SubmitPost
from .models import Post, Thread
import datetime

# Create your views here.

from django.http import HttpResponse

from .models import Post


def index(request):
    # temporary landing page
    return HttpResponse('<a href="/posts/">posts here hi</a>')


def detail(request, post_id):
    # shows content of the post
    post = get_object_or_404(Post, pk=post_id)
    context = {"post": post}
    return render(request, "post/detail.html", context)


# def new_post(request):
#     # create form
#     form = SubmitPost()

#     # if there is data coming in, normally GET, but when data, POST
#     if request.method == 'POST':
#         # print("POST!")
#         # print(request.POST)

#         # create the model form the QueryDict
#         form = SubmitPost(request.POST)

#         # varify
#         if form.is_valid():
#             print('Valid')
#             # save data to the modele
#             save_data = form.save()
#             # redirect to the post that was just posted
#             return redirect('/posts/' + str(save_data.id) + '/')
#     # print(form)

#     # if just opened the page
#     else:
#         context = {
#             'form' : form
#         }
#         return render(request, 'post/newPost.html', context)

class LogIn(View):
    def get(self, request):
        context={}
        return render(request, "post/logIn.html", context)

    def post(self, request):
        print(request.POST["username"])
        print(request.POST["password"])
        return HttpResponse('hi')

class NewPost(View):
    def get(self, request):
        form = SubmitPost()
        context = {"form": form}
        return render(request, "post/newPost.html", context)

    def post(self, request):
        print(request.POST)
        form = request.POST
        save_data = Post.objects.create(
            userPosted=get_object_or_404(User, pk=form["userPosted"]),
            thread=get_object_or_404(Thread, pk=form["thread"]),
            title=form["title"],
            content=form["content"],
            pub_date=datetime.datetime.now(),
        )
        save_data.save()
        return HttpResponse("view my post" + str(save_data.id))
        # verify
        # if form.is_valid():
        #     print('Valid')
        #     # save data to the modele
        #     save_data = form.save(commit=False)
        #     save_data.pub_date = datetime.datetime.now()
        #     save_data.save()
        #     # save_data.pub_time = datetime.datetime.now()
        #     # save_data.save()
        #     # redirect to the post that was just posted
        #     return HttpResponse('view my post')

        # return HttpResponse('invalid')

def post_list_view(request):
    post_objects = Post.objects.order_by("pub_date")
    context = {"post_objects": post_objects}
    return render(request, "post/index.html", context)

