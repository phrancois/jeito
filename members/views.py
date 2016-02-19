from datetime import date, timedelta
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic import View, TemplateView


class AdhesionsJsonView(View):
    def serie(self, season):
        sql = '''select date, sum(count(id)) over (order by date)
                 from generate_series(%s::date, %s::date, '1 day'::interval) date
                 left join members_adhesion
                 using (date)
                 group by date
                 order by date;'''
        self.today = now().date()
        start = date(season - 1, 9, 1)
        end = min(date(season, 8, 31), self.today)
        cursor = connection.cursor()
        cursor.execute(sql, [start, end])
        return cursor.fetchall()

    def get(self, request, season, reference):
        result = self.serie(int(season))
        ref_result = self.serie(int(reference))
        data = {
            'labels': [x[0].strftime('%b') if x[0].day == 1 else '' for x in ref_result],
            'series': [
                [x[1] for x in ref_result],
                [x[1] for x in result],
            ],
        }
        return JsonResponse(data)


class AdhesionsView(TemplateView):
    template_name = 'members/adhesions.html'

    def get_context_data(self, **kwargs):
        today = now().date()
        current_season = today.year + (1 if today.month >= 9 else 0)
        season = int(self.request.GET.get('season', current_season))
        reference = int(self.request.GET.get('reference', season - 1))
        context = super().get_context_data(**kwargs)
        print(current_season, season, reference)
        context.update({
            'season': season,
            'reference': reference,
        })
        return context
