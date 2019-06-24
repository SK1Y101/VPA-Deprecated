import sys,threading,datetime,os,time,subprocess

def _say(text=""):
    for x in "System: "+str(text)+"\n":
        sys.stdout.write(x)
        time.sleep(0.003)

def _logtext(text="null"):
    y=open("log.txt","a")
    y.write("["+str(datetime.datetime.now())+"] - "+text[0].upper()+text[1:len(text)]+"\n")
    y.close()

def _startpers():
    import socket
    perpas="version:"+corever+"#"
    for x in modules+[":"]+module.persistfunc+[":"]+module.pstartfunc:
        perpas+=x+";"
    pers=threading.Thread(name="Persistent functions",target=lambda:subprocess.call(["python","persistent.py",perpas],creationflags=subprocess.CREATE_NEW_CONSOLE))
    pers.start()
    globals()["per_server"]=startlocalserver(multiply("LOaBIS"))
    globals()["per_module"]=addlocalclient(per_server)

def _closepers():
    send_message(per_module,"shutdown")
    per_server.close()

def startsoftware():
    coremem=getcoredata()
    for x in ["\n"]+getmem("logo",coremem):
        say(x)
    say((getmem("software",coremem))[0]+"\nVersion "+corever+" developed by "+str(getmem("development",coremem)[0]).split("\t")[0])
    while not globals()["Shutdown"]:
        getcom(listen("\nWhat would you like to do?"))

def getcom(text=""):
    text+=" "
    for x in module.cwords:
        if x in text:
            x=module.funcs[module.cwords.index(x)]
            break
    _logtext("Function: "+x.replace(" ","")+" requested by user")
    if x.replace(" ","")=="closesoftware":
        globals()["Shutdown"]=True
    try:
        globals()[x.replace(" ","")](text.replace(x,"").replace(module.cwords[module.funcs.index(x)],""))
    except Exception as e:
        _logtext("Could not perform function: "+str(x)+"\nError: "+str(type(e))+"; "+str(e))
        say("The function, "+str(x)+" could not be executed\n")

