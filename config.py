"""
Configurações do Robô de Conferência de Estoque
===============================================
"""
import os

# --- CONFIGURAÇÕES DO NAVEGADOR ---
HEADLESS_MODE = False  # False = Abre o Chrome visível para você ver o robô trabalhando
TIMEOUT_PADRAO = 15    # Tempo máximo de espera por elementos (segundos)
DELAY_ENTRE_ACOES = 1  # Pausa entre cliques para o site não travar

# --- CREDENCIAIS DA SEGURADORA ---

SEGURADORA_URL = "**"
SEGURADORA_EMPRESA = "**"
SEGURADORA_LOGIN = "**"
SEGURADORA_SENHA = "**"

# --- CONFIGURAÇÕES DA API BORGALI-DEMAK ---
API_ENDPOINT = "***"
API_KEY = "***"
API_COD_CLI = "DEM"

# --- SELETORES DO SITE ---
SELETORES = {
    "campo_empresa": "#iptPainel_empresa",
    "campo_login": "#iptPainel_login",
    "campo_senha": "#iptPainel_senha",
    "botao_entrar": "button[type='submit']",
    
    # Tabela de Peças
    "id_partnumber_prefix": "partnumber_",
    "id_checkbox_prefix": "sequencia_",

    # NOVOS SELETORES PARA DESCONTO
    "estado": "body > center:nth-child(25 ) > div > div:nth-child(10) > div.box-generico",
    "marca": "body > center:nth-child(25) > div > div:nth-child(8) > div.box-generico",
    "campo_desconto": "#desconto_repl",
    "botao_aplicar_desconto": "#bt_replica_desconto"
}

# --- TABELA DE DESCONTOS (Marca / Estado) ---
TABELA_DESCONTOS = {
    "AUDI": {"SP": 40.00, "OUTROS": 40.00},
    "CHEVROLET": {"SP": 50.00, "OUTROS": 48.00},
    "CITROEN": {"SP": 45.00, "OUTROS": 42.00},
    "FIAT": {"SP": 56.00, "OUTROS": 53.00},
    "FORD": {"SP": 42.00, "OUTROS": 40.00},
    "HONDA": {"SP": 19.00, "OUTROS": 16.00},
    "HYUNDAI": {"SP": 43.00, "OUTROS": 40.00},
    "JEEP": {"SP": 52.00, "OUTROS": 48.00},
    "KIA": {"SP": 43.00, "OUTROS": 40.00},
    "MIT": {"SP": 23.00, "OUTROS": 21.00},
    "NISSAN": {"SP": 44.00, "OUTROS": 42.00},
    "PEUGEOT": {"SP": 44.00, "OUTROS": 42.00},
    "RENAULT": {"SP": 43.00, "OUTROS": 40.00},
    "TOYOTA": {"SP": 24.00, "OUTROS": 22.00},
    "VOLKSWAGEN": {"SP": 40.00, "OUTROS": 38.00},
}

# --- DIRETÓRIOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
RELATORIO_DIR = os.path.join(BASE_DIR, "relatorios")
PERFIL_CHROME_DIR = os.path.join(BASE_DIR, "perfil_robo")

# Cria as pastas se não existirem
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(RELATORIO_DIR, exist_ok=True)
os.makedirs(PERFIL_CHROME_DIR, exist_ok=True)
