import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Canvas
from tkinter import messagebox
from tkinter import simpledialog

janela = Tk()
janela.geometry("500x400")
janela.title("Banco Eletronico")
janela.config(bg= "light sky blue")
janela.resizable(False, False)
estilo = ttk.Style()
estilo.theme_use('clam')


# Variáveis 
ARQUIVO_SALDO = "saldo.txt"  # Nome do arquivo para armazenar o saldo
SALDO_INICIAL = 1000.00  # Saldo inicial do usuário
CEDULAS = [100, 50, 20, 10, 5, 2]  # Cédulas disponíveis para saque

SALDO = SALDO_INICIAL
conta_atual = ""
saldos = {}

opcao_var = tk.StringVar()  # Variável para armazenar a opção selecionada

def carregar_saldo():
    saldos = {}
    try:
        with open(ARQUIVO_SALDO, "r") as f:
            for line in f:
                conta, saldo = line.strip().split(":")
                saldos[conta] = float(saldo)
    except FileNotFoundError:
        pass
    return saldos

def salvar_saldo(saldos):
    with open(ARQUIVO_SALDO, "w") as f:
        for conta, saldo in saldos.items():
            f.write(f"{conta}:{saldo}\n")

def ler_valor(titulo, texto):
    entrada = tk.simpledialog.askstring(titulo, texto, parent=janela)
    if entrada is None:
        return None
    entrada = entrada.strip()

    if "." in entrada or "," in entrada:
        messagebox.showerror("Erro", "Valores fracionários não são permitidos. Por favor, insira um valor inteiro.")
        return None
    try:
        valor = int(entrada)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor inteiro.")
        return None
    if valor <= 0:
        messagebox.showerror("Erro", "Por favor, insira um valor positivo.")
        return None
    return valor

def consultar_saldo():
    messagebox.showinfo("Saldo", f"Seu saldo atual é: R$ {SALDO:.2f}")

