from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import FloatField
from django.db.models.functions import Greatest

from goods.models import Products

MIN_SEARCH_RANK = 0.5


# Searches products by id or by word similarity in the name and description.
def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    tokens = [token for token in query.split() if len(token) >= 2]
    if not tokens:
        return Products.objects.none()

    return (
        Products.objects.annotate(
            rank=Greatest(
                *(
                    similarity
                    for token in tokens
                    for similarity in (
                        TrigramWordSimilarity(token, "name"),
                        TrigramWordSimilarity(token, "description"),
                    )
                ),
                output_field=FloatField(),
            )
        )
        .filter(rank__gte=MIN_SEARCH_RANK)
        .order_by("-rank")
    )
