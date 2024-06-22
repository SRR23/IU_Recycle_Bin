from .models import Category

def all_ctgry(request):
    categorys=Category.objects.all()
    context={"categorys":categorys}
    return context