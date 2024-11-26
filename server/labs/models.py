from django.db import models
from tlsa_server.models import TLSA_User

class Lab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class ManageLab(models.Model):
    manager = models.ForeignKey(TLSA_User, on_delete=models.CASCADE, to_field='id', db_column='manager_id')
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, to_field='id', db_column='lab_id')

    class Meta:
        db_table = 'manage_lab'

    def __str__(self):
        return f"Manager {self.manager.id} manages Lab {self.lab.id}"