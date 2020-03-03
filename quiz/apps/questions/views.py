from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .models import Quiz, Question, Score
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib import messages

import os.path
from django.db import connection

# Create your views here.
def premain (request):
    return render(request, 'questions/premain.html',)

def quizes(request):
    quiz_list = Quiz.objects.all()
    return render(request, 'questions/quizes.html', {'quiz_list':quiz_list})

def questions_list(request):
    try:
        questions_list = Question.objects.order_by('question_list')
        return render(request, 'questions/question_list.html', {'questions_list': questions_list})


    except:
        raise Http404 ('Question_list не найден')


def question(request, question_id, quiz_id):

    try:
        quiz_num = Quiz.objects.get(id=quiz_id)
        question_setup = quiz_num.question_set.all()[question_id]
        questions_quant = int(quiz_num.question_set.count())
        next_question_id = int(question_id)+ 1
        prev_question_id = int(question_id) - 1
        variant_1 = question_setup.variant_1
        variant_2 = question_setup.variant_2
        variant_3 = question_setup.variant_3
        correct_var = question_setup.correct_var
        value = question_setup.value
        cursor = connection.cursor()
        user = request.user.get_username()
        sql_record_for_question = """SELECT questions_question.question_text, questions_score.score, auth_user.username 
        FROM questions_score 
        LEFT JOIN questions_question ON questions_score.question_id = questions_question.id
        LEFT JOIN auth_user on questions_score.user_id = auth_user.id
        WHERE auth_user.username = '%s' and questions_question.question_text = '%s'""" %(user, question_setup)
        cursor.execute(sql_record_for_question)
        total = cursor.fetchall()
        cursor.close()
        #print(user, total)




    except:
        raise Http404 ('Вопрос не найден')


    if request.POST.get('var') == correct_var:
    # if request.POST.get('search_text')==correct_var:
        cursor = connection.cursor()
        user = request.user.get_username()
        sql_record = """SELECT questions_question.question_text, questions_score.score, auth_user.username 
        FROM questions_score 
        LEFT JOIN questions_question ON questions_score.question_id = questions_question.id
        LEFT JOIN auth_user on questions_score.user_id = auth_user.id
        WHERE auth_user.username = '%s' and questions_question.question_text = '%s'""" %(user, question_setup)
        cursor.execute(sql_record)
        results = cursor.fetchall()
        cursor.close()
        if user == "" and results == []:
            # messages.add_message(request, messages.SUCCESS, 'Правильно!')
            pass
        elif user != "" and results == []:
            pass # перенесена в check_is_correct
        elif user != "" and results != []:
            player = results[0][2]
            # messages.add_message(request, messages.SUCCESS, ('Правильно! Игрок {} отгадал вопрос раньше и получил {} очков').format(player, value))
        cursor.close()

        return render(request, 'questions/question.html',
                      {'question_setup': question_setup, "variant_1": variant_1, "variant_2": variant_2,
                       "variant_3": variant_3, 'correct_var':correct_var, 'next_question_id':next_question_id,
                       'prev_question_id':prev_question_id, 'quiz_id':quiz_id, 'questions_quant':questions_quant, 'value':value})


        #return HttpResponse(request.POST.get('var'))
    elif request.POST.get('var') != correct_var and request.POST.get('var') == variant_1 or request.POST.get('var') == variant_2 \
            or request.POST.get('var') == variant_3  :
        # messages.add_message(request, messages.SUCCESS, 'Неправильно!')
        return render(request, 'questions/question.html',
                      {'question_setup': question_setup, "variant_1": variant_1, "variant_2": variant_2,
                       "variant_3": variant_3, 'correct_var':correct_var, 'next_question_id':next_question_id,
                       'prev_question_id':prev_question_id, 'quiz_id':quiz_id, 'questions_quant':questions_quant})

    else :
        return render(request, 'questions/question.html',
                      {'question_setup': question_setup, "variant_1": variant_1, "variant_2": variant_2,
                       "variant_3": variant_3, 'correct_var':correct_var, 'next_question_id':next_question_id,
                       'prev_question_id':prev_question_id, 'quiz_id':quiz_id, 'questions_quant':questions_quant})

    #return render(request, 'questions/question.html', {'question_setup': question_setup, "variant_1":variant_1, "variant_2":variant_2,"variant_3":variant_3})
#

