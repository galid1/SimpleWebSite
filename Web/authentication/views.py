from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import *

# Create your views here.

###### request page ######
def write(request):
    # 로그인 중인지 확인
    if not confirm_session(request):
        return render(request, 'authentication/service_using_fail.html')
    return render(request, 'authentication/write.html')

def board(request):
    #로그인 중인지 확인
    if not confirm_session(request):
        return render(request, 'authentication/service_using_fail.html')

    board_list = Board.objects.all()
    context = {
        'board_list': board_list
    }
    return render(request, 'authentication/board.html', context)

def board_contents(request, board_id):
    # 로그인 중인지 확인
    if not confirm_session(request):
        return render(request, 'authentication/service_using_fail.html')
    try:
        board_record = Board.objects.get(pk=board_id)
    except: #해당 객체가 존재하지 않는경우 보여질 페이지
        return render(request, 'authentication/board_load_fail.html')
    context = {
        'board_record': board_record
    }
    return render(request, 'authentication/board_contents.html', context)

def login(request):
    #로그인 중인지 확인
    if confirm_session(request):
        context = {
            'login': "True"
        }
        return render(request, 'authentication/login_fail.html', context)
    return render(request, 'authentication/login.html')

def join(request):
    return render(request, 'authentication/join.html')

def main(request):
    return render(request, 'authentication/main.html')

###### request active ######
def do_write(request):
    # 로그인 중인지 확인
    if not confirm_session(request):
        return render(request, 'authentication/service_using_fail.html')

    if request.method == 'POST':
        title = request.POST['title']
        contents = request.POST['contents']
        pw = request.POST['pw']
        #글쓰기 검증
        context = write_verification(request, title, contents, pw)
        #글쓰기 에러페이지 출력
        if context is not None :
            return render(request, 'authentication/write_fail.html', context)
        # 글쓴이 모델 pk 가져오기
        user_id = request.session['user_id']
        user = WebUser.objects.get(user_id=user_id)
        #글 데이터베이스에 저장
        board_record = Board(board_title=title, board_contents=contents, board_writer=user)
        board_record.save()
    # 글쓰기 완료 후 게시판 사이트 요청
    return redirect(reverse('board'))

def do_login(request):
    if request.method == 'POST':
        user_id = request.POST['id']
        user_pw = request.POST['pw']
        context = login_verification(user_id, user_pw)
        if context is not None:
            return render(request, 'authentication/login_fail.html', context)
        save_session(request, user_id, user_pw)
        return render(request, 'authentication/main.html')

def do_join(request):
    if request.method == 'POST':
        id = request.POST['id']
        pw = request.POST['pw']
        pw_conf = request.POST['pwconf']
        # 회원가입 검증 (ID 중복 확인, PW 일치 확인, 아이디 길이 체크, 특수문자 확인)
        context = join_verification(id, str(pw), str(pw_conf))

        # context가 None이 아닌 경우 joinfail.html을 출력
        if context is not None :
            return render(request, 'authentication/join_fail.html', context)

        new_user = WebUser(user_id=id, user_pw=pw)
        new_user.save()
        return HttpResponseRedirect(reverse('main'))

def do_logout(request):
	del request.session['user_id']
	return render(request, 'authentication/login.html')

###### my method ######
## 글쓰기 관련##
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

def do_login(request):
    if request.method == 'POST':
        user_id = request.POST['id']
        user_pw = request.POST['pw']
        context = login_verification(user_id, user_pw)
        if context is not None:
            return render(request, 'authentication/login_fail.html', context)
        save_session(request, user_id, user_pw)
        return render(request, 'authentication/main.html')

## 인증관련 ##
def login_verification(insert_id, insert_pw):
    # None이 return 될 경우 에러 없음
    context = None
    # 모델이 없는 경우 예외처리를 해주어야 에러가 발생하지 않는다
    try:
        user = WebUser.objects.get(user_id=insert_id)
    except:
        context = {
            'target': 'id_or_pw'
        }
        return context

    if not insert_pw == user.user_pw:
        context = {
            'target': 'id_or_pw'
        }
        return context

    return context

# 회원가입 요청시 검증 메소드
# 키값을 'target'으로 하고 에러의 이름을 value로하는 사전형 자료형을 리턴한다
def join_verification(insert_id, insert_pw, insert_pw_conf):
    context = None
    # 특수문자 확인
    special_symbol = '!@#$%^&*()-_=+`~/*\|><?,.'
    if any(sym in insert_id for sym in special_symbol):
        context={
            'target': 'sym'
        }
        return context

    # ID 10자 이하 확인
    if len(str(insert_id)) > 9:
        context={
            'target': 'len'
        }
        return context

    user_list = WebUser.objects.all()
    # id 존재 확인
    for user in user_list:
        if user.user_id == insert_id:
            context={
                'target': 'id'
            }
        return context

    # 암호 일치 확인
    if not insert_pw == insert_pw_conf:
        context={
            'target': 'pw'
        }
        return context
    return context

## 세션 관련 ##
def save_session(request, user_id, user_pw):
    request.session['user_id'] = user_id
    request.session['user_pw'] = user_pw

def confirm_session(request):
    try:
        if request.session['user_id'] is not None:
            return True
    except:
        return False
