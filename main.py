import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import re

# Cores
COR_FUNDO = "black"       
COR_BOTAO = "#009688"         
COR_HOVER = "#e0e0e0"       
COR_TEXTO_BOTAO = "white" 
COR_TEXTO = "white"         

# Variáveis globais
selected_item_original = None
current_user = None

# Arquivos para salvar dados
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_ITENS = "itens.json"

# Funções de arquivo
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as file:
            usuarios = json.load(file)
            updated = False
            for user in usuarios:
                if 'admin' not in user:
                    user['admin'] = (user['id'] == 1)
                    updated = True
            if updated:
                salvar_usuarios(usuarios)
            return usuarios
    return []

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as file:
        json.dump(usuarios, file, ensure_ascii=False, indent=4)

def carregar_itens():
    if os.path.exists(ARQUIVO_ITENS):
        with open(ARQUIVO_ITENS, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def salvar_itens(itens):
    with open(ARQUIVO_ITENS, "w", encoding="utf-8") as file:
        json.dump(itens, file, ensure_ascii=False, indent=4)



# Funções de usuário
def cadastrar_usuario():
    username = entry_user_reg.get()
    password = entry_pass_reg.get()
    if not username or not password:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u.get("Usuario") == username:
            messagebox.showwarning("Aviso", "Usuário já cadastrado!")
            return
    novo_id = len(usuarios) + 1
    admin = (novo_id == 1)
    novo_usuario = {
        "id": novo_id,
        "Usuario": username,
        "Senha": password,
        "admin": admin
    }
    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)
    messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
    show_login()

def validar_login():
    global current_user
    usuario = entry_user_login.get().strip()
    senha = entry_pass_login.get().strip()
    if not usuario or not senha:
        messagebox.showwarning("Aviso", "Preencha os campos de usuário e senha!")
        return
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["Usuario"] == usuario and u["Senha"] == senha:
            current_user = u
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            show_sistema()
            return
    messagebox.showwarning("Erro", "Usuário ou senha inválidos.")

# Funções de navegação
def show_login():
    global current_user
    current_user = None
    frame_sistema.pack_forget()
    frame_registro.pack_forget()
    frame_cadastro_item.pack_forget()
    frame_listagem_item.pack_forget()
    frame_login.pack(fill="both", expand=True)

def show_registro():
    frame_login.pack_forget()
    frame_registro.pack(fill="both", expand=True)

def show_sistema():
    frame_login.pack_forget()
    frame_sistema.pack(fill="both", expand=True)

def show_cadastro_item():
    frame_sistema.pack_forget()
    frame_listagem_item.pack_forget()
    frame_cadastro_item.pack(fill="both", expand=True)

def show_listagem_item():
    frame_sistema.pack_forget()
    frame_cadastro_item.pack_forget()
    listar_itens()
    if current_user and current_user.get('admin'):
        btn_editar.pack(pady=5)
        btn_excluir.pack(pady=5)
    else:
        btn_editar.pack_forget()
        btn_excluir.pack_forget()
    frame_listagem_item.pack(fill="both", expand=True)

def back_to_sistema():
    frame_cadastro_item.pack_forget()
    frame_listagem_item.pack_forget()
    frame_sistema.pack(fill="both", expand=True)



