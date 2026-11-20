from django.core.cache import cache


# Міксин для роботи з кешем.
class CacheMixin:
    # Повертає дані з кешу або зберігає в кеш результат запиту.
    def set_get_cache(self, query, cache_name, cache_time):
        data = cache.get(cache_name)

        if not data:
            data = query
            cache.set(cache_name, data, cache_time)

        return data