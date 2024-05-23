from django.db import models

class ScoreRecord(models.Model):
    candidate = models.CharField(max_length=100)
    score = models.FloatField()
    scoring_date = models.DateField()
    province = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.candidate} - {self.score} on {self.scoring_date}"
