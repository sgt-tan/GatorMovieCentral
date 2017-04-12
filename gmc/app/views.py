# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from app.db_query import *

@csrf_exempt
def home(request):
    return render(request, 'index.html', {'tuple_count': tuple_count()})

@csrf_exempt
def results(request):
    return render_to_response('results.html', {'query': request.GET['q'], 'movies': search_movie(request.GET['q']), 'people': search_person(request.GET['q'])})

@csrf_exempt
def person(request, id):
    return render(request, 'person.html', {})

@csrf_exempt
def movie(request, id):
    return render(request, 'movie.html', {})
