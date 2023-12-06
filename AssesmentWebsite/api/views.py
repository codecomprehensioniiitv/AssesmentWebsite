from django.shortcuts import render

# Create your views here.

# Demographic
from .Demographic.views import *

from .Demographic.models import *
from .Demographic.serializers import *

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

user_id = None
question_bank_id = None
question_bank_level_id = None
code_id = None
evaluation_id = None


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

            return Response(
                {"msg": "Data Created", "user_id": user_id},
                status=status.HTTP_201_CREATED,
            )
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
        dic = request.data
        # dic['fuid'] = request.session['user_id']
        user_id = int(request.query_params["ffuid"])
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
def language(request):
    dic = request.data
    # dic['fuid'] = request.session['user_id']
    user_id = int(request.query_params["ffuid"])
    dic["fuid"] = user_id

    serializer = LanguageSerializer(data=dic)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Data Created"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# EVALUATION
from .Evaluation.models import *
from .Evaluation.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import collections
import csv
import pandas as pd

from .Demographic.models import *
from .Demographic.serializers import *
from .Questions.models import *


@api_view(["GET", "POST", "DELETE"])
def evaluation(request, pk=None):
    global evaluation_id
    if request.method == "GET":
        id = pk
        if id is not None:
            eval = Evaluation.objects.get(evid=id)
            serializer = EvaluationSerializer(eval)
            return Response(serializer.data)

        eval = Evaluation.objects.all()
        serializer = EvaluationSerializer(eval, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        dic = request.data
        print("D")
        user_id = int(request.query_params["ffuid"])

        dic["ffuid"] = user_id
        questionbanklang = int(Expertise.objects.get(fuid=user_id).selectedLanguage)

        dic["ffqbid"] = QuestionBank.objects.get(
            admin_programming_language=questionbanklang
        ).qbid

        print(user_id)
        serializer = EvaluationSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            # request.session['evaluation_id'] = Evaluation.objects.order_by('-evid')[0].evid
            evaluation_id = Evaluation.objects.order_by("-evid")[0].evid

            return Response(
                {"msg": "Data Created", "evaluation_id": evaluation_id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        id = pk
        eval = Evaluation.objects.get(evid=id)
        eval.delete()
        return Response({"msg": "Data Deleted"})


@api_view(["GET", "POST", "DELETE"])
def score(request, pk=None):
    print("quesry params", request.query_params)
    if request.method == "GET":
        id = pk
        if id is not None:
            stu = Score.objects.get(sid=id)
            serializer = ScoreSerializer(stu)
            return Response(serializer.data)

        stu = Score.objects.all()
        serializer = ScoreSerializer(stu, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        print("hello post ")
        print("request data", request.data)
        evaluation_id = int(request.query_params["evid"])
        user_id = int(request.query_params["ffuid"])
        dic = request.data

        dic["fevid"] = evaluation_id
        # dic['fevid'] = None
        #   questionbankevaluation_id = 6
        # language = Expertise.objects.get(fuid=request.session['user_id']).programming_language
        language = int(Expertise.objects.get(fuid=user_id).selectedLanguage)
        temp_questionbank_id = int(
            QuestionBank.objects.get(admin_programming_language=language).qbid
        )
        queries = request.query_params

        temp_questionbanklevel_id = QuestionsBankLevel.objects.filter(
            fqbid=temp_questionbank_id, qlevel=int(queries["level"][0])
        ).first()
        #   temp_questionbank_id = QuestionBankEvaluation.objects.get(evqbid =questionbankevaluation_id).ffqbid
        #   queries = request.query_params
        temp_code_id = Code.objects.filter(fqblid=temp_questionbanklevel_id)[
            int(queries["code_no"][0])
        ].cid
        temp_question_id = Question.objects.filter(fcid=temp_code_id)[
            int(queries["question_no"][0])
        ].qid
        dic["fqid"] = temp_question_id
        if (
            dic["selected_answer"]
            == Question.objects.get(qid=temp_question_id).correct_option
        ):
            dic["marks"] = Question.objects.get(qid=temp_question_id).marks
            dic["decision"] = "1"
        else:
            dic["marks"] = 0
            dic["decision"] = "2"
        serializer = ScoreSerializer(data=dic)
        # print("questionbankevaluation_id id",questionbankevaluation_id)
        print("question bank evaluation data", dic)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Data Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        id = pk
        stu = Score.objects.get(sid=id)
        stu.delete()
        return Response({"msg": "Data Deleted"})


@api_view(["GET", "POST", "DELETE"])
def time(request, pk=None):
    print("quesry params", request.query_params)
    if request.method == "GET":
        id = pk
        if id is not None:
            stu = Time.objects.get(sid=id)
            serializer = TimeSerializer(stu)
            return Response(serializer.data)

        stu = Time.objects.all()
        serializer = TimeSerializer(stu, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        print("hello post ")
        print("request data", request.data)
        dic = request.data

        queries = request.query_params
        evaluation_id = int(queries["evid"])
        user_id = int(queries["ffuid"])

        dic["ffevid"] = evaluation_id

        language = int(Expertise.objects.get(fuid=user_id).selectedLanguage)
        temp_questionbank_id = int(
            QuestionBank.objects.get(admin_programming_language=language).qbid
        )

        temp_questionbanklevel_id = int(
            QuestionsBankLevel.objects.filter(
                fqbid=temp_questionbank_id, qlevel=queries["level"][0]
            )
            .first()
            .qblid
        )
        print("E")

        temp_code_id = int(
            Code.objects.filter(fqblid=temp_questionbanklevel_id)[
                int(queries["code_no"][0])
            ].cid
        )

        dic["fcfid"] = temp_code_id
        serializer = TimeSerializer(data=dic)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Data Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        id = pk
        stu = Time.objects.get(sid=id)
        stu.delete()
        return Response({"msg": "Data Deleted"})


def getlanguage(id):
    if id == 1:
        return "Python"
    if id == 2:
        return "C++"
    if id == 3:
        return "Javascript"


def getdecision(id):
    if id == "1":
        return "Y"
    else:
        return "N"


@api_view(["GET"])
def download(request):
    try:
        dic = {}
        dic["User"] = []
        dic["Programming language"] = []
        dic["code_reading_time"] = []

        dic["Correct answer"] = []
        dic["Selected answer"] = []
        dic["Marks"] = []

        dic["Decision"] = []

        iterative_question_id = []
        for i in range(6):
            iterative_question_id.append("1")
            iterative_question_id.append("2")
            iterative_question_id.append("3")
            iterative_question_id.append("4")
            iterative_question_id.append("5")

        dic["Question"] = []
        levelArr = [0] * 10 + [1] * 10 + [2] * 10
        dic["Level"] = []

        user_ids = Demographic.objects.values_list("uid", flat=True)

        all_data = []
        for user_id in user_ids:
            uid = int(user_id)
            question_ids = []
            correct_answers = []
            selected_answers = []
            marks = []
            decisions = []
            code_ids = []
            time_code = []
            print(len(dic["Question"]))
            expertise = Expertise.objects.filter(fuid=uid)
            if len(expertise) == 0:
                continue
            program_language = int(expertise[0].selectedLanguage)
            levels = [1, 2, 3]
            question_bank_id = QuestionBank.objects.filter(
                admin_programming_language=program_language
            )
            if len(question_bank_id) == 0:
                continue
            question_bank_id = int(question_bank_id.first().qbid)

            question_bank_level_ids = []

            for level in levels:
                temp = QuestionsBankLevel.objects.filter(
                    fqbid=question_bank_id, qlevel=level
                )

                if len(temp) == 0:
                    continue
                question_bank_level_ids.append(int(temp[0].qblid))

            ind = -1
            for id in question_bank_level_ids:
                ind = ind + 1
                temp = Code.objects.filter(fqblid=id)
                if len(temp) == 0:
                    continue
                if len(temp) == 1:
                    code_ids.append(int(temp[0].cid))
                if len(temp) == 2:
                    code_ids.append(int(temp[0].cid))
                    code_ids.append(int(temp[1].cid))
            print("F")
            for id in code_ids:
                temp = Question.objects.filter(fcid=id)
                if len(temp) == 0:
                    continue
                question_ids.append(int(temp[0].qid))
                question_ids.append(int(temp[1].qid))
                question_ids.append(int(temp[2].qid))
                question_ids.append(int(temp[3].qid))
                question_ids.append(int(temp[4].qid))

            evaluations_id = Evaluation.objects.filter(
                ffuid=user_id, ffqbid=question_bank_id
            )
            print(len(dic["Question"]))

            if len(evaluations_id) == 0:
                continue
            evaluation_id = int(evaluations_id.first().evid)

            for id in question_ids:
                temp1 = Question.objects.filter(qid=id)
                if len(temp1) == 0:
                    continue
                correct_answers.append(int(temp1.first().correct_option))

                temp = Score.objects.filter(fevid=evaluation_id, fqid=id)
                if len(temp) == 0:
                    selected_answers.append("None")
                    marks.append(0)
                    decisions.append(2)
                    time_code.append("None")
                    continue
                temp = temp.first()
                selected_answers.append(temp.selected_answer)
                marks.append(temp.marks)
                decisions.append(temp.decision)

            times = Time.objects.filter(ffevid=evaluation_id)
            for time in times:
                time_code = time_code + [time.code_read_time] * 5

            n = len(question_ids)

            dic["User"] = dic["User"] + ([uid] * n)
            dic["Programming language"] = dic["Programming language"] + (
                [getlanguage(program_language)] * n
            )

            # this added
            dic["Question"] = dic["Question"] + iterative_question_id
            dic["Level"] = dic["Level"] + levelArr
            dic["Selected answer"] = dic["Selected answer"] + (selected_answers)
            dic["Correct answer"] = dic["Correct answer"] + (correct_answers)
            print("LLD")
            dic["Decision"] = dic["Decision"] + [
                getdecision(decision) for decision in decisions
            ]
            dic["Marks"] = dic["Marks"] + (marks)

            dic["code_reading_time"] = dic["code_reading_time"] + (time_code)
        print
        print(len(dic["code_reading_time"]))
        print(len(dic["User"]))
        print(len(dic["Question"]))
        print(len(dic["Marks"]))
        print(len(dic["Correct answer"]))
        print(len(dic["Selected answer"]))

        df = pd.DataFrame(dic)
        response = HttpResponse(content_type="text/csv")
        # your filename
        response["Content-Disposition"] = 'attachment; filename="data.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "S.No.",
                "User",
                "Programming language",
                "Level",
                "Code Read Time",
                "Question",
                "Selected answer",
                "Correct answer",
                "Decision",
                "Marks",
            ]
        )
        for ind in range(df.shape[0]):
            writer.writerow(
                [
                    ind,
                    df["User"][ind],
                    df["Programming language"][ind],
                    df["Level"][ind],
                    df["code_reading_time"][ind],
                    df["Question"][ind],
                    df["Selected answer"][ind],
                    df["Correct answer"][ind],
                    df["Decision"][ind],
                    df["Marks"][ind],
                ]
            )

        return response
        # for user_id in user_ids:
        #     program_language = Expertise.objects.get(fuid=int(user_id)).selectedLanguage
        #     print(program_language)
        #     levels = ["1", "2", "3"]
        #     print(user_id)
        #     question_bank_id = QuestionBank.objects.get(
        #         admin_programming_language=program_language
        #     ).qbid

        #     question_bank_level_ids = [
        #         int(
        #             QuestionsBankLevel.objects.get(
        #                 fqbid=question_bank_id, qlevel=level
        #             ).qblid
        #         )
        #         for level in levels
        #     ]

        #     code_ids = [
        #         int(Code.objects.get(fqblid=id).cid) for id in question_bank_level_ids
        #     ]

        #     question_ids = [int(Question.objects.get(fcid=id).qid) for id in code_ids]

        #     int(
        #         evaluation_id=Evaluation.objects.get(
        #             ffuid=user_id, ffqbid=question_bank_id
        #         ).evid
        #     )

        #     correct_answers = [
        #         int(Question.objects.get(qid=id).correct_option for id in question_ids)
        #     ]
        #     selected_answers = [
        #         int(Score.objects.get(fevid=evaluation_id, fqid=id).selected_answer)
        #         for id in question_ids
        #     ]
        #     marks = [
        #         int(Score.objects.get(fevid=evaluation_id, fqid=id).marks)
        #         for id in question_ids
        #     ]
        #     decisions = [
        #         getdecision(Score.objects.get(fevid=evaluation_id, fqid=id).decision)
        #         for id in question_ids
        #     ]

        #     times = Time.objects.filter(ffevid=evaluation_id)
        #     time_code = [time.code_read_time for time in times]
        #     time_que = [time.question_read_time for time in times]

        #     iterative_question_id = [f"Q{i+1}" for i in range(5)] * len(levels)

        #     dic = collections.defaultdict(list)
        #     n = len(question_ids)

        #     dic["User"] = [Demographic.objects.get(uid=user_id).name] * n
        #     dic["Programming language"] = [getlanguage(program_language)] * n
        #     dic["Level"] = (
        #         (["E"] * int(n / 3)) + (["M"] * int(n / 3)) + (["H"] * int(n / 3))
        #     )
        #     dic["Code"] = (
        #         (["c1"] * int(n / 6))
        #         + (["c2"] * int(n / 6)) * 2
        #         + (["c1"] * int(n / 6))
        #         + (["c2"] * int(n / 6))
        #     )
        #     dic["Question"] = iterative_question_id
        #     dic["Selected answer"] = selected_answers
        #     dic["Correct answer"] = correct_answers
        #     dic["Decision"] = decisions
        #     dic["Marks"] = marks
        #     dic["question_time"] = (
        #         ([time_que[0]] * int(n / 6)) * 2
        #         + ([time_que[1]] * int(n / 6)) * 2
        #         + ([time_que[2]] * int(n / 6)) * 2
        #     )
        #     dic["code_time"] = (
        #         ([time_code[0]] * int(n / 6)) * 2
        #         + ([time_code[1]] * int(n / 6)) * 2
        #         + ([time_code[2]] * int(n / 6)) * 2
        #     )

        #     all_data.append(pd.DataFrame(dic))

        # all_data_df = pd.concat(all_data, ignore_index=True)

        # response = HttpResponse(content_type="text/csv")
        # response["Content-Disposition"] = 'attachment; filename="all_data.csv"'
        # writer = csv.writer(response)
        # writer.writerow(
        #     [
        #         "S.No.",
        #         "User",
        #         "Programming language",
        #         "Level",
        #         "Code",
        #         "Code Read Time",
        #         "Question",
        #         "Question Read Time",
        #         "Selected answer",
        #         "Correct answer",
        #         "Decision",
        #         "Marks",
        #     ]
        # )

        # for ind in range(all_data_df.shape[0]):
        #     writer.writerow(
        #         [
        #             ind,
        #             all_data_df["User"][ind],
        #             all_data_df["Programming language"][ind],
        #             all_data_df["Level"][ind],
        #             all_data_df["Code"][ind],
        #             all_data_df["code_time"][ind],
        #             all_data_df["Question"][ind],
        #             all_data_df["question_time"][ind],
        #             all_data_df["Selected answer"][ind],
        #             all_data_df["Correct answer"][ind],
        #             all_data_df["Decision"][ind],
        #             all_data_df["Marks"][ind],
        #         ]
        #     )

        # return response
    except Exception as e:
        print("Exception", e)
        return Response(
            {"msg": "Sorry, not able to generate CSV."}, status=status.HTTP_201_CREATED
        )


@api_view(["GET"])
def getCSV(request):
    if request.method == "GET":
        # if id is not None:
        #     stu = Demographic.objects.get(uid=id)
        #     serializer = DemographicSerializer(stu)
        #     return Response(serializer.data)
        all_evals = Evaluation.objects.all()
        stu_eval_id = []
        for eval in all_evals:
            stu_eval_id.append(eval.ffuid.uid)
        print(stu_eval_id)
        stu = Demographic.objects.filter(uid__in=stu_eval_id)
        serializer = DemographicSerializer(stu, many=True)
        print(serializer.data)
        return Response(serializer.data)


def getLevel(level):
    if level == "1":
        return "Novice"
    elif level == "2":
        return "Intermediate"
    else:
        return "Expert"


def getGender(gender):
    if gender == "1":
        return "Female"
    elif gender == "2":
        return "Male"
    else:
        return "Other"


def getRole(role):
    if role == "1":
        return "Student"
    elif role == "2":
        return "Industralist"
    else:
        return "Proffessor"


@api_view(["GET"])
def getUsersData(request):
    # all users
    dic = {}
    users = Demographic.objects.all()
    # finding Their Expertise
    dic["UserID"] = []
    dic["Role"] = []
    dic["Gender"] = []
    dic["Age"] = []
    dic["Language_Name"] = []
    dic["Expertise_In_Language"] = []
    dic["Time_In_Language"] = []
    dic["Frequency"] = []
    for user in users:
        exp = Expertise.objects.filter(fuid=user.uid)
        if len(exp) == 0:
            continue
        exp = exp.first()
        dic["UserID"].append(user.uid)
        dic["Role"].append(getRole(user.profession))
        dic["Gender"].append(getGender(user.gender))
        dic["Age"].append(user.age)

        dic["Language_Name"].append(getlanguage(int(exp.selectedLanguage)))
        dic["Expertise_In_Language"].append(getLevel(exp.level))
        dic["Time_In_Language"].append(exp.duration)
        dic["Frequency"].append(exp.time)

        # OTHER LANGUAGES CODE IS WRITTEN HERE ::
        langs = Language.objects.filter(fuid=user.uid)

        for lang in langs:
            dic["UserID"].append(user.uid)
            dic["Role"].append(getRole(user.profession))
            dic["Gender"].append(getGender(user.gender))
            dic["Age"].append(user.age)

            dic["Language_Name"].append(getlanguage(int(lang.selectedLanguage)))
            dic["Expertise_In_Language"].append(getLevel(lang.level))
            dic["Time_In_Language"].append(lang.duration)
            dic["Frequency"].append(lang.time)

    print(dic)
    df = pd.DataFrame(dic)
    response = HttpResponse(content_type="text/csv")
    # your filename
    response["Content-Disposition"] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "S.No.",
            "UserId",
            "Role",
            "Gender",
            "Age",
            "Experimental_Language_Name",
            "Expertise_In_Experimental_Language",
            "Time_In_Experimental_Language",
            "Frequency",
        ]
    )
    for ind in range(df.shape[0]):
        print(ind)
        writer.writerow(
            [
                ind,
                df["UserID"][ind],
                df["Role"][ind],
                df["Gender"][ind],
                df["Age"][ind],
                df["Language_Name"][ind],
                df["Expertise_In_Language"][ind],
                df["Time_In_Language"][ind],
                df["Frequency"][ind],
            ]
        )

    return response


#### Questionsgi


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


from .Questions.models import *
from .Questions.serializers import *
from .Demographic.serializers import Expertise


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
            return Response(
                {"msg": "Data Created", "question_bank_id": question_bank_id},
                status=status.HTTP_201_CREATED,
            )
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

            return Response(
                {
                    "msg": "Data Created",
                    "question_bank_level_id": question_bank_level_id,
                },
                status=status.HTTP_201_CREATED,
            )
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

            return Response(
                {"msg": "Data Created", "code_id": code_id},
                status=status.HTTP_201_CREATED,
            )
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
        queries = request.query_params
        level = int(queries["level"])
        codeNo = int(queries["code"])
        user_id = int(queries["ffuid"])
        programming_language = int(Expertise.objects.get(fuid=user_id).selectedLanguage)

        question_bank_id = int(
            QuestionBank.objects.filter(admin_programming_language=programming_language)
            .first()
            .qbid
        )

        qblid = int(
            QuestionsBankLevel.objects.filter(
                fqbid=question_bank_id,
                qlevel=level,
            )
            .first()
            .qblid
        )

        # request.session['question_code_id'] = Code.objects.filter(fqblid = level)[int(queries['code'][0])].cid
        user_code_id = int(Code.objects.filter(fqblid=qblid)[codeNo].cid)
        print(user_code_id)
        # stu = Code.objects.get(cid=request.session['question_code_id'])
        stu = Code.objects.get(cid=user_code_id)
        serializer = CodeSerializer(stu)
        return Response(serializer.data)


@api_view(["GET"])
def getquestion(request):
    if request.method == "GET":
        # request.session['question_code_id'] = 1
        # question_code_id = 10
        # print("quesry params", request.query_params)
        # # user_id = 1
        queries = request.query_params
        index = int(queries["question"][0])
        fcid = int(queries["fcid"])
        question_code_id = Question.objects.filter(fcid=fcid)[index].qid
        print(question_code_id)
        stu = Question.objects.get(qid=question_code_id)
        serializer = QuestionSerializer(stu)
        return Response(serializer.data)
