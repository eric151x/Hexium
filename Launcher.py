import minecraft_launcher_lib
import subprocess
from tkinter import *
from tkinter import messagebox, ttk
import customtkinter
import os
from CTkListbox import *
from PIL import Image

yn_local = False

if yn_local:
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

    def callback(progress):
        progress["value"] = progress["progress"] * 100
        ver.update_idletasks()

    def baixar():
        global installed_versions
        decisao = messagebox.askokcancel("Quer instalar essa versão?", f"Tem certeza que quer instalar a versão {selesao.get()}?")
        if decisao:
            minecraft_launcher_lib.install.install_minecraft_version(selesao.get(), mc_dir, callback)
            messagebox.showinfo("Instalado!", f"Versão {selesao.get()} instalada com sucesso!")
            reload()

    versions = minecraft_launcher_lib.utils.get_version_list()

    idi = [v["id"] for v in versions]

    selesao = StringVar(ver)
    selesao.set(idi[0])

    lista = customtkinter.CTkOptionMenu(ver, values=selesao, *idi)
    list.set(idi[0])
    lista.grid(column=0, row=0)

    down = customtkinter.CTkButton(ver, text="Baixar", command=baixar)
    down.grid(column=0, row=1)

    progress = ttk.Progressbar(ver, orient="vertical", length=100, mode="determinate")
    progress.grid(column=1, row=0)

    ver.mainloop()

def start():
    versao = list.get(list.curselection())

    option = {"username": User.get(),
               "uuid": "1234567890abcdef1234567890abcdef",
               "token": ""
               }
    if local.get() != "Nenhum":
        option["gameDirectory"] = f"{mc_dir}\\instances\\{local.get()}"

    command = minecraft_launcher_lib.command.get_minecraft_command(version=versao, minecraft_directory=mc_dir, options=option)
    main.withdraw()
    subprocess.run(command)
    main.deiconify()

main = Tk()
main.title("NexusMC")
main.geometry("500x250")
#main.iconbitmap("logo.ico")
main.configure(bg="#1f1f1f")

User = customtkinter.CTkEntry(
    master=main,
    placeholder_text="Username",
    placeholder_text_color="#616161",
    font=("Arial", 14),
    text_color="#ffffff",
    height=30,
    width=180,
    border_width=2,
    corner_radius=15,
    border_color="#000000",
    bg_color="#1f1f1f",
    fg_color="#303030",
    )
User.place(x=0, y=0)

list = CTkListbox(main, hover_color="#21a346", highlight_color="#2fe964", height=160)
list.place(x=0, y=30)

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
    border_width=2,
    corner_radius=15,
    border_color="#000000",
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=start,
    )
comeca.place(x=400, y=210)

ins_ver = customtkinter.CTkButton(
    master=main,
    text="Instalar Versão",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
        hover_color="#21a346",
    height=30,
    width=95,
    border_width=2,
    corner_radius=15,
    border_color="#000000",
    bg_color="#1f1f1f",
    fg_color="#2fe964",
    command=install,
    )
ins_ver.place(x=10, y=210)

value_local = StringVar(main)
value_local.set("Nenhum")

local = customtkinter.CTkOptionMenu(main, variable=value_local, values=os.listdir(f"{mc_dir}\\instances"), fg_color="#21a346", button_color="#2fe964", hover=True, button_hover_color="#21a346")
local.place(x=350, y=10)

main.mainloop()