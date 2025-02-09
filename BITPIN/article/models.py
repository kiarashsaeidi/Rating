from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    total_rating = models.BigIntegerField(default=0)
    rating_count = models.BigIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)


    def update_rating_stats(self, new_rating, old_rating = None):

        if old_rating is not None:
            self.total_rating = self.total_rating - old_rating + new_rating
        else:
            self.total_rating += new_rating
            self.rating_count += 1

        decay_factor = 0.9
        self.average_rating = (self.average_rating * decay_factor) + (
                    (1 - decay_factor) * (self.total_rating / self.rating_count))

        self.save(update_fields=['total_rating', 'rating_count', 'average_rating'])

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(6)])  # 0 تا 5 ستاره

    class Meta:
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['post', 'user']),
        ]

    # def save(self, *args, **kwargs):
    #
    #     old_rating = None
    #     if self.pk:
    #         old_rating = Rating.objects.get(pk = self.pk).rating
    #
    #     super().save(*args, **kwargs)
    #     self.post.update_rating_stats(self.rating, old_rating)
