"""
Módulo de Scraping - Focado em Peças e Estoque (IDs Sequenciais)
================================================================

Responsável por ler os códigos PARTNUMBER e marcar os checkboxes de estoque.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

logger = logging.getLogger(__name__)


class Peca:
    """Classe que representa uma peça na cotação."""
    
    def __init__(self, partnumber, id_linha, checkbox_web=None):
        self.partnumber = partnumber.strip()
        self.id_linha = id_linha # O número da linha (0, 1, 2...)
        self.checkbox_web = checkbox_web
        self.tem_estoque = False
        self.status = "PENDENTE"
    
    def __repr__(self):
        return f"Peca(partnumber={self.partnumber}, linha={self.id_linha})"


class ScraperPecas:
    """Classe responsável por interagir com a tabela de peças."""
    
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config.TIMEOUT_PADRAO)
    
    def listar_pecas(self):
        """
        Lista todas as peças da tabela usando IDs sequenciais.
        """
        try:
            logger.info("Buscando peças na tabela de cotação...")
            time.sleep(self.config.DELAY_ENTRE_ACOES)
            
            pecas = []
            index = 0
            
            # O robô vai tentar encontrar partnumber_0, partnumber_1, etc.
            while True:
                id_pn = f"{self.config.SELETORES['id_partnumber_prefix']}{index}"
                id_chk = f"{self.config.SELETORES['id_checkbox_prefix']}{index}"
                
                try:
                    # Tenta encontrar o campo do PARTNUMBER
                    campo_pn = self.driver.find_element(By.ID, id_pn)
                    pn = campo_pn.get_attribute("value") or campo_pn.text
                    
                    # Tenta encontrar o CHECKBOX correspondente
                    checkbox = self.driver.find_element(By.ID, id_chk)
                    
                    if pn:
                        pecas.append(Peca(partnumber=pn, id_linha=index, checkbox_web=checkbox))
                        logger.debug(f"Peça encontrada na linha {index}: {pn}")
                    
                    index += 1 # Vai para a próxima linha
                    
                except NoSuchElementException:
                    # Se não encontrar o próximo ID, significa que a tabela acabou
                    logger.info(f"Fim da tabela alcançado no índice {index}")
                    break
                except Exception as e:
                    logger.warning(f"Erro ao ler linha {index}: {e}")
                    index += 1
                    continue
            
            logger.info(f"✓ Total de {len(pecas)} peças identificadas com sucesso")
            return pecas
            
        except Exception as e:
            logger.error(f"Erro ao listar peças: {e}")
            return []
    
    def marcar_estoque(self, peca):
        """
        Marca o checkbox de estoque para a peça.
        """
        try:
            logger.info(f"Marcando estoque para peça {peca.partnumber} (Linha {peca.id_linha})...")
            
            # Scroll até o checkbox
            self.driver.execute_script("arguments[0].scrollIntoView(true);", peca.checkbox_web)
            time.sleep(0.5)
            
            # Verifica se já está marcado
            if not peca.checkbox_web.is_selected():
                # Tenta clicar via JavaScript para evitar erros de elementos sobrepostos
                self.driver.execute_script("arguments[0].click();", peca.checkbox_web)
                time.sleep(0.5)
            
            logger.info(f"✓ Peça {peca.partnumber} marcada com sucesso")
            peca.tem_estoque = True
            peca.status = "MARCADO"
            return True
            
        except Exception as e:
            logger.error(f"✗ Erro ao marcar checkbox da peça {peca.partnumber}: {e}")
            peca.status = "ERRO_MARCACAO"
            return False
