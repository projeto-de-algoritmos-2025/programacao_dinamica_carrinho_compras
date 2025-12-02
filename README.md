# Carrinho de Compras Inteligente

Sistema de otimização de compras baseado no Problema da Mochila (0/1 Knapsack) implementado com Programação Dinâmica.

## Sobre o Projeto

Aplicação web completa que resolve o problema da mochila aplicado a um carrinho de compras. O sistema encontra a combinação ótima de itens que maximiza a prioridade total respeitando um orçamento definido.

### Algoritmo

**Técnica:** Programação Dinâmica  
**Problema:** Knapsack 0/1  
**Complexidade Temporal:** O(n × W)  
**Complexidade Espacial:** O(n × W)

Onde:
- n = número de itens
- W = orçamento em centavos

## Execução

### Requisitos

- Python 3.8+
- Navegador web

### Instalação

```bash
pip install -r requirements.txt
```

### Iniciar Aplicação

```bash
python main.py
```

A aplicação estará disponível em `http://localhost:8000`

O navegador será aberto automaticamente com a interface web.

## Funcionalidades

- Definir orçamento disponível
- Adicionar itens com nome, preço e prioridade (1-10)
- Remover itens do carrinho
- Otimizar seleção de itens usando Programação Dinâmica
- Interface web responsiva
- API RESTful completa

## API Endpoints

### Orçamento
- `POST /budget` - Define o orçamento
- `GET /budget` - Retorna o orçamento atual

### Itens
- `POST /items` - Adiciona item
- `GET /items` - Lista todos os itens
- `GET /items/{item_id}` - Retorna item específico
- `PUT /items/{item_id}` - Atualiza item
- `DELETE /items/{item_id}` - Remove item
- `DELETE /items` - Remove todos os itens

### Otimização
- `POST /optimize` - Otimiza lista de itens fornecida
- `POST /optimize/current` - Otimiza itens atuais do carrinho
- `POST /optimize/detailed` - Otimização com informações detalhadas

### Carrinho
- `GET /cart/status` - Status completo do carrinho
- `POST /reset` - Reseta carrinho

## Documentação

Documentação interativa disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Tecnologias

**Backend**
- FastAPI
- Pydantic
- Uvicorn

**Frontend**
- HTML5
- CSS3
- JavaScript ES6+

**Algoritmo**
- Python

## Estrutura

```
programacao_dinamica_carrinho_compras/
├── models/
│   ├── __init__.py
│   ├── item.py
│   ├── budget.py
│   ├── optimize.py
│   └── cart_state.py
├── routes/
│   ├── __init__.py
│   ├── budget.py
│   ├── items.py
│   ├── optimization.py
│   └── cart.py
├── static/
│   └── index.html
│      
├── main.py
├── knapsack.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Problema da Mochila

**Entrada:**
- Orçamento disponível (W)
- Lista de itens com preço e prioridade

**Objetivo:**
Maximizar prioridade total sem ultrapassar o orçamento

**Solução:**
Tabela de programação dinâmica dp[i][w]:
- i = itens considerados
- w = orçamento disponível
- dp[i][w] = prioridade máxima alcançável

## Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## Apresentação em video

[clique aqui](https://youtu.be/t7oNxeypieI)
