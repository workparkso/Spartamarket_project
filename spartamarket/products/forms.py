from django import forms
from .models import Product, Hashtag


# 상품 안의 폼

class ProductForm(forms.ModelForm):
    hashtags_str = forms.CharField(required=False)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Product
        fields = ["title", "description", "image", "hashtags_str"]
        
    # save 메서드는 폼에서 입력한 데이터를 db에  적재한다.
    def save(self, commit=True):
        # 부모 클래스의 save 메서드를 호출하되, commit=Fasle 할 것 -> 해당 상품은 들고오되, db에는 저장x
        # 해시태그에서 처리가 필요. 입력값에 , 등 다 처리가 필요함.
        # 1. product 객체를 생성하고, 추가작업(해시태그 처리)를 완료한 뒤에 commit을 한다.(db에 반영한다.)
        # 2. user와 연결 시켜줘야한다. 그 결과를 db에 적재하기 위해서 일단 commit을 false로 한다.
        product = super().save(commit=False)
        
        if self.user:
            product.user= self.user
            
        if commit:
            product.save()
            
        # 해시태그 처리
        # 입력받은 hashtags_str 문자열을 쉼표나 공백으로 구분해본다.(제한)
        #각 해시태그 선언, 이미 저장되면 가져오는는   
        hashtags_input = self.cleaned_data.get("hashtags_str","")
        hashtag_list = [h for h in hashtags_input.replace(","," ").split() if h]
        
        new_hashtags = []
        for ht in hashtag_list:
            ht_obj, created = Hashtag.objects.get_or_create(name=ht)
            new_hashtags.append(ht_obj)
        
        # 다대다 관계 설정정    
        product.hashtags.set(new_hashtags)
        
        if not commit:
            product.save()
            
        return product