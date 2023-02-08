import math
from math import  degrees, atan
import ezdxf
from . import check 




def get_data(file):
    global data , msp , tri_data
    data={}
    tri_data={}
    doc = ezdxf.readfile(file)
    msp=doc.modelspace()
    lin=msp.query("LWPOLYLINE")
    v=1
    for e in lin:
        point_duplicate=[]
        points={}
        a=1
        for pp in e.get_points():
            pp=(round(pp[0],2),round(pp[1],2))
            if pp in point_duplicate:
                a=1
            else:
                point_duplicate.append(pp)
                points[str(a)]=(pp[0],pp[1])
                a+=1
            
        keys=list(points.keys())
        num=len(keys)
        keys2=list(points.keys())
        min1=[keys[0],points[keys[0]][0],points[keys[0]][1]]
        keys.pop(0)
        mini=min1
        for k in keys:
            i=[k,points[k][0],points[k][1]]
            if i[1] < mini[1]: 
                mini=i
        
        keys2.remove(mini[0])
        #keys2.pop()
        min2=[keys2[0],points[keys2[0]][0],points[keys2[0]][1]]
        keys2.pop(0)
        mini2=min2
        for k in keys2:
            i=[k,points[k][0],points[k][1]]
            if i[1] < mini2[1]: 
                mini2=i
        start=mini
        left=mini2
        if mini2[2]<mini[2]:
            start=mini2
            left=mini
        #print(min1,min2,min)
        if num==4:
            sp=int(start[0])
            lp=int(left[0])
            if sp==1 or sp==2:
                op=sp+2
            if sp==3 or sp==4:
                op=sp-2
            if lp==1 or lp==2:
                rp=lp+2
            if lp==3 or lp==4:
                rp=lp-2
            points=[points[str(sp)],points[str(rp)],points[str(op)],points[str(lp)]]
            data["q"+str(v)]=points
            
        elif num==3:
            sp=int(start[0])
            lp=int(left[0])
            for i in[1,2,3]:
                if i!=sp and i!=lp:
                    rp=i
            points=[points[str(sp)],points[str(rp)],points[str(lp)]]
            tri_data["t"+str(v)]=points
        v+=1
    




    def get_text():
        global text
        text={}
        tex=msp.query("TEXT")
        for t in tex:
            a,p,c=t.get_placement()
            text[t.dxf.get("text")]=p

    get_text()
	

    def calculate_slope_distance():
        global final_data ,text_keys
        final_data={}
        text_keys=list(text.keys())
        keys=list(data.keys())
        for k in keys:
            dwg_name=k+" no_name_found"
            point=data[k]
            s=point[0]
            r=point[1]
            o=point[2]
            l=point[3]
            down=math.sqrt(((s[0]-r[0])**2)+((s[1]-r[1])**2))
            right=math.sqrt(((o[0]-r[0])**2)+((o[1]-r[1])**2))
            left=math.sqrt(((s[0]-l[0])**2)+((s[1]-l[1])**2))
            if s[0]==r[0]:
                down_angle=90
            else:
                down_angle=degrees(atan((s[1]-r[1])/(s[0]-r[0])))
            if s[0]==l[0]:
                left_angle=90
            else:
                left_angle=degrees(atan((s[1]-l[1])/(s[0]-l[0])))
                if left_angle<0:
                    left_angle=left_angle+180
            
            if o[0]==r[0]:
                right_angle=90
            else:
                right_angle=degrees(atan((o[1]-r[1])/(o[0]-r[0])))	
                if right_angle<0:
                    right_angle=right_angle+180
                right_angle=180-right_angle    
            
            for i in text_keys:
                text_point=(text[i][0],text[i][1])
                if check.check(s,r,o,l,4,text_point)==True:
                    dwg_name=i
                    text_keys.remove(i)
                    break
            #print(down,right,left,down_angle,right_angle,left_angle,dwg_name)
            this={"name":dwg_name,"type":"quad","down":down,"right":right,"left":left,"d_angle":down_angle,"l_angle":left_angle,"r_angle":right_angle}
            final_data[dwg_name]=this

    calculate_slope_distance()

    def tri_slope_distance():
        global tri_final_data
        tri_final_data={}
        keys=list(tri_data.keys())
        for k in keys:
            dwg_name=k+" no_name_found"
            point=tri_data[k]
            s=point[0]
            r=point[1]
            l=point[2]
            for i in text_keys:
                x_text_point=text[i][0]
                y_text_point=text[i][1]
                if check.check_tri(s[0],s[1],r[0],r[1],l[0],l[1],x_text_point,y_text_point)==True:
                    dwg_name=i
                    text_keys.remove(i)
                    break
            down=math.sqrt(((s[0]-r[0])**2)+((s[1]-r[1])**2))
            right=math.sqrt(((l[0]-r[0])**2)+((l[1]-r[1])**2))
            left=math.sqrt(((s[0]-l[0])**2)+((s[1]-l[1])**2))
            if s[0]==r[0]:
                down_angle=90
            else:
                down_angle=degrees(atan((s[1]-r[1])/(s[0]-r[0])))
            if s[0]==l[0]:
                left_angle=90
            else:
                left_angle=degrees(atan((s[1]-l[1])/(s[0]-l[0])))
                if left_angle<0:
                    left_angle=left_angle+180
            
            if l[0]==r[0]:
                right_angle=90
            else:
                right_angle=degrees(atan((l[1]-r[1])/(l[0]-r[0])))	
                if right_angle<0:
                    right_angle=right_angle+180
                right_angle=180-right_angle
            this={"name":dwg_name,"type":"tri","down":down,"right":right,"left":left,"d_angle":down_angle,"l_angle":left_angle,"r_angle":right_angle}
            final_data[dwg_name]=this
            
    tri_slope_distance()

    for k in final_data.keys():
        print(k,final_data[k])
    return(final_data)
    


    





