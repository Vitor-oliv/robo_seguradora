
"""
Módulo Processador de Peças (Relatório Completo)
=================================================
"""

import logging
from typing import List
from .scraper import Peca
from .relatorio import GeradorRelatorio

logger = logging.getLogger(__name__)

class ProcessadorPecas:
    """Classe responsável por processar peças da cotação."""
    
    def __init__(self, config, consultor_estoque, scraper):
        self.config = config
        self.consultor_estoque = consultor_estoque
        self.scraper = scraper
        self.gerador_relatorio = GeradorRelatorio(config)
        self.relatorio = {
            'total_pecas': 0,
            'em_estoque': 0,
            'indisponiveis': 0,
            'erros': 0
        }
    
    def processar_todas_pecas(self, pecas: List[Peca]) -> dict:
        """Processa todas as peças da lista e gera um relatório completo."""
        self.relatorio['total_pecas'] = len(pecas)
        
        logger.info(f"Iniciando conferência de {len(pecas)} peças...")
        logger.info("=" * 60)
        
        for i, peca in enumerate(pecas, 1):
            logger.info(f"\n[{i}/{len(pecas)}] Verificando {peca.partnumber}")
            
            # Passo 1: Consultar estoque via API
            peca.tem_estoque = self.consultor_estoque.verificar_disponibilidade(peca.partnumber)
            
            # Passo 2: Se tem estoque, marca o checkbox
            if peca.tem_estoque:
                logger.info(f"✓ Item {peca.partnumber} encontrado em estoque!")
                sucesso = self.scraper.marcar_estoque(peca)
                if sucesso:
                    self.relatorio['em_estoque'] += 1
                else:
                    self.relatorio['erros'] += 1
            else:
                logger.warning(f"✗ Item {peca.partnumber} não disponível no estoque.")
                self.relatorio['indisponiveis'] += 1
        
        # Passo 3: Gerar Excel com TODOS os itens processados
        self.gerador_relatorio.gerar_excel_estoque(pecas)
        
        logger.info("\n" + "=" * 60)
        logger.info("Conferência concluída!")
        self._exibir_relatorio()
        
        return self.relatorio
    
    def _exibir_relatorio(self):
        logger.info("\n" + "=" * 60)
        logger.info("RESUMO DA CONFERÊNCIA")
        logger.info("=" * 60)
        logger.info(f"Total de peças lidas:       {self.relatorio['total_pecas']}")
        logger.info(f"Itens em estoque (Marcados): {self.relatorio['em_estoque']}")
        logger.info(f"Itens indisponíveis:        {self.relatorio['indisponiveis']}")
        logger.info(f"Erros de marcação:          {self.relatorio['erros']}")
        logger.info("=" * 60 + "\n")
