from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField("タイトル", max_length=50)
    description = models.TextField("説明", null=True, blank=True, max_length=100)
    completed = models.BooleanField("完了", default=False)
    created_Date = models.DateTimeField("作成日", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["completed", "-created_Date"]
        db_table = "Tasks"
        verbose_name = "タスク"
        verbose_name_plural = "タスク一覧"
