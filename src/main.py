import minecraft_launcher_lib, subprocess, customtkinter, os, threading, uuid, configparser, sys, platform, requests, webbrowser, wget
from tkinter import *
from tkinter import messagebox
from CTkListbox import *
from pypresence import Presence
import shutil

versao = 1.3

#Identifica se a versão é beta
if True:
    #Versão do launcher
    lau_ver = str(versao) + " " + "Beta"
else:
    lau_ver = versao

#Para identificar qual OS está sendo usado
if platform.system() == "Windows":
    #Para identificar está sendo rodado o código ou o executável
    if getattr(sys, 'frozen', False):
        icon = os.path.join(sys._MEIPASS, "logo.ico")
    else:
        icon = "logo.ico"

def icone(janela):
    if platform.system() == "Windows":
        janela.iconbitmap(icon)

#Aqui cria o arquivo de configuração caso não exista
config = configparser.ConfigParser()

if not os.path.isfile("./config.ini"):
    config["Launcher"] = {
        "ely.by": False,
        "show_cmd": False,
        "jav_arguments": ""
    }
    config["Account"] = {
        "name": ""
    }
    config["Config"] = {
        "check_atu": True,
        "local": False,
        "r_presence": False,
        "save_log": True
    }
    config.write(open("config.ini", "w"))

#Isso lê o arquivo de configuração
config.read("config.ini")

#Receber a versão mais recente
try:
    response = requests.get("https://api.github.com/repos/eric151x/Hexium/releases/latest")
    response.raise_for_status()
    latest_version = response.json().get("name").lstrip("vV")
except:
    pass

#Verifica se a versão atual é inferior a versão mais recente
def latest_function():
    try:
        if float(lau_ver) < float(latest_version):
            atu_message = messagebox.askyesno("Nova atualização!", "Nova atualização Disponível! Deseja baixar?")
            if atu_message:
                webbrowser.open("https://github.com/eric151x/Hexium/releases/latest")
    except:
        pass

#ID do Rich Presence
RPC = Presence("1400279407565869168")

#Isso define se vai ler a pasta do Minecraft local ou do AppData
if config["Config"]["local"] == "True":
    if os.path.isdir(".minecraft"):
        mc_dir = os.path.join(os.getcwd(), ".minecraft")
    else:
        os.mkdir(".minecraft")
        mc_dir = os.path.join(os.getcwd(), ".minecraft")
else:
    mc_dir = minecraft_launcher_lib.utils.get_minecraft_directory()

# Recarrega a lista das versões
def reload():
    global installed_versions
    list.delete(0,END)
    installed_versions = minecraft_launcher_lib.utils.get_installed_versions(mc_dir)
    for version in installed_versions:
        list.insert(END, version["id"])

