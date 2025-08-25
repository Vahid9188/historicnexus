from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Article

@receiver([post_save, post_delete], sender=Article)
def clear_article_cache(sender, instance, **kwargs):
    cache_key = f"article_{instance.pk}"
    cache.delete(cache_key)
