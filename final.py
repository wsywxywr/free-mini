'''
Created on 2013-3-10

@author: PC2
'''

# -- coding: UTF-8 --
#=============================================================================
#     FileName: 
#       Author: Wang Siyu
#        Email: wsy.refree@gmail.com
#     HomePage: 
#      Version: 1.0
#   LastChange: 
#      History: 
#=============================================================================



from Tkinter import *
import time
import re
import os
from ScrolledText import *
import tkMessageBox
from tkFileDialog import *
import fileinput
import thread
import string
import smtplib

rule=re.compile('\s\d+\s')


####               qing li
class clear:
    def __init__(self):
        self.top=Tk()
        self.top.title('clear')
        self.la=Label(self.top,text='The processes')
        self.la.pack()
        
        self.Va=StringVar(self.top)
        
        self.clfm=Frame(self.top)
        self.clsb=Scrollbar(self.clfm)
        self.clsb.pack(side='right',fill=Y)
        self.clsb2=Scrollbar(self.clfm,orient=HORIZONTAL)
        self.clsb2.pack(side=BOTTOM,fill=X)
        self.cllb=Listbox(self.clfm, height=15,
                            width=50, yscrollcommand=self.clsb.set)
        self.clsb.config(command=self.cllb.yview)
        self.clsb2.config(command=self.cllb.xview)
        self.cllb.pack(side=LEFT, fill=BOTH)
        self.clfm.pack()
        
        self.clbufm=Frame(self.top)
        self.clbu1=Button(self.clbufm,text='一键清理',command=self.clql)
        self.clbu2=Button(self.clbufm,text='高级',command=self.clzd)
        self.clbu1.pack(side=LEFT)
        self.clbu2.pack(side=LEFT)
        self.clbufm.pack()
        
        self.la2=Label(self.top,fg='red')
        self.la2.pack()
        
        self.startNewThread()
        
    
    def startNewThread(self):
        thread.start_new_thread(self.hel,())
    
    def hel(self):
        while 1>0:
            n=-1
            self.cllb.delete(0, END)
            self.ProMessage = os.popen('tasklist').readlines()
            for eachPro in self.ProMessage:
                n=n+1
                if n==1:
                    self.cllb.insert(END,eachPro.decode("mbcs"))
                else:
                    self.cllb.insert(END,eachPro)
            time.sleep(10)
    
    def clql(self):
        self.KillProclist = [
                    'PPLiveU.exe',
                    'PPLive.exe',
                    'BitCometService.exe',
                    'BitComet.exe',
                    'FTPServer.exe',
                    'QvodTerminal.exe',
                    'PPStream.exe',
                    'PPSAP.exe',
                    'emule.exe',
                    'QvodPlayer.exe',
                    'wireshark.exe ',
                    'SogouCloud.exe',
                    'PPAP.exe',
                    'IcbcDaemon.exe',]
        
        table={}
        for eachline in self.ProMessage:
            for sub in self.KillProclist:
                if eachline.find(sub)==0:
                    ret = re.search(rule,eachline) 
                    if ret is not None:
                        table.update({sub:ret.group(0)}) 

        if table == {}:
            self.la2.config( text='No useless process is running!')
        else:
            for key in table.keys():
                cmd='TaskKill /T /F /PID %s' % (table[key])
                os.popen(cmd)
                self.la2.config(text='success!')
                
    def clzd(self):
        os.popen('taskmgr')
    

####



####                   shut down
class shutdown:
    def __init__(self):
        self.top=Tk()
        self.top.title('Shut down')
        self.la=Label(self.top,text='Enter the time you want to shut down:')
        self.la.pack()
        
        self.sdVar1=StringVar(self.top)
        self.sdVar2=StringVar(self.top)
        
        ####         Entry
        self.sdFm=Frame(self.top)
        self.sbs1=Entry(self.sdFm,width=10,textvariable=self.sdVar1)
        self.sbs1.pack(side=LEFT)
        self.laa=Label(self.sdFm,text=' : ')
        self.laa.pack(side=LEFT)
        self.sbs2=Entry(self.sdFm,width=10,textvariable=self.sdVar2)
        self.sbs2.pack(side=LEFT)
        self.sdFm.pack()
        
        ####
        self.bu=Button(self.top,text='yes',command=self.startNewThread)
        self.bu.pack()
        self.la2=Label(self.top,fg='red')
        self.la2.pack()
        
        ####
        self.inh=[]
        self.inm=[]
        nh=0
        nm=0
        while nh<24:
            self.inh.append(nh)
            nh+=1
        while nm<60:  
            self.inm.append(nm)
            nm+=1
    
    def startNewThread(self):
        thread.start_new_thread(self.yy,())
    
    def yy(self):
        
        c1=False
        self.h=self.sdVar1.get()
        self.h=string.atoi(self.h,10)
        for eachh in self.inh:
            if self.h==eachh:
                c1=True
                break
            elif eachh==23:
                self.la2.config(text='Wrong!')
        
        c2=False
        self.m=self.sdVar2.get()
        self.m=string.atoi(self.m,10)
        for eachm in self.inm:           
            if self.m==eachm:
                c2=True
                break
            elif eachm==59:
                self.la2.config(text='Wrong!')
        
        self.sdVar1.set('')
        self.sdVar2.set('')
        
        if c1 and c2:
            self.la2.config(text='OK! ')
            yyee(self.h,self.m)
    

            