def quiz_details(request, quiz_id):

    
    a = Quiz.objects.get(id=quiz_id)
    cursor = connection.cursor()
    user = request.user.get_username()
    if user != "":
    
        select_questions_list = """select questions_question.id, questions_question.question_text from questions_question where questions_question.quiz_id = '%s' order by id""" %(quiz_id)
        # print('select_questions_list', select_questions_list)
        cursor.execute(select_questions_list)
        quest_list = cursor.fetchall()
        x = []
        for quest in quest_list:
            x.append(quest)
        #print(x)
        
        select_user_id_in_quiz = """select auth_user.id
                from auth_user
                WHERE auth_user.username = '%s'""" %(user,)
        cursor.execute(select_user_id_in_quiz)
        user_id = cursor.fetchall()

        select_done_score = """select questions_question.id, question_text from questions_question 
        left join questions_quiz on questions_question.quiz_id = questions_quiz.id
        WHERE questions_quiz.id = '%s' order by 1 """ %(quiz_id)
        cursor.execute(select_done_score)
        new_data = cursor.fetchall()
        data_sent_to_template = []
        for elem in new_data:
            print(user_id[0][0], elem[0])
            select_score_for_question = """ select score from questions_score where user_id = %s and question_id = %s"""%(user_id[0][0], elem[0])
            cursor.execute(select_score_for_question)
            score_for_the_question = cursor.fetchall()
            print(score_for_the_question)
            if score_for_the_question!=[]:
                print(score_for_the_question[0])
                elem = elem+score_for_the_question[0]
                print(elem)
                data_sent_to_template.append(elem)
            else:
                elem = elem+(0,)
                print(elem)
                data_sent_to_template.append(elem)
        print(data_sent_to_template)
        

    elif user == "":
        a = Quiz.objects.get(id=quiz_id)
        data_sent_to_template = a.question_set.all() 
        print(data_sent_to_template)


    return render(request, 'questions/question_list.html', {'data_sent_to_template':data_sent_to_template})



def login_user(request):
    #logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../../quizes')
    return render(request, 'questions/login.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect("../../quizes")
    else:
        form = UserCreationForm()
    return render(request, 'questions/signup.html', {'form': form})


def LogoutView(request):
    logout(request)

    # После чего, перенаправляем пользователя на главную страницу.
    return HttpResponseRedirect("../../quizes")

def check_is_correct(request, question_id, quiz_id):

    quiz_num = Quiz.objects.get(id=quiz_id)
    question_setup = quiz_num.question_set.all()[question_id]
    correct_var = question_setup.correct_var
    value = question_setup.value
    print(request.POST)
    # print(request.POST.get('search_text'))
    if request.POST.get('search_text')==correct_var:
        print(request.POST.get('search_text'))
        cursor = connection.cursor()
        user = request.user.get_username()
        sql_record = """SELECT questions_question.question_text, questions_score.score, auth_user.username 
        FROM questions_score 
        LEFT JOIN questions_question ON questions_score.question_id = questions_question.id
        LEFT JOIN auth_user on questions_score.user_id = auth_user.id
        WHERE auth_user.username = '%s' and questions_question.question_text = '%s'""" %(user, question_setup)
        cursor.execute(sql_record)
        results = cursor.fetchall()
        cursor.close()
        print(user, results)
        if user == "" and results == []:
            return HttpResponse("Верно")
        elif user != "" and results == []:
            user_for_input = request.user.get_username()
            select_user_id = """select auth_user.id
            from auth_user
            WHERE auth_user.username = '%s'""" %(user,)
            cursor = connection.cursor()
            cursor.execute(select_user_id)
            user_id = cursor.fetchall()
            select_questions_id = """SELECT id from questions_question where question_text = '%s'""" %(question_setup,)
            cursor.execute(select_questions_id)
            quest_id = cursor.fetchall()
            inserting_score = """INSERT INTO questions_score  (score, question_id, user_id) values ('%s', '%s', '%s')""" %(value, quest_id[0][0], user_id[0][0],)
            print('inserting_score',inserting_score) 
            cursor.execute(inserting_score)
            inserted_score = cursor.fetchall()
            cursor.close()
            return HttpResponse("Верно")
        elif user != "" and results != []:
            return HttpResponse("Верно")
    elif request.POST.get('search_text')!=correct_var:
        return HttpResponse("Неверно")