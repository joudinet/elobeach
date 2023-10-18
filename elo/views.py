from django.core.serializers.json import Serializer
from django.shortcuts import render, get_object_or_404
from .models import Result, Team
from django.views import generic
from whr import whole_history_rating
from datetime import timedelta, date

START_DATE = date(2023, 10, 1)

class TeamSerializer(Serializer):
    def get_dump_object(self, obj):
        if isinstance(obj, Team):
            return str(obj)
        return super().get_dump_object(obj)

def compute_ratings(results):
    serializer = TeamSerializer()
    whr = whole_history_rating.Base({'w2': 14, 'uncased': True})
    if len(results) > 0:
        first_day = results[0].date
        team_names = {};
        for result in results:
            whr.create_game(str(result.winner), str(result.loser), 'B',
                            (result.date - first_day).days, 0)
            team_names[str(result.winner).upper()] = result.winner
            team_names[str(result.loser).upper()] = result.loser
        whr.auto_iterate(time_limit = 60, precision = 10E-3)
        ordered_ratings = whr.get_ordered_ratings(current = True,
                                                  compact = False)
        res = []
        for i in reversed(range(len(ordered_ratings))):
            ratings = []
            for hist in whr.ratings_for_player(ordered_ratings[i][0]):
                date = first_day + timedelta(days=hist[0])
                ratings.append([str(date), hist[1] + 1500, hist[2]])
            team = team_names[ordered_ratings[i][0].upper()]
            p1cat = team.players.first().category.first()
            p2cat = team.players.last().category.first()
            cat = str(p1cat) + ' - ' + str(p2cat)
            res.append({
                'name': team,
                'cat': cat,
                'elo': ratings[-1][1],
                'matches': team.lost_to.filter(date__gt=START_DATE).union(team.won_against.filter(date__gt=START_DATE)).count(),
                'faces': serializer.serialize(Team.objects.filter(
                    pk__in=list(team.lost_to.values_list('winner', flat=True).union(
                        team.won_against.values_list('loser', flat=True)))))
            })
        return res

def index(request, genre='m'):
    """View function for the home page."""

    results = Result.objects.filter(genre__exact = genre,
                                    date__gt = START_DATE)
    ratings = compute_ratings(results)
    context = { 'ratings': [], 'serialized_ratings': []}
    if ratings is not None:
        context = {
            'ratings': ratings,
            'serialized_ratings': [{
                'name': str(t['name']),
                'elo': t['elo'],
                'faces': t['faces']
            } for t in ratings],
        }


    return render(request, 'index.html', context=context)

class ResultListView(generic.ListView):
    model = Result

    def get_queryset(self):
        self.genre = self.kwargs.get('genre', 'M')
        return Result.objects.filter(genre = self.genre,
                                     date__gt = START_DATE)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the genre
        context['genre'] = self.genre
        return context

class TeamInfoView(generic.DetailView):
    model = Team
