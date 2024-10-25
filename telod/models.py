from django.db import models


class Medicine(models.Model):
    main_name = models.CharField(max_length=511)
    description = models.TextField()

    def __str__(self):
        return self.main_name


class MedicineName(models.Model):
    name = models.CharField(max_length=511)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
