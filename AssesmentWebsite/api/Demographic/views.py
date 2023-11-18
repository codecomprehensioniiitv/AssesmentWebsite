from .models import *
from .serializers import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse

import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

global user_id
question_bank_id = None
question_bank_level_id = None
code_id = None
evaluation_id = None
# questionbankevaluation_id = None
user_code_id = None


@api_view(["GET", "POST", "DELETE"])
def demographic(request, pk=None):
    global user_id
    if request.method == "GET":
        id = pk
        if id is not None:
            stu = Demographic.objects.get(uid=id)
            serializer = DemographicSerializer(stu)
            return Response(serializer.data)

        stu = Demographic.objects.all()
        serializer = DemographicSerializer(stu, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = DemographicSerializer(data=request.data)
        # print("now i am here")
        if serializer.is_valid():
            serializer.save()
            # request.session['user_id'] = Demographic.objects.order_by('-uid')[0].uid
            user_id = Demographic.objects.order_by("-uid")[0].uid

            return Response({"msg": "Data Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        id = pk
        stu = Demographic.objects.get(uid=id)
        stu.delete()
        return Response({"msg": "Data Deleted"})


@api_view(["GET", "POST", "PUT", "DELETE"])
def expertise(request, pk=None):
    if request.method == "GET":
        id = pk
        if id is not None:
            id = str(id)
            exp = Expertise.objects.get(eid=id)
            serializer = ExpertiseSerializer(exp)
            return Response(serializer.data)
        exp = Expertise.objects.all()
        serializer = ExpertiseSerializer(exp, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        print("EH")
        dic = request.data
        # dic['fuid'] = request.session['user_id']
        dic["fuid"] = user_id

        serializer = ExpertiseSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Data Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PUT":
        id = pk
        exp = Expertise.objects.get(eid=id)
        serializer = ExpertiseSerializer(exp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Data Updated"})
        return Response(serializer.errors)

    if request.method == "DELETE":
        id = pk
        exp = Expertise.objects.get(eid=id)
        exp.delete()
        return Response({"msg": "Data Deleted"})


@api_view(["POST"])
def login1(request):
    if request.method == "POST":
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        user_name = pythondata.get("username", None)
        user_password = pythondata.get("password", None)
        user = authenticate(request, username=user_name, password=user_password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            json_data = json.dumps(
                {"ans": "login is successful", "token": token.key, "created": created}
            )
            return HttpResponse(json_data, content_type="application/json")
        else:
            json_data = json.dumps({"ans": "login is unsuccessful"})
            return HttpResponse(json_data, content_type="application/json")

    return HttpResponse(
        json.dumps({"result": "Please login yourself"}), content_type="application/json"
    )
