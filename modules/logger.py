"""
Módulo de Logging
=================

Configura e gerencia o sistema de logs do robô.
"""

import logging
import os
from datetime import datetime


def configurar_logger(config):
    """
    Configura o sistema de logging.
    
    Args:
        config: Módulo de configuração
        
    Returns:
        logging.Logger: Logger configurado
    """
    # Cria diretório de logs se não existir
    os.makedirs(config.LOG_DIR, exist_ok=True)
    
    # Gera nome do arquivo de log com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(config.LOG_DIR, f"robo_seguradora_{timestamp}.log")
    
    # Configura formato do log
    log_format = '%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Converte nível de log da config
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    # Configura logging básico
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # Handler para arquivo
            logging.FileHandler(log_filename, encoding='utf-8'),
            # Handler para console
            logging.StreamHandler()
        ]
    )
    
    # Obtém logger raiz
    logger = logging.getLogger()
    
    # Reduz verbosidade de bibliotecas externas
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    logger.info("=" * 80)
    logger.info("ROBÔ DE AUTOMAÇÃO - SEGURADORA")
    logger.info("=" * 80)
    logger.info(f"Arquivo de log: {log_filename}")
    logger.info(f"Nível de log: {config.LOG_LEVEL}")
    logger.info("=" * 80)
    
    return logger


class LoggerContexto:
    """Context manager para logging de seções."""
    
    def __init__(self, logger, mensagem_inicio, mensagem_fim=None):
        """
        Inicializa o context manager.
        
        Args:
            logger: Logger a ser usado
            mensagem_inicio: Mensagem ao entrar no contexto
            mensagem_fim: Mensagem ao sair do contexto (opcional)
        """
        self.logger = logger
        self.mensagem_inicio = mensagem_inicio
        self.mensagem_fim = mensagem_fim or "Concluído"
    
    def __enter__(self):
        """Entra no contexto."""
        self.logger.info(f">>> {self.mensagem_inicio}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sai do contexto."""
        if exc_type is None:
            self.logger.info(f"<<< {self.mensagem_fim}")
        else:
            self.logger.error(f"<<< Erro durante: {self.mensagem_inicio}")
            self.logger.error(f"    {exc_type.__name__}: {exc_val}")
        return False  # Não suprime exceções