# Funções de itens
def salvar_item():
    global selected_item_original
    if selected_item_original and not (current_user and current_user.get('admin')):
        messagebox.showwarning("Acesso negado", "Você não tem permissão para editar itens.")
        selected_item_original = None
        limpar_campos_item()
        back_to_sistema()
        return
    
    nome_pessoa = entry_nome_pessoa.get().strip()
    nome = entry_nome.get().strip()
    categoria = entry_categoria.get().strip()
    local = entry_local.get().strip()
    data = entry_data.get().strip()
    status = entry_status.get().strip()
    numero = entry_numero.get().strip()
    
    if not all([nome_pessoa, nome, categoria, local, data, status, numero]):
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    if not re.match(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$', data):
        messagebox.showwarning("Erro", "Formato de data inválido! Use DD/MM/AAAA.")
        return
    
    try:
        dia, mes, ano = map(int, data.split('/'))
        if (mes in [4,6,9,11] and dia > 30) or \
           (mes == 2 and ((ano % 4 != 0 and dia > 28) or (ano % 4 == 0 and dia > 29))):
            raise ValueError
        if dia > 31 or mes > 12 or ano < 1900:
            raise ValueError
    except:
        messagebox.showwarning("Erro", "Data inválida! Verifique dia, mês ou ano.")
        return

    if not numero.isdigit() or len(numero) < 8:
        messagebox.showwarning("Erro", "Número inválido! Deve conter apenas dígitos e ter pelo menos 8 números.")
        return
    
    itens = carregar_itens()
    
    if selected_item_original is None:
        novo_item = {
            'id': len(itens) + 1,
            'NomePessoa': nome_pessoa,
            'Nome': nome,
            'Categoria': categoria,
            'Local': local,
            'Data': data,
            'Status': status,
            'Numero': numero
        }
        itens.append(novo_item)
        messagebox.showinfo("Sucesso", "Item cadastrado com sucesso!")
    else:
        item_id = selected_item_original["id"]
        for i in itens:
            if i["id"] == item_id:
                i.update({
                    'NomePessoa': nome_pessoa,
                    'Nome': nome,
                    'Categoria': categoria,
                    'Local': local,
                    'Data': data,
                    'Status': status,
                    'Numero': numero
                })
                break
        messagebox.showinfo("Sucesso", "Item editado com sucesso!")
        selected_item_original = None
    
    salvar_itens(itens)
    limpar_campos_item()
    back_to_sistema()

def limpar_campos_item():
    entry_nome_pessoa.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_local.delete(0, tk.END)
    entry_data.delete(0, tk.END)
    entry_status.delete(0, tk.END)
    entry_numero.delete(0, tk.END)

def listar_itens():
    treeview_itens.delete(0, tk.END)
    itens = carregar_itens()
    for item in itens:
        treeview_itens.insert(tk.END, 
            f"ID: {item['id']} | Pessoa: {item.get('NomePessoa', 'N/A')} | "
            f"Item: {item['Nome']} - {item['Categoria']} | "
            f"Local (encontrado ou perdido): {item['Localidade']} | Data: {item['Data']} | "
            f"Status: {item['Status']} | Contato: {item.get('Numero', 'N/A')}")

def selecionar_item():
    global selected_item_original
    if not (current_user and current_user.get('admin')):
        messagebox.showwarning("Acesso negado", "Você não tem permissão para editar itens.")
        return
    
    try:
        # Captura o item selecionado no Treeview
        selected_item = treeview_itens.selection()[0]  # Pega o ID do item selecionado
        item_values = treeview_itens.item(selected_item, "values")  # Pega os valores do item
        
        # Extrai o ID do item
        item_id = int(item_values[0])
        
        # Carrega a lista de itens
        itens = carregar_itens()
        
        # Encontra o item correspondente na lista
        for item in itens:
            if item["id"] == item_id:
                # Preenche os campos do formulário com os dados do item
                entry_nome_pessoa.delete(0, tk.END)
                entry_nome_pessoa.insert(0, item.get("NomePessoa", ""))
                entry_nome.delete(0, tk.END)
                entry_nome.insert(0, item["Nome"])
                entry_categoria.delete(0, tk.END)
                entry_categoria.insert(0, item["Categoria"])
                entry_local.delete(0, tk.END)
                entry_local.insert(0, item["Local"])
                entry_data.delete(0, tk.END)
                entry_data.insert(0, item["Data"])
                entry_status.delete(0, tk.END)
                entry_status.insert(0, item["Status"])
                entry_numero.delete(0, tk.END)
                entry_numero.insert(0, item.get("Numero", ""))
                
                # Armazena o item original para edição
                selected_item_original = item.copy()
                break
        
        # Mostra a tela de cadastro para edição
        show_cadastro_item()
    
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione um item para editar.")

def excluir_item():
    if not (current_user and current_user.get('admin')):
        messagebox.showwarning("Acesso negado", "Você não tem permissão para excluir itens.")
        return
    
    try:
        # Captura o item selecionado no Treeview
        selected_item = treeview_itens.selection()[0]  # Pega o ID do item selecionado
        item_values = treeview_itens.item(selected_item, "values")  # Pega os valores do item
        
        # Extrai o ID do item
        item_id = int(item_values[0])
        
        # Confirmação de exclusão
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este item?")
        if resposta:
            # Carrega a lista de itens
            itens = carregar_itens()
            
            # Remove o item da lista
            itens = [item for item in itens if item["id"] != item_id]
            
            # Salva a lista atualizada
            salvar_itens(itens)
            
            # Atualiza a listagem
            listar_itens()
            messagebox.showinfo("Sucesso", "Item excluído com sucesso!")
    
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione um item para excluir.")


# Interface
janela = tk.Tk()
janela.title("Sistema de Cadastro de Itens")
janela.geometry("600x480") 
janela.resizable(True, True)
janela.configure(bg=COR_FUNDO)

# Estilos
ESTILO_BOTAO = {
    'bg': COR_BOTAO,
    'fg': COR_TEXTO_BOTAO,
    'activebackground': COR_HOVER,
    'activeforeground': COR_TEXTO_BOTAO,
    'relief': 'flat',
    'padx': 15,
    'pady': 5
}

ESTILO_ENTRY = {
    'bg': 'white',
    'fg': 'black',
    'relief': 'flat',
    'highlightthickness': 1,
    'highlightcolor': COR_BOTAO,
    'highlightbackground': '#cccccc'
}

#placeholder para os campo usuario do login
def on_focus_in_user(event):
    if entry_user_login.get() == "Digite seu usuário":
        entry_user_login.delete(0,tk.END)
        entry_user_login.config(fg="black")

def on_focus_out_user(event):
    if entry_user_login.get() == "":
        entry_user_login.insert(0,"Digite seu usuário")
        entry_user_login.config(fg="gray")

#placeholder para os campo senha do login
def on_focus_in_pass(event):
    if entry_pass_login.get() == "Digite sua senha":
        entry_pass_login.delete(0,tk.END)
        entry_pass_login.config(fg="black")

def on_focus_out_pass(event):
    if entry_pass_login.get() == "":
        entry_pass_login.insert(0,"Digite sua senha")
        entry_pass_login.config(fg="gray")

#placeholder para os campo usuario do cadastro
def on_focus_in_user_reg(event):
    if entry_user_reg.get() == "Digite seu usuário":
        entry_user_reg.delete(0,tk.END)
        entry_user_reg.config(fg="black")

def on_focus_out_user_reg(event):
    if entry_user_reg.get() == "":
        entry_user_reg.insert(0,"Digite seu usuário")
        entry_user_reg.config(fg="gray")

#placeholder para os campo senha do cadastro
def on_focus_in_pass_reg(event):
    if entry_pass_reg.get() == "Digite sua senha":
        entry_pass_reg.delete(0,tk.END)
        entry_pass_reg.config(fg="black")

def on_focus_out_pass_reg(event):
    if entry_pass_reg.get() == "":
        entry_pass_reg.insert(0,"Digite sua senha")
        entry_pass_reg.config(fg="gray")


# Frames
def criar_container(frame):
    container = tk.Frame(frame, bg=COR_FUNDO)
    container.pack(expand=True, padx=20, pady=20)
    return container

frame_login = tk.Frame(janela, bg=COR_FUNDO)
frame_registro = tk.Frame(janela, bg=COR_FUNDO)
frame_sistema = tk.Frame(janela, bg=COR_FUNDO)
frame_cadastro_item = tk.Frame(janela, bg=COR_FUNDO)
frame_listagem_item = tk.Frame(janela, bg=COR_FUNDO)

container_login = criar_container(frame_login)
container_registro = criar_container(frame_registro)
container_sistema = criar_container(frame_sistema)
container_cadastro_item = criar_container(frame_cadastro_item)
container_listagem_item = criar_container(frame_listagem_item)



# Tela de Login
tk.Label(container_login, text="Login de Usuário", font=("Arial", 16, "bold"), 
        bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=20)


lbl_user = tk.Label(container_login, text="Usuário", font=("Arial", 10), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=3)


entry_user_login = tk.Entry(container_login, **ESTILO_ENTRY, width=25)
entry_user_login.pack(pady=3)
entry_user_login.insert(0, "Digite seu usuário")
entry_user_login.bind("<FocusIn>", on_focus_in_user)
entry_user_login.bind("<FocusOut>", on_focus_out_user)

lbl_pass = tk.Label(container_login, text="Senha", font=("Arial", 10), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=3)

entry_pass_login = tk.Entry(container_login, **ESTILO_ENTRY, width=25)
entry_pass_login.pack(pady=3)
entry_pass_login.insert(0, "Digite sua senha")
entry_pass_login.bind("<FocusIn>", on_focus_in_pass)
entry_pass_login.bind("<FocusOut>", on_focus_out_pass)

btn_login = tk.Button(container_login, **ESTILO_BOTAO, text="Login",font=("Arial", 10, "bold"), command=validar_login)
btn_login.pack(pady=25, ipady=3, side="left", padx=10, ipadx=15)

btn_login.bind("<Enter>", lambda e: btn_login.config(bg=COR_HOVER))
btn_login.bind("<Leave>", lambda e: btn_login.config(bg=COR_BOTAO))



btn_cadastrar = tk.Button(container_login, **ESTILO_BOTAO, text="Cadastrar",font=("Arial", 10, "bold"), command=show_registro)
btn_cadastrar.pack(pady=25, ipady=3, side="left",padx=10, ipadx=10)

btn_cadastrar.bind("<Enter>", lambda e: btn_cadastrar.config(bg=COR_HOVER))
btn_cadastrar.bind("<Leave>", lambda e: btn_cadastrar.config(bg=COR_BOTAO))


# Tela de Cadastro
tk.Label(container_registro, text="Cadastre-se", font=("Arial", 16, "bold"), 
        bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=20)

tk.Label(container_registro, text="Usuário", font=("Arial", 10), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=3)

entry_user_reg = tk.Entry(container_registro, **ESTILO_ENTRY, width=25)
entry_user_reg.pack(pady=3)
entry_user_reg.insert(0, "Digite seu usuário")
entry_user_reg.bind("<FocusIn>", on_focus_in_user_reg)
entry_user_reg.bind("<FocusOut>", on_focus_out_user_reg)

tk.Label(container_registro, text="Senha", font=("Arial", 10), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=3)

entry_pass_reg = tk.Entry(container_registro, **ESTILO_ENTRY, width=25)
entry_pass_reg.pack(pady=3)
entry_pass_reg.insert(0, "Digite sua senha")
entry_pass_reg.bind("<FocusIn>", on_focus_in_pass_reg)
entry_pass_reg.bind("<FocusOut>", on_focus_out_pass_reg)

btn_registrar = tk.Button(container_registro, **ESTILO_BOTAO, text="Cadastrar",font=("Arial", 10, "bold"), command=cadastrar_usuario)
btn_registrar.pack(pady=25, ipady=3, side="left", padx=10, ipadx=10)
btn_registrar.bind("<Enter>", lambda e: btn_registrar.config(bg=COR_HOVER))
btn_registrar.bind("<Leave>", lambda e: btn_registrar.config(bg=COR_BOTAO))


btn_voltar_login = tk.Button(container_registro, **ESTILO_BOTAO, text="Voltar",font=("Arial", 10, "bold"), command=show_login)
btn_voltar_login.pack(pady=25, ipady=3, side="left",padx=10, ipadx=20)
btn_voltar_login.bind("<Enter>", lambda e: btn_voltar_login.config(bg=COR_HOVER))
btn_voltar_login.bind("<Leave>", lambda e: btn_voltar_login.config(bg=COR_BOTAO))


# Sistema Principal
tk.Label(container_sistema, text="Sistema de Achados e Perdidos", font=("Arial", 16, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=20)

btn_cad_item = tk.Button(container_sistema, **ESTILO_BOTAO, text="Cadastrar Item", font=("Arial", 10, "bold"), command=show_cadastro_item)
btn_cad_item.pack(pady=10, ipady=3, ipadx=20)

btn_cad_item.bind("<Enter>", lambda e: btn_cad_item.config(bg=COR_HOVER))
btn_cad_item.bind("<Leave>", lambda e: btn_cad_item.config(bg=COR_BOTAO))

btn_listar = tk.Button(container_sistema, **ESTILO_BOTAO, text="Listar Itens", font=("Arial", 10, "bold"), command=show_listagem_item)
btn_listar.pack(pady=10, ipady=3, ipadx=20)
btn_listar.bind("<Enter>", lambda e: btn_listar.config(bg=COR_HOVER))
btn_listar.bind("<Leave>", lambda e: btn_listar.config(bg=COR_BOTAO))

btn_logout = tk.Button(container_sistema, **ESTILO_BOTAO, text="Voltar para Login", font=("Arial", 10, "bold"), command=show_login)
btn_logout.pack(pady=10, ipady=3, ipadx=20)
btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg=COR_HOVER))
btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg=COR_BOTAO))



