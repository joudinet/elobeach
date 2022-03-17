from django.contrib import admin
from .models import Category, Player, Result, Team

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_filter = ('genre',)

class WonResultsInline(admin.TabularInline):
    model = Result
    fk_name = "winner"
    extra = 0
    verbose_name = "victory"

class LostResultsInline(admin.TabularInline):
    model = Result
    fk_name = "loser"
    extra = 0
    verbose_name = "defeat"

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('display_players',)
    inlines = [WonResultsInline, LostResultsInline]

class TeamsInline(admin.TabularInline):
    model = Team.players.through
    extra = 0

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'sex', 'display_category')
    inlines = [TeamsInline]

admin.site.register(Category)
