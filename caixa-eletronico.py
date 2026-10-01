import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Canvas
from tkinter import messagebox

janela = Tk()
janela.geometry("500x400")
janela.title("Banco Eletronico")
janela.config(bg= "aliceblue")
janela.resizable(False, False)

estilo = ttk.Style()
estilo.theme_use('clam')

#----------- Titulo -----------
label_boasvindas = tk.Label(janela, text="Bem vindo ao Caixa Eletrônico!", bg= "aliceblue",font=("Arial", 15, "bold"))
label_boasvindas.pack(padx=10)

#----------- Label conta e senha -----------
label_usuario = tk.Label(janela, text="Digite sua Conta:",bg= "aliceblue", font=("Arial", 12))
label_usuario.pack(anchor="w")

label_senha = tk.Label(janela, text="Digite sua senha:",bg= "aliceblue", font=("Arial", 12))
label_senha.pack(anchor="w")


#----------- Frame onde vai ficar as opções do Menu -----------

frame_principal = tk.Frame(janela, bg="white" ,padx=25, pady=25)
frame_principal.pack(fill="both", expand=True, padx=25, pady=(0, 25))

#----------- Label do menu -----------
label_menu = tk.Label(frame_principal, text="Menu", bg= "white",font=("Arial", 17, "bold"))
label_menu.pack(anchor="w")

#   Botões das opções

teste_rdbtn = tk.StringVar(value="")

saldo_rdbtn = tk.Radiobutton(
    frame_principal, 
    text="1 - Consultar Saldo", 
    bg="white", 
    font=("Arial", 13),
    value="1").pack(anchor="w")

sacar_rdbtn = tk.Radiobutton(
    frame_principal,
    text="2 - Sacar",
    bg="white",
    font=("Arial", 13),
    value="2").pack(anchor="w")

depositar_rdbtn = tk.Radiobutton(
    frame_principal,
    text="3 - Depositar",
    bg="white",
    font=("Arial", 13),
    value="3").pack(anchor="w")

sair_rdbtn = tk.Radiobutton(
    frame_principal,
    text="4 - Sair",
    bg="white",
    font=("Arial", 13),
    value="4"
).pack(anchor="w")

escolher_label = tk.Label(
    frame_principal,
    text="Escolha uma opção:",
    font=("Arial", 13),
    bg="white"
).pack(anchor="w", pady=10)



janela.mainloop()