#placeholder para o campo nome pessoa 
def on_focus_in_user_nome_pessoa(event):
    if entry_nome_pessoa.get() == "Digite seu nome":
        entry_nome_pessoa.delete(0,tk.END)
        entry_nome_pessoa.config(fg="black")

def on_focus_out_nome_pessoa(event):
    if entry_nome_pessoa.get() == "":
        entry_nome_pessoa.insert(0,"Digite seu nome")
        entry_nome_pessoa.config(fg="gray")

#placeholder para os campo senha do login
def on_focus_in_nome_item(event):
    if entry_nome.get() == "Digite o nome do item":
        entry_nome.delete(0,tk.END)
        entry_nome.config(fg="black")

def on_focus_out_nome_item(event):
    if entry_nome.get() == "":
        entry_nome.insert(0,"Digite o nome do item")
        entry_nome.config(fg="gray")

#placeholder para o campo categoria
def on_focus_in_categoria(event):
    if entry_categoria.get() == "Digite a categoria do item":
        entry_categoria.delete(0,tk.END)
        entry_categoria.config(fg="black")

def on_focus_out_categoria(event):
    if entry_categoria.get() == "":
        entry_categoria.insert(0,"Digite a categoria do item")
        entry_categoria.config(fg="gray")


#placeholder para o campo local
def on_focus_in_local(event):
    if entry_local.get() == "Digite o local (encontrado/perdido)":
        entry_local.delete(0,tk.END)
        entry_local.config(fg="black")

