import minecraft_launcher_lib, subprocess, customtkinter, os, threading, uuid, configparser, sys, platform
from tkinter import *
from tkinter import messagebox
from CTkListbox import *
from pypresence import Presence
from shutil import rmtree

lau_ver = 1.0

if platform.system() == "Windows":
    if getattr(sys, 'frozen', False):
        icon = os.path.join(sys._MEIPASS, "logo.ico")
    else:
        icon = "logo.ico"

def icone(janela):
    if platform.system() == "Windows":
        janela.iconbitmap(icon)

config = configparser.ConfigParser()

if not os.path.isfile("./config.ini"):
    config["Launcher"] = {
        "local": False,
        "r_presence": False,
        "show_cmd": False,
        "jav_arguments": ""
    }
    config["Account"] = {
        "name": ""
    }
    config.write(open("config.ini", "w"))

config.read("config.ini")

RPC = Presence("1400279407565869168")

if config["Launcher"]["local"] == "True":
    if os.path.isdir(".minecraft"):
        mc_dir = os.path.join(os.getcwd(), ".minecraft")
    else:
        os.mkdir(".minecraft")
        mc_dir = os.path.join(os.getcwd(), ".minecraft")
else:
    mc_dir = minecraft_launcher_lib.utils.get_minecraft_directory()

def reload():
    global installed_versions
    list.delete(0,END)
    installed_versions = minecraft_launcher_lib.utils.get_installed_versions(mc_dir)
    for version in installed_versions:
        list.insert(END, version["id"])

def install():
    ver = customtkinter.CTk(fg_color="#1f1f1f")
    ver.title("Instalar versão")
    icone(ver)
    ver.geometry("300x270")

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
            minecraft_launcher_lib.install.install_minecraft_version(list_ver.get(), mc_dir, callback={"setProgress": setpro})
            progreso.set(0)
            messagebox.showinfo("Instalado!", f"Versão instalada com sucesso!")
            reload()

    def bai_thre():
        thread = threading.Thread(target=baixar)
        thread.start()

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

    release = [v for v in minecraft_launcher_lib.utils.get_version_list() if v["type"] == "release"]
    snapshot = [v for v in minecraft_launcher_lib.utils.get_version_list() if v["type"] == "snapshot"]
    alpha = [v for v in minecraft_launcher_lib.utils.get_version_list() if v["type"] == "old_alpha"]
    beta = [v for v in minecraft_launcher_lib.utils.get_version_list() if v["type"] == "old_beta"]

    types = customtkinter.CTkOptionMenu(ver, variable=StringVar(ver).set("Release"), values=["Lançamento", "Snapshot", "Alpha Antiga", "Beta Antiga"], fg_color="#21a346", button_color="#2fe964", hover=True, button_hover_color="#21a346", command=atualizar)
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

    list_ver = CTkListbox(ver, hover_color="#21a346", highlight_color="#2fe964", height=160, border_width=0, fg_color="#272727")
    list_ver.place(x=10, y=50)
    for version in release:
        list_ver.insert(END, version["id"])

    ver.mainloop()

def start():
    versao = list.get(list.curselection())

    if User.get() == "":
        aviso = messagebox.askyesno("Aviso!", "Você não colocou nenhum Nome, quer continuar?")
        if not aviso:
            return

    if not versao:
        messagebox.showerror("Erro!", "Selecione uma versão!")
        return

    uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, User.get())).replace("-", "")

    option = {"username": User.get(),
               "uuid": uid,
               "token": "",
               "launcher_name": "NexusMC",
               "launcher_version": str(lau_ver),
               }
    if local.get() != "Nenhum":
        option["gameDirectory"] = f"{mc_dir}/instances/{local.get()}"
    if jav_arg.get():
        option["jvmArguments"] = jav_arg.get().split()

    command = minecraft_launcher_lib.command.get_minecraft_command(version=versao, minecraft_directory=mc_dir, options=option)
    main.withdraw()

    if User.get() != "":
        nome = User.get()
    else:
        nome = "Nenhum Nome"

    if dis_rich.get():
        try:
            RPC.connect()
            RPC.update(
                details=nome,
                large_image="mine",
                large_text=versao,
                small_image="logo",
                small_text="Nexus MC",
                state=f"jogando {versao}"
                )
        except:
            pass

    if platform.system() == "Windows" and not show_cmd.get():
        processo = subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        processo = subprocess.Popen(command)

    processo.wait()

    if dis_rich.get():
        try:
            RPC.clear()
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
        text_color="#000000",
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
            os.rmdir(f"{mc_dir}/instances/{local.get()}")
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
        text_color="#000000",
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
        rmtree(f"{mc_dir}/versions/{list.get()}")
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

    widlabel = customtkinter.CTkLabel(delver, text=f"Você tem certeza que quer apagar {list.get()}?")
    widlabel.place(x=40, y=10)

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
        text_color="#000000",
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

main = customtkinter.CTk(fg_color="#1f1f1f")
main.title("NexusMC")
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
comeca.place(x=400, y=230)

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
    width=40,
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

dis_rich = customtkinter.CTkCheckBox(options_frame, text="Rich Presence", variable=customtkinter.BooleanVar(value=config["Launcher"]["r_presence"]), onvalue=True, offvalue=False, fg_color="#2fe964", hover=True, hover_color="#21a346")
dis_rich.place(x=5, y=5)

if platform.system() != "Windows":
    abilitado = DISABLED
else:
    abilitado = NORMAL

show_cmd = customtkinter.CTkCheckBox(options_frame, text="Mostrar Console", variable=customtkinter.BooleanVar(value=config["Launcher"]["show_cmd"]), onvalue=True, offvalue=False, fg_color="#2fe964", hover=True, hover_color="#21a346", state=abilitado)
show_cmd.place(x=5, y=35)

jav_arg = customtkinter.CTkEntry(options_frame, placeholder_text="Java Arguments", placeholder_text_color="#616161", font=("Arial", 14), text_color="#ffffff", height=30, width=130, border_width=0, corner_radius=15, bg_color="#272727", fg_color="#303030")
jav_arg.place(x=5, y=65)
if config["Launcher"]["jav_arguments"]:
    jav_arg.insert(0, config["Launcher"]["jav_arguments"])

list = CTkListbox(main, hover_color="#21a346", highlight_color="#2fe964", height=160, border_width=0, fg_color="#272727")
list.place(x=10, y=50)

reload()

def fechar():
    config["Launcher"]["r_presence"] = str(dis_rich.get())
    config["Launcher"]["show_cmd"] = str(show_cmd.get())
    config["Launcher"]["jav_arguments"] = jav_arg.get()
    config["Account"]["name"] = str(User.get())
    config.write(open("config.ini", "w"))
    main.destroy()

main.protocol("WM_DELETE_WINDOW", fechar)
main.mainloop()
