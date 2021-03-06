from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required	# Esse docoreto vai impedir usuários não autorizados acessem rotas protegidas
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator # Paginação
from django.contrib.auth.views import (PasswordChangeView, PasswordResetView, 
										PasswordResetDoneView, PasswordResetConfirmView, 
										PasswordResetCompleteView)

from .forms import TaskForm
from .models import Task
import datetime

# Funções relacionadas as URL's do arquivo urls.py

@login_required
def taskList(request):		#   order_by: ordena por data de criação do mais novo para mais antigo 
	search = request.GET.get('search')	# reseach é name do input de busca que está no html list.html
	filter = request.GET.get('filter') # Filtro
	dias_30 = datetime.datetime.now()-datetime.timedelta(days=30)
	taskFeitaRecente = Task.objects.filter(done='feito', update_at__gt=dias_30, user=request.user).count()
	taskFeito = Task.objects.filter(done='feito', user=request.user).count()
	taskFazendo = Task.objects.filter(done='fazendo', user=request.user).count()

	if search: # Filtrar pelo nome
		# Vai buscar uma lista de tasks e vai filtrar pelo request.user (o usuário da requisição)
		tasks = Task.objects.filter(title__icontains=search, user=request.user)#, user=request.user)
	elif filter: # Filtrar pelo estado (feito ou fazendo)
		tasks = Task.objects.filter(done=filter, user=request.user) # Vai filtrar pelo user e pelo done
	else:
		# Vou pegar todos as tasks e filtrar pelo request.user
		tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user)
		# Paginação
		paginacao = Paginator(tasks_list, 10) # (lista, num de páginas)
		page = request.GET.get('page')	
		tasks = paginacao.get_page(page) # Vai exibir o numero correto na página que está

	# render: "renderiza"  a página
	return render(request, 'tasks/list.html', {'tasks': tasks, 'taskFeitaRecente': taskFeitaRecente, 
               'taskFeito': taskFeito, 'taskFazendo': taskFazendo})


@login_required
def perfil(request):
	return render(request, 'user/perfil.html', {'name': request.user})


@login_required
def taskView(request, id):
	task = get_object_or_404(Task, pk=id)
	return render(request, 'tasks/task.html', {'task':task})
											#		'-> Argumento enviado para p front-end		


@login_required
def newTask(request):
	# Dispor e tratar formulário
	if request.method == 'POST': # Se for POST vai fazer inserção
		form = TaskForm(request.POST) # Passa request.POST para preencher o formulário

		if form.is_valid(): # Se o formulário for válido
			task = form.save(commit=False) # Com o commit=False ele vai parar o processo save e esperar até salvar
			task.done = 'fazendo'
			task.user = request.user	# Envia o user altenticado
			task.save()

			messages.info(request, 'Tarefa adicionada com sucesso!')	# Mensagem enviada para o front-end

			return redirect('/') # Volta para home, se não voltaria para msm url

	else: # Senão vai mostrar o formulário
		form = TaskForm()	# Chama o formulário. Lembrandoq em TaskForm temos Metadados
		return render(request, 'tasks/addtask.html', {'form':form})


@login_required
def editTasks(request, id):
	# O id vem do parametro da url para poder achar a task
	task = get_object_or_404(Task, pk=id)
						#	(model, primary_key)
	form = TaskForm(instance=task) # Para puxar o formulário. No instance=task deixar o form prepopulado

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task) # instance=task para saber qual form está sendo alterado

		if form.is_valid(): # Se o formulário for válido	
			task.save()
			messages.info(request, 'Tarefa editada com sucesso!')	# Mensagem enviada para o front-end
			return redirect('/')
		else:
			return render(request, 'tasks/edittask.html', {'form':form, 'task':task})	# Volta para mesma página, em caso de erro
	else:
		return render(request, 'tasks/edittask.html', {'form':form, 'task':task})


@login_required
def deleteTasks(request, id):
	task = get_object_or_404(Task, pk=id)
	task.delete()
	messages.info(request, 'Tarefa deletada com sucesso!') # Mensagem enviada para o front-end

	return redirect('/')

@login_required
def changestatus(request, id):
	task = get_object_or_404(Task, pk=id)

	if task.done == 'fazendo':
		task.done = 'feito'
	else:
		task.done = 'fazendo'

	task.save()

	return redirect('/')

def helloWorld(request):
	return HttpResponse('Hello World')


def yourName(request, name):
	return render(request, 'tasks/yourname.html', {'name':name})