def on_focus_out_local(event):
    if entry_local.get() == "":
        entry_local.insert(0,"Digite o local (encontrado/perdido)")
        entry_local.config(fg="gray")

#placeholder para o campo data
def on_focus_in_data(event):
    if entry_data.get() == "Data do dia (encontrado/perdido)":
        entry_data.delete(0,tk.END)
        entry_data.config(fg="black")

def on_focus_out_data(event):
    if entry_data.get() == "":
        entry_data.insert(0,"Data do dia (encontrado/perdido)")
        entry_data.config(fg="gray")

#placeholder para o campo status
def on_focus_in_status(event):
    if entry_status.get() == "Status (encontrado/perdido)":
        entry_status.delete(0,tk.END)
        entry_status.config(fg="black")

def on_focus_out_status(event):
    if entry_status.get() == "":
        entry_status.insert(0,"Status (encontrado/perdido)")
        entry_status.config(fg="gray")


#placeholder para o campo contato
def on_focus_in_contato(event):
    if entry_numero.get() == "Digite seu contato":
        entry_numero.delete(0,tk.END)
        entry_numero.config(fg="black")

def on_focus_out_contato(event):
    if entry_numero.get() == "":
        entry_numero.insert(0,"Digite seu contato")
        entry_numero.config(fg="gray")

