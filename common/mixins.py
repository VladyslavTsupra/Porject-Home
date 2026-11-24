from django.core.cache import cache


# Mixin for working with the cache.
class CacheMixin:
    # Returns data from the cache or stores the query result in the cache.
    def set_get_cache(self, query, cache_name, cache_time):
        data = cache.get(cache_name)

        if not data:
            data = query
            cache.set(cache_name, data, cache_time)

        return data