class yyee:    
    
    def __init__(self,h,m):
        rh=int(time.strftime("%H",time.localtime()))
        rm=int(time.strftime("%M",time.localtime()))
        cmd="cmd.exe /k shutdown -s -t 0"
    
        if h==rh:
            if m<=rm:
                os.system(cmd)
            else:
                time.sleep((m-rm)*60)
                os.system(cmd)
        elif h>rh:
            tem1=(h-rh-1)*3600+(60-rm+m)*60
            time.sleep(tem1)
            os.system(cmd)
        else:
            tem2=(23-rh+h)*3600+(60-rm+m)*60
            time.sleep(tem2)
            os.system(cmd)
####




####                  search
class search:
    
    def __init__(self): 
        self.top=Tk()
        self.top.title('Search')
        self.la=Label(self.top, text='Search:',fg='blue', font=('Helvetica', 12, 'bold'))
        self.la.pack()
        
        self.cwd = StringVar(self.top)
        
        ####  list box
        self.dirfm = Frame(self.top)
        self.dirswb = Scrollbar(self.dirfm)
        self.dirswb.pack(side=RIGHT, fill=Y)
        self.dirswbb = Scrollbar(self.dirfm, orient=HORIZONTAL)
        self.dirswbb.pack(side=BOTTOM,fill=X)
        self.dirsw = Listbox(self.dirfm, height=15,
                            width=50, yscrollcommand=self.dirswb.set)
        self.dirsw.bind('<Double-1>',self.dak)
        self.dirswb.config(command=self.dirsw.yview)
        self.dirswbb.config(command=self.dirsw.xview)
        self.dirsw.pack(side=LEFT, fill=BOTH)
        self.dirfm.pack()
        
        ####   Check button
        self.curfm = Frame(self.top)
        self.curfmm = Frame(self.curfm)
        self.curdiskss=self.existdisk()
        chbo=Checkbutton(self.curfmm,text=self.curdiskss[0],\
                         command=(lambda :self.callCheckButton(0)))
        chbo.pack(side=LEFT)
        chbw=Checkbutton(self.curfmm,text=self.curdiskss[1],\
                         command=(lambda :self.callCheckButton(1)))
        chbw.pack(side=LEFT)
        chbt=Checkbutton(self.curfmm,text=self.curdiskss[2],\
                         command=(lambda :self.callCheckButton(2)))
        chbt.pack(side=LEFT)
        chbf=Checkbutton(self.curfmm,text=self.curdiskss[3],\
                         command=(lambda :self.callCheckButton(3)))
        chbf.pack(side=LEFT)
        
        self.curfmm.pack()
        
        self.dirn = Entry(self.curfm, width=50,textvariable=self.cwd)
        self.dirn.bind('<Return>',self.search)
        self.dirn.pack(side=BOTTOM)
        self.curfm.pack()
        
        
        self.bu = Button(self.top,text='GO',
                         command=self.search,
                         activeforeground='white',
                         activebackground='blue')
        self.bu.pack()
        
        self.var=[]
        self.var.append('')
        self.var.append('')
        self.var.append('')
        self.var.append('')
        
        
    def search(self ,ev=None):
        self.startNewThread()

    def hel(self):
        src=self.cwd.get()
        self.la.config(text='Search:'+src)
        self.cwd.set('')
        self.dirsw.delete(0,END)
        self.dirsw.insert(END,'--begin--Please wait--')
        for disk in self.var:
            if not disk=='':
                self.dirsw.insert(END,'')
                self.dirsw.insert(END,'begin in--'+disk)
                disk = disk + '\\'
                self.SearchDirFile(disk, src)
        self.dirsw.insert(END, "完成搜索")
        
   
    def SearchDirFile(self,pa, srcc):
        for tt , dd, files in os.walk(pa):
            for file in files:
                file_path=os.path.join(tt,file)
                if srcc in file:
                    self.dirsw.insert(END,file_path)


    def startNewThread(self):
        thread.start_new_thread(self.hel,())

    def existdisk(self):
        self.curdisks = []
        allDisks = ['C:','D:','E:', 'F:', 'G:','H:','I:','J:', 'K:', \
                    'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', \
                    'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:', 'A:', 'B:']
        for disk in allDisks:
            if os.path.exists(disk):
                self.curdisks.append(disk)               
        return self.curdisks   

    
    def callCheckButton(self,nn):        
        self.cd=self.existdisk()
        self.var[nn]=self.cd[nn]
    
    def dak(self,dakev=None):
        self.dakk=self.dirsw.get(self.dirsw.curselection())
        self.dakk2='cd '+self.dakk
        os.popen(self.dakk)
