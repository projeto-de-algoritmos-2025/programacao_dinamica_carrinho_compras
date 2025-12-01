const API_URL = 'http://localhost:8000';

let budget = 0;
let items = [];

const budgetInput = document.getElementById('budget');
const setBudgetBtn = document.getElementById('setBudget');
const budgetDisplay = document.getElementById('budgetDisplay');
const currentBudgetSpan = document.getElementById('currentBudget');
const itemForm = document.getElementById('itemForm');
const itemNameInput = document.getElementById('itemName');
const itemPriceInput = document.getElementById('itemPrice');
const itemPriorityInput = document.getElementById('itemPriority');
const emptyCart = document.getElementById('emptyCart');
const cartItems = document.getElementById('cartItems');
const optimizationSection = document.getElementById('optimizationSection');
const optimizeBtn = document.getElementById('optimizeBtn');
const optimizedResult = document.getElementById('optimizedResult');
const optimizedItems = document.getElementById('optimizedItems');
const optimizedTotal = document.getElementById('optimizedTotal');
const optimizedPriority = document.getElementById('optimizedPriority');
const remainingBudget = document.getElementById('remainingBudget');

setBudgetBtn.addEventListener('click', setBudget);
itemForm.addEventListener('submit', addItem);
optimizeBtn.addEventListener('click', optimizeCart);
window.addEventListener('DOMContentLoaded', loadCartStatus);

async function loadCartStatus() {
    try {
        const response = await fetch(`${API_URL}/cart/status`);
        if (response.ok) {
            const data = await response.json();
            budget = data.budget;
            items = data.items || [];
            
            if (budget > 0) {
                currentBudgetSpan.textContent = formatCurrency(budget);
                budgetDisplay.classList.remove('hidden');
            }
            
            renderCart();
            
            if (budget > 0 && items.length > 0) {
                optimizationSection.classList.remove('hidden');
            }
        }
    } catch (error) {
        console.error('Erro ao carregar status do carrinho:', error);
        showError('Não foi possível conectar à API. Certifique-se de que o servidor FastAPI está rodando.');
    }
}

// Definir orçamento
async function setBudget() {
    const value = parseFloat(budgetInput.value);
    
    if (isNaN(value) || value <= 0) {
        alert('Por favor, insira um valor válido para o orçamento.');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/budget`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ budget: value })
        });
        
        if (response.ok) {
            const data = await response.json();
            budget = data.budget;
            currentBudgetSpan.textContent = formatCurrency(budget);
            budgetDisplay.classList.remove('hidden');
            budgetInput.value = '';
            
            if (items.length > 0) {
                optimizationSection.classList.remove('hidden');
            }
        } else {
            throw new Error('Erro ao definir orçamento');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao definir orçamento. Verifique se a API está rodando.');
    }
}

// Adicionar item ao carrinho
async function addItem(e) {
    e.preventDefault();
    
    const name = itemNameInput.value.trim();
    const price = parseFloat(itemPriceInput.value);
    const priority = parseInt(itemPriorityInput.value);
    
    if (!name || isNaN(price) || price <= 0 || isNaN(priority) || priority < 1 || priority > 10) {
        alert('Por favor, preencha todos os campos corretamente.');
        return;
    }
    
    const item = {
        name: name,
        price: price,
        priority: priority
    };
    
    try {
        const response = await fetch(`${API_URL}/items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(item)
        });
        
        if (response.ok) {
            const data = await response.json();
            items.push(data.item);
            
            itemForm.reset();
            renderCart();
            
            if (budget > 0) {
                optimizationSection.classList.remove('hidden');
            }
        } else {
            throw new Error('Erro ao adicionar item');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao adicionar item. Verifique se a API está rodando.');
    }
}

// Deletar item do carrinho
async function deleteItem(id) {
    if (confirm('Tem certeza que deseja remover este item?')) {
        try {
            const response = await fetch(`${API_URL}/items/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                items = items.filter(item => item.id !== id);
                renderCart();
                
                if (items.length === 0) {
                    optimizationSection.classList.add('hidden');
                    optimizedResult.classList.add('hidden');
                }
            } else {
                throw new Error('Erro ao deletar item');
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao deletar item. Verifique se a API está rodando.');
        }
    }
}

// Renderizar carrinho
function renderCart() {
    if (items.length === 0) {
        emptyCart.classList.remove('hidden');
        cartItems.classList.add('hidden');
        cartItems.innerHTML = '';
        return;
    }
    
    emptyCart.classList.add('hidden');
    cartItems.classList.remove('hidden');
    
    cartItems.innerHTML = items.map(item => `
        <div class="cart-item">
            <div class="item-info">
                <div class="item-name">${escapeHtml(item.name)}</div>
                <div class="item-details">
                    <div class="item-detail">
                        <span class="item-detail-label">Preço</span>
                        <span class="item-detail-value item-price">${formatCurrency(item.price)}</span>
                    </div>
                    <div class="item-detail">
                        <span class="item-detail-label">Prioridade</span>
                        <span class="item-detail-value item-priority">${item.priority}/10</span>
                    </div>
                </div>
            </div>
            <button class="btn btn-danger" onclick="deleteItem(${item.id})">Deletar</button>
        </div>
    `).join('');
}

async function optimizeCart() {
    if (items.length === 0) {
        alert('Adicione itens ao carrinho primeiro.');
        return;
    }
    
    if (budget <= 0) {
        alert('Defina um orçamento primeiro.');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/optimize/current`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            renderOptimizedResult(
                data.selected_items,
                data.total_price,
                data.total_priority,
                data.remaining_budget
            );
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao otimizar carrinho');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao otimizar carrinho: ' + error.message);
    }
}

// Renderizar resultado da otimização
function renderOptimizedResult(selectedItems, totalPrice, totalPriority, remaining) {
    optimizedResult.classList.remove('hidden');
    
    if (selectedItems.length === 0) {
        optimizedItems.innerHTML = '<p style="text-align: center; color: #6c757d; padding: 20px;">Nenhum item pode ser selecionado com o orçamento disponível.</p>';
        optimizedTotal.textContent = formatCurrency(0);
        optimizedPriority.textContent = '0';
        remainingBudget.textContent = formatCurrency(budget);
        return;
    }
    
    optimizedItems.innerHTML = selectedItems.map(item => `
        <div class="optimized-item">
            <span class="optimized-item-name">${escapeHtml(item.name)}</span>
            <div class="optimized-item-info">
                <span>${formatCurrency(item.price)}</span>
                <span>${item.priority}/10</span>
            </div>
        </div>
    `).join('');
    
    optimizedTotal.textContent = formatCurrency(totalPrice);
    optimizedPriority.textContent = totalPriority;
    remainingBudget.textContent = formatCurrency(remaining);
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #dc3545; color: white; padding: 15px 20px; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); z-index: 1000; max-width: 400px;';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}
