"""
Módulo de Consulta de Estoque via API Borgali-Demak
==================================================
"""

import requests
import logging

logger = logging.getLogger(__name__)

class ConsultorEstoque:
    """Classe para consultar a disponibilidade de itens na API Borgali-Demak."""
    
    def __init__(self, config=None):
        self.config = config
        
        # Endpoint e APIKEY extraídos do manual Borgali-Demak v2.1
        self.api_url = "https://nfe9.websiteseguro.com/borgalilog/public/v2/PRODUTOS"
        self.apikey = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJwYXNzIjoiMTIzNCJ9.jymZ8KW7Uxf3lzIgWSRaCa7e_fyk1HsaYtf6dngEP7s"
        
        # Conforme o manual, o Authorization deve conter a APIKEY
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.apikey
        }
    
    def verificar_disponibilidade(self, partnumber: str) -> bool:
        """
        Verifica se um item está disponível em estoque na API Borgali-Demak.
        Consulta realizada via POST utilizando o campo 'cod_prod_alternativo'.
        """
        try:
            logger.info(f"Consultando estoque para: {partnumber}")
            
            # Payload conforme exemplo da página 2 do manual
            payload = {
                "cod_cli": "DEM", # Código do cliente fixo conforme manual/config anterior
                "cod_prod_cliente": partnumber,
                "cod_prod_alternativo": ""
            }
            
            # A consulta de PRODUTOS deve ser via POST conforme o manual
            response = requests.post(
                self.api_url, 
                json=payload,
                headers=self.headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Verifica se a resposta indica sucesso e se há produtos retornados
                if data.get("sucesso") and data.get("produtos"):
                    for produto in data["produtos"]:
                        # Verifica a quantidade disponível (nr_qtde_disponivel)
                        # O manual mostra nr_qtde_disponivel como um número (ex: 312.000000)
                        try:
                            qtde_disponivel = float(produto.get("nr_qtde_disponivel", 0))
                            if qtde_disponivel > 0:
                                logger.info(f"✓ Item {partnumber} disponível: {qtde_disponivel} unidades.")
                                return True
                        except (ValueError, TypeError):
                            continue
                
                logger.info(f"✗ Item {partnumber} não encontrado ou sem estoque disponível.")
                return False
            
                
        except Exception as e:
            return False
