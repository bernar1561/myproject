from django.db import models


class ProfileManager(models.Model):
    use_for_related_fields = True

    def all_photo(self):
        return self.all_photo()


# class ProfileStatusManager(models.Manager):
#     use_for_related_fields = True
#
#     def article_status(self):
#         return self.get_queryset().status(status=False)
