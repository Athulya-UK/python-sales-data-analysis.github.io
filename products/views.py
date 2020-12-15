from django.shortcuts import render
from .models import Product,Purchase
import pandas as pd
from .forms import PurchaseForm
from django.http import HttpResponse
from .utils import get_simple_plot,get_image,get_product_plot
import matplotlib.pyplot as plt
import seaborn as sns
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings 

@login_required
def chart_select_view(request):
    error_message=None
    df=None
    graph=None
    price=None
    try:
        product_df=pd.DataFrame(Product.objects.all().values())
        purchase_df=pd.DataFrame(Purchase.objects.all().values())
        product_df['product_id'] = product_df['id'] 
        if purchase_df.shape[0] > 0:
            df=pd.merge(purchase_df,product_df,on='product_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)
            price=df['price']
            if request.method == 'POST':
                chart_type = request.POST.get('sales')
                date_from = request.POST['date_from']
                date_to = request.POST['date_to'] 
                df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
                df2 = df.groupby('date',as_index=False)['total_price'].agg('sum')
                if chart_type !="":
                    if(date_from !="" and date_to !=""):   
                        df = df[(df['date']>date_from)&(df['date']<=date_to)]
                        df2 = df.groupby(df['date'],as_index=False)['total_price'].agg('sum')
                        graph = get_simple_plot(chart_type,x=df2['date'],y=df2['total_price'],data=df)
                    else:
                        error_message="please select a date to continue"
                else:
                    error_message='please select a chart type to continue'
        else:
            error_message="No records in the  database"
    except:
        product_df=None
        purchase_df=None
        error_message="No records in the  database"
    context={
        'graph':graph,
        'error_message':error_message,
        'price':price,
    }
    return render(request,'products/main.html',context)

@login_required
def count_daily_product(request):
    error_message=None
    df=None
    graph=None
    price=None
    try:
        product_df=pd.DataFrame(Product.objects.all().values())
        purchase_df=pd.DataFrame(Purchase.objects.all().values())
        product_df['product_id'] = product_df['id']
        if purchase_df.shape[0] > 0:
            df=pd.merge(purchase_df,product_df,on='product_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)
            price=df['price']
            if request.method == 'POST':
                chart_type = request.POST.get('sales')
                date_from = request.POST['date_from']
                date_to = request.POST['date_to']
                df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
                df2 = df.groupby('date',as_index=False)['total_price'].agg('sum')
                if chart_type !="":
                    if(date_from !="" and date_to !=""):
                        df = df[(df['date']>date_from)&(df['date']<=date_to)]   
                        df2 = df.groupby(df['date'],as_index=False)['quantity'].agg('sum')    
                        graph = get_product_plot(chart_type,x=df2['date'],y=df2['quantity'],data=df)
                    else:
                        error_message="please select a date to continue"
                else:
                    error_message='please select a chart type to continue'
        else:
            error_message="No records in the  database"
    except:
        product_df=None
        purchase_df=None
        error_message="No records in the  database"
    context={
        'graph':graph,
        'error_message':error_message,
        'price':price,
    }
    return render(request,'products/pdaily.html',context)

@login_required
def dashboard_view(request):
    product_df=pd.DataFrame(Product.objects.all().values())
    purchase_df=pd.DataFrame(Purchase.objects.all().values())
    product_df['product_id'] = product_df['id']
    df=pd.merge(purchase_df,product_df,on='product_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)          
    df['date']=df['date'].apply(lambda x:x.strftime('%Y-%m-%d'))
    df.groupby(['branchname'])['total_price'].max()
    df['date']= pd.to_datetime(df['date']) 
    data=df.groupby([df['date'].dt.year])["total_price"].sum()
    d=data.tail(3)
    fyd=data.tail(5)
    graph=d.plot.pie(autopct="%1.1f%%")
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig2 = plt.gcf()
    fig2.gca().add_artist(centre_circle)
    graph2=get_image()
    plt.switch_backend('Agg')
    plt.xticks(rotation=45)
    lines=fyd.plot.line()
    graph3=get_image()
    data1=df.groupby("name")["total_price"].sum()
    rrp=data1.tail(2)
    graph=rrp.plot.pie(autopct="%.1f%%")
    graph4=get_image()
    plt.switch_backend('Agg')
    plt.xticks(rotation=45)
    sns.barplot(x=df['branchname'],y=df['total_price'],hue=df['branchname'],data=df)
    plt.tight_layout()
    graph1=get_image()
    total_price=df['total_price']
    return render(request,'products/dashboard.html',{'graph1':graph1,'graph2':graph2,'graph3':graph3,'graph4':graph4,'total_price':total_price})

@login_required
def top_perf_view(request):
    product_df=pd.DataFrame(Product.objects.all().values())
    purchase_df=pd.DataFrame(Purchase.objects.all().values())
    product_df['product_id'] = product_df['id']
    df=pd.merge(purchase_df,product_df,on='product_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)          
    df['date']=df['date'].apply(lambda x:x.strftime('%y-%m-%d'))
    df2 = df.groupby('salesman',as_index=False)['total_price'].agg('sum')
    df3=df2.nlargest(3,'total_price')
    plt.switch_backend('Agg')
    plt.xticks(rotation=45)
    sns.barplot(x=df3['salesman'],y=df3['total_price'],hue=df3['salesman'],data=df)
    plt.tight_layout()
    graph=get_image()
    return render(request,'products/top_perf.html',{'graph':graph})

@login_required
def low_perf_view(request):
    product_df=pd.DataFrame(Product.objects.all().values())
    purchase_df=pd.DataFrame(Purchase.objects.all().values())
    product_df['product_id'] = product_df['id']
    df=pd.merge(purchase_df,product_df,on='product_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)          
    df['date']=df['date'].apply(lambda x:x.strftime('%y-%m-%d'))
    df2 = df.groupby('salesman',as_index=False)['total_price'].agg('sum')
    df3=df2.nsmallest(3,'total_price')
    plt.switch_backend('Agg')
    plt.xticks(rotation=45)
    sns.barplot(x=df3['salesman'],y=df3['total_price'],hue=df3['salesman'],data=df)
    plt.tight_layout()
    graph=get_image()
    return render(request,'products/low_perf.html',{'graph':graph})

@login_required
def top_branch_view(request):
    product_df=pd.DataFrame(Product.objects.all().values())
    purchase_df=pd.DataFrame(Purchase.objects.all().values())
    product_df['product_id'] = product_df['id']
    df=pd.merge(purchase_df,product_df,on='product_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)          
    df['date']=df['date'].apply(lambda x:x.strftime('%y-%m-%d'))
    df2 = df.groupby('branchname',as_index=False)['total_price'].agg('sum')
    df3=df2.nlargest(3,'total_price')
    plt.switch_backend('Agg')
    plt.xticks(rotation=45)
    sns.barplot(x=df3['branchname'],y=df3['total_price'],hue=df3['branchname'],data=df)
    plt.tight_layout()
    graph=get_image()
    return render(request,'products/top_branch.html',{'graph':graph})

@login_required
def low_branch_view(request):
    product_df=pd.DataFrame(Product.objects.all().values())
    purchase_df=pd.DataFrame(Purchase.objects.all().values())
    product_df['product_id'] = product_df['id']
    df=pd.merge(purchase_df,product_df,on='product_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)          
    df['date']=df['date'].apply(lambda x:x.strftime('%y-%m-%d'))
    df2 = df.groupby('branchname',as_index=False)['total_price'].agg('sum')
    df3=df2.nsmallest(3,'total_price')
    plt.switch_backend('Agg')
    plt.xticks(rotation=45)
    sns.barplot(x=df3['branchname'],y=df3['total_price'],hue=df3['branchname'],data=df)
    plt.tight_layout()
    graph=get_image()
    return render(request,'products/low_branch.html',{'graph':graph})

@login_required
def add_purchase_view(request):
    form=PurchaseForm(request.POST or None)
    added_message=None
    if form.is_valid():
        obj=form.save(commit=False)
        obj.save()
        form=PurchaseForm()
        added_message="The Purchase has been added"
    context={
        'form':form,
        'added_message':added_message,
    }
    return render(request,'products/add.html',context)

@login_required
def send_email_view(request):
    if request.method=="POST":
        subject=request.POST['subject']
        body=request.POST['body']
        product_df=pd.DataFrame(Product.objects.all().values())
        purchase_df=pd.DataFrame(Purchase.objects.all().values())
        product_df['product_id'] = product_df['id']
        df=pd.merge(purchase_df,product_df,on='product_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)          
        df['date']=df['date'].apply(lambda x:x.strftime('%y-%m-%d'))
        df2 = df.groupby('salesman_emailid',as_index=False)['total_price'].agg('sum')
        df3=df2.nlargest(1,'total_price')
        a=[]
        for i in df3['salesman_emailid']:
            a.append(i)
        email_from = settings.EMAIL_HOST_USER 
        send_mail( subject, body, email_from, a ) 
    return render(request,'products/sendemail.html',{})

@login_required
def send_email_low_view(request):
    if request.method=="POST":
        subject=request.POST['subject']
        body=request.POST['body']
        product_df=pd.DataFrame(Product.objects.all().values())
        purchase_df=pd.DataFrame(Purchase.objects.all().values())
        product_df['product_id'] = product_df['id']
        df=pd.merge(purchase_df,product_df,on='product_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)          
        df['date']=df['date'].apply(lambda x:x.strftime('%y-%m-%d'))
        df2 = df.groupby('salesman_emailid',as_index=False)['total_price'].agg('sum')
        df3=df2.nsmallest(1,'total_price')
        a=[]
        for i in df3['salesman_emailid']:
            a.append(i)
        email_from = settings.EMAIL_HOST_USER 
        send_mail( subject, body, email_from, a ) 
    return render(request,'products/sendemail.html',{})