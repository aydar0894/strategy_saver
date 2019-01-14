from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
# from PRIPS_workflow import run_workflow
from .MatrixCalculation import MultiplierCorrelationCalculator, MongoConnector
import json
from bson import ObjectId

from pymongo import MongoClient


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class MatrixForm(forms.Form):
    json_representation = forms.CharField()
    ast = forms.CharField()
    id = forms.CharField()
    user_id = forms.CharField()
    bot_name = forms.CharField()
    bot_description = forms.CharField()
    frontend_graph = forms.CharField()


@csrf_exempt
def add_error_code(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        code = request.GET.get('code')
        description = request.GET.get('description')

        error_codes = db.error_codes
        result = {}
        document = error_codes.insert_one({'code' : code, 'description': description})

        return JsonResponse({"message": "Success"}, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)

@csrf_exempt
def get_backtester_error_codes(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        error_codes = db.error_codes
        result = {}
        cursor = error_codes.find()
        i = 0
        for document in cursor:
            result.update({str(i): JSONEncoder().encode(document)})
            i +=1
        return JsonResponse(result, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)

# Strategies ----------------------------------------------------------------

@csrf_exempt
def remove_bot_by_id(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        bot_id = message = request.GET.get('id')
        strategies = db.strategies
        result = {}
        cursor = strategies.delete_one({'_id': ObjectId(bot_id)})
        i = 0
        for document in cursor:
            result.update({str(i): JSONEncoder().encode(document)})
            i +=1
        return JsonResponse(result, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)

@csrf_exempt
def get_bot_by_id(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        bot_id = message = request.GET.get('id')
        strategies = db.strategies
        result = {}
        cursor = strategies.find({'_id': ObjectId(bot_id)}, {'_id': 1, 'bot_description': 1, 'bot_name': 1, 'user_id': 1, 'ast': 1, 'frontend_graph': 1, 'json_representation': 1})
        i = 0
        for document in cursor:
            result.update({str(i): JSONEncoder().encode(document)})
            i +=1
        return JsonResponse(result, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)


@csrf_exempt
def get_user_strategies(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        user_id = message = request.GET.get('user_id')
        strategies = db.strategies
        result = {}
        cursor = strategies.find({'user_id': user_id}, {'_id': 1,'bot_description':1, 'bot_name': 1, 'user_id': 1, 'ast': 1, 'frontend_graph': 1, 'json_representation': 1})
        i = 0
        for document in cursor:
            result.update({str(i): JSONEncoder().encode(document)})
            i +=1
        return JsonResponse(result, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)

@csrf_exempt
def get_user_published_strategies(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        user_id = message = request.GET.get('user_id')
        strategies = db.strategies
        result = {}
        cursor = strategies.find({'user_id': user_id, 'published': 'True'}, {'_id': 1,'bot_description':1, 'bot_name': 1, 'user_id': 1, 'ast': 1, 'frontend_graph': 1, 'json_representation': 1})
        i = 0
        for document in cursor:
            result.update({str(i): JSONEncoder().encode(document)})
            i +=1
        return JsonResponse(result, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)

@csrf_exempt
def published_strategies_list(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        strategies = db.strategies
        result = {}
        cursor = strategies.find({'published': 'True'}, {'_id': 1, 'bot_description': 1, 'bot_name': 1, 'user_id': 1, 'ast': 1, 'frontend_graph': 1, 'json_representation': 1})
        i = 0
        for document in cursor:
            result.update({str(i): JSONEncoder().encode(document)})
            i +=1
        return JsonResponse(result, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)


@csrf_exempt
def strategies_list(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        strategies = db.strategies
        result = {}
        cursor = strategies.find({}, {'_id': 1, 'bot_description': 1, 'bot_name': 1, 'user_id': 1, 'ast': 1, 'frontend_graph': 1, 'json_representation': 1})
        i = 0
        for document in cursor:
            result.update({str(i): JSONEncoder().encode(document)})
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
            bot_description = form.cleaned_data['bot_description']
            frontend_graph = form.cleaned_data['frontend_graph']

            strategy_id = strategies.insert_one({'published': 'False', 'user_id': user_id, 'bot_name' : bot_name, 'bot_description': bot_description, 'frontend_graph': frontend_graph, 'ast': ast, 'json_representation': json_representation}).inserted_id

            return JsonResponse({"message": "Success", "id": str(strategy_id)}, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)

@csrf_exempt
def publish_strategy(request):

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
            bot_description = form.cleaned_data['bot_description']
            frontend_graph = form.cleaned_data['frontend_graph']

            strategy_id = strategies.insert_one({'published': 'True', 'user_id': user_id, 'bot_name' : bot_name, 'bot_description': bot_description, 'frontend_graph': frontend_graph, 'ast': ast, 'json_representation': json_representation}).inserted_id

            return JsonResponse({"message": "Success", "id": str(strategy_id)}, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)

@csrf_exempt
def update_by_id(request):
    if request.method == 'POST':
        form = MatrixForm(request.POST)
        if form.is_valid():
            client = MongoClient('localhost',
                            authSource='bitcoin')
            db = client.bitcoin
            bot_id = message = request.GET.get('id')
            strategies = db.strategies
            json_representation = form.cleaned_data['json_representation']
            ast  = form.cleaned_data['ast']
            user_id = form.cleaned_data['user_id']
            bot_name = form.cleaned_data['bot_name']
            bot_description = form.cleaned_data['bot_description']
            frontend_graph = form.cleaned_data['frontend_graph']
            bot_id = form.cleaned_data['id']


            result = {}
            document = strategies.find_and_modify({'_id': ObjectId(bot_id)}, {'published': 'False', 'user_id': user_id, 'bot_name' : bot_name, 'bot_description': bot_description, 'frontend_graph': frontend_graph, 'ast': ast, 'json_representation': json_representation})

            return JsonResponse(JSONEncoder().encode(document), safe=False)
    return JsonResponse({"message": "Error"}, safe=False)


# User Layouts ----------------------------------------------------------------

class LayoutsForm(forms.Form):
    json_representation = forms.CharField()
    email = forms.CharField()
    title = forms.CharField()
    description = forms.CharField()


@csrf_exempt
def remove_layout_by_id(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        layout_id = message = request.GET.get('id')
        user_layouts = db.user_layouts
        result = {}
        cursor = user_layouts.delete_one({'_id': ObjectId(layout_id)})
        i = 0
        for document in cursor:
            result.update({str(i): JSONEncoder().encode(document)})
            i +=1
        return JsonResponse(result, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)

@csrf_exempt
def get_layout_by_id(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        layout_id = message = request.GET.get('id')
        user_layouts = db.user_layouts
        result = {}
        cursor = user_layouts.find({'_id': ObjectId(layout_id)})
        i = 0
        for document in cursor:
            result.update({str(i): JSONEncoder().encode(document)})
            i +=1
        return JsonResponse(result, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)


@csrf_exempt
def get_user_layouts(request):
    if request.method == 'GET':
        client = MongoClient('localhost',
                        authSource='bitcoin')
        db = client.bitcoin
        email = message = request.GET.get('email')
        user_layouts = db.user_layouts
        result = {}
        cursor = user_layouts.find({'email': email})
        i = 0
        for document in cursor:
            result.update({str(i): JSONEncoder().encode(document)})
            i +=1
        return JsonResponse(result, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)



@csrf_exempt
def save_layout(request):

    if request.method == 'POST':
        form = LayoutsForm(request.POST)
        print(form)
        if form.is_valid():
            client = MongoClient('localhost',
                            authSource='bitcoin')

            db = client.bitcoin
            user_layouts = db.user_layouts

            json_representation = form.cleaned_data['json_representation']
            email = form.cleaned_data['email']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']

            user_layout_id = user_layouts.insert_one({'email': email, 'title' : title, 'description': description, 'json_representation': json_representation}).inserted_id

            return JsonResponse({"message": "Success", "id": str(user_layout_id)}, safe=False)
    return JsonResponse({"message": "Error"}, safe=False)


@csrf_exempt
def update_layout_by_id(request):
    if request.method == 'POST':
        form = MatrixForm(request.POST)
        if form.is_valid():
            client = MongoClient('localhost',
                            authSource='bitcoin')
            db = client.bitcoin
            user_layouts = db.user_layouts

            json_representation = form.cleaned_data['json_representation']
            email = form.cleaned_data['email']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            id = form.cleaned_data['id']


            result = {}
            document = strategies.find_and_modify({'_id': ObjectId(id)}, {'email': email, 'title' : title, 'description': description, 'json_representation': json_representation})

            return JsonResponse(JSONEncoder().encode(document), safe=False)
    return JsonResponse({"message": "Error"}, safe=False)
