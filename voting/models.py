from django.db import models
from django.db.models.signals import pre_save
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Participant(models.Model):
    name = models.CharField(
        _("nome"), null=False, blank=False, max_length=255, unique=True
    )
    description = models.TextField(_("descrição"), null=True, blank=True)
    video_url = models.URLField(_("URL do vídeo"), null=False, blank=False)
    start_date = models.DateTimeField(_("início"), default=now)
    end_date = models.DateTimeField(_("término"))
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)

    @property
    def votes(self):
        return Vote.objects.filter(participant=self).count()

    class Meta:
        verbose_name = _("participante")
        verbose_name_plural = _("participantes")

    def __str__(self):
        return self.name


class Vote(models.Model):
    cookie = models.TextField(unique=True)
    ip_address = models.GenericIPAddressField()
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, null=False)
    created_date = models.DateTimeField(
        _("created date"), auto_now_add=True, editable=False
    )

    class Meta:
        verbose_name = _("voto")
        verbose_name_plural = _("votos")


def check_vote(sender, instance, *args, **kwargs):
    count_ip = (
        Vote.objects.filter(ip_address=instance.ip_address)
        .exclude(cookie=instance.cookie)
        .count()
    )
    max_count_ip = 3
    if count_ip >= max_count_ip:
        raise ValueError(
            _(
                f"Só é possível votar no mesmo participante {max_count_ip} vezes por uma mesma rede. Conecte-se a outra rede e tente novamente."
            )
        )

    if instance.participant.start_date >= now():
        raise ValueError(_("Votação ainda não foi aberta."))

    if instance.participant.end_date <= now():
        raise ValueError(_("Votação já foi finalizada."))


def check_dates(sender, instance, *args, **kwargs):
    if instance.start_date > instance.end_date:
        raise ValueError(_("Data de término deve ser maior que a data de início."))


pre_save.connect(check_vote, sender=Vote)
pre_save.connect(check_dates, sender=Participant)
