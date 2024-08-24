import sqlite3
import tkinter as tk
from tkinter import messagebox
import re

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('estoque.db')
c = conn.cursor()

# Criar tabela se não existir
c.execute('''CREATE TABLE IF NOT EXISTS componentes (
             codigo_barras TEXT PRIMARY KEY
             )''')
conn.commit()

# Função para validar o formato do código de barras
def validar_codigo_barras(codigo_barras):
    padrao = re.compile(r'^\d{3}\.\d{4}\.\d{2}$')
    return bool(padrao.match(codigo_barras))

# Função para adicionar componente ao banco de dados
def adicionar_componente(codigo_barras):
    if not validar_codigo_barras(codigo_barras):
        messagebox.showerror("Erro", "Código de barras no formato inválido. Use o formato 000.0000.00")
        return
    
    try:
        c.execute('INSERT INTO componentes (codigo_barras) VALUES (?)', (codigo_barras,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Componente adicionado ao seu estoque!")
        limpar_campos()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Componente com esse código de barras já existe no estoque.")

# Função para pesquisar componente pelo código de barras
def pesquisar_componente():
    codigo_barras = entry_pesquisa_codigo.get()

    if not validar_codigo_barras(codigo_barras):
        messagebox.showerror("Erro", "Código de barras no formato inválido. Use o formato 000.0000.00")
        return

    c.execute('SELECT * FROM componentes WHERE codigo_barras = ?', (codigo_barras,))
    resultado = c.fetchone()
    if resultado:
        entry_codigo_barras.delete(0, tk.END)
        entry_codigo_barras.insert(0, resultado[0])  # código de barras
        messagebox.showinfo("Sucesso", "Componente encontrado.")
    else:
        messagebox.showinfo("Erro", "Componente não encontrado.")
        limpar_campos()

# Função para remover componente pelo código de barras com confirmação
def remover_componente():
    codigo_barras = entry_pesquisa_codigo.get()

    if not validar_codigo_barras(codigo_barras):
        messagebox.showerror("Erro", "Código de barras no formato inválido. Use o formato 000.0000.00")
        return
    
    if messagebox.askyesno("Confirmação", "Você tem certeza que deseja remover este componente?"):
        c.execute('DELETE FROM componentes WHERE codigo_barras = ?', (codigo_barras,))
        if c.rowcount > 0:
            conn.commit()
            messagebox.showinfo("Sucesso", "Componente removido do estoque.")
        else:
            messagebox.showinfo("Erro", "Componente não encontrado.")
        limpar_campos()

# Função para limpar campos de entrada
def limpar_campos():
    entry_codigo_barras.delete(0, tk.END)

# Função para lidar com a leitura do código de barras
def ler_codigo_barras(event):
    codigo_barras = entry_codigo_barras.get()
    adicionar_componente(codigo_barras)

# Função para fechar a conexão com o banco de dados ao sair da aplicação
def on_closing():
    conn.close()
    root.destroy()

# Função para abrir a janela principal do gerenciador de componentes
def abrir_gerenciador_componentes():
    global root
    usuario = entry_usuario.get()
    if not usuario:
        messagebox.showerror("Erro", "Por favor, insira seu nome.")
        return

    login_window.destroy()

    root = tk.Tk()
    root.title(f"Gerenciador de Componentes Pessoais de {usuario}")
    root.geometry("600x200")

    # Widgets da janela principal
    tk.Label(root, text="Pesquisar por código do componente:").pack()
    global entry_pesquisa_codigo
    entry_pesquisa_codigo = tk.Entry(root)
    entry_pesquisa_codigo.pack()

    btn_pesquisar = tk.Button(root, text="Pesquisar", command=pesquisar_componente)
    btn_pesquisar.pack()

    btn_remover = tk.Button(root, text="Remover Componente", command=remover_componente)
    btn_remover.pack()

    tk.Label(root, text="\nAdicionar um novo componente ao seu estoque:").pack()
    global entry_codigo_barras
    entry_codigo_barras = tk.Entry(root)
    entry_codigo_barras.pack()
    entry_codigo_barras.bind('<Return>', ler_codigo_barras)  # Lê o código de barras quando Enter é pressionado

    btn_adicionar = tk.Button(root, text="Adicionar Componente", command=lambda: adicionar_componente(entry_codigo_barras.get()))
    btn_adicionar.pack()

    # Fechar a aplicação corretamente
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

# Função para lidar com a tecla Enter na tela de login
def login_enter(event):
    abrir_gerenciador_componentes()

# Janela de login
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Digite seu nome para entrar:").pack()
entry_usuario = tk.Entry(login_window)
entry_usuario.pack()
entry_usuario.bind('<Return>', login_enter)  # Lê o nome do usuário quando Enter é pressionado

btn_entrar = tk.Button(login_window, text="Entrar", command=abrir_gerenciador_componentes)
btn_entrar.pack()

login_window.mainloop()











