import zipfile
import os
from django.conf import settings
import threading
from . import models
from .product import quadrangle_new
import time

def check_thread(name):
    threads=[]
    for thread in threading.enumerate(): 
        threads.append(thread.name)
    if name in threads:
        return True
    else:
        return False

def start_job(job_data,parts):
    job=models.job.objects.filter(id=job_data['id'])
    job.update(state='2')
    parts.update(state='2')
    while check_thread("dxf_creator")==True:
        time.sleep(5)
    drawing_thread = threading.Thread(target=ppp, name="dxf_creator", args=(job_data,parts))
    drawing_thread.start()

def ppp(job_data,parts):
    succees1=0
    succees2=0
    job=models.job.objects.filter(id=job_data['id'])
    zf = zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT,"jobs",str(job_data['id'])+".zip"), mode="w")
    job_area=job.values()[0]['Total_area']
    job.update(state='2')
    parts.update(state='2')
    if job_area==None:
        job_area=0
    for part in parts:
        print(part['id'])
        try:
            new=quadrangle_new.main(job_data,part)
            zf.write(new[1] ,part['Name']+".zip")
            models.part.objects.filter(id=part['id']).update(area=new[2],Total_area=new[2]*part['qty'],stiffner_length=new[3],stiffner_no=new[4],state='3')
            job_area+=new[2]
            succees1=1
        except:
            succees2=1
            models.part.objects.filter(id=part['id']).update(state='4')


    if succees1==1 and succees2==0:
        job.update(state='3', Total_area=job_area)
    elif succees1==1 and succees2==1:
        job.update(state='5', Total_area=job_area)
    elif succees1==0 and succees2==1:
        job.update(state='4', Total_area=job_area)

    zf.close()
        
