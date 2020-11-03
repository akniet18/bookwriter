from django.db import models

class Note(models.Model):
    text = models.TextField()
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE, related_name="inote", blank=True, null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="my_notes")

    def __str__(self):
        return f'{self.user.id} - {self.user.email}'
