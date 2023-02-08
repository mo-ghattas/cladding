import time
import math
from math import  degrees, atan
import ezdxf
import pandas as pd
from ezdxf.addons import Importer
from ezdxf.layouts import Paperspace
from ezdxf.tools.standards import setup_dimstyle
import zipfile
t1=time.time()

details={'Name': 'quad',"type":"quad" ,'qty':10,'down': 3398.187916706962, 'right': 2007.8187050593767, 'left': 1652.9813335655847,'down_angle': -4.469297745597041, 'right_angle': 50.46462733004034, 'left_angle': 52.931071811966746
         ,'bend_right':1,'bend_left':1,'bend_top':1,'bend_down':1,'bend':20,'new_bend':20}
job_data={'edge_distance': 100,"max_distance": 500 ,'max_stiffner_distance': 500, 'stiffner_type': 'stiffner_type'}
#details={'name': 'quad',"type":"tri", 'down': 919.2807653974486, 'right': 884.989435571992, 'left': 995.5372378353555, 'd_angle': 76.57432408287724, 'l_angle': 131.45516715802756, 'r_angle': 170.3710578788588}
#details={'name': 'quad',"type":"tri", 'down': 1642.307766289078, 'right': 995.5372378353554, 'left': 1306.1701295377152, 'd_angle': 4.141228799030738, 'l_angle': 41.45516715802759, 'r_angle': 48.544832841972436}
#details={'name': 'quad', 'type': 'tri', 'down': 1006.0706829940854, 'right': 841.0978338387156, 'left': 961.6170492925309, 'd_angle': 61.985462258895744, 'l_angle': 112.53586011784137, 'r_angle': 180.0}
#details={'name': 'quad', 'type': 'quad', 'down': 1261.7543611003266, 'right': 2213.4612146352324, 'left': 1039.2810758687106, 'd_angle': -63.82378760371779, 'l_angle': 14.97266804216603, 'r_angle': 174.28484148567796}
#details={'name': 'quad', 'type': 'quad', 'down': 1440.9046159270913, 'right': 1104.2147921939827, 'left': 941.2273112272081, 'd_angle': 0.2580676487741021, 'l_angle': 62.82758235143965, 'r_angle': 104.11426894535616}
def main(job_data:dict=job_data ,details:dict=details):
    name=details["Name"]
    type=details["type"]
    down=details["down"]
    left=details["left"]
    right=details["right"]
    qty=details["qty"]
 #'angle_plan_right', 'angle_plan_left', 'angle_plan_down', 'angle_plan_up'
    rr=details["bend_right"]
    ll=details["bend_left"]
    uu=details["bend_top"]
    if type=="tri":
        uu=0
    dd=details["bend_down"]
    bend=details["bend"]
    new_bend=details["new_bend"]

    d_angle=details["down_angle"]
    r_angle=details["right_angle"]
    if type=="tri" and r_angle>90:
        r_angle=r_angle-180
    l_angle=details["left_angle"]

    #'job_no', 'sttifner_block', 'angle_plan_block', 'material', 'color', 'approved', 'checked', 'client', 'project'
    of=4

    min_distance=job_data["edge_distance"]
    sp=min_distance+70
    max_distance=job_data["max_distance"]
    max_stiffner=job_data["max_stiffner_distance"]
    sttifner_type=job_data["stiffner_type"]

   







    global  base_r ,hr , base_l , hl, hd , base_d
    doc = ezdxf.new("R2018",setup=True)
    doc.layers.add(name="Cladding", color=40)
    doc.layers.add(name="Cladding Hatch", color=8)
    doc.layers.add(name="Steel Hatch", color=252)
    doc.layers.add(name="Profile", color=54)
    doc.layers.add(name="Text", color=10)
    doc.layers.add(name="table", color=7) 
    doc.layers.add(name="htext", color=100) 
    doc.layers.add(name="Groove", color=31) 
    doc.layers.add(name="Cutting out", color=30)
    doc.styles.add("swiss 721 blk bt", font="swissk.ttf")
    #import required blocks
    doc2 = ezdxf.readfile("C:\\Users\\dell 15\\Desktop\\dxf\\BLOCK.dxf") 
    bl2=["rectangle","ben_small","benstif"]  
    importer = Importer(doc2, doc)
    importer.import_blocks(bl2)
    importer.finalize()
    # paperspace layout or block definition).  
    msp = doc.modelspace()
    #doc.create_layout("layout1")
    psp=doc.layout("layout1")
    #-------------------------------------------------------
    hd=math.sin(math.radians(d_angle))*down
    base_d=math.cos(math.radians(d_angle))*down
    hr=hd+(math.sin(math.radians(r_angle))*right)
    base_r=base_d-(math.cos(math.radians(r_angle))*right)
    hl=math.sin(math.radians(l_angle))*left
    base_l=math.cos(math.radians(l_angle))*left
    #-------------------------------------------------------
    def distance(p1,p2):
        return(math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2)))
    #-----------------------------------------------------
    try:
        up_angle=degrees(atan((hl-hr)/(base_l-base_r)))
    except:
        up_angle=0
    if up_angle<0:
                up_angle=up_angle
    up=math.sqrt(((base_r-base_l)**2)+((hr-hl)**2))

    #------------------------------------------------------
    hd_b=math.sin(math.radians(-d_angle))*down
    base_d_b=math.cos(math.radians(-d_angle))*down
    hr_b=hd_b+(math.sin(math.radians(l_angle))*left)
    base_r_b=base_d_b-(math.cos(math.radians(l_angle))*left)
    hl_b=math.sin(math.radians(r_angle))*right
    base_l_b=math.cos(math.radians(r_angle))*right

    xbr=math.sin(math.radians(l_angle))
    ybr=math.cos(math.radians(l_angle))

    xlr=math.sin(math.radians(r_angle))
    ylr=math.cos(math.radians(r_angle))

    xur=math.sin(math.radians(-up_angle))
    yur=math.cos(math.radians(-up_angle))
    
    xdr=math.sin(math.radians(-d_angle))
    ydr=math.cos(math.radians(-d_angle))
    def becal(point:tuple,line:str,bend:int=-of):
        if line=="r":
            return((point[0]+(xbr*bend) ,point[1]+(ybr*bend)))
        if line=="l":
            return((point[0]-(xlr*bend) ,point[1]+(ylr*bend)))
        if line=="u":
            return((point[0]-(xur*bend) ,point[1]+(yur*bend)))
        if line=="d":
            return((point[0]+(xdr*bend) ,point[1]-(ydr*bend)))
        
    #-----------------------------------------------------
    y_r=math.sin(math.radians(r_angle))
    x_r=math.cos(math.radians(180-r_angle))

    y_l=math.sin(math.radians(l_angle))
    x_l=math.cos(math.radians(l_angle))  
    
    y_u=math.sin(math.radians(up_angle))
    x_u=math.cos(math.radians(up_angle))

    y_d=math.sin(math.radians(d_angle))
    x_d=math.cos(math.radians(d_angle))
    def cal(distance,point:tuple,line:str,bend:bool=False):
        if line=="r":
            y=y_r*distance
            x=x_r*distance
        elif line=="l":
            y=y_l*distance
            x=x_l*distance
        elif line=="u":
            y=y_u*distance
            x=x_u*distance
        elif line=="d":
            y=y_d*distance
            x=x_d*distance

        if bend==False:
            return((point[0]+x ,point[1]+y))
        else:
            if line=="r":
                return((point[0]-x ,point[1]+y))
            if line=="l":
                return((point[0]-x ,point[1]+y))
            if line=="u":
                return((point[0]+x ,point[1]-y))
            if line=="d":
                return((point[0]+x ,point[1]-y))

                

    #-------------------------------------------------------
    
    #######

    #######

    #######
    try:
        r_avail= (right-min_distance-sp)
        r_num= math.ceil(r_avail/max_distance)
        r_space=r_avail / r_num
    except:
        r_space=0
    try:
        l_avail= (left-min_distance-sp)
        l_num= math.ceil(l_avail/max_distance)
        l_space=l_avail / l_num
    except:
        l_space=0
    try:
        d_avail= (down-min_distance-sp)
        d_num= math.ceil(d_avail/max_distance)
        d_space=d_avail / d_num
    except:
        d_space=0

    try:
        u_avail= (up-min_distance-sp)
        u_num= math.ceil(u_avail/max_distance)
        u_space=u_avail / u_num
    except:
        u_space=0

    s_avail= max(left,right)
    s_num= math.ceil(s_avail/max_stiffner)
    s_space=s_avail / s_num
    s_num=s_num-1


    line_data={"l":[l_space,l_num,l_angle],"r":[r_space,r_num,360-r_angle],"d":[d_space,d_num,180+d_angle],"u":[u_space,u_num,up_angle]}
    del l_space,l_num,l_avail ,r_space,r_num,r_avail ,d_space,d_num,d_avail ,u_space,u_num,u_avail
    #-------------------------------------------------------
    if base_l_b>=0:
        hanty=0
    else:
        hanty=base_l_b
    xb=max(base_d,base_r)-hanty+1000
    yb=hd
    x=0
    y=0

    #----------------------------------
    

    def draw_quadrangle( x:float=0,y:float=0 , layer:str="Cladding"):
        msp.add_lwpolyline([(x, y), (base_d+x, y+hd), (base_r+x, hr+y),(base_l+x, hl+y), (x, y)] , dxfattribs={ "layer": layer})
        msp.add_aligned_dim(p2=(base_d+x, y+hd),p1=(base_r+x, hr+y), distance=200,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
        msp.add_aligned_dim(p1=(x, y),p2=(base_l+x, hl+y), distance=200,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
        msp.add_aligned_dim(p2=(base_d+x, y+hd),p1=(x, y), distance=-200,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1,"dimtad": 4}).render()        
        if type=="quad":
            msp.add_aligned_dim(p1=(base_l+x, hl+y),p2=(base_r+x, hr+y), distance=200,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1,"dimtad": 1}).render()        
   
    draw_quadrangle( x, y )

    def draw_bend(x:float=0,y:float=0):
        global bend_right , bend_left , bend_up , bend_down
        bend_left=bend_down=bend_right=bend_up=bend
        if uu==2 or dd==2:
            bend_up=bend_down=bend-5
        if rr==2 or ll==2:
            bend_right=bend_left=bend-5
        #----------------------------------
        points=[(x,y)]
        left_arr=[becal((x,y),"l",bend_right) , becal((base_l_b+x, hl_b+y),"l",bend_right) , (base_l_b+x, hl_b+y)]
        up_arr=[becal((base_l_b+x, hl_b+y),"u",bend_up) , becal((base_r_b+x, hr_b+y),"u",bend_up) , (base_r_b+x, hr_b+y)]
        right_arr=[becal((base_r_b+x, hr_b+y),"r",bend_left) ,becal((base_d_b+x, hd_b+y),"r",bend_left) , (base_d_b+x, hd_b+y)]
        down_arr=[becal((base_d_b+x, hd_b+y),"d",bend_down) ,becal((x, y),"d",bend_down) , (x, y)]
        #----------------------------------
        groove=[(x, y), (base_d_b+x, y+hd_b), (base_r_b+x, hr_b+y),(base_l_b+x, hl_b+y), (x, y)]
        groove_l=[(base_l_b+x, hl_b+y), (x, y)]
        groove_r=[(base_d_b+x, y+hd_b), (base_r_b+x, hr_b+y)]
        groove_d=[(x, y), (base_d_b+x, y+hd_b)]
        groove_u=[(base_l_b+x, hl_b+y),(base_r_b+x, hr_b+y)]
        groove_arr=[groove_l,groove_r,groove_d,groove_u]
        #----------------------------------
        msp.add_aligned_dim(p2=(base_d_b+x, y+hd_b),p1=(base_r_b+x, hr_b+y), distance=200,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
        msp.add_aligned_dim(p1=(x, y),p2=(base_l_b+x, hl_b+y), distance=200,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
        msp.add_aligned_dim(p2=(base_d_b+x, y+hd_b),p1=(x, y), distance=-200,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1,"dimtad": 4}).render()        
        if type=="quad":
            msp.add_aligned_dim(p1=(base_l_b+x, hl_b+y),p2=(base_r_b+x, hr_b+y), distance=200,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1,"dimtad": 1}).render()        
   
        if rr==0:
            left_arr.pop(0)
            left_arr.pop(0)
            groove_arr.remove(groove_l)
            bend_right=0
        else:
            try:
                msp.add_aligned_dim(p1=left_arr[1],p2=left_arr[2], distance=360,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 0,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1,"dimtad": 1}).render()        
            except:
                pass
        #------------------------------------
        if uu==0 :
            up_arr.pop(0)
            up_arr.pop(0)
            groove_arr.remove(groove_u)
            bend_up=0
        else:
            try:
                msp.add_aligned_dim(p2=up_arr[2],p1=up_arr[1], distance=360,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 0,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
            except:
                pass
        #------------------------------------
        if ll==0:
            right_arr.pop(0)
            right_arr.pop(0)
            groove_arr.remove(groove_r)
            bend_left=0
        else:
            try:
                msp.add_aligned_dim(p2=right_arr[1],p1=right_arr[2], distance=-360,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 0,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1,"dimtad": 4}).render()        
            except:
                pass

        #------------------------------------
        if dd==0:
           down_arr.pop(0)
           down_arr.pop(0)
           groove_arr.remove(groove_d)
           bend_down=0
        else:
            try:
                msp.add_aligned_dim(p1=down_arr[1],p2=down_arr[2], distance=360,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 0,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
            except:
                pass
        #------------------------------------
        #-------draw groove---------#
        if rr!=0 and ll!=0 and dd!=0 and uu!=0:
            msp.add_lwpolyline(groove , dxfattribs={ "layer": "Groove"})
        else: 
            for i in groove_arr:
                msp.add_line(i[0],i[1] , dxfattribs={ "layer": "Groove"})

        #------------------------------------bend=2 appearance
        if rr==2:
            msp.add_lwpolyline( left_arr, dxfattribs={ "layer": "Groove"})
            p_dim=left_arr[1]
            left_arr=[becal((x,y),"l",bend_right+new_bend) , becal((base_l_b+x, hl_b+y),"l",bend_right+new_bend) , (base_l_b+x, hl_b+y)]
            msp.add_aligned_dim(p1=left_arr[1],p2=p_dim, distance=290,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 0,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1,"dimtad": 1}).render()        
        if ll==2:
            msp.add_lwpolyline( right_arr, dxfattribs={ "layer": "Groove"})
            p_dim=right_arr[1]
            right_arr=[becal((base_r_b+x, hr_b+y),"r",bend_left+new_bend) ,becal((base_d_b+x, hd_b+y),"r",bend_left+new_bend) , (base_d_b+x, hd_b+y)]
            msp.add_aligned_dim(p2=right_arr[1],p1=p_dim, distance=-290,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 0,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1,"dimtad": 4}).render()        
        if uu==2:
            msp.add_lwpolyline( up_arr, dxfattribs={ "layer": "Groove"})
            p_dim=up_arr[1]
            up_arr=[becal((base_l_b+x, hl_b+y),"u",bend_up+new_bend) , becal((base_r_b+x, hr_b+y),"u",bend_up+new_bend) , (base_r_b+x, hr_b+y)]
            msp.add_aligned_dim(p1=up_arr[1],p2=p_dim, distance=290,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 0,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
        if dd==2:
            msp.add_lwpolyline( down_arr, dxfattribs={ "layer": "Groove"})
            p_dim=down_arr[1]
            down_arr=[becal((base_d_b+x, hd_b+y),"d",bend_down+new_bend) ,becal((x, y),"d",bend_down+new_bend) , (x, y)]
            msp.add_aligned_dim(p1=down_arr[1],p2=p_dim, distance=290,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 0,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()




        #-------draw Cutting---------#
        arr=[left_arr,up_arr,right_arr,down_arr]
        for i in arr:
            for p in i:
                points.append(p)   
        msp.add_lwpolyline(points , dxfattribs={ "layer": "Cutting out"})




        #---------------get greatest dimensions------------- for area also#
        p2=up_arr[0]  #left
        if uu==0:
            if rr==0:
                p2=left_arr[0]
            else:
                p2=left_arr[2]

        if dd==0:
            p1=down_arr[0]
        else:
            p1=down_arr[1]
        msp.add_aligned_dim(p1=p1,p2=p2, distance=270,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
  
            #-----#d

        p2=down_arr[0]   #right
        if dd==0:
            if ll==0:
                p2=right_arr[0]
            else:
                p2=right_arr[2]
        if uu==0:
            p1=up_arr[0]
        else:
            p1=up_arr[1]
        msp.add_aligned_dim(p2=p2,p1=p1, distance=270,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()

            #-----#
        p2=left_arr[0]  #down
        if rr==0:
            if dd==0:
                p2=down_arr[0]
            else:
                p2=down_arr[2]
        if ll==0:
            p1=right_arr[0]
        else:
            p1=right_arr[1]
        msp.add_aligned_dim(p1=p2,p2=p1, distance=-270,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1,"dimtad": 4}).render()        
            #-----#u
        if type=="quad":
            p2=right_arr[0]
            if ll==0:
                if up==0:
                    p2=up_arr[0]
                else:
                    p2=up_arr[2]
            if rr==0:
                p1=left_arr[0]
            else:
                p1=left_arr[1]
            msp.add_aligned_dim(p1=p1,p2=p2, distance=370,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1,"dimtad": 1}).render()        
        del left_arr,up_arr,right_arr,down_arr,arr,groove,groove_arr,groove_d,groove_l,groove_r,groove_u

    draw_bend(xb,yb)

    def offset(x:float=0,y:float=0):
        dr=r_angle+d_angle
        dl=l_angle-d_angle
        ur=180-r_angle-up_angle
        ul=180-l_angle+up_angle
        def habd(point,line):
            if line=="dl":
                d=of/math.sin(math.radians(dl*0.5))
                a=(.5*dl)+d_angle-90
                xx=math.sin(math.radians(a))*d
                yy=math.cos(math.radians(a))*d
                return((point[0]-(xx) ,point[1]+(yy)))
            if line=="dr":
                d=9/math.sin(math.radians(dr*0.5))
                a=(.5*dr)+180-d_angle-90
                xx=math.sin(math.radians(a))*d
                yy=math.cos(math.radians(a))*d
                return((point[0]-xx ,point[1]+(yy)))
            if line=="ur" and type!="tri":
                xx=math.sin(math.radians(ur*.5))*of
                yy=math.cos(math.radians(ur*.5))*of
                return((point[0]-(xx) ,point[1]-(yy)))
            if line=="ul":
                xx=math.sin(math.radians(ul*.5))*of
                yy=math.cos(math.radians(ul*.5))*of
                return((point[0]+(xx) ,point[1]-(yy)))
        msp.add_lwpolyline([habd((x, y),"dl"),habd((base_d+x, y+hd),"dr"),habd((base_r+x, hr+y),"ur"),habd((base_l+x, hl+y),"ul")] , dxfattribs={ "layer": "Cladding Hatch"})  
    #offset()

    

    def add_block(x,y,line,block,bend:bool=False):
        space=line_data[line][0]
        num=line_data[line][1]
        angle=line_data[line][2]
        sp=min_distance+70
        ss=min_distance
        factor=-100
        if line=="l" or line=="u":
            ss=min_distance+70
            sp=min_distance
            factor=100
        if bend==True:
            if line=="r":
                angle=270-angle
                factor=100
            if line=="l":
                angle=270-angle
                factor=-100
            if line=="u":
                angle=270-angle
                sp=min_distance+70
                ss=min_distance
            if line=="d":
                angle=270-angle
                ss=min_distance+70
                sp=min_distance

        points=[(x,y),cal(ss,(x,y),line,bend)]
        dist=ss
        for i in range(num):
            points.append(cal(dist+space,(x,y),line,bend))
            dist=dist+space
        points.append(cal(dist+sp,(x,y),line,bend))
        le=len(points)
        for i in range(le):
            if i ==0:
                msp.add_aligned_dim(p1=points[i],p2=points[i+1], distance=factor,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
            elif i<le-1:
                msp.add_aligned_dim(p1=points[i],p2=points[i+1], distance=factor,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
                msp.add_blockref(block, points[i], dxfattribs={'xscale': 0,'yscale': 0,'rotation': angle}) 
        return ((num+1,points))
    #------------------------
    angle_plan_num=0
    points_r=[]
    points_l=[]
    if  ll!=0:
        labd=add_block(x, y,"l","rectangle")
        a_p_temp=labd[0]
        points_l=labd[1]
        angle_plan_num=a_p_temp+angle_plan_num
        add_block(base_d_b+xb,hd_b+yb,"l","ben_small",True)    


    if  rr!=0:
        labd=add_block(base_d,hd,"r","rectangle")
        a_p_temp=labd[0]
        points_r=labd[1]
        angle_plan_num=a_p_temp+angle_plan_num
        add_block(xb,yb,"r","ben_small",True)                   

    if  dd!=0:
        angle_plan_num=add_block(x, y,"d","rectangle")[0]+angle_plan_num
        add_block(xb,yb,"d","ben_small",True)                   


    if type!="tri" or uu!=0:
        angle_plan_num=add_block(base_l,hl,"u","rectangle")[0]+angle_plan_num
        add_block(base_l_b+xb,hl_b+yb,"u","ben_small",True)

    msp.add_text(name,dxfattribs={'height': 100 ,"layer": "htext",'style': 'LiberationSerif'}).set_pos((0,-500))



    def sttifener_non_specific_points(points,line):
        new=[]
        points.pop(0)
        for i in range(len(points)-1):
            new.append([cal(65,points[i],line),cal(-65,points[i+1],line)])
        return(new)
    points_l=sttifener_non_specific_points(points_l,"l")
    points_r=sttifener_non_specific_points(points_r,"r")

    
    def points():  
        ponits_r_new=[]
        factor=math.sin(math.radians(r_angle+d_angle))/math.sin(math.radians(l_angle-d_angle))
        for i in points_r:
            p1=i[0]
            p2=i[1]
            d=distance(p1,(base_d,hd))
            if d*factor>=left:
                break
            p1=cal(d*factor,(x,y),"l")
            d=distance(p2,(base_d,hd))
            p2=cal(d*factor,(x,y),"l")
            if d*factor>=left:
                break
            ponits_r_new.append([p1,p2])
        return(ponits_r_new)
    
    def final():
        final=[]
        po=points()
        for r in po:
            r1=r[0]
            r2=r[1]
            for w in points_l:
                w1=w[0]
                w2=w[1]
                dict={r1[1]:r1[0],r2[1]:r2[0],w1[1]:w1[0],w2[1]:w2[0]}
                arr=[r1[1],r2[1],w1[1],w2[1]]
                if r1[1]>=w1[1] and r1[1]<=w2[1]:
                    arr.sort()
                    p1=(dict[arr[1]],arr[1])
                    p2=(dict[arr[2]],arr[2])
                    final.append([p1,p2])
                if r2[1]>=w1[1] and r2[1]<=w2[1]:
                    arr.sort()
                    p1=(dict[arr[1]],arr[1])
                    p2=(dict[arr[2]],arr[2])
                    final.append([p1,p2]) 
        if len(final)==0:
            final=points_l
        return(final) 
      
    def get_sttifner_points():
        sttifner_points=[]
        s_p=[]
        factor=math.sin(math.radians(l_angle-d_angle))/math.sin(math.radians(r_angle+d_angle))
        p=(x,y)
        for i in range(s_num):
            p=cal(s_space,p,"l")
            s_p.append(p)
        s_p.append((base_l,hl))
        for u in range(len(s_p)-1):
            i=s_p[u]
            q=0
            while q==0:
                #print(i[1])
                if i[1]>=s_p[u+1][1]:
                    break
                for o in final():
                    p1=o[0]
                    p2=o[1]
                    if i[1]>p1[1]and i[1]<p2[1]:
                        d=distance(i,(x,y))
                        sttifner_points.append([i,cal(d*factor,(base_d,hd),"r")])
                        q=1
                        break
                    else:
                        i=cal(1,i,"l")
        return(sttifner_points)
    sttifner_points=get_sttifner_points()

    def add_sttifner():
        sttif_w=[]
        dl=15
        yl=9*math.sin(math.radians(90-l_angle))
        xl=9*math.cos(math.radians(90-l_angle))
        dr=15
        yl=9*math.sin(math.radians(90-r_angle))
        xl=9*math.cos(math.radians(90-r_angle))


        sttifner_points.insert(0,[(x,y),(base_d,hd)])
        sttifner_points.append([(base_l,hl),(base_r,hr)])
        for o in range(len(sttifner_points)):
            if o==len(sttifner_points)-1:
                msp.add_aligned_dim(p2=sttifner_points[o][0],p1=pl, distance=-100,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
                msp.add_aligned_dim(p1=sttifner_points[o][1],p2=pr, distance=-100,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
                break
            i=sttifner_points[o]
            pl=(i[0][0]+xl,i[0][1]-yl)
            pr=(i[1][0]-xl,i[1][1]-yl)
            if o==0:
                pl_dim=pl
                pr_dim=pr
            else:
                sttifner_line=msp.add_lwpolyline([pl ,cal(dl,pl,"l"), cal(dr,pr,"r"), pr, cal(-dr,pr,"r"), cal(-dl,pl,"l"),pl]  ,dxfattribs={ "layer": "Profile"}) 
                sttif_w.append(distance(pl,pr))
                tex=msp.add_text(sttifner_type ,dxfattribs={'height': 30 ,"layer": "Text",'style': 'LiberationSerif'}).set_pos(((pl[0]+pr[0])/2, (pl[1]+pr[1]+100)/2), align='MIDDLE_Center')   
                tex.dxf.rotation=d_angle
                msp.add_aligned_dim(p1=pl,p2=pr, distance=120,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
                sttifner_line.dxf.linetype="DASHED" 
                msp.add_aligned_dim(p1=pl_dim,p2=pl, distance=-100,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
                msp.add_aligned_dim(p2=pr_dim,p1=pr, distance=-100,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
                pl_dim=pl
                pr_dim=pr
        return(sttif_w)
    sttif_w=add_sttifner() 

    def add_sttifner_bend():
        sttifner_points_bend=[]
        for i in sttifner_points:
            pl=i[0]
            pr=i[1]
            dl=distance(pl,(x,y))
            dr=distance(pr,(base_d,hd))
            sttifner_points_bend.append([cal(dr,(xb,yb),"r",True),cal(dl,(base_d_b+xb,hd_b+yb),"l",True)])
        dl=15
        yl=9*math.sin(math.radians(90-r_angle))
        xl=9*math.cos(math.radians(90-r_angle))
        dr=15
        yl=9*math.sin(math.radians(90-l_angle))
        xl=9*math.cos(math.radians(90-l_angle))
        for o in range(len(sttifner_points_bend)):
            if o==len(sttifner_points_bend)-1:
                msp.add_aligned_dim(p2=sttifner_points_bend[o][0],p1=pl, distance=-100,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
                msp.add_aligned_dim(p1=sttifner_points_bend[o][1],p2=pr, distance=-100,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
                break
            i=sttifner_points_bend[o]
            pl=(i[0][0]+xl,i[0][1]-yl)
            pr=(i[1][0]-xl,i[1][1]-yl)
            if o==0:
                pl_dim=pl
                pr_dim=pr
            else:
                sttifner_line=msp.add_lwpolyline([pl ,cal(dl,pl,"r",True), cal(dr,pr,"l",True), pr, cal(-dr,pr,"l",True), cal(-dl,pl,"r",True),pl]  ,dxfattribs={ "layer": "Profile"}) 
                tex=msp.add_text(sttifner_type ,dxfattribs={'height': 30 ,"layer": "Text",'style': 'LiberationSerif'}).set_pos(((pl[0]+pr[0])/2, (pl[1]+pr[1]+100)/2), align='MIDDLE_Center')   
                tex.dxf.rotation=-d_angle
                msp.add_aligned_dim(p1=pl,p2=pr, distance=120,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
                sttifner_line.dxf.linetype="DASHED" 
                msp.add_aligned_dim(p1=pl_dim,p2=pl, distance=-100,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
                msp.add_aligned_dim(p2=pr_dim,p1=pr, distance=-100,override={"dimtxsty": "swiss 721 blk bt" ,"dimtxt": 30,"dimclrt": 100,"dimrnd":1.0 ,"dimexo": 25,"dimexe": 10,"dimgap": 15,"dimzin": 8 ,"dimasz":15,"dimtsz": 0,"dimblk": "OPEN90","dimdec":0,"dimsep":".","dimlfac":1}).render()
                msp.add_blockref("benstif", i[0], dxfattribs={'xscale': 0,'yscale': 0,'rotation': r_angle-90}) 
                msp.add_blockref("benstif", i[1], dxfattribs={'xscale': 0,'yscale': 0,'rotation': 270-l_angle}) 
                
                pl_dim=pl
                pr_dim=pr
    add_sttifner_bend()



        


    def add_sttifnerv01():
        factor=math.sin(math.radians(l_angle-d_angle))/math.sin(math.radians(r_angle+d_angle))
        sp_final=[]
        slp=[]
        srp=[]
        pl=(x,y)
        pr=(base_d,hd)
        last_p=points_l[-1][1]
        for i in range(s_num):
            pl=cal(s_space,pl,"l")
            slp.append(pl)
            pr=cal(s_space,pr,"r")
            srp.append(pr)
        for i in range(s_num):
            pl=slp[i]
            pr=srp[i]
            q=0
            while q==0:
                if pl[1]>last_p:
                    break
                for o in points_l:
                    if q==1:
                        break
                    elif pl[1]>o[0] and pl[1]<o[1]:
                        for k in points_r:
                            if pr[1]>k[0] and pr[1]<k[1]:
                                sp_final.append([pl,pr])
                                q=1
                                break
                    else:
                        pl=cal(1,pl,"l")
                        pr=cal(factor,pr,"r")

        for i in sp_final:
            msp.add_line(i[0],i[1])
    #add_sttifner()
    



    def shoelace_area():
        x_list =[x,  base_l,  base_r,  base_d,  x]
        y_list =[y,  hl,      hr,      hd      ,y]  
        a1,a2=0,0
        for j in range(len(x_list)-1):
            a1 += x_list[j]*y_list[j+1]
            a2 += y_list[j]*x_list[j+1]
        area=abs(a1-a2)/2
        return area
    if type=="quad":
        area=(shoelace_area()+(bend*(bend_down+bend_up+bend_left+bend_right)))/1000000
    elif type=="tri":
        s = (down + left + right) / 2  
        # calculate the area  
        area = (((s*(s-down)*(s-left)*(s-right)) ** 0.5 ) + (bend*(bend_down+bend_up+bend_left+bend_right)))/1000000
    
    
    import os
    #print(os.path.dirname(os.path.abspath(__file__)))
    #print(Path().resolve())
    #from pathlib import Path
    #import os
    from django.conf import settings
    temp_path=os.path.join(settings.MEDIA_ROOT,"temp")
    part_path=os.path.join(temp_path,str(details['id'])+".dxf")
    doc.saveas(part_path)
    
    #zipObj = ZipFile(os.path.join(settings.MEDIA_ROOT,"parts",str(details['id'])+".zip"), 'w')
    zip_path=os.path.join(settings.MEDIA_ROOT,"parts",str(details['id'])+".zip")
    zf = zipfile.ZipFile(zip_path, mode="w")
    zf.write(part_path ,name+".dxf")
    zf.close()
    os.remove(part_path)
    return [name , zip_path, area , sum(sttif_w) , len(sttif_w)]


print(time.time()-t1)
