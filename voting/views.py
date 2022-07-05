import secrets
from django.db import IntegrityError
from django.shortcuts import render, redirect
from voting.models import Participant, Vote
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


def participants(request):
    context = {}

    context["participants"] = Participant.objects.filter(
        start_date__lte=now(), end_date__gt=now()
    )

    response = render(request, "vote/participants.html", context=context)

    if not "uuid" in request.COOKIES:
        uuid = secrets.token_urlsafe(24)
        response.set_cookie(key="uuid", value=uuid)

    return response


def vote(request, participant_id):
    print(request.META.get("HTTP_X_FORWARDED_FOR"))

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
                "participant_id": participant_id,
                "ip_address": request.META.get("REMOTE_ADDR"),
            },
        )

        messages.success(
            request,
            _("Voto salvo com sucesso."),
        )

    except ValueError as e:
        messages.error(request, e)

    return participants(request)