def sacar():
    global SALDO
    valor = ler_valor("Saque", "Digite o valor que deseja sacar:")
    if valor is None:
        return

    if valor > SALDO:
        messagebox.showerror("Erro", "Saldo insuficiente.")
        return

    resto = valor
    quantidades = []
    for cedula in CEDULAS:
        quantidades.append(resto // cedula)
        resto = resto % cedula

    if resto != 0:
        messagebox.showerror("Erro", "Não é possível sacar o valor solicitado com as cédulas disponíveis.")
        return

    SALDO = SALDO - valor
    detalhes = ""
    for i in range(len(CEDULAS)):
        if quantidades[i] > 0:
            detalhes += f"{quantidades[i]} nota(s) de R$ {CEDULAS[i]}\n"

    messagebox.showinfo("Saque realizado", 
                        f"Saque de R$ {valor:.2f} realizado com sucesso!\n\n"
                        f"Detalhes do saque:\n{detalhes}\n"
                        f"Saldo restante: R$ {SALDO:.2f}")




def consultar_saldo():
    messagebox.showinfo("Saldo", f"Seu saldo atual é: R$ {SALDO:.2f}")

def depositar():
    global SALDO
    valor = ler_valor("Depósito", "Digite o valor que deseja depositar:")
    if valor is None:
        return

    SALDO += valor
    messagebox.showinfo("Depósito realizado",
                        f"Depósito de R$ {valor} realizado com sucesso!\n"
                        f"Novo saldo: R$ {SALDO:.2f}")

def sair():
    if conta_atual != "":
        saldos = carregar_saldo()
        saldos[conta_atual] = SALDO
        salvar_saldo(saldos)
    janela.destroy()



def executar_opcao():
    opcao = opcao_var.get()
    if opcao == "1":
        consultar_saldo()
    elif opcao == "2":
        sacar()
    elif opcao == "3":
        depositar()
    elif opcao == "4":
        sair()
        return
    else:
        messagebox.showerror("Erro", "Opção inválida. Por favor, escolha uma opção válida.")

    opcao_var.set("")  # Limpa a seleção após a execução da opção
# Titulo
label_boasvindas = tk.Label(janela, text="Bem vindo ao Caixa Eletrônico!", bg= "light sky blue",font=("Arial", 15, "bold"))
label_boasvindas.pack(padx=10, pady=(20, 10))

#Frame conta e senha
frame_login = tk.Frame(janela, bg="light blue", padx=10, pady=20 )
frame_login.pack(fill="both", expand=True, padx=25, pady=(0, 15))

label_usuario = tk.Label(frame_login, text="Digite sua Conta:", bg="light blue", font=("Arial", 12, "bold"))
label_usuario.pack(side="top", padx=10, pady=(40, 0))

usuario_entry = tk.Entry(frame_login, font=("Arial", 12))
usuario_entry.pack(side="top", padx=10, pady=10)

label_senha = tk.Label(frame_login, text="Digite sua senha:", bg="light blue", font=("Arial", 12, "bold"))
label_senha.pack(side="top", padx=10, pady=(10, 0))

senha_entry = tk.Entry(frame_login, show="*", font=("Arial", 12))
senha_entry.pack(side="top", padx=10, pady=5)


# Função de login 
def login():
    global SALDO, conta_atual, saldos

    conta_atual = usuario_entry.get().strip()

    saldos = carregar_saldo()
    if conta_atual in saldos:
        SALDO = saldos[conta_atual]
    else:
        SALDO = SALDO_INICIAL
        saldos[conta_atual] = SALDO
        salvar_saldo(saldos)

# Esconde o frame de login e o botão de login


    frame_login.pack_forget()
    botao_login.pack_forget()


# Frame onde vai ficar as opções do Menu

    frame_principal = tk.Frame(janela, bg="white" ,padx=25, pady=25)
    frame_principal.pack(fill="both", expand=True, padx=25, pady=(0, 25))


# Label do menu 
    label_menu = tk.Label(frame_principal, text="Menu", bg= "white",font=("Arial", 15, "bold"))
    label_menu.pack(anchor="w")

# Botões das opções
    opcao_var.set("")  # Variável para armazenar a opção selecionada

    opcoes = [
        ("1 - Consultar Saldo", "1"),
        ("2 - Sacar", "2"),
        ("3 - Depositar", "3"),
        ("4 - Sair", "4")]

    for texto, valor in opcoes:
        tk.Radiobutton(
            frame_principal,
            text=texto,
            variable=opcao_var,
            value=valor,
            bg="white",
            font=("Arial", 13),
            command=executar_opcao
            ).pack(anchor="w")

    escolher_label = tk.Label(
        frame_principal,
        text="Escolha uma opção",
        font=("Arial", 13),
        bg="white").pack(anchor="w", pady=10)

    

botao_login = tk.Button(frame_login, text="Login", command=login, font=("Arial", 12, "bold"), bg="blue", fg="white")
botao_login.pack(pady=10)

janela.protocol("WM_DELETE_WINDOW", sair)  # Chama a função sair() ao fechar a janela

janela.mainloop()



    # saldo_rdbtn = tk.Radiobutton(
    # frame_principal, 
    # text="1 - Consultar Saldo", 
    # variable=opcao_var,
    # value="1",
    # bg="white", 
    # font=("Arial", 13)).pack(anchor="w")

    # sacar_rdbtn = tk.Radiobutton(
    # frame_principal,
    # text="2 - Sacar",
    # variable=opcao_var,
    # value="2",
    # bg="white",
    # font=("Arial", 13)).pack(anchor="w")

    # depositar_rdbtn = tk.Radiobutton(
    # frame_principal,
    # text="3 - Depositar",
    # variable=opcao_var,
    # value="3",
    # bg="white",
    # font=("Arial", 13)).pack(anchor="w")

    # sair_rdbtn = tk.Radiobutton(
    # frame_principal,
    # text="4 - Sair",
    # variable=opcao_var,
    # value="4",
    # bg="white",
    # font=("Arial", 13),
    # command=sair
    # ).pack(anchor="w")

    # escolher_label = tk.Label(
    # frame_principal,
    # text="Escolha uma opção",
    # font=("Arial", 13),
    # bg="white").pack(anchor="w", pady=10)