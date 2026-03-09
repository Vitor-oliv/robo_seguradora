# Guia de Customização Avançada

Este documento fornece orientações detalhadas para adaptar o robô ao seu ambiente específico.

## 🎯 Pontos Críticos de Customização

### 1. Seletores CSS/XPath

Os seletores são a parte mais importante para adaptar ao seu site. Aqui está como descobri-los:

#### Método 1: Chrome DevTools

1. Abra o site da seguradora
2. Pressione `F12` para abrir DevTools
3. Clique no ícone de seleção (ou `Ctrl+Shift+C`)
4. Clique no elemento desejado na página
5. No painel Elements, clique com botão direito no elemento destacado
6. Escolha: **Copy → Copy selector** (para CSS) ou **Copy → Copy XPath**

#### Método 2: Testar Seletores no Console

No console do Chrome (F12 → Console), teste seus seletores:

```javascript
// Testar seletor CSS
document.querySelector("#username")

// Testar seletor que retorna múltiplos elementos
document.querySelectorAll(".pedido-item")

// Contar quantos elementos foram encontrados
document.querySelectorAll(".pedido-item").length
```

#### Exemplos de Seletores Comuns

```python
# Por ID
"#campo-usuario"

# Por classe
".btn-login"

# Por atributo
"input[name='username']"
"button[type='submit']"

# Combinações
"form#login button.btn-primary"
"div.pedido-container .item-codigo"

# XPath (mais poderoso, mas mais complexo)
"//input[@id='username']"
"//button[contains(text(), 'Entrar')]"
"//div[@class='pedido']//span[@class='item-codigo']"
```

### 2. Estrutura da Página de Pedidos

O robô precisa saber como extrair informações dos pedidos. Veja exemplos de diferentes estruturas HTML:

#### Exemplo 1: Dados em Atributos

```html
<div class="pedido-item" data-pedido-id="12345" data-item="ABC123" data-quantidade="2" data-estado="SP">
    <span class="pedido-numero">Pedido #12345</span>
    <button class="btn-recusar">Recusar</button>
</div>
```

**Configuração para este caso:**

```python
# Em modules/scraper.py, método _extrair_dados_pedido:
id_pedido = elemento.get_attribute("data-pedido-id")
item = elemento.get_attribute("data-item")
quantidade = elemento.get_attribute("data-quantidade")
estado = elemento.get_attribute("data-estado")
```

#### Exemplo 2: Dados em Sub-elementos

```html
<div class="pedido-item">
    <div class="pedido-header">
        <span class="pedido-id">12345</span>
    </div>
    <div class="pedido-body">
        <span class="item-codigo">ABC123</span>
        <span class="item-qtd">2</span>
        <span class="cliente-estado">SP</span>
    </div>
    <div class="pedido-actions">
        <button class="btn-recusar">Recusar</button>
        <input class="campo-desconto" type="number">
        <button class="btn-aplicar">Aplicar</button>
    </div>
</div>
```

**Configuração para este caso:**

```python
# Em modules/scraper.py, método _extrair_dados_pedido:
id_pedido = elemento.find_element(By.CSS_SELECTOR, ".pedido-id").text
item = elemento.find_element(By.CSS_SELECTOR, ".item-codigo").text
quantidade = elemento.find_element(By.CSS_SELECTOR, ".item-qtd").text
estado = elemento.find_element(By.CSS_SELECTOR, ".cliente-estado").text
```

#### Exemplo 3: Dados em Tabela

```html
<table class="tabela-pedidos">
    <tbody>
        <tr class="pedido-row">
            <td class="col-id">12345</td>
            <td class="col-item">ABC123</td>
            <td class="col-qtd">2</td>
            <td class="col-estado">SP</td>
            <td class="col-acoes">
                <button class="btn-recusar">Recusar</button>
            </td>
        </tr>
    </tbody>
</table>
```

**Configuração para este caso:**

```python
# config.py
SELETORES = {
    "lista_pedidos": "tr.pedido-row",  # Cada linha é um pedido
    # ...
}

# modules/scraper.py, método _extrair_dados_pedido:
colunas = elemento.find_elements(By.TAG_NAME, "td")
id_pedido = colunas[0].text
item = colunas[1].text
quantidade = colunas[2].text
estado = colunas[3].text
```

### 3. Estrutura da API de Estoque

A API pode ter diferentes formatos de requisição e resposta. Veja como adaptar:

#### Exemplo 1: API REST com POST

**Requisição:**
```json
POST /api/estoque/verificar
{
    "codigo_item": "ABC123",
    "quantidade": 2
}
```

**Resposta:**
```json
{
    "disponivel": true,
    "quantidade": 150,
    "item": "ABC123"
}
```

**Configuração:**

```python
# Em modules/estoque.py, método verificar_disponibilidade:
payload = {
    "codigo_item": codigo_item,
    "quantidade": quantidade
}

response = requests.post(url, json=payload, headers=self.headers, timeout=10)
data = response.json()

disponivel = data.get('disponivel', False)
quantidade_estoque = data.get('quantidade', 0)
```

#### Exemplo 2: API REST com GET

**Requisição:**
```
GET /api/estoque/verificar?item=ABC123&qtd=2
```

**Resposta:**
```json
{
    "status": "ok",
    "estoque": {
        "disponivel": 150,
        "reservado": 20
    }
}
```

