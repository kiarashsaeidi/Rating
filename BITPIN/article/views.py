import json
import redis
from django.utils.timezone import now
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from BITPIN import settings
from .models import Rating, Post
from .serializers import PostSerializer
from django.core.cache import cache
from rest_framework.response import Response

class PostListApiView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        cache_key = "post_list"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            cached_data = Post.objects.all()
            cache.set(cache_key, cached_data, timeout=60 * 60 * 24)

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

class RatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):

        user = request.user
        score = request.data.get('score')

        if score is None or not (0 <= score <= 5):
            return Response({"error": "امتیاز باید بین 0 تا 5 باشد."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error":"پست یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        rating, created = Rating.objects.get_or_create(user=user, post=post, defaults={"score": score})
        old_score = rating.score if not created else None

        if not created:
            rating.score = score
            rating.save(update_fields=['score'])


        cache_key = f"post_rating_{post_id}"


        recent_ratings = cache.get(cache_key, [])
        recent_ratings.append((user.id, score, now()))

        if len(recent_ratings) > 10:  # اگر در زمان کوتاه بیش از ۱۰ امتیاز داده شد
            return Response(
                {"message": "امتیازات زیادی در بازه کوتاه ثبت شده‌اند. تأثیر آنها به تدریج اعمال خواهد شد."},
                status=status.HTTP_202_ACCEPTED)

        cache.set(cache_key, recent_ratings, timeout=60*10)  # ذخیره در کش برای ۲ دقیقه
        post.update_rating_stats(new_rating=score, old_rating=old_score)

        return Response({"message": "امتیاز شما ثبت شد.", "average_rating": post.average_rating}, status=status.HTTP_200_OK)










