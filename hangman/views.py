from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
import random
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from . import models
import operator

class RegisterUser(CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'cadastrousuario.html'

class RegisterWord(CreateView):
    model = models.Word
    template_name = 'cadastropalavra.html'
    success_url = reverse_lazy('home')
    fields = ['word', 'clue']

class CreateMatch(ListView):
    model = models.Match
    template_name = 'partida.html'
    def post(self, form):
        if (models.Match.objects.filter(user_id = self.request.user.pk)):
            partida_user = models.Match.objects.get(user_id = self.request.user.pk)
            if (partida_user.status == 1):
                models.Match.objects.filter(user_id=self.request.user.pk).delete()
                palavras = models.Word.objects.all()
                list_id = []
                for x in palavras:
                    list_id.append(x.id)
                id_selecionado = random.choice(list_id)
                print (id_selecionado)
                palavraObj = models.Word.objects.get(id = id_selecionado)
                criacao = models.Match.objects.create(user_id=self.request.user, word=palavraObj, status=2)
                criacao.save()
                return HttpResponseRedirect('/partida/')
            elif (partida_user.status == 2):
                return HttpResponseRedirect('/')
        else:
            palavras = models.Word.objects.all()
            list_id = []
            for x in palavras:
                list_id.append(x.id)
            id_selecionado = random.choice(list_id)
            print (id_selecionado)
            palavraObj = models.Word.objects.get(id = id_selecionado)
            criacao = models.Match.objects.create(user_id=self.request.user, word=palavraObj, status=2)
            criacao.save()
            return HttpResponseRedirect('/partida/')

class Win(ListView):
    model = models.Match
    template_name = 'win.html'

class GameMatch(ListView):
    model = models.Match
    template_name = 'jogo.html'
    key = []
    def get_context_data(self, **kwargs):
        kwargs['object_list'] = models.Match.objects.filter(user_id = self.request.user)
        palavra = kwargs['object_list'] 
        return super(GameMatch, self).get_context_data(**kwargs)
    def post(self, request):
        palavra_id = self.request.POST['palavra_id']
        match = models.Match.objects.get(pk = palavra_id)
        palavra = match.word.word.lower()
        palavra2 = set(list(palavra))
        print(self.key)
        if len(self.key) == len(palavra2):
            match.status = 1
            match.save()
            obj, created = models.Score.objects.get_or_create(user = self.request.user)
            obj.score = 10 - match.errors
            obj.save()
            self.key = []
            return HttpResponseRedirect('/win/')
        elif ('letra' in self.request.POST):
            if (self.request.POST['letra'].lower() in palavra):
                self.key.append(self.request.POST['letra'].lower())
            else:
                match.errors += 1
                match.save()

        return HttpResponseRedirect('/partida/')


# class MatchEmAndamento(ListView):

class RankingView(ListView):
    model = models.Score
    template_name = 'ranking.html'

    def get_queryset(self):

        scores = models.Score.objects.all()
        lista = []

        for x in scores:
            lista.append(x)

        lista.sort(key=operator.attrgetter('score','user.username'), reverse=True)

        print(lista)
        return lista