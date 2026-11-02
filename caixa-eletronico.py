import tkinter as tk
from tkinter import Tk
from tkinter import messagebox
from tkinter import simpledialog

janela = Tk()
janela.geometry("500x400")
janela.title("Banco Eletronico")
janela.config(bg= "white")
janela.resizable(False, False)


# Variáveis 
ARQUIVO_SALDO = "saldo.txt"  # Nome do arquivo para armazenar o saldo
SALDO_INICIAL = 1000.00  # Saldo inicial do usuário
CEDULAS = [100, 50, 20, 10, 5, 2]  # Cédulas disponíveis para saque

SALDO = SALDO_INICIAL 
conta_atual = ""
saldos = {}

opcao_var = tk.StringVar()  # Variável para armazenar a opção selecionada

# Funções de arquivo

def carregar_saldo():
    saldos = {}
    try:
        with open(ARQUIVO_SALDO, "r") as f:
            for linha in f:
                linha = linha.strip()
                if linha == "":
                    continue
                # rsplit separa só no ÚLTIMO ":", assim a conta pode ter ":" no nome
                conta, saldo = linha.rsplit(":", 1)
                saldos[conta] = float(saldo)
    except FileNotFoundError:
        pass  # Primeiro uso: o arquivo ainda não existe
    return saldos

def salvar_saldo(saldos): 
    #Grava o dicionário {conta:saldo} no arquivo
    with open(ARQUIVO_SALDO, "w") as f:
        for conta, saldo in saldos.items():
            f.write(f"{conta}:{saldo}\n")

def salvar_conta_atual():
    #Guarda o saldo da conta logada no arquivo (sem apagar as outras contas)
    if conta_atual != "":
        saldos = carregar_saldo()
        saldos[conta_atual] = SALDO
        salvar_saldo(saldos)

# Funções do caixa

def formatar(valor):
    return f"{valor:.2f}".replace(".", ",") #Serve para formatar o valor com vírgula

def ler_valor(titulo, texto):
    entrada = tk.simpledialog.askstring(titulo, texto, parent=janela)
    if entrada is None:
        return None
    entrada = entrada.strip()

    # Para números com . ou , 

    if "." in entrada or "," in entrada:
        messagebox.showerror("Erro", "Valores fracionários não são permitidos. Por favor, insira um valor inteiro.")
        return None

    # Precisa ser um número
    try:
        valor = int(entrada)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor inteiro.")
        return None
    
    # Não pode ser zero nem negativo
    if valor <= 0:
        messagebox.showerror("Erro", "Por favor, insira um valor positivo.")
        return None
    
    return valor

# Funções das opções do caixa

def consultar_saldo():
    messagebox.showinfo("Saldo", f"Seu saldo atual é: R$ {formatar(SALDO)}")

