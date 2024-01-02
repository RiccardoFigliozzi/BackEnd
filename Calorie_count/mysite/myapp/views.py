from django.shortcuts import render, redirect
from .models import Food, Consume
# Create your views here.

def index(req):

    user = req.user

    if req.method == "POST":
        food_consumed = req.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        user = user
        user_consume = Consume(user=user,food_consumed=consume)
        user_consume.save()
        foods = Food.objects.all()

    else:
        foods = Food.objects.all()

    diet = Consume.objects.filter(user=user)
    
    res = render(req,'myapp/index.html', {'foods':foods, 'diet':diet})
    return res

def delete_consume(req,id):
    consume_food=Consume.objects.get(id=id)
    if req.method=='POST':
        consume_food.delete()
        return redirect('/')
    else:
        return render(req, 'myapp/delete.html')
    
def delete_all(req):
    consume_food=Consume.objects.all()
    if req.method=='POST':
        consume_food.delete()
        return redirect('/')
    else:
        return render(req, 'myapp/delete.html')
