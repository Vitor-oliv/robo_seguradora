# Robô de Automação - Seguradora

Robô desenvolvido em Python para automatizar o processamento de pedidos no sistema da seguradora, integrando com API de estoque e aplicando descontos por estado.

## 📋 Funcionalidades

O robô executa as seguintes tarefas automaticamente:

1. **Acessa o site da seguradora** com login e senha
2. **Lista todos os pedidos** pendentes na página
3. **Consulta a API de estoque** para verificar disponibilidade de cada item
4. **Recusa pedidos** quando não há estoque disponível (clica no botão de recusa)
5. **Aplica descontos** baseados no estado do pedido quando há estoque
6. **Informa disponibilidade** no sistema da seguradora
7. **Valida Estados**: Verifica se o estado de cobrança é igual ao de entrega
8. **Salva Alterações**: Clica no botão de salvar após aplicar descontos
9. **Gera Relatório Excel**: Cria uma planilha com todos os pedidos cotados no dia
10. **Gera logs detalhados** de todas as operações

## 🏗️ Estrutura do Projeto

```
robo_seguradora/
├── config.py              # Configurações (URLs, credenciais, descontos)
├── main.py                # Script principal
├── modules/
│   ├── __init__.py
│   ├── auth.py           # Autenticação no site
│   ├── scraper.py        # Extração de dados dos pedidos
│   ├── estoque.py        # Integração com API de estoque
│   ├── processador.py    # Lógica de processamento
│   └── logger.py         # Sistema de logs
├── requirements.txt       # Dependências Python
├── logs/                  # Diretório de logs (criado automaticamente)
├── ARQUITETURA.md        # Documentação da arquitetura
└── README.md             # Este arquivo
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Acesso à internet

### Passo a Passo

1. **Clone ou baixe o projeto**

```bash
cd robo_seguradora
```

2. **Instale as dependências**

```bash
pip install -r requirements.txt
```

Ou usando pip3:

```bash
pip3 install -r requirements.txt
```

## ⚙️ Configuração

**IMPORTANTE**: Antes de executar o robô, você DEVE configurar os seguintes itens no arquivo `config.py`:

### 1. Credenciais da Seguradora

```python
SEGURADORA_URL = "https://sistema.seguradora.com.br"  # URL do sistema
SEGURADORA_LOGIN = "seu_usuario_aqui"                 # Seu usuário
SEGURADORA_SENHA = "sua_senha_aqui"                   # Sua senha
```

### 2. Seletores CSS/XPath

Os seletores precisam ser ajustados conforme a estrutura HTML real do site da seguradora. Para descobrir os seletores corretos:

1. Abra o site da seguradora no Chrome
2. Clique com botão direito no elemento → "Inspecionar"
3. Copie o seletor CSS ou XPath

Exemplo de configuração:

```python
SELETORES = {
    "campo_login": "#username",           # Seletor do campo de usuário
    "campo_senha": "#password",           # Seletor do campo de senha
    "botao_entrar": "button[type='submit']",  # Botão de login
    "lista_pedidos": ".pedido-item",      # Itens de pedido
    "botao_recusar": ".btn-recusar",      # Botão de recusa
    "campo_desconto": "#desconto",        # Campo de desconto
    "botao_aplicar_desconto": ".btn-aplicar-desconto",
    "campo_observacao": "#observacao",    # Campo de observação
}
```

### 3. API de Estoque

Configure a URL e chave de autenticação da sua API:

```python
ESTOQUE_API_URL = "https://api.seuestoque.com.br/v1"
ESTOQUE_API_KEY = "sua_api_key_aqui"
ESTOQUE_ENDPOINT = "/estoque/verificar"  # Endpoint de consulta
```

**Ajuste também a estrutura da requisição/resposta** no arquivo `modules/estoque.py` conforme a documentação da sua API.

### 4. Tabela de Descontos

Atualize os percentuais de desconto por estado conforme definido pelo seu chefe:

```python
DESCONTOS_ESTADO = {
    "SP": 14.0,  # São Paulo
    "RJ": 15.0,  # Rio de Janeiro
    "MG": 12.0,  # Minas Gerais
    # ... outros estados
}
```

### 5. Modo de Execução

```python
HEADLESS_MODE = False  # False = mostra navegador, True = executa em background
```

## ▶️ Execução

### Execução Normal

```bash
python main.py
```

Ou:

```bash
python3 main.py
```

### Execução com Logs Detalhados

Para ver logs mais detalhados, altere em `config.py`:

```python
LOG_LEVEL = "DEBUG"
```

### Usando Variáveis de Ambiente (Opcional)

Para maior segurança, você pode usar variáveis de ambiente para credenciais:

```bash
export SEGURADORA_LOGIN="seu_usuario"
export SEGURADORA_SENHA="sua_senha"
export ESTOQUE_API_KEY="sua_api_key"
python main.py
```

## 📊 Logs

Os logs são salvos automaticamente em:

```
logs/robo_seguradora_YYYYMMDD_HHMMSS.log
```

Cada execução gera um novo arquivo de log com timestamp.

### Exemplo de Log

```
2026-02-12 15:30:00 | INFO     | __main__            | >>> Realizando login no site da seguradora
2026-02-12 15:30:05 | INFO     | modules.auth        | ✓ Login realizado com sucesso!
2026-02-12 15:30:06 | INFO     | modules.scraper     | Encontrados 15 pedidos na página
2026-02-12 15:30:10 | INFO     | modules.processador | [1/15] Processando Pedido(id=12345, item=ABC123, qtd=2, estado=SP)
2026-02-12 15:30:11 | INFO     | modules.estoque     | ✓ Item ABC123 disponível em estoque (qtd: 50)
2026-02-12 15:30:12 | INFO     | modules.processador | Desconto para SP: 14.0%
2026-02-12 15:30:13 | INFO     | modules.scraper     | ✓ Desconto aplicado e disponibilidade informada
```

## 🔧 Personalização

### Ajustar Tempos de Espera

Em `config.py`:

```python
TIMEOUT_PADRAO = 10          # Timeout para elementos (segundos)
DELAY_ENTRE_ACOES = 1        # Delay entre ações (segundos)
```

### Modificar Lógica de Extração

Edite o método `_extrair_dados_pedido()` em `modules/scraper.py` para ajustar como os dados são extraídos do HTML.

### Modificar Estrutura da API

Edite os métodos em `modules/estoque.py` para ajustar:
- Formato da requisição (payload)
- Método HTTP (GET/POST)
- Estrutura da resposta

## 🐛 Solução de Problemas

### Erro: "Element not found"

**Causa**: Seletores CSS/XPath incorretos ou página não carregou completamente.

**Solução**:
1. Verifique os seletores em `config.py`
2. Aumente `TIMEOUT_PADRAO` e `DELAY_ENTRE_ACOES`
3. Execute com `HEADLESS_MODE = False` para visualizar o navegador

### Erro: "Login failed"

**Causa**: Credenciais incorretas ou estrutura de login diferente.

**Solução**:
1. Verifique `SEGURADORA_LOGIN` e `SEGURADORA_SENHA`
2. Ajuste seletores de login em `SELETORES`
3. Modifique método `_verificar_login_sucesso()` em `modules/auth.py`

### Erro: "API connection failed"

**Causa**: URL da API incorreta, API fora do ar, ou chave inválida.

**Solução**:
1. Verifique `ESTOQUE_API_URL` e `ESTOQUE_API_KEY`
2. Teste a API manualmente (Postman, curl)
3. Verifique logs para detalhes do erro

### Pedidos não sendo processados

**Causa**: Estrutura da página diferente do esperado.

**Solução**:
1. Execute com `LOG_LEVEL = "DEBUG"` para ver detalhes
2. Inspecione o HTML da página de pedidos
3. Ajuste seletores e lógica de extração em `modules/scraper.py`

## 📝 Checklist de Configuração

Antes de executar em produção, verifique:

- [ ] Credenciais da seguradora configuradas
- [ ] Todos os seletores CSS/XPath ajustados e testados
- [ ] URL e chave da API de estoque configuradas
- [ ] Estrutura de requisição/resposta da API ajustada
- [ ] Tabela de descontos atualizada com valores reais
- [ ] Teste manual realizado com `HEADLESS_MODE = False`
- [ ] Logs verificados para garantir funcionamento correto

## 🔒 Segurança

**IMPORTANTE**: 

- **Nunca** compartilhe o arquivo `config.py` com credenciais preenchidas
- Use variáveis de ambiente para dados sensíveis em produção
- Mantenha os logs seguros (podem conter informações sensíveis)
- Revise permissões de acesso ao diretório do projeto

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs em `logs/`
2. Consulte a seção "Solução de Problemas" acima
3. Revise a documentação da arquitetura em `ARQUITETURA.md`

## 📄 Licença

Este projeto foi desenvolvido para uso interno. Todos os direitos reservados.

---

**Desenvolvido com Manus AI** | Versão 1.0 | 2026-02-12