####


####                    directory
class DirList(object):
    
    def __init__(self,initdir=None):
        self.top=Tk()
        self.top.title('Directory')
        self.label=Label(self.top,text='Directory Lister')
        self.label.pack()
    
        self.cwd = StringVar(self.top)

        self.dirl = Label(self.top, fg='blue', font=('Helvetica', 12, 'bold'))
        self.dirl.pack()
        
        self.dirfm = Frame(self.top)
        self.dirsb = Scrollbar(self.dirfm)
        self.dirsb.pack(side=RIGHT, fill=Y)
        self.dirs = Listbox(self.dirfm, height=15,
                            width=50, yscrollcommand=self.dirsb.set)
        self.dirs.bind('<Double-1>', self.setDirAndGo)
        self.dirsb.config(command=self.dirs.yview)
        self.dirs.pack(side=LEFT, fill=BOTH)
        self.dirfm.pack()
        
        self.dirn = Entry(self.top, width=50,
                          textvariable=self.cwd)
        self.dirn.bind('<Return>', self.doLS)
        self.dirn.pack()
        
        self.bfm = Frame(self.top)
        self.clr = Button(self.bfm, text='Clear',
                          command=self.clrDir,
                          activeforeground='white',
                          activebackground='blue')
        self.ls = Button(self.bfm,
                         text='List Directory',
                         command=self.doLS,
                         activeforeground='white',
                         activebackground='green')
        self.clr.pack(side=LEFT)
        self.ls.pack(side=LEFT)
        self.bfm.pack()
        
        if initdir:
            self.cwd.set(os.curdir)
            self.doLS()
            
    def clrDir(self, ev=None):
        self.cwd.set('')
    
    def setDirAndGo(self, ev=None):
        self.last = self.cwd.get()
        self.dirs.config(selectbackground='red')
        check = self.dirs.get(self.dirs.curselection())
        if not check:
            check = os.curdir
        self.cwd.set(check)
        self.doLS()
    
    def doLS(self, ev=None):
        error = ''
        tdir = self.cwd.get()
        if not tdir:
            tdir = os.curdir
        if not os.path.exists(tdir):
            error = tdir + ': no such file'
        elif not os.path.isdir(tdir):
            error = tdir + ': not a directory'
        
        if error:
            self.cwd.set(error)
            self.top.update()
            time.sleep(2)
            if not (hasattr(self, 'last') and self.last):
                self.last = os.curdir
            self.cwd.set(self.last)
            self.dirs.config(selectbackground='LightSkyBlue')
            self.top.update()
            return
        
        self.cwd.set('FETCHING DIRECTORY CONTENTS...')
        self.top.update()
        dirlist = os.listdir(tdir)
        dirlist.sort()
        os.chdir(tdir)
        self.dirl.config(text=os.getcwd())
        self.dirs.delete(0,END)
        self.dirs.insert(END, os.curdir)
        self.dirs.insert(END, os.pardir)
        for eachFile in dirlist:
            self.dirs.insert(END, eachFile)
        self.cwd.set(os.curdir)
        self.dirs.config(selectbackground='LightSkyBlue')
####


