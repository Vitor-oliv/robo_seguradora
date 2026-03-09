# Arquitetura do Robô de Automação - Seguradora

## Visão Geral

O robô será desenvolvido em Python utilizando Selenium para automação web e requests para integração com API REST.

## Estrutura de Arquivos

```
robo_seguradora/
├── config.py              # Configurações (credenciais, URLs, descontos)
├── main.py                # Script principal de execução
├── modules/
│   ├── __init__.py
│   ├── auth.py           # Autenticação no site da seguradora
│   ├── scraper.py        # Extração de dados dos pedidos
│   ├── estoque.py        # Integração com API de estoque
│   ├── processador.py    # Lógica de processamento e decisão
│   └── logger.py         # Sistema de logs
├── requirements.txt       # Dependências do projeto
├── logs/                  # Diretório de logs
└── README.md             # Documentação de uso

```

## Fluxo de Execução

1. **Inicialização**: Carrega configurações e credenciais
2. **Autenticação**: Faz login no site da seguradora
3. **Listagem**: Identifica todos os pedidos pendentes
4. **Processamento** (para cada pedido):
   - Extrai informações (item, quantidade, estado)
   - Consulta API de estoque
   - **Se NÃO tem estoque**: Clica no botão de recusa
   - **Se TEM estoque**: 
     - Calcula desconto baseado no estado
     - Aplica desconto no sistema
     - Informa disponibilidade
5. **Finalização**: Gera relatório e logs

## Tecnologias

- **Selenium WebDriver**: Automação do navegador
- **Requests**: Chamadas HTTP para API
- **Python-dotenv**: Gerenciamento de variáveis de ambiente
- **Logging**: Sistema de logs nativo do Python

## Configurações Necessárias

### config.py (valores placeholder)

```python
# Credenciais Seguradora
SEGURADORA_URL = "https://sistema.seguradora.com.br"
SEGURADORA_LOGIN = "seu_usuario"
SEGURADORA_SENHA = "sua_senha"

# API Estoque
ESTOQUE_API_URL = "https://api.seuestoque.com.br"
ESTOQUE_API_KEY = "sua_api_key"

# Descontos por Estado (%)
DESCONTOS_ESTADO = {
    "SP": 10,
    "RJ": 15,
    "MG": 12,
    "RS": 8,
    "BA": 7,
    # ... outros estados
}
```

## Pontos de Atenção

1. **Seletores CSS/XPath**: Precisarão ser ajustados conforme a estrutura HTML real do site
2. **Tempo de espera**: Configurar waits adequados para carregamento de páginas
3. **Tratamento de erros**: Capturar exceções de rede, timeout, elementos não encontrados
4. **Logs detalhados**: Registrar todas as ações para auditoria