def sacar():
    global SALDO
    valor = ler_valor("Saque", "Digite o valor que deseja sacar:")
    if valor is None:
        return

    # Verifica se há saldo suficiente
    if valor > SALDO:
        messagebox.showerror("Erro", "Saldo insuficiente.")
        return

    # Calcula quantas cédulas de cada valor são necessárias.
    # Começa pela maior cédula e vai usando o resto para as menores.
    resto = valor
    quantidades = []
    i = 0
    while i < len(CEDULAS):
        quantidades.append(resto // CEDULAS[i])  # Quantas cédulas desse valor cabem
        resto = resto % CEDULAS[i]               # O que sobrou para as próximas
        i += 1

    # Se sobrou algo, o caixa não consegue pagar esse valor (ex.: 1, 11, 13...)
    if resto != 0:
        messagebox.showerror("Erro", "O caixa não trabalha com esse valor.\n"
                                     "Cédulas disponíveis: R$ 100, 50, 20, 10, 5 e 2.")
        return

    SALDO = SALDO - valor


    detalhes = ""
    for i in range(len(CEDULAS)):
        if quantidades[i] > 0:
            detalhes += f"{quantidades[i]} nota(s) de R$ {CEDULAS[i]}\n"

    messagebox.showinfo("Saque realizado", 
                        f"Saque de R$ {valor:.2f} realizado com sucesso!\n\n"
                        f"Detalhes do saque:\n{detalhes}\n"
                        f"Saldo atual: R$ {formatar(SALDO)}")


def depositar():
    global SALDO
    valor = ler_valor("Depósito", "Digite o valor que deseja depositar:")
    if valor is None:
        return

    SALDO += valor
    messagebox.showinfo("Depósito realizado",
                        f"Depósito de R$ {valor} realizado com sucesso!\n"
                        f"Saldo atual: R$ {formatar(SALDO)}")

def sair():
    #salva o saldo e volta para a tela de conta e senha
    global conta_atual, SALDO
 
    salvar_conta_atual()
    messagebox.showinfo("Até logo", "Obrigado por usar nosso sistema!")
 
    # Limpa a sessão
    conta_atual = ""
    SALDO = SALDO_INICIAL
    opcao_var.set("")
    usuario_entry.delete(0, tk.END)
    senha_entry.delete(0, tk.END)
 
    # Troca o menu pela tela de login
    frame_principal.pack_forget()
    frame_login.pack(fill="both", expand=True, padx=25, pady=(0, 15))
    usuario_entry.focus()

def fechar_janela():
    #Clicar no X da janela: salva (se houver conta logada) e encerra o programa
    salvar_conta_atual()
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

# Login
def login():
    global SALDO, conta_atual
 
    conta = usuario_entry.get().strip()
 
    if conta == "":
        messagebox.showerror("Erro", "Digite o número da conta.")
        return
 
    saldos = carregar_saldo()
    if conta in saldos:
        SALDO = saldos[conta]       # Conta já usada: busca o saldo salvo
    else:
        SALDO = SALDO_INICIAL       # Conta nova: começa com o saldo fictício
        saldos[conta] = SALDO
        salvar_saldo(saldos)
 
    conta_atual = conta
 
    # Troca a tela de login pelo menu
    frame_login.pack_forget()
    frame_principal.pack(fill="both", expand=True, padx=25, pady=(0, 25))
    opcao_var.set("")


# Interface da tela de conta e senha

frame_login = tk.Frame(janela, bg="light gray", padx=10, pady=20)
frame_login.pack(fill="both", expand=True, padx=25, pady=(0, 15))
 
label_usuario = tk.Label(frame_login, text="Digite sua Conta:",
                         bg="light gray", font=("Arial", 12, "bold"))
label_usuario.pack(side="top", padx=10, pady=(40, 0))
 
usuario_entry = tk.Entry(frame_login, font=("Arial", 12))
usuario_entry.pack(side="top", padx=10, pady=10)
 
label_senha = tk.Label(frame_login, text="Digite sua senha:",
                       bg="light gray", font=("Arial", 12, "bold"))
label_senha.pack(side="top", padx=10, pady=(10, 0))
 
senha_entry = tk.Entry(frame_login, show="*", font=("Arial", 12))
senha_entry.pack(side="top", padx=10, pady=5)
 
botao_login = tk.Button(frame_login, text="Login", command=login,
                        font=("Arial", 12, "bold"), bg="blue", fg="white")
botao_login.pack(pady=10)
 

# Interface do menu

frame_principal = tk.Frame(janela, bg="light gray", padx=25, pady=25)
 
label_menu = tk.Label(frame_principal, text="MENU", bg="light gray",
                      font=("Arial", 15, "bold"))
label_menu.pack(anchor="w")
 
label_escolher = tk.Label(frame_principal, text="Escolha uma opção:",
                          font=("Arial", 13, "bold"), bg="light gray")
label_escolher.pack(anchor="w")
 
opcoes = [
    ("1 - Consultar Saldo", "1"),
    ("2 - Sacar", "2"),
    ("3 - Depositar", "3"),
    ("4 - Sair", "4"),
]
 
for texto, valor in opcoes:
    tk.Radiobutton(
        frame_principal,
        text=texto,
        variable=opcao_var,
        value=valor,
        bg="light gray",
        font=("Arial", 13),
        command=executar_opcao
    ).pack(anchor="w")
 
# Ao fechar a janela no X, salva o saldo antes de encerrar
janela.protocol("WM_DELETE_WINDOW", fechar_janela)
 
janela.mainloop()