**Configuração:**

```python
# Em modules/estoque.py, método verificar_disponibilidade:
params = {
    "item": codigo_item,
    "qtd": quantidade
}

response = requests.get(url, params=params, headers=self.headers, timeout=10)
data = response.json()

quantidade_estoque = data.get('estoque', {}).get('disponivel', 0)
disponivel = quantidade_estoque >= quantidade
```

#### Exemplo 3: API com Autenticação Bearer Token

```python
# config.py
ESTOQUE_API_HEADERS = {
    "Authorization": f"Bearer {ESTOQUE_API_KEY}",
    "Content-Type": "application/json"
}
```

#### Exemplo 4: API com API Key no Header

```python
# config.py
ESTOQUE_API_HEADERS = {
    "X-API-Key": ESTOQUE_API_KEY,
    "Content-Type": "application/json"
}
```

### 4. Fluxo de Aplicação de Desconto

Dependendo do site, o fluxo pode variar:

#### Opção 1: Campo de Desconto + Botão

```python
# modules/scraper.py, método aplicar_desconto_e_informar:
campo_desconto = pedido.elemento_web.find_element(By.CSS_SELECTOR, self.config.SELETORES["campo_desconto"])
campo_desconto.clear()
campo_desconto.send_keys(str(desconto_percentual))

botao_aplicar = pedido.elemento_web.find_element(By.CSS_SELECTOR, self.config.SELETORES["botao_aplicar_desconto"])
botao_aplicar.click()
```

#### Opção 2: Dropdown de Desconto

```python
from selenium.webdriver.support.ui import Select

dropdown_desconto = Select(pedido.elemento_web.find_element(By.CSS_SELECTOR, "#desconto-select"))
dropdown_desconto.select_by_value(str(desconto_percentual))
```

#### Opção 3: Modal de Desconto

```python
# Clica em botão que abre modal
botao_abrir_modal = pedido.elemento_web.find_element(By.CSS_SELECTOR, ".btn-editar")
botao_abrir_modal.click()

# Aguarda modal aparecer
modal = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-desconto")))

# Preenche desconto no modal
campo_desconto = modal.find_element(By.CSS_SELECTOR, "#desconto")
campo_desconto.send_keys(str(desconto_percentual))

# Confirma
botao_confirmar = modal.find_element(By.CSS_SELECTOR, ".btn-confirmar")
botao_confirmar.click()
```

### 5. Tratamento de Modais de Confirmação

Se o site exibe modais de confirmação ao recusar pedidos:

```python
# Em modules/scraper.py, método recusar_pedido:

# Clica no botão de recusar
botao_recusar.click()
time.sleep(1)

# Aguarda modal de confirmação
try:
    modal_confirmacao = self.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-confirmacao"))
    )
    botao_confirmar = modal_confirmacao.find_element(By.CSS_SELECTOR, ".btn-sim")
    botao_confirmar.click()
    time.sleep(self.config.DELAY_ENTRE_ACOES)
except:
    # Se não houver modal, continua normalmente
    pass
```

## 🔍 Debugging

### Modo Visual (Desativar Headless)

```python
# config.py
HEADLESS_MODE = False
```

Isso permite ver o navegador em ação e identificar problemas.

### Logs Detalhados

```python
# config.py
LOG_LEVEL = "DEBUG"
```

### Screenshots de Erro

Adicione em `modules/scraper.py`:

```python
def _tirar_screenshot_erro(self, nome):
    """Tira screenshot em caso de erro."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/erro_{nome}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot salvo: {filename}")
    except:
        pass
```

Use em pontos críticos:

```python
try:
    elemento = self.driver.find_element(By.CSS_SELECTOR, seletor)
except:
    self._tirar_screenshot_erro("elemento_nao_encontrado")
    raise
```

### Pausar Execução para Inspeção

```python
# Adicione onde quiser pausar
import pdb; pdb.set_trace()

# Ou simplesmente:
input("Pressione Enter para continuar...")
```

## 🚀 Otimizações

### Paralelização (Avançado)

Se você tem muitos pedidos, pode processar em paralelo:

```python
from concurrent.futures import ThreadPoolExecutor

def processar_lote(pedidos_lote):
    # Cada thread teria sua própria instância do driver
    driver = configurar_driver()
    # ... processar pedidos
    driver.quit()

# Divide pedidos em lotes
lotes = [pedidos[i:i+5] for i in range(0, len(pedidos), 5)]

with ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(processar_lote, lotes)
```

### Cache de Consultas de Estoque

```python
# Em modules/estoque.py
from functools import lru_cache

@lru_cache(maxsize=1000)
def verificar_disponibilidade_cached(self, codigo_item: str, quantidade: int):
    return self.verificar_disponibilidade(codigo_item, quantidade)
```

## 📞 Dicas Finais

1. **Sempre teste com poucos pedidos primeiro** antes de processar em larga escala
2. **Faça backup dos dados** antes de executar o robô
3. **Monitore os logs** durante as primeiras execuções
4. **Ajuste os delays** se o site for lento ou rápido demais
5. **Considere usar proxies** se houver limitação de taxa
6. **Implemente retry logic** para requisições que podem falhar temporariamente

---

**Boa sorte com a customização!** 🚀
