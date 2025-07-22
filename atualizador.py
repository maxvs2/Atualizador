import os
import subprocess
import urllib.request
import customtkinter as ctk
from tkinter import messagebox
import datetime
import threading

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

LOG_FILE = "log_atualizador.txt"

def escrever_log(mensagem):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        data = datetime.datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
        f.write(f"{data} {mensagem}\n")

def is_winget_installed():
    try:
        subprocess.run(["winget", "--version"], check=True, stdout=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def instalar_winget():
    try:
        progress.set(0.2)
        escrever_log("Iniciando instalação do Winget...")
        url = "https://aka.ms/getwinget"
        local_file = "AppInstaller.msixbundle"
        urllib.request.urlretrieve(url, local_file)
        progress.set(0.5)
        os.system(f"powershell -Command Add-AppxPackage -Path .\\{local_file}")
        progress.set(1.0)
        escrever_log("Winget instalado com sucesso.")
        messagebox.showinfo("Sucesso", "Winget instalado! Reinicie o programa.")
    except Exception as e:
        escrever_log(f"Erro ao instalar Winget: {e}")
        messagebox.showerror("Erro", f"Falha ao instalar Winget: {e}")
    progress.set(0)

def atualizar_com_winget():
    try:
        escrever_log("Iniciando atualização via Winget...")
        progress.set(0.2)
        subprocess.run(["winget", "upgrade", "--all", "--accept-package-agreements", "--accept-source-agreements"])
        progress.set(1.0)
        messagebox.showinfo("Atualização", "Programas atualizados com sucesso via Winget!")
        escrever_log("Atualização via Winget concluída.")
    except Exception as e:
        escrever_log(f"Erro com Winget: {e}")
        messagebox.showerror("Erro", f"Erro ao executar o Winget: {e}")
    progress.set(0)

def verificar_atualizacoes_windows():
    try:
        escrever_log("Iniciando verificação do Windows Update...")
        progress.set(0.3)
        subprocess.run(["powershell", "-Command", "UsoClient StartScan"], check=True)
        progress.set(1.0)
        messagebox.showinfo("Windows Update", "Verificação de atualizações iniciada!")
        escrever_log("Verificação do Windows Update iniciada.")
    except Exception as e:
        escrever_log(f"Erro ao verificar atualizações: {e}")
        messagebox.showerror("Erro", f"Erro ao iniciar verificação: {e}")
    progress.set(0)

# Funções em threads para evitar congelamento da interface
def thread_wrapper(func):
    threading.Thread(target=func, daemon=True).start()

# Interface Gráfica
app = ctk.CTk()
app.geometry("500x500")
app.title("Assistente de Atualização")

label = ctk.CTkLabel(app, text="Assistente de Atualização do Sistema", font=ctk.CTkFont(size=18, weight="bold"))
label.pack(pady=20)

progress = ctk.CTkProgressBar(app, width=400)
progress.pack(pady=10)
progress.set(0)

ctk.CTkButton(app, text="Verificar atualizações do Windows", command=lambda: thread_wrapper(verificar_atualizacoes_windows)).pack(pady=10)

# Verificação do Winget
if is_winget_installed():
    msg = "✅ Winget está instalado. Você pode atualizar seus programas automaticamente."
    ctk.CTkLabel(app, text=msg, wraplength=400).pack(pady=10)
    ctk.CTkButton(app, text="Atualizar programas com Winget", command=lambda: thread_wrapper(atualizar_com_winget)).pack(pady=10)
else:
    msg = "❌ Winget não está instalado. Escolha uma alternativa:"
    ctk.CTkLabel(app, text=msg, wraplength=400).pack(pady=10)
    ctk.CTkButton(app, text="Instalar Winget", command=lambda: thread_wrapper(instalar_winget)).pack(pady=10)

app.mainloop()