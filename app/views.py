from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView

from app.forms import PostForm
from app.models import Post
import os
import openai


def index(request: HttpRequest) -> HttpResponse:
    qs = Post.objects.all()
    return render(
        request,
        "app/index.html",
        {
            "post_list": qs,
        },
    )


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = Post.objects.get(pk=pk)
    return render(
        request,
        "app/post_detail.html",
        {
            "post": post,
        },
    )


post_new = CreateView.as_view(
    model=Post,
    form_class=PostForm,
    success_url="/app/",
)

GPT_API_KEY = os.environ.get("GPT_API_KEY", "YOUR_DEFAULT_API_KEY")

openai.api_key = GPT_API_KEY

USER_PROMPT = os.environ.get("USER_PROMPT", "")


def analyze_text(request):
    if request.method == "POST":
        text = request.POST.get("text")
        prompt = USER_PROMPT + text

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
        analysis = response.choices[0].message.content
        return render(request, "app/analysis.html", {"analysis": analysis})
    return render(request, "app/analyze_text.html")
