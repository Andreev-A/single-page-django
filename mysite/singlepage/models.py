from django.db import models


# Create your models here.
class Table(models.Model):
    """
    date - дата
    name - название
    amount - количество
    distance - расстояние
    """

    date = models.DateField()
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    distance = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.date} {self.name} {self.amount} {self.distance}'
