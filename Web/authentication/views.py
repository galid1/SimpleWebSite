from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import *

# Create your views here.

## request page ##
def write(request):
    # 로그인 검증
    if not confirm_session(request):
        return render(request, 'authentication/service_using_fail.html')
    return render(request, 'authentication/write.html')

def board(request):
	try:
		request.session['user_id']
	except:
		return render(request, 'authentication/service_using_fail.html')
	return render(request, 'authentication/board.html')

def login(request):
	return render(request, 'authentication/login.html')

def join(request):
    return render(request, 'authentication/join.html')

def main(request):
    return render(request, 'authentication/main.html')

## request active ##
def do_write(request):
    # 로그인 검증
    if not confirm_session(request):
        return render(request, 'authentication/service_using_fail.html')

    if request.method == 'POST':
        title = request.POST['title']
        contents = request.POST['contents']
        pw = request.POST['pw']
        #글쓰기 검증
        context = write_verification(request, title, contents, pw)
        #글쓰기 에러페이지 출력
        if not context == None :
            return render(request, 'authentication/write_fail.html', context)
        # 글쓴이 모델 pk 가져오기
        user_id = request.session['user_id']
        user = WebUser.objects.get(user_id=user_id)
        user_pk = user.pk
        #글 데이터베이스에 저장
        board_record = Board(title, contents, user_pk)
    # 글쓰기 완료 후 게시판 사이트 요청
    return render(request, 'authentication/board.html')

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
        # 회원가입 검증 (ID 중복 확인, PW 일치 확인)
        context = join_verification(id, str(pw), str(pw_conf))
        # 회원가입 에러페이지 출력)
        if not context == None :
            return render(request, 'authentication/join_fail.html', context)
        new_user = WebUser(user_id=id, user_pw=pw)
        new_user.save()
        return HttpResponseRedirect(reverse('main'))

def do_logout(request):
	del request.session['user_id']
	return render(request, 'authentication/login.html')

## my method ##
def write_verification(request, title, contents, pw):
    context = None
    if len(str(title)) <= 1:
        context = {
            'target': 'title'
        }
    elif len(str(contents)) <= 1:
        context = {
            'target': 'contents'
        }
    elif not pw == request.session['user_pw']:
        context = {
            'target': 'pw'
        }
    else:
        context = None
    return context

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

def confirm_session(request):
    try:
        if not request.session['user_id'] == None:
            return True
    except:
        return False
