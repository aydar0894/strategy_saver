from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
# from PRIPS_workflow import run_workflow
from .MatrixCalculation import MultiplierCorrelationCalculator, MongoConnector
import json
from pymongo import MongoClient



class MatrixForm(forms.Form):
    json_representation = forms.CharField()
    ast = forms.CharField()
    user_id = forms.CharField()
    name = forms.CharField()

@csrf_exempt
def save_strategy(request):

    if request.method == 'POST':
        form = MatrixForm(request.POST)
        # pprint(request.form)
        if form.is_valid():
            client = MongoClient('localhost',
                            authSource='bitcoin')

            db = client.bitcoin
            strategies = db.strategies

            json_representation = int(form.cleaned_data['json_representation'])
            ast  = form.cleaned_data['ast']
            user_id = form.cleaned_data['user_id']
            name = form.cleaned_data['name']

            strategies.update({'user_id': user_id, 'name' : name}, {'$set':  {'ast': ast, 'json_representation': json_representation}}, upsert=True)

            return JsonResponse(data, safe=False)
