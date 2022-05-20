from django.db import models

from users.models import User


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="following",
    )
    followed_user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        related_name="followed_by",
    )
    
    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )

    def __str__(self):
        return f"{self.followed_user.username} - follows {self.user.username}"