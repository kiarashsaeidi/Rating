from django.core.cache import cache
from .models import Post, Rating
from django.utils.timezone import now


def process_post_ratings():

    keys = cache.keys("post_rating_*")

    for cache_key in keys:
        post_id = cache_key.split("_")[-1]
        recent_ratings = cache.get(cache_key, [])

        if not recent_ratings:
            continue

        post = Post.objects.get(id=post_id)

        for user_id, new_rating, timestamp in recent_ratings:
            rating = Rating.objects.filter(user_id=user_id, post=post).first()
            old_rating = rating.score if rating else None

            if rating:
                rating.score = new_rating
                rating.save(update_fields=['score'])
            else:
                Rating.objects.create(user_id=user_id, post=post, score=new_rating)

            post.update_rating_stats(new_rating=new_rating, old_rating=old_rating)

        cache.delete(cache_key)
