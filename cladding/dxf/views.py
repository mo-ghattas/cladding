from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from . import models
from django.conf import settings
from .Threadhandler import start_job
import pandas as pd 
from numpy import nan
import threading
import os
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .product import lattice_slicing
#user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
# Create your views here.
d={'1':'pending','2':'working','3':'finished','4':'failed','5':'didnot compelete',}
def page404(request , exception ):
    return render(request,'page404.html')

def register(request):
    check=False
    if request.method=='POST':
        data=request.POST
        username=data['username']
        password=data['password']
        try:
            user = User.objects.create_user(username, 'lennon@thebeatles.com', password)
            return redirect('/dxf/login/')
        except:
            check=True
    context={'check':check} 
    template='register.html'
    return render(request ,template,context)

def login(request):
    check=False
    if request.method=='POST':
        data=request.POST
        username=data['username']
        password=data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect('/dxf/home/')
        else:
            check=True
    context={'check':check}
    template='login.html'
    return render(request ,template,context)

@login_required(login_url='../login')
def home(request):
    id=request.user.id
    job_list=models.job.objects.filter(user_id=id).order_by('-Creation_date').values('id','job_no','project','client','Creation_date','state')[0:5]
    user_data=models.user.objects.filter(id=id).values('Total_area','Total_jobs','Total_parts')[0]
    for job in job_list:
        job['state']=d[job['state']]
    context={'user_id':id,'job_list':job_list,'area':user_data['Total_area'],'jobs':user_data['Total_jobs'],'parts':user_data['Total_parts']}
    template='home.html'
    return render(request ,template,context)


def add_parts_from_excel(file,job):
    df = pd.read_excel(file)
    df=df.replace(nan,1)
    print(df)
    for i in range(len(df)) :
        dict=df.iloc[[i]].to_dict("list")
        models.part.objects.create(job_id=job,Name=dict['partName'][0],type='quad',qty=dict['quantity'][0],
            right=dict['height'][0],left=dict['height'][0],down=dict['width'][0],right_angle=90,left_angle=90,down_angle=0,
            bend=dict['bend'][0],new_bend=dict['newBend'][0],bend_top=dict['top'][0],bend_right=dict['right'][0],bend_left=dict['left'][0],bend_down=dict['bottom'][0],
            angle_plan_right=dict['angle plan right'][0],angle_plan_left=dict['angle plan left'][0],
            angle_plan_down=dict['angle plan bottom'][0],angle_plan_up=dict['angle plan top'][0],)


@login_required(login_url='../login')
def new_job(request):
    id=request.user.id
    if request.method=='POST':
        data=dict(request.POST)
        user=models.user.objects.get(id=id)
        job=models.job.objects.create(user_id=user, job_no= data['job_no'][0], material= data['material'][0],project= data['project'][0],
            color= data['color'][0],client= data['client'][0],edge_distance= data['edge_distance'][0],max_distance= data['max_distance'][0],
            angle_plan_block= data['angle_plan_block'][0],approved= data['approved'][0],checked= data['checked'][0],
            max_stiffner_distance= data['max_stiffner_distance'][0],
            stiffner_type= data['stiffner_type'][0],sttifner_block= data['sttifner_block'][0]) 
        excel=request.FILES['uploadParts'] 
        excel.flush()
        with open('static/temp/'+str(job.id)+'.xlsx', 'wb+') as destination:
            for chunk in excel.chunks():
                destination.write(chunk)
        try:
            add_parts_from_excel('static/temp/'+str(job.id)+'.xlsx',job)
        except:
            return render(request,'page404.html',{'title':'the excel you uploaded has some altered values', 'msg': 'make sure:\n  - the headlines are the same\n  - there are no string in a cell that is must be a number'})
        return redirect('/dxf/home/job/'+str(job.id))
    context={'id':id}
    template='newJob.html'
    return render(request ,template,context)

@login_required(login_url='../login')    
def viewjob(request,id):
    job=models.job.objects.filter(id=id)
    parts=models.part.objects.filter(job_id=id).values()
    if request.method=='POST':
        data=dict(request.POST)
        #print(data)
        job.update( job_no= data['job_no'][0], material= data['material'][0],project= data['project'][0],
            color= data['color'][0],client= data['client'][0],edge_distance= data['edge_distance'][0],max_distance= data['max_distance'][0],
            angle_plan_block= data['angle_plan_block'][0],approved= data['approved'][0],checked= data['checked'][0],
            max_stiffner_distance= data['max_stiffner_distance'][0],
            stiffner_type= data['stiffner_type'][0],sttifner_block= data['sttifner_block'][0])

    job=job.values()[0]
    if job['state'] =='1' :
        disabled=' '
    else:
        disabled='disabled'
    context={'disabled':disabled,'job':job,'parts':parts}
    template='viewJob.html'
    return render(request ,template,context)

@login_required(login_url='../login')    
def job_handler(request,id):
    if request.method=='POST':
        data=request.POST
        aim=data['aim']
        id=data['id']
        if aim=='remove':
            models.job.objects.filter(id=id).delete()
            return redirect('/dxf/home')
        elif aim=='start':
            job_data=models.job.objects.filter(id=id).values('id','job_no', 'edge_distance', 'max_distance', 'max_stiffner_distance', 'stiffner_type', 'sttifner_block', 'angle_plan_block', 'material', 'color', 'approved', 'checked', 'client', 'project')[0]
            parts=models.part.objects.filter(job_id=id).values('id','Name', 'type', 'right', 'left', 'down', 'right_angle', 'left_angle', 'down_angle', 'qty', 'bend', 'new_bend', 'bend_top', 'bend_right', 'bend_left', 'bend_down', 'angle_plan_right', 'angle_plan_left', 'angle_plan_down', 'angle_plan_up')
            drawing_thread = threading.Thread(target=start_job , args=(job_data,parts))
            drawing_thread.start()
            
            return redirect('/dxf/home/job/'+str(id))

