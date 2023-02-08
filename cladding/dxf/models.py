from django.db import models
# Create your models here.
class user(models.Model):
    #user = models.ForeignKey(user , default= 1,null= True , on_delete= models.CASCADE )
    Name=models.CharField(unique=True,max_length=50)
    email = models.EmailField(max_length=120)
    phone=models.CharField(max_length=50)
    company=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    Total_area=models.FloatField(max_length=30,default=0,null=True,blank=True)
    Total_jobs=models.IntegerField(default=0,null=True,blank=True)
    Total_parts=models.IntegerField(default=0,null=True,blank=True)
    register_date=models.DateField(auto_now_add=True)
    last_login_date=models.DateField(auto_now_add=True,null=True,blank=True)

class job(models.Model):
    user_id=models.ForeignKey(user,on_delete=models.SET_NULL,null=True)
    job_no=models.CharField(max_length=50)
    edge_distance=models.FloatField(max_length=10)
    max_distance=models.FloatField(max_length=10)
    max_stiffner_distance=models.FloatField(max_length=10)
    stiffner_type=models.CharField(max_length=50)
    sttifner_block=models.CharField(max_length=50,help_text='hi')
    angle_plan_block=models.CharField(max_length=50,help_text='hi')
    material=models.CharField(max_length=50)
    color=models.CharField(max_length=50)
    approved=models.CharField(max_length=50)
    checked=models.CharField(max_length=50)
    client=models.CharField(max_length=50)
    project=models.CharField(max_length=50)
    Creation_date=models.DateField(auto_now_add=True,auto_now=False)
    last_edit_date=models.DateField(auto_now=True,auto_now_add=False)
    Total_area=models.FloatField(max_length=10,default=0,null=True,blank=True)
    state=models.CharField(max_length=1,default='1')

    def get_state(self):
        d={'1':'pending',
           '2':'working',
           '3':'finished',
           '4':'failed',
           '5':'didn\'t compelete', 
           }
        return(d[self.state])

class part(models.Model):
    job_id=models.ForeignKey(job, on_delete= models.CASCADE)
    Name=models.CharField(max_length=50)
    type=models.CharField(max_length=10)

    right=models.FloatField(max_length=30)
    left=models.FloatField(max_length=30)
    down=models.FloatField(max_length=30)
    right_angle=models.FloatField(max_length=30)
    left_angle=models.FloatField(max_length=30)
    down_angle=models.FloatField(max_length=30)
    
    qty=models.FloatField(max_length=10,default=1,null=True)

    bend=models.FloatField(max_length=10,default=20,null=True)
    new_bend=models.FloatField(max_length=10,default=0,null=True)

    bend_top=models.IntegerField(default=1,null=True)
    bend_right=models.IntegerField(default=1,null=True)
    bend_left=models.IntegerField(default=1,null=True)
    bend_down=models.IntegerField(default=1,null=True)

    angle_plan_right=models.IntegerField(default=1,null=True)
    angle_plan_left=models.IntegerField(default=1,null=True)
    angle_plan_down=models.IntegerField(default=1,null=True)
    angle_plan_up=models.IntegerField(default=1,null=True)


    stiffner_length=models.FloatField(max_length=10,null=True,blank=True)
    stiffner_no=models.FloatField(max_length=10,null=True,blank=True)
    screw=models.IntegerField(null=True,blank=True)
    pop_revit=models.IntegerField(null=True,blank=True)
    area=models.FloatField(max_length=10,null=True,blank=True)
    Total_area=models.FloatField(max_length=10,null=True,blank=True)

    Creation_date=models.DateField(auto_now_add=True,auto_now=False)
    last_edit_date=models.DateField(auto_now=True,auto_now_add=False)
    state=models.CharField(max_length=1,default='1',null=True)

    def get_state(self):
        d={'1':'pending','2':'working','3':'finished','4':'failed'}
        return(d[self.state])


