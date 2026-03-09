import tkinter as tk
from tkinter import messagebox
import threading
import main
import config

class RoboGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automação Planetun")
        self.root.geometry("450x550") # Tamanho fixo para um visual mais controlado
        self.root.resizable(False, False) # Impede redimensionamento
        self.root.configure(bg='#f0f0f0') # Cor de fundo suave

        # Estilos de fonte e cor
        self.font_title = ("Arial", 16, "bold")
        self.font_label = ("Arial", 10, "bold")
        self.font_button = ("Arial", 11, "bold")
        self.color_primary = "#4CAF50" # Verde para ações principais
        self.color_secondary = "#2196F3" # Azul para login
        self.color_text = "#333333"
        self.color_bg = "#f0f0f0"
        self.color_entry_bg = "#ffffff"

        # Título Principal
        tk.Label(root, text="Automação Planetun", font=self.font_title, bg=self.color_bg, fg=self.color_text).pack(pady=15)

        # Frame para Credenciais (Login)
        login_frame = tk.LabelFrame(root, text=" Credenciais de Acesso ", font=self.font_label, bg=self.color_bg, fg=self.color_text, padx=15, pady=10)
        login_frame.pack(pady=10, padx=20, fill="x")

        # Campo Empresa
        tk.Label(login_frame, text="Empresa:", font=self.font_label, bg=self.color_bg, fg=self.color_text).grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.ent_empresa = tk.Entry(login_frame, width=35, bg=self.color_entry_bg, fg=self.color_text, relief="flat", bd=2)
        self.ent_empresa.grid(row=0, column=1, pady=5, padx=5)
        self.ent_empresa.insert(0, config.SEGURADORA_EMPRESA)

        # Campo Usuário
        tk.Label(login_frame, text="Usuário:", font=self.font_label, bg=self.color_bg, fg=self.color_text).grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.ent_user = tk.Entry(login_frame, width=35, bg=self.color_entry_bg, fg=self.color_text, relief="flat", bd=2)
        self.ent_user.grid(row=1, column=1, pady=5, padx=5)
        # REMOVIDO O IF: Agora ele sempre insere o que estiver no config
        self.ent_user.insert(0, config.SEGURADORA_LOGIN)

        # Campo Senha
        tk.Label(login_frame, text="Senha:", font=self.font_label, bg=self.color_bg, fg=self.color_text).grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.ent_pass = tk.Entry(login_frame, width=35, show="*", bg=self.color_entry_bg, fg=self.color_text, relief="flat", bd=2)
        self.ent_pass.grid(row=2, column=1, pady=5, padx=5)
        # REMOVIDO O IF: Agora ele sempre insere o que estiver no config
        self.ent_pass.insert(0, config.SEGURADORA_SENHA)

        # Botão de Login
        self.btn_login = tk.Button(root, text="FAZER LOGIN", font=self.font_button, bg=self.color_secondary, fg="white", 
                                     width=30, height=2, command=self.start_login_thread, relief="raised", bd=2)
        self.btn_login.pack(pady=15)

        # Botão de Conferir Estoque e Aplicar Desconto
        self.btn_conferir = tk.Button(root, text="CONFERIR ESTOQUE", font=self.font_button, bg=self.color_primary, fg="white", 
                                     width=30, height=2, command=self.start_conferir_thread, relief="raised", bd=2)
        self.btn_conferir.pack(pady=10)

        # Status
        self.status_var = tk.StringVar(value="Aguardando início...")
        self.lbl_status = tk.Label(root, textvariable=self.status_var, font=("Arial", 10), bg=self.color_bg, fg="#555555")
        self.lbl_status.pack(pady=10)

        # Configura fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_login_thread(self):
        empresa = self.ent_empresa.get()
        user = self.ent_user.get()
        password = self.ent_pass.get()

        if not empresa or not user or not password:
            messagebox.showwarning("Aviso", "Por favor, preencha Empresa, Usuário e Senha.")
            return

        # Atualiza as configurações globais
        config.SEGURADORA_EMPRESA = empresa
        config.SEGURADORA_LOGIN = user
        config.SEGURADORA_SENHA = password
        
        self.btn_login.config(state="disabled", bg="#cccccc")
        self.status_var.set("Abrindo navegador e fazendo login...")
        threading.Thread(target=self.run_login, daemon=True).start()

    def run_login(self):
        try:
            driver = main.iniciar_navegador()
            if driver:
                self.status_var.set("Login realizado! Navegue até a cotação.")
                
            else:
                self.status_var.set("Erro ao abrir navegador.")
                messagebox.showerror("Erro", "Não foi possível abrir o navegador ou fazer login. Verifique o console para detalhes.")
        except Exception as e:
            self.status_var.set(f"Erro: {str(e)}")
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro inesperado: {str(e)}")
        finally:
            self.root.after(0, lambda: self.btn_login.config(state="normal", bg=self.color_secondary))

    def start_conferir_thread(self):
        self.btn_conferir.config(state="disabled", bg="#cccccc")
        self.status_var.set("Conferindo estoque e aplicando descontos...")
        threading.Thread(target=self.run_conferir, daemon=True).start()

    def run_conferir(self):
        try:
            resultado = main.conferir_estoque_e_aplicar_desconto()
            
            if 'erro' in resultado:
                self.root.after(0, lambda: messagebox.showerror("Erro", resultado['erro']))
                self.status_var.set("Erro na conferência/aplicação de desconto.")
            else:
                self.root.after(0, lambda: messagebox.showinfo("Concluído", resultado['mensagem']))
                
        except Exception as e:
            self.status_var.set(f"Erro: {str(e)}")
           
        finally:
            self.root.after(0, lambda: self.btn_conferir.config(state="normal", bg=self.color_primary))

    def on_closing(self):
        if messagebox.askokcancel("Sair", "Deseja fechar o robô e o navegador?"):
            try:
                main.fechar_tudo()
            except:
                pass
            self.root.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = RoboGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar a interface: {e}")
        input("Pressione Enter para fechar...") # Mantém o CMD aberto em caso de erro
