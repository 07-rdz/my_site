from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
import re
import sqlite3
from fractions import Fraction
import matplotlib
matplotlib.use('Agg')
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image
from io import StringIO,BytesIO


# Create your views here.
def index(request):
    if request.method=="POST":
        eq=request.POST.get("equation").replace(" ","").split('=')
        ls=eq[0]
        rs=eq[1]
        t_start=request.POST.get("t_start")
        t_stop=request.POST.get("t_stop")
        t_step=request.POST.get("t_step")
        
        #Регулярным выражением разбираем строку на коэффициенты и элементы
        pattern=r"([\d\/\d]+)(\w+(\(\w\))?)"
        ls_matches=re.findall(pattern,ls)
        rs_matches=re.findall(pattern,rs)
        
        #Получаем коэффициенты при элементах и сами элементы в виде списка
        l_k=[]
        l_el=[]
        for i in ls_matches:
            l_k.append(list(i)[0])
            l_el.append(list(i)[1])
        r_k=[]
        r_el=[]
        for i in rs_matches:
            r_k.append(list(i)[0])
            r_el.append(list(i)[1])
        
        #Получаем значения энтальпий и энтропий для каждого елемента

        #Подключение к БД
        conn = sqlite3.connect('tab2.sqlite')
        cursor = conn.cursor()
        l_h=[]
        for i in l_el:
            cursor.execute("SELECT H_298_kJ_mol FROM chem WHERE Formula= :lim",{"lim":i})
            # Получаем результат сделанного запроса
            l_h.append(cursor.fetchall())
        conn.close()
        #Подключение к БД
        conn = sqlite3.connect('tab2.sqlite')
        cursor = conn.cursor()
        l_s=[]
        for i in l_el:
            cursor.execute("SELECT S_298_J_mol_K FROM chem WHERE Formula= :lim",{"lim":i})
            l_s.append(cursor.fetchall())
        conn.close()
        #Подключение к БД
        conn = sqlite3.connect('tab2.sqlite')
        cursor = conn.cursor()
        r_h=[]
        for i in r_el:
            cursor.execute("SELECT H_298_kJ_mol FROM chem WHERE Formula= :lim",{"lim":i})
            r_h.append(cursor.fetchall())
        conn.close()
        #Подключение к БД
        conn = sqlite3.connect('tab2.sqlite')
        cursor = conn.cursor()
        r_s=[]
        for i in r_el:
            cursor.execute("SELECT S_298_J_mol_K FROM chem WHERE Formula= :lim",{"lim":i})
            r_s.append(cursor.fetchall())
        conn.close()
        
        ll_h=[]
        for i in l_h:
            for x in i:
                ll_h.append(list(x)[0])
        ll_s=[]
        for i in l_s:
            for x in i:
                ll_s.append(list(x)[0])        
        rr_h=[]
        for i in r_h:
            for x in i:
                rr_h.append(list(x)[0])    
        rr_s=[]
        for i in r_s:
            for x in i:
                rr_s.append(list(x)[0])

        ll_k=[]
        for i in l_k:
            ll_k.append(float(Fraction(i)))

        rr_k=[]
        for i in r_k:
            rr_k.append(float(Fraction(i)))

        #Рассчитываем общую энтальпию и энтропию реакции
        tot_h=sum([x * y for x, y in zip(rr_h, rr_k)])-sum([x * y for x, y in zip(ll_h, ll_k)])
        tot_s=sum([x * y for x, y in zip(rr_s, rr_k)])-sum([x * y for x, y in zip(ll_s, ll_k)])
        G=[]
        for i in range(int(t_start),int(t_stop),int(t_step)):
            G.append((tot_h*1000)-((tot_s*i)))
        t_o=((tot_h*1000)/(tot_s))
        # Construct the graph
        plot(range(int(t_start),int(t_stop),int(t_step)), G)
        xlabel('Temperature,[K]')
        ylabel('Gibbs energy, [J]')
        title('Gibbs energy for reaction: {}=>{} \n G={},kJ - {},J/K * T,K \n Reaction starts after {},K'.format(ls,rs,round(tot_h,2),round(tot_s,2),round(t_o,2)))
        grid(True)

        # Store image in a string buffer
        buffer = BytesIO()
        canvas = pylab.get_current_fig_manager().canvas
        canvas.draw()
        pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
        pilImage.save(buffer, "PNG")
        pylab.close()
        
    # Send buffer in a http response the the browser with the mime type image/png set
        return HttpResponse(buffer.getvalue(), "image/png")
    else:
        userform=UserForm()
        return render(request,"index.html",{"form":userform})
