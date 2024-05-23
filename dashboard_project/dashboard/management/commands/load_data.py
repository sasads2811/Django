from datetime import datetime

import pandas as pd
from django.core.management.base import BaseCommand
from dashboard.models import ScoreRecord

class Command(BaseCommand):
    help = 'Load data from CSV into the database'

    def handle(self, *args, **kwargs):
        data = pd.read_csv('/home/aleksandar/Downloads/project_data.csv', delimiter=';')
        for _, row in data.iterrows():
            print(row)
            scoring_date = datetime.strptime(row['scoring_date'], '%Y/%m/%d').date()
            ScoreRecord.objects.create(
                candidate=row['candidate'],
                score=row['score'],
                scoring_date=scoring_date,
                province=row['province']
            )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
