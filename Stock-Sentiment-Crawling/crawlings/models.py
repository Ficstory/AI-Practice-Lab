from django.db import models


class Comment(models.Model):
    company_name = models.CharField(max_length=100)
    stock_code = models.CharField(max_length=20, null=True, blank=True)
    content = models.TextField()
    saved_date = models.DateTimeField(auto_now_add=True)
