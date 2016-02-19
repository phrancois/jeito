from datetime import date, timedelta
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic import View, TemplateView


class AdhesionsJsonView(View):
    def serie(self, season, active):
        sql = '''
            SELECT date, SUM(COUNT(members_adhesion.id)) OVER (ORDER BY date)
            FROM generate_series(%s::date, %s::date, '1 day'::interval) AS date
            LEFT JOIN members_adhesion USING (date)'''
        if active is not None:
            sql += '''
                LEFT JOIN members_rate ON (members_rate.id = rate_id)
                WHERE active = %s OR active IS NULL'''
        sql += '''
            GROUP BY date
            ORDER BY date'''
        self.today = now().date()
        start = date(season - 1, 9, 1)
        end = min(date(season, 8, 31), self.today)
        params = [start, end]
        if active is not None:
            params.append(active)
        cursor = connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    def get(self, request):
        season = int(self.request.GET['season'])
        reference = int(self.request.GET['reference'])
        if self.request.GET.get('active') == 'on':
            active = True
        elif  self.request.GET.get('active') == 'off':
            active = False
        else:
            active = None
        result = self.serie(int(season), active)
        ref_result = self.serie(int(reference), active)
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
        if self.request.GET.get('active') == 'on':
            active = True
        elif  self.request.GET.get('active') == 'off':
            active = False
        else:
            active = None
        context = super().get_context_data(**kwargs)
        context.update({
            'season': season,
            'reference': reference,
            'active': active,
        })
        return context
