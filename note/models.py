from django.db import models

class Note(models.Model):
    text = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="my_notes")

    def __str__(self):
        return f'{self.user.id} - {self.user.email}'
