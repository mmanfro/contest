from django.shortcuts import redirect, render


def index(request):
    return redirect("/voting/", permanent=True)


def handler500(request, exception=None):
    return render(
        request, "contest/error.html", context={"exception": exception}, status=500
    )


def handler404(request, exception=None):
    return render(
        request, "contest/error.html", context={"exception": exception}, status=404
    )


def handler403(request, exception=None):
    return render(
        request, "contest/error.html", context={"exception": exception}, status=403
    )


def handler400(request, exception=None):
    return render(
        request, "contest/error.html", context={"exception": exception}, status=400
    )
