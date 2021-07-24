from django.db import models


class Stock(models.Model):
    company_name = models.CharField(max_length=10)
    open_price = models.FloatField()
    close_price = models.FloatField()
    transaction = models.IntegerField()
    image = models.FileField(upload_to="images", null=True, blank=True)

    def __str__(self):
        return self.company_name