# Cadastro de Item
tk.Label(container_cadastro_item, text="Cadastro de Item", font=("Arial", 16, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=20)

# Frame para o formulário
form_frame = tk.Frame(container_cadastro_item, bg=COR_FUNDO)
form_frame.pack(pady=10)

# Rótulos e campos de entrada organizados em grid
tk.Label(form_frame, text="Nome da Pessoa:", font=("Arial", 12), bg=COR_FUNDO, fg=COR_TEXTO).grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_nome_pessoa = tk.Entry(form_frame, **ESTILO_ENTRY, width=35)
entry_nome_pessoa.grid(row=0, column=1, padx=10, pady=5, sticky="w")
entry_nome_pessoa.insert(0, "Digite seu nome")
entry_nome_pessoa.bind("<FocusIn>", on_focus_in_user_nome_pessoa)
entry_nome_pessoa.bind("<FocusOut>", on_focus_out_nome_pessoa)

tk.Label(form_frame, text="Nome do Item:", font=("Arial", 12), bg=COR_FUNDO, fg=COR_TEXTO).grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_nome = tk.Entry(form_frame, **ESTILO_ENTRY, width=35)
entry_nome.grid(row=1, column=1, padx=10, pady=5, sticky="w")
entry_nome.insert(0, "Digite o nome do item")
entry_nome.bind("<FocusIn>", on_focus_in_nome_item)
entry_nome.bind("<FocusOut>", on_focus_out_nome_item)

tk.Label(form_frame, text="Categoria:", font=("Arial", 12), bg=COR_FUNDO, fg=COR_TEXTO).grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_categoria = tk.Entry(form_frame, **ESTILO_ENTRY, width=35)
entry_categoria.grid(row=2, column=1, padx=10, pady=5, sticky="w")
entry_categoria.insert(0, "Digite a categoria do item")
entry_categoria.bind("<FocusIn>", on_focus_in_categoria)
entry_categoria.bind("<FocusOut>", on_focus_out_categoria)

tk.Label(form_frame, text="Localidade:", font=("Arial", 12), bg=COR_FUNDO, fg=COR_TEXTO).grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_local = tk.Entry(form_frame, **ESTILO_ENTRY, width=35)
entry_local.grid(row=3, column=1, padx=10, pady=5, sticky="w")
entry_local.insert(0, "Digite o local (encontrado/perdido)")
entry_local.bind("<FocusIn>", on_focus_in_local)
entry_local.bind("<FocusOut>", on_focus_out_local)

tk.Label(form_frame, text="Data:", font=("Arial", 12), bg=COR_FUNDO, fg=COR_TEXTO).grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_data = tk.Entry(form_frame, **ESTILO_ENTRY, width=35)
entry_data.grid(row=4, column=1, padx=10, pady=5, sticky="w")
entry_data.insert(0, "Data do dia (encontrado/perdido)")
entry_data.bind("<FocusIn>", on_focus_in_data)
entry_data.bind("<FocusOut>", on_focus_out_data)

tk.Label(form_frame, text="Status do item:", font=("Arial", 12), bg=COR_FUNDO, fg=COR_TEXTO).grid(row=5, column=0, padx=10, pady=5, sticky="e")
entry_status = tk.Entry(form_frame, **ESTILO_ENTRY, width=35)
entry_status.grid(row=5, column=1, padx=10, pady=5, sticky="w")
entry_status.insert(0, "Status (encontrado/perdido)")
entry_status.bind("<FocusIn>", on_focus_in_status)
entry_status.bind("<FocusOut>", on_focus_out_status)

tk.Label(form_frame, text="Contato:", font=("Arial", 12), bg=COR_FUNDO, fg=COR_TEXTO).grid(row=6, column=0, padx=10, pady=5, sticky="e")
entry_numero = tk.Entry(form_frame, **ESTILO_ENTRY, width=35)
entry_numero.grid(row=6, column=1, padx=10, pady=5, sticky="w")
entry_numero.insert(0, "Digite seu contato")
entry_numero.bind("<FocusIn>", on_focus_in_contato)
entry_numero.bind("<FocusOut>", on_focus_out_contato)

# Frame para os botões
button_frame = tk.Frame(container_cadastro_item, bg=COR_FUNDO)
button_frame.pack(pady=20)

btn_salvar = tk.Button(button_frame, **ESTILO_BOTAO, text="Salvar Item", font=("Arial", 10, "bold"), command=salvar_item)
btn_salvar.grid(row=0, column=0, padx=10, ipady=3, ipadx=10)
btn_salvar.bind("<Enter>", lambda e: btn_salvar.config(bg=COR_HOVER))
btn_salvar.bind("<Leave>", lambda e: btn_salvar.config(bg=COR_BOTAO))

btn_voltar_cad = tk.Button(button_frame, **ESTILO_BOTAO, text="Voltar", font=("Arial", 10, "bold"), command=back_to_sistema)
btn_voltar_cad.grid(row=0, column=1, padx=10, ipady=3, ipadx=10)
btn_voltar_cad.bind("<Enter>", lambda e: btn_voltar_cad.config(bg=COR_HOVER))
btn_voltar_cad.bind("<Leave>", lambda e: btn_voltar_cad.config(bg=COR_BOTAO))


# ... (restante do código anterior)

# Listagem de Itens (SEÇÃO MODIFICADA)
tk.Label(container_listagem_item, text="Listagem de Itens", font=("Arial", 16, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=20)

# Frame para Treeview + scrollbar
frame_lista = tk.Frame(container_listagem_item, bg=COR_FUNDO)
frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Scrollbar vertical
scrollbar = ttk.Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Treeview com colunas
treeview_itens = ttk.Treeview(
    frame_lista,
    columns=("ID", "Pessoa", "Item", "Categoria", "Local", "Data", "Status", "Contato"),
    show="headings",
    yscrollcommand=scrollbar.set,
    selectmode="browse",
    style="Custom.Treeview"  # Estilo personalizado para o Treeview
)
treeview_itens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=treeview_itens.yview)

# Configurar cabeçalhos das colunas
treeview_itens.heading("ID", text="ID", anchor="center")
treeview_itens.heading("Pessoa", text="Pessoa", anchor="center")
treeview_itens.heading("Item", text="Item", anchor="center")
treeview_itens.heading("Categoria", text="Categoria", anchor="center")
treeview_itens.heading("Local", text="Local", anchor="center")
treeview_itens.heading("Data", text="Data", anchor="center")
treeview_itens.heading("Status", text="Status", anchor="center")
treeview_itens.heading("Contato", text="Contato", anchor="center")

# Ajustar largura das colunas
treeview_itens.column("ID", width=50, anchor="center")
treeview_itens.column("Pessoa", width=120, anchor="w")
treeview_itens.column("Item", width=150, anchor="w")
treeview_itens.column("Categoria", width=100, anchor="w")
treeview_itens.column("Local", width=150, anchor="w")
treeview_itens.column("Data", width=100, anchor="center")
treeview_itens.column("Status", width=100, anchor="w")
treeview_itens.column("Contato", width=120, anchor="w")

# Adicionar estilo para zebrar as linhas
style = ttk.Style()
style.configure("Custom.Treeview", background="white", fieldbackground="white", foreground="black")
style.map("Custom.Treeview", background=[("selected", COR_BOTAO)], foreground=[("selected", "white")])

# Função para listar itens no Treeview
def listar_itens():
    # Limpar o Treeview antes de adicionar novos itens
    for item in treeview_itens.get_children():
        treeview_itens.delete(item)
    
    itens = carregar_itens()
    for idx, item in enumerate(itens):
        # Adiciona uma cor de fundo alternada para o efeito zebrado
        tag = "evenrow" if idx % 2 == 0 else "oddrow"
        treeview_itens.insert("", tk.END, values=(
            item['id'],
            item.get('NomePessoa', 'N/A'),
            item['Nome'],
            item['Categoria'],
            item['Local'],
            item['Data'],
            item['Status'],
            item.get('Numero', 'N/A')
        ), tags=(tag,))

# Configurar tags para o efeito zebrado
treeview_itens.tag_configure("evenrow", background="#f0f0f0")  # Cor para linhas pares
treeview_itens.tag_configure("oddrow", background="#ffffff")   # Cor para linhas ímpares

# Frame para os botões
frame_botoes = tk.Frame(container_listagem_item, bg=COR_FUNDO)
frame_botoes.pack(pady=15)

# Botões com espaçamento maior
btn_editar = tk.Button(frame_botoes, **ESTILO_BOTAO, text="Editar", font=("Arial", 10, "bold"), command=selecionar_item)
btn_editar.pack(side=tk.LEFT, padx=20, ipady=3)
btn_editar.bind("<Enter>", lambda e: btn_editar.config(bg=COR_HOVER))
btn_editar.bind("<Leave>", lambda e: btn_editar.config(bg=COR_BOTAO))

btn_excluir = tk.Button(frame_botoes, **ESTILO_BOTAO, text="Excluir", font=("Arial", 10, "bold"), command=excluir_item)
btn_excluir.pack(side=tk.LEFT, padx=20, ipady=3)
btn_excluir.bind("<Enter>", lambda e: btn_excluir.config(bg=COR_HOVER))
btn_excluir.bind("<Leave>", lambda e: btn_excluir.config(bg=COR_BOTAO))

btn_voltar_sis = tk.Button(frame_botoes, **ESTILO_BOTAO, text="Voltar", font=("Arial", 10, "bold"), command=back_to_sistema)
btn_voltar_sis.pack(side=tk.RIGHT, padx=20, ipady=3)
btn_voltar_sis.bind("<Enter>", lambda e: btn_voltar_sis.config(bg=COR_HOVER))
btn_voltar_sis.bind("<Leave>", lambda e: btn_voltar_sis.config(bg=COR_BOTAO))

# Inicialização
show_login()
janela.mainloop()