####              ji shi ben
class editor:
    def __init__(self,rt):

        self.top=Tk()
        self.top.title('记事本')
        self.top.geometry('300x400')
        self.bar=Menu(self.top)
  
        self.filem=Menu(self.bar)
        self.filem.add_command(label="打开",command=self.openfile)
        self.filem.add_command(label="新建",command=self.neweditor)
        self.filem.add_command(label="保存",command=self.savefile)
        self.filem.add_command(label="关闭",command=self.close)

        self.helpm=Menu(self.bar)
        self.helpm.add_command(label="Help",command=self.about)
        self.bar.add_cascade(label="文件",menu=self.filem)
        self.bar.add_cascade(label="帮助",menu=self.helpm)
        self.top.config(menu=self.bar)
  
        self.f=Frame(self.top,width=512)
        self.f.pack(expand=1,fill=BOTH)
  
        self.st=ScrolledText(self.f,background="white")
        self.st.pack(side=LEFT,fill=BOTH,expand=1)
        
    def close(self):
        self.top.destroy()
 
    def openfile(self):
        p1=END
        oname=askopenfilename()#filetypes=[("Python file","*.*")])
        if oname:
            for line in fileinput.input(oname):
                self.st.insert(p1,line)
                self.top.title(oname)
 
    def savefile(self):
        sname=asksaveasfilename()
        if sname:
            ofp=open(sname,"w")
            ofp.write(self.st.get(1.0,END).encode('utf-8'))
            ofp.flush()
            ofp.close()
            self.top.title(sname)
 
    def neweditor(self):
        global root
        self.top.append(editor(root))
        
        
    def about(self):
        tkMessageBox.showwarning("Tkeditor",'What?\n记事本也要帮助？')
####


####                info
class sysinfo:
    def __init__(self):
        self.top=Tk()
        self.top.title('system')
        self.la=Label(self.top,text='system infomation:')
        self.la.pack()
        
        self.infm=Frame(self.top)
        self.insb=Scrollbar(self.top)
        self.insb.pack(side='right',fill=Y)
        self.te=Listbox(self.infm, height=25,
                            width=70, yscrollcommand=self.insb.set)
        self.insb.config(command=self.te.yview())
        self.te.pack(side='left',fill=BOTH)
        self.infm.pack()
        
        
        na=os.popen('systeminfo').readlines()
        n=-1
        for each in na:
            n=n+1
            if n<32 or n>195:
                self.te.insert(END,each.decode("mbcs"))
####


####
def compmg():
    startNewTh()
def startNewTh():
    thread.start_new_thread(compmg2(),())  
def compmg2():
    sysinfo()


####            mu lu
def mulu():
    DirList(os.curdir)

####           ding shi guan
def dingshi():
    shutdown()



####            sou suo
def sousuo():
    search()


####               qing li
def qingli():
    clear()


####              su ji
def suji():
    root=None
    editor(root)


####              The primer
def fir():
    labe=Label(top)

####              guan  yu
def guanyu():
    tkMessageBox.showinfo("关于",'\n  free助手   v1.0'+'\n作者   csu cs 1101 王思宇')

####
def gaoji():
    tkMessageBox.showwarning("...",'此功能暂未开放')
    

    
####               mail
def mail():
    handle = smtplib.SMTP('smtp.163.com', 25)
    handle.login('py_free@163.com','174524wsy')
    msg = "To: 1847697670@qq.com\r\nFrom: py_free@163.com\r\nSubject: startpc \r\n\r\nstart,ip[1]\r\n"
    handle.sendmail('py_free@163.com','1847697670@qq.com', msg)



####              menu for the main
def MainMenu():
    MaMebar = Menu(top)
    
    #first
    cipanmenu = Menu(MaMebar)
    cipanmenu.add_command(label='目录', command=mulu)
    cipanmenu.add_command(label='搜索', command=sousuo)
    MaMebar.add_cascade(label='磁盘管理', menu=cipanmenu)
    
    #second
    sujimenu = Menu(MaMebar)
    sujimenu.add_command(label='便签', command=suji)
    MaMebar.add_cascade(label='速记', menu=sujimenu)  
    
    #third
    jinchmenu=Menu(MaMebar)
    jinchmenu.add_command(label='进程清理',command=qingli)
    MaMebar.add_cascade(label='进程清理',menu=jinchmenu)    
    
    #forth
    shezhimenu = Menu(MaMebar)
    shezhimenu.add_command(label='定时关机', command=dingshi)
    shezhimenu.add_command(label='设备信息', command=compmg)
    shezhimenu.add_command(label='高级',command=gaoji)
    MaMebar.add_cascade(label='pc管理',menu=shezhimenu)
    
    #fifth
    helpmenu = Menu(MaMebar)
    helpmenu.add_command(label='Help')#, command=openDirectory)
    helpmenu.add_separator()
    helpmenu.add_command(label='关于', command=guanyu)
    MaMebar.add_cascade(label='帮助', menu=helpmenu)
    
    top.config(menu=MaMebar)
####





####
if __name__=='__main__':
    top=Tk()
    top.title('Free  mini')
    top.geometry('300x350')
    fir()
    MainMenu()
#    mail()
    top.mainloop()