#Janela de instalação de versão
def install():
    ver = customtkinter.CTk(fg_color="#1f1f1f")
    ver.title("Instalar versão")
    icone(ver)
    ver.geometry("230x270")

    #Definir o progresso da barra
    def setpro(baixado):
        progreso.set(baixado / 1000)

    def baixar():
        global installed_versions
        for ver in installed_versions:
            if list_ver.get() in ver["id"]:
                messagebox.showwarning("Aviso!", "Essa versão já existe")
                return        
        decisao = messagebox.askokcancel("Quer instalar essa versão?", f"Tem certeza que quer instalar a versão {list_ver.get()}?")
        if decisao:
            instal.configure(text="Baixando...", state=DISABLED, fg_color="#21a346")
            minecraft_launcher_lib.install.install_minecraft_version(list_ver.get(), mc_dir, callback={"setProgress": setpro})
            instal.configure(text="Baixar", state=NORMAL, fg_color="#2fe964")
            progreso.set(0)
            reload()
            messagebox.showinfo("Instalado!", f"Versão instalada com sucesso!")

    #Começa a instalação em outro Thread
    def bai_thre():
        thread = threading.Thread(target=baixar)
        thread.start()

    #Atualiza a lista quando seleciona alguma opção
    def atualizar(valor):
        list_ver.delete(0,END)
        if valor == "Lançamento":
            for v in release:
                list_ver.insert(END, v["id"])
        elif valor == "Snapshot":
            for v in snapshot:
                list_ver.insert(END, v["id"])
        elif valor == "Alpha Antiga":
            for v in alpha:
                list_ver.insert(END, v["id"])
        elif valor == "Beta Antiga":
            for v in beta:
                list_ver.insert(END, v["id"])

    #Lista dos tipos de versões
    release = [v for v in minecraft_launcher_lib.utils.get_version_list() if v["type"] == "release"]
    snapshot = [v for v in minecraft_launcher_lib.utils.get_version_list() if v["type"] == "snapshot"]
    alpha = [v for v in minecraft_launcher_lib.utils.get_version_list() if v["type"] == "old_alpha"]
    beta = [v for v in minecraft_launcher_lib.utils.get_version_list() if v["type"] == "old_beta"]

    types = customtkinter.CTkOptionMenu(ver, variable=StringVar(ver).set("Lançamento"), values=["Lançamento", "Snapshot", "Alpha Antiga", "Beta Antiga"], fg_color="#21a346", button_color="#2fe964", hover=True, button_hover_color="#21a346", command=atualizar)
    types.place(x=10, y=10)

    instal = customtkinter.CTkButton(
    master=ver,
    text="Baixar",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#21a346",
    height=30,
    width=170,
    corner_radius=15,
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=bai_thre,
    )
    instal.place(x=10, y=230)

    progreso = customtkinter.CTkProgressBar(ver, progress_color="#2fe964", fg_color="#272727", orientation="vertical", height=172, width=20, )
    progreso.place(x=190, y=50)
    progreso.set(0)

    list_ver = CTkListbox(ver, hover_color="#21a346", text_color="#ffffff", highlight_color="#2fe964", height=160, border_width=0, fg_color="#272727")
    list_ver.place(x=10, y=50)
    for version in release:
        list_ver.insert(END, version["id"])

    ver.mainloop()

#Função de logar na conta Ely.by
def login():
    logar = customtkinter.CTk(fg_color="#1f1f1f")
    logar.title("Login")
    logar.geometry("300x180")
    icone(logar)

    def exit():
        global access, request, username, uid
        try:
            logar.quit()
            logar.destroy()
            access = None
            request = None
            username = None
            uid = None
        except:
            pass

    def auth():
        global access, request, username, uid
        params = {
            "username": name.get(),
            "password": passwd.get(),
            "clientToken": str(uuid.uuid4())
        }
        try:
            r = requests.post("https://authserver.ely.by/auth/authenticate", json=params)
            dados = r.json()
            if "error" in dados:
                messagebox.showerror("Erro!", dados["errorMessage"])
                return
        except Exception as e:
            messagebox.showerror("Erro!", "Erro de conexão.")
            return
        access = dados["accessToken"]
        request = dados["clientToken"]
        username = dados["selectedProfile"]["name"]
        uid = dados["selectedProfile"]["id"]
        logar.quit()
        logar.destroy()


    text = customtkinter.CTkLabel(logar, text="Por favor entre na sua conta Ely.by. (pedirá suas credenciais somente uma vez e não irá salvar)", wraplength=280)
    text.place(relx=0.5, y=10, anchor="n")

    name = customtkinter.CTkEntry(
        master=logar,
        placeholder_text="Username",
        placeholder_text_color="#616161",
        font=("Arial", 14),
        text_color="#ffffff",
        height=30,
        width=220,
        border_width=0,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#303030"
        )
    name.place(relx=0.5, y=50, anchor="n")

    passwd = customtkinter.CTkEntry(
        master=logar,
        placeholder_text="Senha",
        placeholder_text_color="#616161",
        font=("Arial", 14),
        text_color="#ffffff",
        height=30,
        width=220,
        border_width=0,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#303030"
        )
    passwd.place(relx=0.5, y=90, anchor="n")

    logar_button = customtkinter.CTkButton(
        master=logar,
        text="Login",
        font=("undefined", 14),
        text_color="#000000",
        hover=True,
        hover_color="#21a346",
        height=30,
        width=95,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#2fe964",
        command=auth
        )
    logar_button.place(x=160, y=130)

    cancelar = customtkinter.CTkButton(
        master=logar,
        text="Cancelar",
        font=("undefined", 14),
        text_color="#ffffff",
        hover=True,
        hover_color="#222222",
        height=30,
        width=95,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#303030",
        command=exit
        )
    cancelar.place(x=50, y=130)

    logar.mainloop()
    return access, request, username, uid