@login_required(login_url='../login')
def part_handler(request,id):
    if request.method=='POST':
        data=request.POST
        aim=data['aim']
        part_id=data['id']
        if aim=='delete':
            models.part.objects.filter(id=part_id).delete()
        elif aim=='edit':
            pass
        elif aim=='new':
            job=models.job.objects.get(id=id)
            models.part.objects.create(job_id=job,Name=data['Name'][0],type='quad',qty=data['qty'][0],
                right=data['hieght'][0],left=data['hieght'][0],down=data['width'][0],right_angle=90,left_angle=90,down_angle=0,
                bend=data['bend'][0],new_bend=data['new_bend'][0],bend_top=data['bend_top'][0],bend_right=data['bend_right'][0],bend_left=data['bend_left'][0],bend_down=data['bend_down'][0],
                angle_plan_right=data['angle_plan_right'][0],angle_plan_left=data['angle_plan_left'][0],
                angle_plan_down=data['angle_plan_down'][0],angle_plan_up=data['angle_plan_up'][0],)
    return redirect('/dxf/home/job/'+str(id))



def download_part(request,partid):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(settings.MEDIA_ROOT,"parts")
    filepath = os.path.join(filepath,partid+'.zip')
    path = open(filepath, 'rb')
    filename=models.part.objects.filter(id=partid).values('Name')[0]['Name']+'.zip'
    #return FileResponse(zip_file)
    #mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type='application/force-download')
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def download_job(request,jobid):
    filepath = os.path.join(settings.MEDIA_ROOT,"jobs")
    filepath = os.path.join(filepath,jobid+'.zip')
    path = open(filepath, 'rb')
    filename=models.job.objects.filter(id=jobid).values('job_no')[0]['job_no']+'.zip'
    response = HttpResponse(path, content_type='application/force-download')
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def lattice(request):
    id=request.user.id
    if request.method=='POST':
        data=dict(request.POST)
        user=models.user.objects.get(id=id)
        job=models.job.objects.create(user_id=user, job_no= data['job_no'][0], material= data['material'][0],project= data['project'][0],
            color= data['color'][0],client= data['client'][0],edge_distance= data['edge_distance'][0],max_distance= data['max_distance'][0],
            angle_plan_block= data['angle_plan_block'][0],approved= data['approved'][0],checked= data['checked'][0],
            max_stiffner_distance= data['max_stiffner_distance'][0],
            stiffner_type= data['stiffner_type'][0],sttifner_block= data['sttifner_block'][0]) 
        excel=request.FILES['uploadParts'] 
        dxf=request.FILES['uploaddxf'] 
        excel.flush()
        with open('static/temp/'+str(job.id)+'.xlsx', 'wb+') as destination:
            for chunk in excel.chunks():
                destination.write(chunk)
        print(dxf)
        dxf.flush()
        with open('static/temp/'+str(job.id)+'.dxf', 'wb+') as destination:
            for chunk in dxf.chunks():
                destination.write(chunk)
        #try:
        if True:
            partsexcel={}
            df = pd.read_excel('static/temp/'+str(job.id)+'.xlsx')
            df=df.replace(nan,1)
            print(df)
            for i in range(len(df)) :
                dict2=df.iloc[[i]].to_dict("list")
                print(dict2)
                partsexcel[dict2['partName'][0]]=dict2
        #except:
            #return render(request,'page404.html',{'title':'the excel you uploaded has some altered values', 'msg': 'make sure:\n  - the headlines are the same\n  - there are no string in a cell that is must be a number'})
        partsdxf= lattice_slicing.get_data('static/temp/'+str(job.id)+'.dxf')
        
        for k in partsdxf.keys():
            if k in list(partsexcel.keys()):
                dxf=partsdxf[k]
                excel=partsexcel[k]
                models.part.objects.create(job_id=job, Name=k, type=dxf['type'],
                    right=dxf['right'],left=dxf['left'],down=dxf['down'],right_angle=dxf['r_angle'],left_angle=dxf['l_angle'],down_angle=dxf['d_angle'],
                    bend=excel['bend'][0],new_bend=excel['newBend'][0],bend_top=excel['top'][0],bend_right=excel['right'][0],bend_left=excel['left'][0],bend_down=excel['bottom'][0],
                    angle_plan_right=excel['angle plan right'][0],angle_plan_left=excel['angle plan left'][0],qty=excel['quantity'][0],
                    angle_plan_down=excel['angle plan bottom'][0],angle_plan_up=excel['angle plan top'][0],)
            else:
                models.part.objects.create(job_id=job, Name=k, type=dxf['type'],
                    right=dxf['right'],left=dxf['left'],down=dxf['down'],right_angle=dxf['r_angle']
                    ,left_angle=dxf['l_angle'],down_angle=dxf['d_angle'],)
        
        return redirect('/dxf/home/job/'+str(job.id))
    context={'id':id}
    template='lattice.html'
    return render(request ,template,context)