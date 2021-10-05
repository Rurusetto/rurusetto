import os
import requests
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Ruleset, RulesetStatus


@receiver(post_save, sender=Ruleset)
def create_ruleset(sender, instance, created, **kwargs):
    """When receive that has user signed up, it will create Profile and Config object that is bind with User object."""
    if created:
        RulesetStatus.objects.create(ruleset=instance)
