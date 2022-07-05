from django.shortcuts import redirect, render


def index(request):
    return redirect("/voting/", permanent=True)