if __name__=="__main__":
    try:
        start_time=datetime.datetime.now()
        _logtext("Initialising Software")
        _say("Initialising Software")
        globals()["Shutdown"]=False
        modules=next(os.walk(os.getcwd()))[1]
        modules.sort()

        if "__pycache__" in modules:
            modules.pop(modules.index("__pycache__"))

        if "_core" in modules:
            modules.pop(modules.index("_core"))

        _logtext(str(len(modules))+" Modules located: "+str(modules))

        from _core import *
        init()
        corever=getmodinfo("_core")[1]
        _logtext("Core version: "+corever+" Loaded")
        os.system("title LOaBIS v"+str(corever)+" - Local Opperations and Basic Intelligence System")

        stable,unstable,not_inst=0,0,[]

        _logtext("Checking module dependancies")
        _say("Checking module dependancies")
        a=modules
        for x in a:
            b=getmodinfo(x)
            depend=b[4]
            if depend:
                if depend in modules:
                    modules.pop(modules.index(x))
                    modules.insert(modules.index(depend)+1,x)
                else:
                    not_inst.append(x)
                    modules.pop(modules.index(x))
        if len(a)-len(modules):
            _logtext(str(len(a)-len(modules))+" Modules missing dependencies")

        _logtext("Loading modules")
        _say("Loading modules")
        for x in modules:
            a=getmodinfo(x)
            modver,needed=a[1],a[3]
            b=simver(corever,modver)
            if b !=0:
                if module.checkmods(needed):
                    exec("from "+str(x)+" import *")
                    if b==2:
                        stable+=1
                    else:
                        unstable+=1
                else:
                    not_inst.append([x,modver])
                    modules.pop(modules.index(x))
            else:
                not_inst.append(x)
                modules.pop(modules.index(x))
        _logtext(str(stable)+" stable Modules loaded")
        _logtext(str(unstable)+" Unstable Modules loaded")
        _logtext(str(len(not_inst))+" Modules prevented from loading: "+str(not_inst))
        _say(str(stable+unstable)+" Modules loaded, "+str(len(not_inst))+" Modules prevented from loading")

        import_start=datetime.datetime.now()
        modules.insert(0,"_core")
        _logtext("Importing functions from: "+str(modules))
        _say("Importing functions")
        for x in modules:
            try:
                a=[]
                f=open(x+"/commands.txt","r")
                file=csv.reader(f)
                for row in file:
                    module.funcs.append(row[0].split(":")[1])
                    command=row[0].split(":")[0]
                    if not command[-1:]==" ":
                        command+=" "
                    module.cwords.append(command)
                    module.desc.append(row[1])
                    a.append(row[0].split(":")[1])
                f.close()
                _logtext("Importing functions from: "+str(x)+"; "+str(a))
            except Exception as e:
                _logtext("Could not load functions from: "+str(x)+"\nError: "+str(type(e))+"; "+str(e))
        import_time=divmod((datetime.datetime.now()-import_start).total_seconds(),60)
        _logtext("Function import complete, took "+str(import_time[0]*60+import_time[1])+" seconds")
        module.funcs.append("null")
        module.cwords.append("null")
        module.desc.append("a null function")

        _logtext("Retrieving modification functions")
        _say("Checking modification functions")
        a,b=[0,0,0,0,0],[0,0,0,0,0]
        offlimits=["getcom","_logtext","_say","checkbackup","writebackup","_startpers","_closepers"]
        for x in modules:
            z=getmodinfo(x)
            start,end,persist,old,new,pstartup=z[5],z[7],z[6],z[8],z[9],z[10]
            if start:
                b[0]+=1
                for y in start:
                    module.startfunc.append(y)
                    a[0]+=1
            if end:
                b[1]+=1
                for y in end:
                    a[1]+=1
                    module.shutdownfunc.append(y)
            if persist:
                b[2]+=1
                for y in persist:
                    a[2]+=1
                    module.persistfunc.append(y)
            if pstartup:
                b[4]+=1
                for y in pstartup:
                    a[4]+=1
                    module.pstartfunc.append(y)
            if old:
                b[3]+=1
                for y in range(len(old)):
                    a[3]+=1
                    if not old[y] in offlimits:
                        globals()[old[y]]=globals()[new[y]]

        _logtext("Modification functions retrieved")
        _say("Modification functions retrieved")
        _logtext(str(a[0])+" Startup functions loaded from "+str(b[0])+" modules")
        _logtext(str(a[1])+" shutdown functions loaded from "+str(b[1])+" modules")
        _logtext(str(a[2])+" persistent functions loaded from "+str(b[2])+" modules")
        _logtext(str(a[4])+" persistent startups loaded from "+str(b[4])+" modules")
        _logtext(str(a[3])+" replacement functions loaded from "+str(b[3])+" modules")

        if module.startfunc:
            _logtext("Executing "+str(len(module.startfunc))+" Startup functions; "+str(module.startfunc))
            _say(str(len(module.startfunc))+" Startup functions located")
            for x in module.startfunc:
                try:
                    globals()[str(x)]()
                except Exception as e:
                    _logtext("Could not perform startup function: "+str(x)+"\nError: "+str(type(e))+"; "+str(e))

        if module.persistfunc:
            _logtext("Starting "+str(len(module.persistfunc))+" persistent functions; "+str(module.persistfunc))
            _say("Starting up "+str(len(module.persistfunc))+" persistent functions")
            _startpers()

        elapsed_time=divmod((datetime.datetime.now()-start_time).total_seconds(),60)
        _logtext("Import successfull, took "+str(elapsed_time[0]*60+elapsed_time[1])+" seconds")
        _say("Software initialised")

        startsoftware()

    except Exception as e:
        _logtext("Software aborted unexpectedly, Consider submitting log to developers.\nError: "+str(type(e))+"; "+str(e)+"\n")
    _closepers()
