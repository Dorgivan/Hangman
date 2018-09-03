from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta

now = datetime.now()
other_time = now + timedelta(hours=1)

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name='user1')
    score = models.IntegerField(default=0, verbose_name='pontuação')

    def __str__(self):
     return "%s - %s"%(self.score, self.user.username)
  
    class Meta:
        verbose_name = 'pontuação'
        verbose_name_plural = 'pontuações'

class Word(models.Model):
    word = models.CharField(max_length=15, verbose_name='palavra')
    clue = models.CharField(max_length=150, verbose_name='dica')

    def __str__(self):
     return "%s" %(self.word)
  
    class Meta:
        verbose_name = 'palavra'
        verbose_name_plural = 'palavras'

class Match(models.Model):
    aux = (
        (1, 'Finalizado'),
        (2, 'Não finalizado')
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user3_user', verbose_name='user1')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='Word')
    status = models.IntegerField(choices=aux)
    errors = models.IntegerField(verbose_name='erros', default=0)

    def __str__(self):
     return "%s" %(self.word)

    def erro(self):
        self.errors+=1
        return errors

    class Meta:
        verbose_name = 'partida'
        verbose_name_plural = 'partidas'
