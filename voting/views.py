import secrets
import requests
from datetime import timedelta

from django.contrib import messages
from django.shortcuts import render
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from voting.models import Participant, Vote


def participants(request):
    context = {}

    context["participants"] = Participant.objects.filter(
        start_date__lte=now(), end_date__gt=now()
    )

    response = render(request, "vote/participants.html", context=context)

    if not "uuid" in request.COOKIES:
        uuid = secrets.token_urlsafe(24)
        response.set_cookie(key="uuid", value=uuid, expires=now() + timedelta(days=30))

    return response


def vote(request):
    if request.method == "POST":
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": "6LeO5MYgAAAAAPqFyh-CdyJ4mIVLA5E-SqqPLqAG",
                "response": request.POST.get("g-recaptcha-response"),
            },
        )

        if not r.json().get("success"):
            messages.error(
                request,
                _("Captcha inválido."),
            )
            return participants(request)

        ip_address = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get(
            "REMOTE_ADDR"
        )

        if not "uuid" in request.COOKIES or not ip_address:
            messages.error(
                request,
                _(
                    "Não foi possível salvar seu voto. Verifique se o seu navegador não está em modo anônimo e se os cookies estão habilitados."
                ),
            )
            return participants(request)

        try:
            vote, created = Vote.objects.update_or_create(
                cookie=request.COOKIES.get("uuid"),
                defaults={
                    "participant_id": request.POST.get("participant-id"),
                    "ip_address": ip_address,
                },
            )

            messages.success(
                request,
                _("Voto salvo com sucesso."),
            )
        except ValueError as e:
            messages.error(request, e)

    return participants(request)
