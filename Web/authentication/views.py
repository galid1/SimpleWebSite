from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import *

# Create your views here.

## request page ##
def duplicated(request):
    return render(request, 'authentication/duplicated.html')

def login(request):
	return render(request, 'authentication/login.html')

def join(request):
    return render(request, 'authentication/join.html')

def main(request):
    return render(request, 'authentication/main.html')

## request active ##
def do_login(request):
    if request.method == 'POST':
        user_id = request.POST['id']
        user_pw = request.POST['pw']
        if login_verification(user_id, user_pw):
            save_session(request, user_id, user_pw)
            return render(request, 'authentication/main.html')
        return render(request, 'authentication/login_fail.html')

def do_join(request):
    if request.method == 'POST':
        id = request.POST['id']
        pw = request.POST['pw']
        pw_conf = request.POST['pwconf']
        # ID 중복 확인, PW 일치 확인
        context = join_verification(id, str(pw), str(pw_conf))
        if not context == None :
            return render(request, 'authentication/join_fail.html', context)
        new_user = WebUser(user_id=id, user_pw=pw)
        new_user.save()
        return HttpResponseRedirect(reverse('main'))

def do_logout(request):
	del request.session['user_id']
	return render(request, 'authentication/login.html')

def go_board(request):
	try:
		request.session['user_id']
	except:
		return render(request, 'authentication/service_using_fail.html')
	return render(request, 'authentication/board.html')

## my method ##
def login_verification(insert_id, insert_pw):
	# 모델이 없는 경우 예외처리를 해주어야 에러가 발생하지 않는다
    try:
        user = WebUser.objects.get(user_id=insert_id)
    except :
        return False     
    if not insert_pw == user.user_pw:
        return False
    return True

def join_verification(insert_id, insert_pw, insert_pw_conf):
    user_list = WebUser.objects.all()
    context = None
    for user in user_list:
        if user.user_id == insert_id:
            context={
                'target': 'id'
            }
    if not insert_pw == insert_pw_conf:
        context={
            'target': 'pw'
        }
    return context

def save_session(request, user_id, user_pw):
    request.session['user_id'] = user_id
    request.session['user_pw'] = user_pw
