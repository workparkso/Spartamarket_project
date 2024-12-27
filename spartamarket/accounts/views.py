from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import ProfileForm
from products.models import Product
from .models import User
from django.contrib import messages



# Create your views here.


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accounts:signup")
        #return redirect("accounts:profile", username=user.username)
    else:
        form = SignupForm()
        
    return render(request, "accounts/signup.html", {"form" : form })


def login_view(request):
    if request.user.is_authenticated:
        return redirect("products:product_list")
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("products:product_list")
        
    else : 
        form = AuthenticationForm(request)
    return render(request, "accounts/login.html", {"form" : form}) 

@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def profile_view(request, username):
    # profile_user는 User 모델에서 username에 해당하는 사용자 객체를 가져온다.
    profile_user = get_object_or_404(User, username=username)
    
    #등록상품
    my_products = Product.objects.filter(user=profile_user)

    #찜
    liked_products = profile_user.liked_products.all()
    # 팔로잉 여부(맨 아래래)
    # 로그인한 사용자(request_user)가 해당 profile_user를 팔로우하고 있는지 확인
    # True/False 반환함
    
    # 로그인한 사용자가 profile_user를 팔로우하고 있는지 확인
    is_following = request.user.follows.filter(pk=profile_user.pk).exists()
    
    # context를 딕셔너리로 수정
    context = {
        "profile_user": profile_user,  # 프로필 사용자 정보
        "is_following": is_following,  # 팔로우 여부
        "liked_products" : liked_products,
        "is_following" : is_following,
    }
    
    return render(request, "accounts/profile.html", context)



@login_required
def profile_edit(request, username):
    if request.user.username != username:
        return redirect("accounts:profile", username=username)
    
    # 프로필을 수정하려는 사용자를 가져오기
    user = get_object_or_404(User, username=username)
    
    # POST 요청일 경우 폼 처리
    if request.method =="POST" :
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", username=username)
    
    else:
        form = ProfileForm(instance=user)
        
    
    return render(request, "accounts/profile_edit.html", {"form" : form})


# def follow_view(request, username): # 프로필에 팔로우 기능을 넣자. profile.html
#     target_user = get_object_or_404(User, username=username)
#     if target_user != request.user:
#     #팔로우되어있는 상태 -> 1
#         if request.user.follows.filter(pk=target_user.pk).exists():
#             # 취소하는 버튼
#             request.user.follows.remove(target_user)
#         else: 
#             request.user.follows.add(target_user)
            
#     return redirect("accounts:profile", username=username) 

def follow_view(request, username): # 프로필에 팔로우 기능을 넣자. profile.html
    # 팔로우할 사용자 가져오기
    target_user = get_object_or_404(User, username=username)

    # 자신을 팔로우하려는 경우 방지
    if target_user == request.user:
        messages.error(request, "자신을 팔로우할 수 없습니다.")
        return redirect("accounts:profile", username=username)
    
    # # 팔로우 상태 확인
    # if request.user.follows.filter(pk=target_user.pk).exists():
    #     # 이미 팔로우 중이면 팔로우 취소
    #     request.user.follows.remove(target_user)
    #     messages.success(request, f"{target_user.username}님 팔로우를 취소했습니다.")
    # else:
    #     # 팔로우하지 않은 경우 팔로우 추가
    #     request.user.follows.add(target_user)
    #     messages.success(request, f"{target_user.username}님을 팔로우했습니다.")
    
    # return redirect("accounts:profile", username=username)
    
    
    # 팔로우 상태 확인 및 팔로우 추가/취소
    if target_user in request.user.follows.all():
        # 이미 팔로우 중이면 팔로우 취소
        request.user.follows.remove(target_user)
        messages.success(request, f"{target_user.username}님 팔로우를 취소했습니다.")
    else:
        # 팔로우하지 않은 경우 팔로우 추가
        request.user.follows.add(target_user)
        messages.success(request, f"{target_user.username}님을 팔로우했습니다.")
    
    return redirect("accounts:profile", username=username)