import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog
import requests
import os
import sys

def verificar_senha():
    senha = simpledialog.askstring("Senha Necessária", "Digite a senha:", show='*')
    return senha == ""

def enviar_dados():
    try:
        email = entry_email.get()
        nome = entry_nome.get()
        senha = entry_senha.get()
        telefone = entry_telefone.get()
        cpf = entry_cpf.get()

        api_cadastro_url = ''

        auth_token = ''

        headers = {
        'accept': 'application/json',
        'x-auth-token': auth_token
        }   

        dados_aluno = {
            'anotacoes': '',
            'telefone': telefone,
            'data_cadastro': '',
            'status': '1',
            'permissao_id': '',
            'tipo': '1',
            'senha': senha,
            'nome': nome,
            'notificar': '',
            'personalizado': '',
            'email': email,
        }

        dados_verificar = {
            'email':email
        }

        response = requests.post(api_cadastro_url, headers=headers, json=dados_aluno)

        email_bloqueado = ""

        if email == email_bloqueado:
            if not verificar_senha():
                log_message("Senha incorreta. Ação bloqueada.")
                return

        if response.status_code == 200:
            resposta_json = response.json() 
            message_success = f"Cadastrado com Sucesso!"
            log_message(message_success)
            aluno_id = resposta_json.get('data',{}).get('aluno_id')
            atualizar_cad(aluno_id, cpf, headers)
            enviar_mensagem(email, nome, telefone, cpf, senha)
        elif response.status_code == 409:

            # Trata do erro de já ser cadastrado. Mas ele pega o usuario e atualiza com os dados que foi preenchido

            api_verificar_user = ''

            verificado = requests.get(api_verificar_user,headers=headers, params=dados_verificar)

            if verificado.status_code == 200:
                resposta_json1 = verificado.json()
                # Verifique se a resposta contém um aluno com o email especificado
                if resposta_json1 and isinstance(resposta_json1, list):
                    # Procure o aluno com o email especificado
                    aluno_encontrado = None
                    for aluno in resposta_json1:
                        if aluno.get('email') == email:
                            aluno_encontrado = aluno
                            break

                if aluno_encontrado:
                    aluno_id = aluno_encontrado.get("aluno_id")
                    atualizar_cad(aluno_id, headers, email, nome, telefone, cpf, senha)
                else:
                    pass

            message_success = f"Cadastrado com Sucesso!"
            log_message(message_success)
            enviar_mensagem(email, nome, telefone, cpf, senha)
        else:
            message = f"Erro ao enviar dados: {response.status_code}\n{response.text}"
            log_message(message)

        entry_email.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_senha.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
    except:
        log_message(f"Ocorreu um erro: {response.status_code}")

def log_message(message):
    text_log.insert(tk.END, message + "\n")
    text_log.see(tk.END)
    text_log.config(state=tk.DISABLED)

def atualizar_cad(aluno_id,cpf, headers):
    
    api_atualizar_url = f'' 

    dados_atualizado = {
        'cpf': cpf
    }

    response = requests.put(api_atualizar_url,headers=headers,json=dados_atualizado)

    if response.status_code == 200:
        print(response.json)
        matricular_(aluno_id,headers)
    else:
        message = f"Erro ao enviar dados: {response.status_code}\n{response.text}"
        log_message(message)

def atualizar_cad_ja_existente(aluno_id, headers, email, nome, telefone, cpf, senha):
    
    api_atualizar_url = f'' 

    dados_atualizado = {
        'email':email,
        'nome': nome,
        'telefone':telefone,
        'senha': senha,
        'cpf': cpf
    }

    response2 = requests.put(api_atualizar_url,headers=headers,json=dados_atualizado)

    if response2.status_code == 200:
        matricular_(aluno_id,headers)
    elif response2.status_code == 409:
        matricular_(aluno_id)
    else:
        message = f"Erro ao enviar dados: {response2.status_code}\n{response2.text}"
        log_message(message)

def matricular_(aluno_id, headers):
    if var1.get()== 1:
        matricular(aluno_id,headers)
    else:
        pass

def matricular(aluno_id,headers):

    api_cadastro_url = ''

    try:
        dados_matricula = {
            'curso_id': '15',
            'usuario_id': aluno_id,
        }

        response = requests.post(api_cadastro_url,headers=headers,json=dados_matricula)
    except:
        message = f"Erro ao enviar dados: {response.status_code}\n{response.text}"
        log_message(message)
    
def enviar_mensagem(email, nome, telefone, cpf, senha):
    text = f""
    key = ''
    account_id = ''
    phone_id = ''
    dialog_id = ''

    # Dados obrigatorios
    headers = {
        'Content-Type': 'application/json'
    }

    api_cg_message_url= f''
    api_cg_dialogo_url= f''
    api_cg_fieldUP_url= f''
    response = requests.post(api_cg_message_url,headers=headers)

    if response.status_code == 200:
        pass
    else:
        message_error = f"Erro ao enviar a mensagem!{response.text}"
        log_message(message_error)
        

    response2 = requests.post(api_cg_dialogo_url,headers=headers)

    if response2.status_code == 200:
        pass
    else:
        message_error = f"Erro ao enviar a mensagem! {response.text}"
        log_message(message_error)

    response3 = requests.post(api_cg_fieldUP_url,headers=headers)

    if response3.status_code == 200:
        print('Deu certo..')
    else:
        message_error = f"Erro ao enviar a mensagem! {response.text}"
        log_message(message_error) 
    

# Criação da janela principal
root = tk.Tk()
root.title("Matricular no EAD")
root.geometry("500x400")
root.attributes("-topmost", True)


if hasattr(sys, '_MEIPASS'):
    icon_path = os.path.join(sys._MEIPASS, 'LT.ico')
else:
    icon_path = 'LT.ico'
root.iconbitmap(icon_path)


# Campos de entrada
ttk.Label(root, text="Email:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Label(root, text="Nome:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Label(root, text="Senha:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Label(root, text="Telefone:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Label(root, text="CPF:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)


entry_email = tk.Entry(root, width=40)
entry_nome = tk.Entry(root, width=40)
entry_senha = tk.Entry(root, width=40)
entry_telefone = tk.Entry(root, width=40)
entry_cpf = tk.Entry(root, width=40)

var1 = tk.IntVar()
c1 = tk.Checkbutton(root, text='Matricular Gratuito',variable=var1, onvalue=1, offvalue=0)

entry_email.grid(row=0, column=1, padx=10, pady=5)
entry_nome.grid(row=1, column=1, padx=10, pady=5)
entry_senha.grid(row=2, column=1, padx=10, pady=5)
entry_telefone.grid(row=3, column=1, padx=10, pady=5)
entry_cpf.grid(row=4, column=1, padx=10, pady=5)
c1.grid(row=5, column=0)

# Botão para enviar dados
button_enviar = tk.Button(root, text="Enviar Dados", command=enviar_dados)
button_enviar.grid(row=5, column=1, padx=10, pady=10)

# Área de texto para logs
text_log = scrolledtext.ScrolledText(root, width=60, height=10, state=tk.NORMAL)
text_log.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Iniciar a interface
root.mainloop()