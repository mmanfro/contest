import secrets
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


def vote(request, participant_id):
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
