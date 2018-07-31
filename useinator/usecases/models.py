from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	category_id = models.AutoField(primary_key=True)
	category_name = models.CharField(max_length=80)
	subcategory_name = models.CharField(max_length=80)
	flag = models.BooleanField()
	users = models.ManyToManyField(User, through='Choose')

	def __str__(self):
		return self.category_name

class Choose(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Project(models.Model):
	project_id = models.AutoField(primary_key=True)
	project_name = models.CharField(max_length=80)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return '{} {}'.format(self.project_name, str(self.project_id))

class Answer(models.Model):
	answer_id = models.AutoField(primary_key=True)
	answer_type = models.IntegerField(blank=True, null=True)
	answer_text = models.CharField(max_length=120)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	def __str__(self):
		return self.answer_text

class Question(models.Model):
	question_id = models.AutoField(primary_key=True)
	question_text = models.TextField()
	category = models.ManyToManyField(Category, through='Concern')

	def __str__(self):
		return self.question_text

class Concern(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Result(models.Model):
	result_id = models.AutoField(primary_key=True)
	result_text = models.CharField(max_length=80)
	child = models.IntegerField(blank=True, null=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)


	def __str__(self):
		return self.result_text