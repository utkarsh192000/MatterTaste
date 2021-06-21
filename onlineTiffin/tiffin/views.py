from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# Create your views here.
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
import reportlab.lib

from .utils import render_to_pdf
import datetime

# Create your views here.
def get2(request,book_id):
    if not request.user.is_staff:
        return redirect('login_admin')
    pro = Booking.objects.get(id=book_id)
    template = get_template('invoice.html')
    data = {
        'pro': pro,
        'book_id':book_id
    }
    html = template.render(data)
    pdf = render_to_pdf('invoice.html',data)
    return HttpResponse(pdf,content_type='application/pdf')


def Home(request):
    pro = Food.objects.all()
    d = {'pro':pro}
    return render(request, 'user_home.html',d)

def View_All_Food(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    pro = Food.objects.all()
    d = {'pro': pro}
    return render(request,'view_all_food.html',d)



def About(request):
    return render(request,'about.html')


def Contact(request):
    return render(request,'contact.html')


def Signup_User(request):
    error = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        p = request.POST['pwd']
        con = request.POST['contact']
        user = User.objects.create_user(username=u, password=p, first_name=f,last_name=l)
        Signup.objects.create(user=user,contact=con)
        error = True
    d = {'error':error}
    return render(request, 'signup.html',d)

def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            error = "yes"
        else:
            error = "not"
    d = {'error': error}
    return render(request,'login.html',d)

def Admin_Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "yes"
            else:
                error = "not"
        except:
            error="not"
    d = {'error': error}
    return render(request,'loginadmin.html',d)


def Logout(request):
    logout(request)
    return redirect('home')

def Admin_Home(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    sign = Booking.objects.all()
    rejected =0
    pending = 0
    confirm = 0
    all_order=0
    for i in sign:
        if i.status.status == "pending":
            pending+=1
        elif i.status.status == "Accept":
            confirm+=1
        elif i.status.status == "Reject":
            rejected+=1
        all_order+=1
    d = {'pending':pending,'rejected':rejected,'confirm':confirm,'all_order':all_order}
    return render(request,'admin_home.html',d)

def view_user(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro1 = Signup.objects.all()
    d = {'pro': pro1}
    return render(request,'view_user.html',d)

def View_Booking(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    user = User.objects.get(id=request.user.id)
    profile = Signup.objects.get(user=user)
    book = Booking.objects.filter(signup=profile)
    d = {'book': book}
    return render(request, 'view_booking.html', d)

def Change_Password(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'change_password.html',d)

def Edit_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    sign = Signup.objects.get(id=pid)
    stat = Status.objects.all()
    if request.method == "POST":
        n = request.POST['username']
        s = request.POST['status']
        user = User.objects.get(username=n)
        sign.user.username = user
        status = Status.objects.get(status=s)
        sign.status = status
        sign.save()
        return redirect('requested_user')
    d = {'book': sign, 'stat': stat}
    return render(request, 'status.html', d)



def Add_Food(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error=False
    if request.method=="POST":
        p = request.POST['type']
        pr = request.POST['price']
        i = request.FILES['img']
        d = request.POST['detail']
        t = request.POST['title']
        Food.objects.create(food_name=p, price=pr, image=i, food_detail=d,title=t)
        error=True
    d = {'error':error}
    return render(request, 'add_food.html', d)


def Edit_Food(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error=False
    pro = Food.objects.get(id=pid)
    if request.method=="POST":
        p = request.POST['pname']
        pr = request.POST['price']
        try:
            i = request.FILES['img']
            pro.image=i
            pro.save()
        except:
            pass
        d = request.POST['detail']
        t = request.POST['title']
        pro.food_name=p
        pro.price=pr
        pro.food_detail=d
        pro.title=t
        pro.save()
        error=True
    d = {'error':error,'pro':pro}
    return render(request, 'edit_food.html', d)

def delete_food(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Food.objects.get(id=pid)
    pro.delete()
    return redirect('view_food')

def View_food(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Food.objects.all()
    d = {'pro': pro}
    return render(request, 'view_food.html',d)

def Booking_order(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    food = Food.objects.get(id=pid)
    data1 = User.objects.get(id=request.user.id)
    data = Signup.objects.filter(user=data1).first()
    rt = datetime.datetime.now()
    rd = datetime.date.today()
    rt1 = str(rt).split(":")
    rt2 = "".join(rt1)
    order_id1 = rt2.split("-")
    order_id2 = "".join(order_id1)
    order_id3 = order_id2.split(" ")
    order_id4 = "".join(order_id3)
    order_id = order_id4.replace("2020","")
    if request.method == "POST":
        d = request.POST['date1']
        td = request.POST['date2']
        c = request.POST['name']
        f = request.POST['fname']
        c1 = request.POST['city']
        ad = request.POST['add']
        e = request.POST['email']
        con = request.POST['contact']
        n = request.POST['quant']
        ti = request.POST['time']
        day2 = request.POST['day']
        ord1 = request.POST['date3']
        t = request.POST['total']
        ord=datetime.date.today()
        user = User.objects.get(username=request.user.username)
        profile = Signup.objects.get(user=user)
        status = Status.objects.get(status="pending")
        book1 = Booking.objects.create(book_id=f,signup=profile,day1=day2,time=ti,order_date=ord,city=c1,address=ad,food=food,from_date=d,to_date=td,total=t,quantity=n,status=status)
        return redirect('payment',book1.total)
    d = {'data': data,'food':food,'rt':order_id}
    return render(request, 'booking.html', d)

def payment(request,total):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = False
    user = User.objects.get(id=request.user.id)
    profile= Signup.objects.get(user=user)
    if request.method=="POST":
        error=True
    d ={'total':total,'error':error}
    return render(request,'payment2.html',d)

def Feedback(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = False
    user = User.objects.get(id=request.user.id)
    pro = Signup.objects.filter(user=user).first()
    date1 = datetime.date.today()
    if request.method == "POST":
        d = request.POST['date']
        u = request.POST['uname']
        e = request.POST['email']
        con = request.POST['contact']
        m = request.POST['desc']
        pro = Signup.objects.get(user=user)
        Send_Feedback.objects.create(signup=pro, date=d, message1=m)
        error = True
    d = {'pro': pro, 'date1': date1,'error':error}
    return render(request, 'feedback.html', d)


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    user = User.objects.get(id=request.user.id)
    pro = Signup.objects.get(user=user)
    user = User.objects.get(id=request.user.id)
    pro = Signup.objects.get(user=user)
    d={'pro':pro,'user':user}
    return render(request,'profile.html',d)


def Edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = False
    user=User.objects.get(id=request.user.id)
    pro = Signup.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        con = request.POST['contact']
        pro.user.username=u
        user.first_name=f
        user.last_name=l
        pro.contact=con
        pro.save()
        pro.user.save()
        user.save()
        error = True
    d = {'error':error,'pro':pro}
    return render(request, 'edit_profile.html',d)

def View_feedback(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.all()
    d = {'feed': feed}
    return render(request, 'view_feedback.html', d)

def delete_feedback(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.get(id=pid)
    feed.delete()
    return redirect('view_feedback')


def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_user')

def Admin_View_Booking(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.all()
    d = {'book': book}
    return render(request, 'admin_viewBokking.html', d)

def Order_Invoice(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.all()
    d = {'book': book}
    return render(request, 'order_invoice.html', d)

def Confirmed_View_Booking(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.all()
    d = {'book': book}
    return render(request, 'confimed_viewBokking.html', d)

def Cancel_View_Booking(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.all()
    d = {'book': book}
    return render(request, 'cancel_view_booking.html', d)

def pending_View_Booking(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.all()
    d = {'book': book}
    return render(request, 'pending_viewBokking.html', d)

def delete_booking(request, pid):
    book = Booking.objects.get(id=pid)
    book.delete()
    if request.user.is_staff:
        return redirect('Admin_View_Booking')
    else:
        return redirect('view_booking')

def Booking_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Booking.objects.get(id=pid)
    d = {'pro':pro,'book_id':pid}
    return render(request,'booking_detail.html',d)

def User_Booking_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    pro = Booking.objects.get(id=pid)
    d = {'pro':pro,'book_id':pid}
    return render(request,'user_booking_detail.html',d)

def Edit_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.get(id=pid)
    stat = Status.objects.all()
    error=False
    if request.method == "POST":
        n = request.POST['book']
        s = request.POST['status']
        book.id = n
        sta = Status.objects.filter(status=s).first()
        book.status = sta
        book.save()
        error=True
    d = {'book': book, 'stat': stat,'error':error}
    return render(request, 'status.html', d)

def Cancel_booking(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    book = Booking.objects.get(id=pid)
    status = Status.objects.get(status="Reject")
    book.status = status
    book.save()
    return redirect('view_booking')