from django.db import models

class MainProcess(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SubProcess(models.Model):
    main_process = models.ForeignKey(MainProcess, related_name='subprocesses', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.main_process.name} - {self.name}"