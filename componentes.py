import sqlite3
import tkinter as tk
from tkinter import messagebox, font
import re

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('estoque.db')
c = conn.cursor()

# Criar tabela se não existir
c.execute('''CREATE TABLE IF NOT EXISTS componentes (
             codigo_componente TEXT PRIMARY KEY
             )''')
conn.commit()

# Função para validar o formato dos componentes
def validar_codigo_componente(codigo_componente):
    padrao = re.compile(r'^\d{3}\.\d{4}\.\d{2}$')
    return bool(padrao.match(codigo_componente))

# Função para adicionar componente ao banco de dados
def adicionar_componente(codigo_componente):
    if not validar_codigo_componente(codigo_componente):
        messagebox.showerror("Erro", "Código de barras no formato inválido. Use o formato 000.0000.00")
        return
    
    try:
        c.execute('INSERT INTO componentes (codigo_componente) VALUES (?)', (codigo_componente,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Componente adicionado ao seu estoque!")
        limpar_campos()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Componente com esse código já existe no estoque.")

# Função para pesquisar componente pelo código de barras
def pesquisar_componente():
    codigo_componente = entry_pesquisa_codigo.get()

    if not validar_codigo_componente(codigo_componente):
        messagebox.showerror("Erro", "Código do componente no formato inválido. Use o formato 000.0000.00")
        return

    c.execute('SELECT * FROM componentes WHERE codigo_componente = ?', (codigo_componente,))
    resultado = c.fetchone()
    if resultado:
        entry_codigo_componente.delete(0, tk.END)
        entry_codigo_componente.insert(0, resultado[0])  # código de barras
        messagebox.showinfo("Sucesso", "Componente encontrado.")
    else:
        messagebox.showinfo("Erro", "Componente não encontrado.")
        limpar_campos()

# Função para remover componente pelo código com confirmação
def remover_componente():
    codigo_componente = entry_pesquisa_codigo.get()

    if not validar_codigo_componente(codigo_componente):
        messagebox.showerror("Erro", "Código do componente no formato inválido. Use o formato 000.0000.00")
        return
    
    if messagebox.askyesno("Confirmação", "Você tem certeza que deseja remover este componente?"):
        c.execute('DELETE FROM componentes WHERE codigo_componente = ?', (codigo_componente,))
        if c.rowcount > 0:
            conn.commit()
            messagebox.showinfo("Sucesso", "Componente removido do estoque.")
        else:
            messagebox.showinfo("Erro", "Componente não encontrado.")
        limpar_campos()

# Função para limpar campos de entrada
def limpar_campos():
    entry_codigo_componente.delete(0, tk.END)

# Função para lidar com a leitura do código de barras
def ler_codigo_componente(event):
    codigo_componente = entry_codigo_componente.get()
    adicionar_componente(codigo_componente)

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
    root.geometry("600x300")
    root.configure(bg="#363636")

    # fontes 
    titulo_font = font.Font(family="Helvetica", size=16, weight="bold")
    texto_font = font.Font(family="Helvetica", size=12)

    # Widgets da janela principal
    tk.Label(root, text="Pesquisar por código do componente:", bg="#363636", fg="#ecf0f1", font=texto_font).pack(pady=10)
    global entry_pesquisa_codigo
    entry_pesquisa_codigo = tk.Entry(root, font=texto_font)
    entry_pesquisa_codigo.pack()
    entry_pesquisa_codigo.bind('<Return>', lambda event: pesquisar_componente())

    btn_pesquisar = tk.Button(root, text="Pesquisar", command=pesquisar_componente, bg="#808080", fg="#ecf0f1", font=texto_font)
    btn_pesquisar.pack(pady=5)

    btn_remover = tk.Button(root, text="Remover Componente", command=remover_componente, bg="#B22222", fg="#ecf0f1", font=texto_font)
    btn_remover.pack(pady=5)

    tk.Label(root, text="\nAdicionar um novo componente ao seu estoque:", bg="#363636", fg="#ecf0f1", font=texto_font).pack(pady=10)
    global entry_codigo_componente
    entry_codigo_componente = tk.Entry(root, font=texto_font)
    entry_codigo_componente.pack()
    entry_codigo_componente.bind('<Return>', ler_codigo_componente)  # Lê o código do componente quando Enter é pressionado

    btn_adicionar = tk.Button(root, text="Adicionar Componente", command=lambda: adicionar_componente(entry_codigo_componente.get()), bg="#008000", fg="#ecf0f1", font=texto_font)
    btn_adicionar.pack(pady=5)

    # Fechar a aplicação corretamente para salvar informações
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

# Função para lidar com a tecla Enter na tela de login
def login_enter(event):
    abrir_gerenciador_componentes()

# Janela de login
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x150")
login_window.configure(background="#363636")

tk.Label(login_window, text="Digite seu nome para entrar:", background="#363636", fg="#ecf0f1", font=("Helvetica", 12)).pack(pady=20)
entry_usuario = tk.Entry(login_window, font=("Helvetica", 12))
entry_usuario.pack()

entry_usuario.bind('<Return>', login_enter)  # Lê o nome do usuário quando Enter é pressionado

btn_entrar = tk.Button(login_window, text="Entrar", command=abrir_gerenciador_componentes, bg="#808080", fg="#ecf0f1", font=("Helvetica", 12))
btn_entrar.pack(pady=10)

login_window.mainloop()











