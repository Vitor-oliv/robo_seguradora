"""
Módulo de Autenticação - Seguradora
===================================
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

logger = logging.getLogger(__name__)

class AutenticadorSeguradora:
    """Classe responsável pelo login no site da seguradora."""
    
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config.TIMEOUT_PADRAO)
    
    def fazer_login(self):
        """
        Realiza o login preenchendo Empresa, Usuário e Senha.
        """
        try:
            logger.info(f"Acessando site: {self.config.SEGURADORA_URL}")
            self.driver.get(self.config.SEGURADORA_URL)
            
            # Aguarda carregamento inicial
            time.sleep(self.config.DELAY_ENTRE_ACOES)
            
            # 1. Preenche Empresa (SG)
            logger.info(f"Preenchendo Empresa: {self.config.SEGURADORA_EMPRESA}")
            campo_empresa = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.config.SELETORES["campo_empresa"]))
            )
            campo_empresa.clear()
            campo_empresa.send_keys(self.config.SEGURADORA_EMPRESA)
            
            # 2. Preenche Usuário
            logger.info(f"Preenchendo Usuário: {self.config.SEGURADORA_LOGIN}")
            campo_user = self.driver.find_element(By.CSS_SELECTOR, self.config.SELETORES["campo_login"])
            campo_user.clear()
            campo_user.send_keys(self.config.SEGURADORA_LOGIN)
            
            # 3. Preenche Senha
            logger.info("Preenchendo Senha...")
            campo_pass = self.driver.find_element(By.CSS_SELECTOR, self.config.SELETORES["campo_senha"])
            campo_pass.clear()
            campo_pass.send_keys(self.config.SEGURADORA_SENHA)
            
            # 4. Clica em Entrar
            logger.info("Clicando no botão de login...")
            botao_entrar = self.driver.find_element(By.CSS_SELECTOR, self.config.SELETORES["botao_entrar"])
            botao_entrar.click()
            
            # Aguarda um pouco para o login processar
            time.sleep(self.config.DELAY_ENTRE_ACOES * 2)
            
            logger.info("✓ Login realizado com sucesso")
            return True
            
        except TimeoutException:
            logger.error("✗ Timeout ao tentar fazer login - elemento não encontrado")
            return False
        except NoSuchElementException as e:
            logger.error(f"✗ Elemento não encontrado durante login: {e}")
            return False
        except Exception as e:
            logger.error(f"✗ Erro inesperado durante login: {e}")
            return False
