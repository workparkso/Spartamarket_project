from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product
from django.contrib.auth.models import User
from django.db.models import Count

# Create your views here.


def product_list_view(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products":products})


@login_required
def product_create_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save() #db 적재 및 저장
            return redirect("products:product_list")
        
    else:
        form = ProductForm()
        
    return render(request, "products/product_form.html", {"form": form})



@login_required
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)  # 주어진 pk에 해당하는 상품을 가져옴
    product.views += 1  # 상품 조회수 증가
    product.save()  # DB에 저장

    # 현재 사용자가 이 상품을 찜한 상태인지 여부 확인
    is_liked = request.user in product.likes.all()

    return render(request, "products/product_detail.html", {
        "product": product,
        "is_liked": is_liked  # 찜 상태 여부를 템플릿에 전달
    })


@login_required
def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.user != request.user:
        return redirect("products:product_detail", pk=pk) #검증 중요
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()  # DB에 저장
            return redirect("products:product_detail", pk=pk)
    else:
        # GET 요청이라면 기존 제품 데이터를 바탕으로 폼을 초기화
        form = ProductForm(instance=product, initial={"hashtags_str": " ".join(ht.name for ht in product.hashtags.all())})

    return render(request, "products/product_form.html", {"form": form, "product": product})



@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.user != request.user:
        return redirect("products:product_detail", pk=pk) #검증 중요
    
    if request.method == "POST": #DB에서 지우기 -> 제공해줌줌
        product.delete()  
        return redirect("products:product_list")
    return render(request, "products/product_detail.html", {"product": product})




@login_required
def product_like_view(request, pk):
    product = get_object_or_404(Product, pk=pk)  # 찜하려는 상품을 가져옴
    
    # 사용자가 해당 상품을 찜한 상태인지 확인
    if request.user in product.likes.all():
        product.likes.remove(request.user)  # 찜을 취소
    else:
        product.likes.add(request.user)  # 찜하기
        
        
    # 저장 후, 최신 정보를 반영하도록 하기 위해 save() 호출
    product.save()
    
    return redirect("products:product_detail", pk=pk)




def product_list_view(request):
    # 검색어 가져오기
    search_query = request.GET.get('search', '')  # GET 방식으로 전달된 검색어

    if search_query:
        # 검색어가 있으면, title 또는 description에 해당하는 항목을 필터링
        products = Product.objects.filter(
            title__icontains=search_query
        )
    else:
        # 검색어가 없다면 모든 상품을 보여줌
        products = Product.objects.all()

    return render(request, "products/product_list.html", {"products": products, "search_query": search_query})