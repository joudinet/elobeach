from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Category(models.Model):
    """Model representing a Player category."""
    name = models.CharField(max_length=64, help_text='Enter a player category')

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Player(models.Model):
    """Model representing a player."""
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    SEX_OPTIONS = (
        ('F', 'Feminin'),
        ('M', 'Masculin'),
        )
    sex = models.CharField(max_length=1, choices=SEX_OPTIONS)
    category = models.ManyToManyField(Category,
                                      help_text='Select player\'s categories')
    license_id = models.PositiveIntegerField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ['lastname', 'firstname']

    def display_category(self):
        """Creates a string for the Category."""
        return ', '.join([category.name for category in self.category.all()])

    display_category.short_description = 'Category'

    def get_absolute_url(self):
        """Returns the url to access a particular player instance."""
        return reverse('player-info', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0} {1}'.format(self.lastname, self.firstname)

class Team(models.Model):
    """Model representing a team."""
    players = models.ManyToManyField(Player,
                                     help_text="Select the team\'s players")

    def display_players(self):
        """Creates a string for the players."""
        return ' / '.join([str(player) for player in self.players.all()])

    display_players.short_description = 'Players'

    def get_absolute_url(self):
        """Returns the url to access a particular player instance."""
        return reverse('team-info', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return ' / '.join([str(player) for player in self.players.all()])

class Result(models.Model):
    GENRE_OPTIONS = (
        ('F', 'Feminin'),
        ('M', 'Masculin'),
        ('X', 'Mixte'),
        )
    genre = models.CharField(max_length=1, choices=GENRE_OPTIONS)
    date = models.DateField()
    winner = models.ForeignKey(Team, on_delete=models.CASCADE,
                              related_name='won_against')
    loser = models.ForeignKey(Team, on_delete=models.CASCADE,
                              related_name='lost_to')

    class Meta:
        ordering = ['date']

    def __str__(self):
        """String for representing the Model object."""
        return '{0}: {1} WON AGAINST {2}'.format(self.date,
                                                 self.winner,
                                                 self.loser)
