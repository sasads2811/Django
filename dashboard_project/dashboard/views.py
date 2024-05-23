from django.shortcuts import render
from django.db.models import Avg, Max, Sum, Subquery
from .models import ScoreRecord
from .forms import FilterForm, FilterFormOnlyYear
from django.db.models.functions import ExtractMonth, ExtractYear



def get_monthly_averages(year):
    data = ScoreRecord.objects.filter(scoring_date__year=year).values('scoring_date__month').annotate(
        average_score=Avg('score'))
    return {d['scoring_date__month']: d['average_score'] for d in data}


def monthly_averages_view(request):
    year = request.GET.get('year', 2020)
    averages = get_monthly_averages(year)
    return render(request, 'dashboard/monthly_averages.html', {'averages': averages, 'year': year})


def get_monthly_averages_by_year_and_province(year, province):
    data = ScoreRecord.objects.filter(scoring_date__year=year, province=province).values(
        'scoring_date__month').annotate(
        average_score=Avg('score'))
    return {d['scoring_date__month']: d['average_score'] for d in data}


def monthly_averages_view_by_year_and_province(request):
    form = FilterForm(request.GET or None)
    year = form.data.get('year', '2020')
    province = form.data.get('province', '')

    filters = {'scoring_date__year': year}
    if province:
        filters['province'] = province

    records = ScoreRecord.objects.filter(**filters)
    averages = records.values('scoring_date__month').annotate(average_score=Avg('score')).order_by(
        'scoring_date__month')
    monthly_averages = {record['scoring_date__month']: record['average_score'] for record in averages}

    provinces = ScoreRecord.objects.values_list('province', flat=True).distinct()
    return render(request, 'dashboard/monthly_averages_by_year_and_province.html',
                  {'averages': monthly_averages, 'year': year, 'provinces': provinces, 'form': form,
                   'records': records})


def total_monthly_scores(request):
    form = FilterFormOnlyYear(request.GET or None)
    year = form.data.get('year', '2020')

    filters = {'scoring_date__year': year}

    records = ScoreRecord.objects.filter(**filters)
    averages = records.values('scoring_date__month').annotate(average_score=Sum('score')).order_by(
        'scoring_date__month')
    monthly_averages = {record['scoring_date__month']: record['average_score'] for record in averages}

    return render(request, 'dashboard/total_monthly_scores.html',
                  {'averages': monthly_averages, 'year': year, 'form': form})

def highest_score_of_the_month(request):
    form = FilterFormOnlyYear(request.GET or None)
    year = form.data.get('year', '2020')

    # Subquery to find the highest score for each month
    highest_scores_subquery = ScoreRecord.objects.annotate(
        month=ExtractMonth('scoring_date'),
        year=ExtractYear('scoring_date'),
    ).values('month', 'year').annotate(
        max_score=Max('score')
    ).filter(year=year)

    # Use this subquery to filter the main queryset
    highest_scores = ScoreRecord.objects.filter(
        scoring_date__year=year,
        score=Subquery(
            highest_scores_subquery.filter(
                month=ExtractMonth('scoring_date')
            ).values('max_score')
        )
    ).order_by('scoring_date__year', 'scoring_date__month')

    monthly_averages = {record['month']: record['max_score'] for record in highest_scores_subquery}
    return render(request, 'dashboard/highest_score_of_the_month.html',
                  {'averages': monthly_averages, 'year': year, 'form': form})