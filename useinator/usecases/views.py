from django.shortcuts import render, redirect
from usecases.forms import RegistrationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import connection
import psycopg2
from psycopg2.extras import NamedTupleCursor
from .models import Question, Result, Category, Project, Answer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def custom_query(query):
	cursor = connection.cursor()
	cursor.execute(query)
	row = cursor.fetchall()
	return row
	#with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
    #	cursor.execute('select * from tbl')
    #	for row in cursor.fetchall():
    #   	print(row.col1, row.col2)
	#cursor = psycopg2.connect(dbname='my_useinator_db', user='postgres', password='20142018', cursor_factory=NamedTupleCursor)
	#cursor.execute(query)
	#row = NamedTupleCursor(cursor)
	#return row

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		return render(request, 'usecases/index.html')


def register(request):
	if request.user.is_authenticated:
		return redirect('dashboard')

	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')

	else:
		form = RegistrationForm()
	
	args= {'form': form}
	return render(request, 'usecases/register.html', args)

def login(request):
	if request.user.is_authenticated:
		return redirect('dashboard')

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)

		if user is not None:
			auth_login(request, user)
			return redirect('dashboard')
		else:
			messages.error(request, 'Username and Password did not match.')
	else:

		return render(request, 'usecases/login.html')

	return render(request, 'usecases/login.html')

def logout(request):
	auth_logout(request)
	return redirect('index')
projectId1 = 0

def dashboard(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			project_data = Answer.objects.filter(project_id= request.POST['proj_id'])
			print(project_data)
			return render(request, 'usecases/diagram.html', {'data': project_data})

		else:
			projects = Project.objects.filter(user_id= request.user.id)
			#here preview past use cases
			return render(request, 'usecases/dashboard.html', {'data': projects})
		
		
	else:
		return redirect('index')

def create_usecase(request):
	global projectId1
	if not request.user.is_authenticated:
		return redirect('index')
	else:
		if request.method == 'POST':
			if not request.POST['sub_category'] == '':
				#print(request.POST['sub_category'])
				#create a use new use case or project in the database
				project = Project(project_name = request.POST['usecase_name'], user_id = request.user.id)
				project.save()
				project_value = Project.objects.filter(project_name = request.POST['usecase_name'])
				for item in project_value:
					projectId = item.project_id

				#print(projectId)
				projectId1 = projectId
				
				#return redirect('/create-usecase/quest/{}/'.format(projectStr))
				return redirect('quest')
			else:
				categories = Category.objects.all()
				return render(request, 'usecases/create-usecase.html', {'data': categories})
		else:
			return render(request, 'usecases/create-usecase.html')


initial_question = 1
first_route = True
d_child = 0

actor = []
case = []
case_data = []
actor_data = []
final_action_list = []

def quest(request):
	global first_route
	global d_child
	filtered_words = []
	userId = request.user.id
	#project = custom_query("SELECT project_id FROM usecases_project WHERE user_id = {}".format(userId))
	#last_project = project.latest('project_id')
	#for item in last_project:
		#print(item.project_id)
	#print(last_project)
	if request.method == 'POST':
		result_id = request.POST['res_id']
		entity_list = list(map(int, request.POST['entity_list'].split(',')))
		question_text = request.POST['quest_text']
		result_text = list(request.POST['res_text'].split(','))

		#print(result_text)
		
		splitted = question_text.split()
		stop_words = set(stopwords.words('english'))
		words = nltk.word_tokenize(question_text)
		for word in words:
			if word not in stop_words:
				filtered_words.append(word)
		tagged_words = nltk.pos_tag(filtered_words)
		if splitted[0] == 'Who':
			actor.append(entity_list)
			for res in result_text:
			#actor_data.append(result_text)
				answers = Answer(answer_text= res, answer_type= 1, project_id= projectId1)
				answers.save()

			#print(result_text)

		else:
			
			case.append(entity_list)
			if 'Yes' in result_text or 'No' in result_text:
				if 'Yes' in result_text:
					
					question_data = words[2:len(words) - 1]
					final_action = " ".join(question_data)
					answers = Answer(answer_text= final_action, answer_type= 2, project_id= projectId1)
					answers.save()
					final_action_list.append(final_action)
					
					print(final_action_list)
				elif 'No' in result_text:
					case_data.append(None)

				#if result_text == 'Yes':
					#print(question_text) # checking question tags for values
			else:
				for res in result_text:
					answers = Answer(answer_text= res, answer_type= 2, project_id= projectId1)
					answers.save()
				case_data.append(result_text)
		
		
		print(actor)
		print(actor_data)
		print(case)
		print(case_data)
		#print(tagged_words)
		answer = Result.objects.filter(result_id = result_id)
		for a in answer:
			d_child = a.child
		if d_child == None:
			return render(request, 'usecases/questions.html', {"finish": "yes"})
		question = Question.objects.filter(question_id = d_child)
		for q in question:
			quest_id = q.question_id
		result = Result.objects.filter(question_id = quest_id)
		return render(request, 'usecases/questions.html', {'question': question, 'result': result})
	else:
		if first_route:
			question = Question.objects.filter(question_id = initial_question)
			result = Result.objects.filter(question_id = initial_question)
			return render(request, 'usecases/questions.html', {'question': question, 'result': result})
	#return render(request, 'usecases/questions.html')


def profile(request):
	if request.user.is_authenticated:
		print(request.user.id)
		args = User.objects.filter(id=request.user.id)
		
		return render(request, 'usecases/profile.html', {'data': args})

	else:
		return redirect('index')


def diagram(request):
	entities = Answer.objects.filter(project_id= projectId1)
	print(entities)
	return render(request, 'usecases/diagram.html', {'data': entities})