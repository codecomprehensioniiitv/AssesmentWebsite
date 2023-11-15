from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .models import *
from .serializers import *
from ..Demographic.serializers import Expertise


user_id = None
question_bank_id = None
question_bank_level_id = None
code_id = None
evaluation_id = None
user_code_id = None


@api_view(["GET", "POST", "DELETE"])
def questionbank(request, pk=None):
    global question_bank_id
    if request.method == "GET":
        id = pk
        if id is not None:
            quebank = QuestionBank.objects.get(qbid=id)
            serializer = QuestionBankSerializer(quebank)
            return Response(serializer.data)

        quebank = QuestionBank.objects.all()
        serializer = QuestionBankSerializer(quebank, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        dic = request.data
        serializer = QuestionBankSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            # request.session['question_bank_id'] = QuestionBank.objects.order_by('-qbid')[0].qbid
            question_bank_id = QuestionBank.objects.order_by("-qbid")[0].qbid

            # print("question_bank_id", request.session['question_bank_id'])
            return Response({"msg": "Data Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        id = pk
        quebank = QuestionBank.objects.get(qbid=id)
        quebank.delete()
        return Response({"msg": "Data Deleted"})


@api_view(["GET", "POST", "DELETE"])
def questionbanklevel(request, pk=None):
    global question_bank_level_id
    if request.method == "GET":
        id = pk

        if id is not None:
            quebanklevel = QuestionsBankLevel.objects.get(qblid=id)
            serializer = QuestionBankLevelSerializer(quebanklevel)
            return Response(serializer.data)
        print("********************************")
        quebanklevel = QuestionsBankLevel.objects.all()
        serializer = QuestionBankLevelSerializer(quebanklevel, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        dic = request.data
        # dic['fqbid'] = request.session['question_bank_id']
        dic["fqbid"] = question_bank_id

        serializer = QuestionBankLevelSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            # request.session['question_bank_level_id'] = QuestionsBankLevel.objects.order_by('-qblid')[0].qblid
            question_bank_level_id = QuestionsBankLevel.objects.order_by("-qblid")[
                0
            ].qblid

            return Response({"msg": "Data Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        id = pk
        quebanklevel = QuestionsBankLevel.objects.get(qblid=id)
        quebanklevel.delete()
        return Response({"msg": "Data Deleted"})


@api_view(["GET", "POST", "DELETE"])
def code(request, pk=None):
    global code_id
    if request.method == "GET":
        id = pk
        if id is not None:
            cod = Code.objects.get(cid=id)
            serializer = CodeSerializer(cod)
            return Response(serializer.data)

        cod = Code.objects.all()
        serializer = CodeSerializer(cod, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        dic = request.data
        # dic['fqblid'] = request.session['question_bank_level_id']
        dic["fqblid"] = question_bank_level_id

        serializer = CodeSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            # request.session['code_id'] = Code.objects.order_by('-cid')[0].cid
            code_id = Code.objects.order_by("-cid")[0].cid

            return Response({"msg": "Data Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        id = pk
        cod = code.objects.get(cid=id)
        cod.delete()
        return Response({"msg": "Data Deleted"})


@api_view(["GET", "POST", "DELETE"])
def question(request, pk=None):
    if request.method == "GET":
        id = pk
        if id is not None:
            que = Question.objects.get(qid=id)
            serializer = QuestionSerializer(que)
            return Response(serializer.data)

        que = Question.objects.all()
        serializer = QuestionSerializer(que, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        dic = request.data
        # dic['fcid'] = request.session['code_id']
        dic["fcid"] = code_id

        serializer = QuestionSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Data Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        id = pk
        que = Question.objects.get(qid=id)
        que.delete()
        return Response({"msg": "Data Deleted"})


@api_view(["GET"])
def getcode(request):
    global user_code_id
    if request.method == "GET":
        # user_id = 1\
        programming_language = Expertise.objects.get(fuid=user_id).programming_language
        question_bank_id = QuestionBank.objects.get(
            admin_programming_language=programming_language
        ).qbid
        queries = request.query_params
        level = QuestionsBankLevel.objects.get(
            fqbid=question_bank_id, qlevel=queries["level"][0]
        ).qblid
        # request.session['question_code_id'] = Code.objects.filter(fqblid = level)[int(queries['code'][0])].cid
        user_code_id = Code.objects.filter(fqblid=level)[int(queries["code"][0])].cid

        # stu = Code.objects.get(cid=request.session['question_code_id'])
        stu = Code.objects.get(cid=user_code_id)
        serializer = CodeSerializer(stu)
        return Response(serializer.data)


@api_view(["GET"])
def getquestion(request):
    if request.method == "GET":
        # request.session['question_code_id'] = 1
        # question_code_id = 1
        print("quesry params", request.query_params)
        # user_id = 1
        queries = request.query_params
        id = Question.objects.filter(fcid=user_code_id)[int(queries["question"][0])].qid
        stu = Question.objects.get(qid=id)
        serializer = QuestionSerializer(stu)
        return Response(serializer.data)