#Função de executar o minecraft
def start():
    versao = list.get(list.curselection())
    natives = os.path.join(mc_dir, "versions", versao, "natives")    
    args = f"-Djava.library.path={natives}" + " " + jav_arg.get()

    if not versao:
        messagebox.showerror("Erro!", "Selecione uma versão!")
        return

    try:
        shutil.rmtree(natives)
    except:
        pass
    minecraft_launcher_lib.natives.extract_natives(versao, mc_dir, natives)

    if User.get() == "":
        aviso = messagebox.askyesno("Aviso!", "Você não colocou nenhum Nome, quer continuar?")
        if not aviso:
            return

    if ely.get():
        #Baixa caso o authlib injector não esteja baixado
        if not os.path.exists("authlib-injector-1.2.7.jar"):
            wget.download("https://authlib-injector.yushi.moe/artifact/55/authlib-injector-1.2.7.jar", "authlib-injector-1.2.7.jar")

        if not config["Account"].get("access"):
            access, client, name, uid = login()
            if access:
                config["Account"]["access"] = access
                config["Account"]["client"] = client
                config["Account"]["name_ely"] = name
                config["Account"]["uuid_ely"] = uid
                config.write(open("config.ini", "w"))
            else:
                return
        else:
            access = config["Account"]["access"]
            client = config["Account"]["client"]
            name = config["Account"]["name_ely"]
            uid = config["Account"]["uuid_ely"]
        
        #Adiciona o argumento authlib injector
        ely_arg = "-javaagent:authlib-injector-1.2.7.jar=ely.by" + " " + args

    #UUID
    if not ely.get():
        uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, User.get())).replace("-", "")
        name = User.get()
        access = ""

    #Opções
    option = {"username": name,
               "uuid": uid,
               "token": access,
               "launcher_name": "Hexium",
               "launcher_version": str(lau_ver),
               }
    if local.get() != "Nenhum":
        option["gameDirectory"] = f"{mc_dir}/instances/{local.get()}"
    if ely.get():
        option["jvmArguments"] = ely_arg.split()
    else:
        if jav_arg.get():
            option["jvmArguments"] = args.split()

    #Comandos de inicialização
    command = minecraft_launcher_lib.command.get_minecraft_command(version=versao, minecraft_directory=mc_dir, options=option)
    main.withdraw()

    if not User.get() and not ely.get():
        nome = "Nenhum Nome"

    #Rich Presence
    if config["Config"]["r_presence"] == "True":
        try:
            RPC.connect()
            RPC.update(
                details=nome,
                large_image="mine",
                large_text=versao,
                small_image="logo",
                small_text=f"v{lau_ver}"
                )
        except:
            pass

    #Iniciar o Minecraft
    if platform.system() == "Windows" and not show_cmd.get():
        processo = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        processo = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    processo.wait()

    #Salvar no log
    if config["Config"]["save_log"] == "True":
        stdout, stderr = processo.communicate()
        with open("log.txt", "w") as f:
            if stdout:
                f.write("===STDOUT===\n")
                f.write(stdout)
            if stderr:
                f.write("===STDERR===\n")
                f.write(stderr)

    try:
        RPC.clear()
    except:
        pass

    try:
        shutil.rmtree(natives)
    except:
        pass

    main.deiconify()

