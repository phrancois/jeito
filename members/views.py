from datetime import date
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.generic import View, TemplateView
from .forms import AdhesionsForm
from .models import Adhesion


class AdhesionsJsonView(View):
    def serie(self, season, category):
        self.today = now().date()
        start = date(season - 1, 9, 1)
        end = min(date(season, 8, 31), self.today)
        if category:
            sql = '''
                SELECT date, SUM(COUNT(members_rate.id)) OVER (ORDER BY date)
                FROM generate_series(%s::date, %s::date, '1 day'::interval) AS date
                LEFT JOIN members_adhesion USING (date)
                LEFT JOIN members_rate ON (members_rate.id=rate_id AND category=%s)
                GROUP BY date
                ORDER BY date'''
            params = [start, end, category]
        else:
            sql = '''
                SELECT date, SUM(COUNT(members_adhesion.id)) OVER (ORDER BY date)
                FROM generate_series(%s::date, %s::date, '1 day'::interval) AS date
                LEFT JOIN members_adhesion USING (date)
                GROUP BY date
                ORDER BY date'''
            params = [start, end]
        cursor = connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    def get(self, request):
        season = int(self.request.GET['season'])
        reference = int(self.request.GET.get('reference', '0')) or season - 1
        category = self.request.GET.get('category')
        result = self.serie(int(season), category)
        ref_result = self.serie(int(reference), category)
        cmp_idx = min(len(result), len(ref_result)) - 1
        date1 = ref_result[cmp_idx][0].strftime('%d/%m/%Y')
        date2 = result[-1][0].strftime('%d/%m/%Y')
        nb1 = ref_result[cmp_idx][1]
        nb2 = result[-1][1]
        diff = nb2 - nb1
        if nb1:
            percent = 100 * diff / nb1
            comment = """Au <strong>{}</strong> : <strong>{}</strong> adhérents<br>
                         Au <strong>{}</strong> : <strong>{}</strong> adhérents,
                         c'est-à-dire <strong>{:+f}</strong> adhérents
                         (<strong>{:+0.2f} %</strong>)
                      """.format(date1, nb1, date2, nb2, diff, percent)
        else:
            comment = """Au <strong>{}</strong> : <strong>{}</strong> adhérents
                      """.format(date2, nb2)
        data = {
            'labels': [x[0].strftime('%b') if x[0].day == 1 else '' for x in ref_result],
            'series': [
                [x[1] for x in ref_result],
                [x[1] for x in result],
            ],
            'comment': comment,
        }
        return JsonResponse(data)


class AdhesionsView(TemplateView):
    template_name = 'members/adhesions.html'

    def get_context_data(self, **kwargs):
        today = now().date()
        current_season = str(today.year + (1 if today.month >= 9 else 0))
        season = self.request.GET.get('season', current_season)
        reference = self.request.GET.get('reference')
        category = self.request.GET.get('category')
        initial = self.request.GET.dict()
        initial.update({
            'season': season,
            'reference': reference,
            'category': category,
        })
        form = AdhesionsForm(initial=initial)
        context = super().get_context_data(**kwargs)
        context['form'] = form
        context.update(initial)
        return context


class TranchesJsonView(View):

    def get(self, request):
        qs = Adhesion.objects.filter(season=2016, rate__name__icontains='enfant')
        qs1 = qs.order_by('rate__bracket')
        qs1 = qs1.values('rate__bracket')
        qs1 = qs1.annotate(n=Count('id'))
        qs2 = qs.values('rate__name', 'rate__rate', 'rate__rate_after_tax_ex')
        qs2 = qs2.annotate(n=Count('id'))
        total1 = sum(x['n'] for x in qs1)
        total2 = sum(x['n'] for x in qs2)
        assert total1 == total2
        average_price = sum([x['n'] * x['rate__rate'] for x in qs2]) / total2
        average_price_after_tax_ex = sum([x['n'] * x['rate__rate_after_tax_ex'] for x in qs2]) / total2
        data = {
            'labels': [x['rate__bracket'] + ' (%0.0f %%)' % (100 * x['n'] / total1) for x in qs1],
            'series': [x['n'] for x in qs1],
            'comment': """Cotisation moyenne : <strong>{:0.02f} €</strong>
                          ({:0.02f} € après défiscalisation)
                          """.format(float(average_price), float(average_price_after_tax_ex)),
        }
        return JsonResponse(data)


class TranchesView(TemplateView):
    template_name = 'members/tranches.html'
