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
    bot_name = forms.CharField()
    frontend_graph = forms.CharField()


@csrf_exempt
def strategies_list(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        strategies = db.strategies
        result = {}
        cursor = strategies.find({}, {'_id': 0, 'bot_name': 1, 'user_id': 1, 'ast': 1, 'frontend_graph': 1, 'json_representation': 1})
        i = 0
        for document in cursor:
            result.update({str(i): document})
            i +=1
        return JsonResponse(result, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)

@csrf_exempt
def save_strategy(request):

    if request.method == 'POST':
        form = MatrixForm(request.POST)
        print(form)
        if form.is_valid():
            client = MongoClient('localhost',
                            authSource='bitcoin')

            db = client.bitcoin
            strategies = db.strategies

            json_representation = form.cleaned_data['json_representation']
            ast  = form.cleaned_data['ast']
            user_id = form.cleaned_data['user_id']
            bot_name = form.cleaned_data['bot_name']
            frontend_graph = form.cleaned_data['frontend_graph']
            strategies.update({'user_id': user_id, 'bot_name' : bot_name}, {'$set':  {'frontend_graph': frontend_graph, 'ast': ast, 'json_representation': json_representation}}, upsert=True)

            return JsonResponse({"message": "Success"}, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)