def instance():
    global inst
    def make_ins():
        if in_name.get() == None:
            messagebox.showerror("Erro!", "Coloque algum nome")
        else:
            os.mkdir(f"{mc_dir}/instances/{in_name.get()}")
            loc = os.listdir(f"{mc_dir}/instances")
            loc.insert(0, "Nenhum")
            local.configure(values=loc)
            local.set(loc[0])
            inswin.quit()
            inswin.destroy()
            messagebox.showinfo("Pronto!", "Criado com sucesso!")

    def sair():
        try:
            inswin.quit()
            inswin.destroy()
        except:
            pass

    inswin = customtkinter.CTk(fg_color="#1f1f1f")
    inswin.title("Criar Local")
    inswin.geometry("300x150")
    icone(inswin)

    widlabel = customtkinter.CTkLabel(inswin, text="Criar Local de Jogo")
    widlabel.place(x=100, y=10)

    in_name = customtkinter.CTkEntry(
        master=inswin,
        placeholder_text="Nome",
        placeholder_text_color="#616161",
        font=("Arial", 14),
        text_color="#ffffff",
        height=30,
        width=175,
        border_width=0,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#303030")
    in_name.place(x=70, y=50)

    criar = customtkinter.CTkButton(
        master=inswin,
        text="Criar",
        font=("undefined", 14),
        text_color="#000000",
        hover=True,
        hover_color="#21a346",
        height=30,
        width=95,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#2fe964",
        command=make_ins
        )
    criar.place(x=160, y=90)

    cancel = customtkinter.CTkButton(
        master=inswin,
        text="Cancelar",
        font=("undefined", 14),
        text_color="#ffffff",
        hover=True,
        hover_color="#222222",
        height=30,
        width=95,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#303030",
        command=sair
        )
    cancel.place(x=50, y=90)

    inswin.mainloop()

def apagar():
    global inst

    def dele():
        if local.get() != "Nenhum":
            shutil.rmtree(f"{mc_dir}/instances/{local.get()}")
            loc = os.listdir(f"{mc_dir}/instances")
            loc.insert(0, "Nenhum")
            local.configure(values=loc)
            local.set(loc[0])
            try:
                delwin.quit()
                delwin.destroy()
            except:
                pass
            messagebox.showinfo("Pronto!", "Apagado com sucesso!")
        else:
            messagebox.showerror("Erro!", "Selecione uma instância")
            
    def exit():
        try:
            delwin.quit()
            delwin.destroy()
        except:
            pass

    delwin = customtkinter.CTk(fg_color="#1f1f1f")
    delwin.title("Cuidado!")
    delwin.geometry("300x120")
    icone(delwin)

    widlabel = customtkinter.CTkLabel(delwin, text="Você tem certeza que quer apagar?")
    widlabel.place(x=55, y=10)

    deletar = customtkinter.CTkButton(
        master=delwin,
        text="Sim",
        font=("undefined", 14),
        text_color="#000000",
        hover=True,
        hover_color="#a32121",
        height=30,
        width=95,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#e92f2f",
        command=dele
        )
    deletar.place(x=160, y=60)

    cancelar = customtkinter.CTkButton(
        master=delwin,
        text="Cancelar",
        font=("undefined", 14),
        text_color="#ffffff",
        hover=True,
        hover_color="#222222",
        height=30,
        width=95,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#303030",
        command=exit
        )
    cancelar.place(x=50, y=60)

    delwin.mainloop()

def delete_version():
    if not list.get():
        messagebox.showerror("Erro!", "Selecione uma versão!")
        return

    def dele_ver():
        shutil.rmtree(f"{mc_dir}/versions/{list.get()}")
        reload()
        messagebox.showinfo("Pronto!", "versão desinstalada com sucesso!")
        exit()

    def exit():
        try:
            delver.quit()
            delver.destroy()
        except:
            pass

    delver = customtkinter.CTk(fg_color="#1f1f1f")
    delver.title("Cuidado!")
    delver.geometry("300x120")
    icone(delver)

    widlabel = customtkinter.CTkLabel(delver, text=f"Você tem certeza que quer apagar {list.get()}?", wraplength=280)
    widlabel.place(relx=0.5, y=10, anchor="n")

    deletar = customtkinter.CTkButton(
        master=delver,
        text="Sim",
        font=("undefined", 14),
        text_color="#000000",
        hover=True,
        hover_color="#a32121",
        height=30,
        width=95,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#e92f2f",
        command=dele_ver
        )
    deletar.place(x=160, y=60)

    cancelar = customtkinter.CTkButton(
        master=delver,
        text="Cancelar",
        font=("undefined", 14),
        text_color="#ffffff",
        hover=True,
        hover_color="#222222",
        height=30,
        width=95,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#303030",
        command=exit
        )
    cancelar.place(x=50, y=60)

    delver.mainloop()

def desconect_conta_ely():
    yesorno = messagebox.askokcancel("Cuidado!", "Você quer desconectar sua conta Ely.By?")
    if yesorno:
        if config.has_option("Account", "access"):
            params = {
                "accessToken": config["Account"]["access"],
                "clientToken": config["Account"]["client"]
            }
            r = requests.post("https://authserver.ely.by/auth/invalidate", json=params)

            config.remove_option("Account", "access")
            config.remove_option("Account", "client")
            config.remove_option("Account", "name_ely")
            config.remove_option("Account", "uuid_ely")

            config.write(open("config.ini", "w"))

            messagebox.showinfo("Pronto!", "Conta desconectada com sucesso!")
        else:
            messagebox.showerror("Erro!", "Nenhuma conta logada.")

def win_config():
    def save_config():
        config["Config"]["r_presence"] = str(dis_rich.get())
        config["Config"]["local"] = str(local_button.get())
        config["Config"]["check_atu"] = str(check_atu.get())
        config["Config"]["save_log"] = str(log_check.get())
        config.write(open("config.ini", "w"))
        config_tk.quit()
        config_tk.destroy()

    def quit():
        config_tk.quit()
        config_tk.destroy()

    config_tk = customtkinter.CTk(fg_color="#1f1f1f")
    config_tk.title("Configurações")
    config_tk.geometry("400x300")
    icone(config_tk)

    check_atu = customtkinter.CTkCheckBox(config_tk, text="Verificar novas atualizações", text_color="#ffffff", variable=customtkinter.BooleanVar(value=config["Config"]["check_atu"]), onvalue=True, offvalue=False, fg_color="#2fe964", hover=True, hover_color="#21a346")
    check_atu.place(x=10, y=10)

    local_button = customtkinter.CTkCheckBox(config_tk, text=".minecraft na pasta local (Precisa reiniciar)", text_color="#ffffff", variable=customtkinter.BooleanVar(value=config["Config"]["local"]), onvalue=True, offvalue=False, fg_color="#2fe964", hover=True, hover_color="#21a346")
    local_button.place(x=10, y=80)

    dis_rich = customtkinter.CTkCheckBox(config_tk, text="Rich Presence", text_color="#ffffff", variable=customtkinter.BooleanVar(value=config["Config"]["r_presence"]), onvalue=True, offvalue=False, fg_color="#2fe964", hover=True, hover_color="#21a346")
    dis_rich.place(x=10, y=110)

    log_check = customtkinter.CTkCheckBox(config_tk, text="Salvar Log", text_color="#ffffff", variable=customtkinter.BooleanVar(value=config["Config"]["save_log"]), onvalue=True, offvalue=False, fg_color="#2fe964", hover=True, hover_color="#21a346")
    log_check.place(x=10, y=140)

    save = customtkinter.CTkButton(
    master=config_tk,
    text="Salvar",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#21a346",
    height=30,
    width=100,
    corner_radius=15,
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=save_config
    )
    save.place(x=290, y=260)

    cancel = customtkinter.CTkButton(
        master=config_tk,
        text="Cancelar",
        font=("undefined", 14),
        text_color="#ffffff",
        hover=True,
        hover_color="#222222",
        height=30,
        width=100,
        corner_radius=15,
        bg_color="#1f1f1f",
        fg_color="#303030",
        command=quit
        )
    cancel.place(x=180, y=260)

    check_now = customtkinter.CTkButton(
    master=config_tk,
    text="Verificar atualização agora",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#21a346",
    height=30,
    width=100,
    corner_radius=15,
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=latest_function
    )
    check_now.place(x=10, y=40)

    delete_ely = customtkinter.CTkButton(
    master=config_tk,
    text="Desconectar conta Ely.By",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#21a346",
    height=30,
    width=100,
    corner_radius=15,
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=desconect_conta_ely
    )
    delete_ely.place(x=10, y=170)

    config_tk.mainloop()

def toggle():
    if ely.get():
        User.configure(state="disabled")
        User.configure(fg_color="#101010")
    else:
        User.configure(state="normal")
        User.configure(fg_color="#303030")

main = customtkinter.CTk(fg_color="#1f1f1f")
main.title("Hexium")
main.geometry("500x270")
icone(main)

User = customtkinter.CTkEntry(
    master=main,
    placeholder_text="Username",
    placeholder_text_color="#616161",
    font=("Arial", 14),
    text_color="#ffffff",
    height=30,
    width=175,
    border_width=0,
    corner_radius=15,
    bg_color="#1f1f1f",
    fg_color="#303030"
    )
User.place(x=10, y=10)
if config["Account"]["Name"]:
    User.insert(0, config["Account"]["Name"])

comeca = customtkinter.CTkButton(
    master=main,
    text="Iniciar",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#21a346",
    height=30,
    width=95,
    corner_radius=15,
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=start,
    )
comeca.place(x=395, y=230)

ins_ver = customtkinter.CTkButton(
    master=main,
    text="Instalar Versão",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#21a346",
    height=30,
    width=95,
    corner_radius=15,
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=install,
    )
ins_ver.place(x=10, y=230)

des_ver = customtkinter.CTkButton(
    master=main,
    text="-",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#21a346",
    height=30,
    width=41,
    corner_radius=15,
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=delete_version,
    )
des_ver.place(x=140, y=230)

value_local = StringVar(main)
value_local.set("Nenhum")

if os.path.isdir(f"{mc_dir}/instances"):
    inst = os.listdir(f"{mc_dir}/instances")
else:
    os.mkdir(f"{mc_dir}/instances")
    inst = os.listdir(f"{mc_dir}/instances")
inst.insert(0, "Nenhum")

local = customtkinter.CTkOptionMenu(main, variable=value_local, values=inst, fg_color="#21a346", button_color="#2fe964", hover=True, button_hover_color="#21a346")
local.place(x=350, y=10)

mais = customtkinter.CTkButton(
    master=main,
    text="+",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#21a346",
    height=29,
    width=29,
    corner_radius=5,
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=instance)
mais.place(x=320, y=10)

menos = customtkinter.CTkButton(
    master=main,
    text="-",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#21a346",
    height=29,
    width=29,
    corner_radius=5,
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=apagar)
menos.place(x=290, y=10)

options_frame = customtkinter.CTkFrame(main, fg_color="#272727", height=100, width=140)
options_frame.place(x=350, y=50)

ely = customtkinter.CTkCheckBox(options_frame, text="Ely.by", text_color="#ffffff", variable=customtkinter.BooleanVar(value=config["Launcher"]["ely.by"]), onvalue=True, offvalue=False, fg_color="#2fe964", hover=True, hover_color="#21a346", command=toggle)
ely.place(x=5, y=5)

toggle()

if platform.system() != "Windows":
    abilitado = DISABLED
else:
    abilitado = NORMAL

show_cmd = customtkinter.CTkCheckBox(options_frame, text="Mostrar Console", text_color="#ffffff", variable=customtkinter.BooleanVar(value=config["Launcher"]["show_cmd"]), onvalue=True, offvalue=False, fg_color="#2fe964", hover=True, hover_color="#21a346", state=abilitado)
show_cmd.place(x=5, y=35)

jav_arg = customtkinter.CTkEntry(options_frame, placeholder_text="Java Arguments", placeholder_text_color="#616161", font=("Arial", 14), text_color="#ffffff", height=30, width=130, border_width=0, corner_radius=15, bg_color="#272727", fg_color="#303030")
jav_arg.place(x=5, y=65)
if config["Launcher"]["jav_arguments"]:
    jav_arg.insert(0, config["Launcher"]["jav_arguments"])

button_config = customtkinter.CTkButton(
    master=main,
    text="Configurações",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#21a346",
    height=30,
    width=140,
    corner_radius=15,
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=win_config,
    )
button_config.place(x=350, y=160)

ver_lau = customtkinter.CTkLabel(main, text_color="#404040", text=f"v{lau_ver}")
ver_lau.place(x=250, y=240)

list = CTkListbox(main, hover_color="#21a346", text_color="#ffffff", highlight_color="#2fe964", height=160, border_width=0, fg_color="#272727")
list.place(x=10, y=50)

reload()

def fechar():
    config["Launcher"]["ely.by"] = str(ely.get())
    config["Launcher"]["show_cmd"] = str(show_cmd.get())
    config["Launcher"]["jav_arguments"] = jav_arg.get()
    config["Account"]["name"] = str(User.get())
    config.write(open("config.ini", "w"))
    main.destroy()

if config["Config"]["check_atu"] == "True":
    main.after(500, latest_function)

main.protocol("WM_DELETE_WINDOW", fechar)
main.mainloop()
