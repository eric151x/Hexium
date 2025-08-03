import minecraft_launcher_lib
import subprocess
from tkinter import *
from tkinter import messagebox
import customtkinter
import os
from CTkListbox import *
from PIL import Image
from pypresence import Presence
import uuid
import configparser

yn_local = False

config = configparser.ConfigParser()

if not os.path.isfile(".\\config.ini"):
    config["Launcher"] = {
        "local": False,
        "r_presence": False
    }
    config["Account"] = {
        "name": ""
    }
    config.write(open("config.ini", "w"))

config.read("config.ini")

RPC = Presence("1400279407565869168")

if config["Launcher"]["local"]:
    if os.path.isdir(".minecraft"):
        mc_dir = os.path.join(os.getcwd(), ".minecraft")
    else:
        os.mkdir(".minecraft")
        mc_dir = os.path.join(os.getcwd(), ".minecraft")
else:
    mc_dir = minecraft_launcher_lib.utils.get_minecraft_directory()

def reload():
    global installed_versions
    installed_versions = minecraft_launcher_lib.utils.get_installed_versions(mc_dir)
    for version in installed_versions:
        list.insert(END, version["id"])

def install():
    ver = Tk()
    ver.title("Instalar versão")
    ver.iconbitmap("logo.ico")
    ver.configure(bg="#1f1f1f")

    def baixar():
        global installed_versions
        decisao = messagebox.askokcancel("Quer instalar essa versão?", f"Tem certeza que quer instalar a versão ?")
        if decisao:
            minecraft_launcher_lib.install.install_minecraft_version("colocar negócio", mc_dir)
            messagebox.showinfo("Instalado!", f"Versão instalada com sucesso!")
            reload()

    ver.mainloop()

def start():
    versao = list.get(list.curselection())

    if User.get() == "":
        aviso = messagebox.askyesno("Aviso!", "Você não colocou nenhum Nome, quer continuar?")
        if not aviso:
            return

    if not versao:
        messagebox.showerror("Erro", "Selecione uma versão!")
        return

    uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, User.get())).replace("-", "")

    option = {"username": User.get(),
               "uuid": uid,
               "token": ""
               }
    if local.get() != "Nenhum":
        option["gameDirectory"] = f"{mc_dir}\\instances\\{local.get()}"

    command = minecraft_launcher_lib.command.get_minecraft_command(version=versao, minecraft_directory=mc_dir, options=option)
    main.withdraw()

    if User.get() != "":
        nome = User.get()
    else:
        nome = "Nenhum Nome"

    if dis_rich.get():
        RPC.connect()
        RPC.update(
            details=nome,
            large_image="mine",
            large_text=versao,
            small_image="logo",
            small_text="Nexus MC",
            state=f"jogando {versao}"
            )
    subprocess.run(command)
    if dis_rich.get():
        RPC.clear()
    main.deiconify()

def instance():
    global inst
    def make_ins():
        if in_name.get() == None:
            messagebox.showerror("Erro!", "Coloque algum nome")
        else:
            os.mkdir(f"{mc_dir}\\instances\\{in_name.get()}")
            loc = os.listdir(f"{mc_dir}\\instances")
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

    inswin = Tk()
    inswin.title("Criar Local")
    inswin.geometry("300x150")
    inswin.iconbitmap("logo.ico")
    inswin.configure(bg="#1f1f1f")

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
            os.rmdir(f"{mc_dir}\\instances\\{local.get()}")
            loc = os.listdir(f"{mc_dir}\\instances")
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
            messagebox.showerror("Erro", "Selecione uma instância")
            
    def exit():
        try:
            delwin.quit()
            delwin.destroy()
        except:
            pass

    delwin = Tk()
    delwin.title("Cuidado!!!")
    delwin.geometry("300x120")
    delwin.iconbitmap("logo.ico")
    delwin.configure(bg="#1f1f1f")

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

main = Tk()
main.title("NexusMC")
main.geometry("500x270")
main.iconbitmap("logo.ico")
main.configure(bg="#1f1f1f")

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
    fg_color="#303030",
    )
User.place(x=10, y=10)
if config["Account"]["Name"]:
    User.insert(0, config["Account"]["Name"])

list = CTkListbox(main, hover_color="#21a346", highlight_color="#2fe964", height=160, border_width=0, fg_color="#272727")
list.place(x=10, y=50)

reload()

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

value_local = StringVar(main)
value_local.set("Nenhum")

if os.path.isdir(f"{mc_dir}\\instances"):
    inst = os.listdir(f"{mc_dir}\\instances")
else:
    os.mkdir(f"{mc_dir}\\instances")
    inst = os.listdir(f"{mc_dir}\\instances")
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

dis_rich = customtkinter.CTkCheckBox(main, text="Rich Presence", variable=customtkinter.BooleanVar(value=config["Launcher"]["r_presence"]), onvalue=True, offvalue=False, fg_color="#2fe964", hover=True, hover_color="#21a346")
dis_rich.place(x=350, y=50)

def fechar():
    config["Launcher"]["r_presence"] = str(dis_rich.get())
    config["Account"]["name"] = str(User.get())
    config.write(open("config.ini", "w"))
    main.destroy()

main.protocol("WM_DELETE_WINDOW", fechar)
main.mainloop()

