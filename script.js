// ==========================================
// ESTADO GLOBAL
// ==========================================

let currentUser = null;
let isRegisterMode = false;
let selectedJogoForEmprestimo = null;

// ==========================================
// INICIALIZAÇÃO
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Inicializar dados de exemplo se não existir
    if (!localStorage.getItem('users')) {
        const defaultUsers = [
            {
                id: '1',
                nome: 'Admin Demo',
                email: 'admin@gameshare.com',
                senha: '123456',
                status: 'ATIVO',
                dataCadastro: new Date().toISOString()
            }
        ];
        localStorage.setItem('users', JSON.stringify(defaultUsers));
    }

    // Verificar se usuário está logado
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        showMainApp();
    }

    // Event Listeners
    setupEventListeners();
}

function setupEventListeners() {
    // Auth form
    document.getElementById('auth-form')?.addEventListener('submit', handleAuth);
    document.getElementById('toggle-auth-btn')?.addEventListener('click', toggleAuthMode);

    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            const page = e.currentTarget.dataset.page;
            if (page) navigateTo(page);
        });
    });

    document.getElementById('logout-btn')?.addEventListener('click', handleLogout);

    // Search
    document.getElementById('search-jogos')?.addEventListener('input', (e) => {
        renderCatalogo(e.target.value);
    });

    // Forms
    document.getElementById('jogo-form')?.addEventListener('submit', handleAddJogo);
    document.getElementById('emprestimo-form')?.addEventListener('submit', handleSolicitarEmprestimo);
}

// ==========================================
// AUTENTICAÇÃO
// ==========================================

function handleAuth(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const nome = document.getElementById('nome').value;

    if (isRegisterMode) {
        if (!nome || !email || !senha) {
            showError('Preencha todos os campos');
            return;
        }
        register(nome, email, senha);
    } else {
        if (!email || !senha) {
            showError('Preencha todos os campos');
            return;
        }
        login(email, senha);
    }
}

function login(email, senha) {
    const users = getUsers();
    const user = users.find(u => u.email === email && u.senha === senha);

    if (user) {
        if (user.status === 'BLOQUEADO') {
            showError('Sua conta está bloqueada por inadimplência');
            return;
        }
        currentUser = user;
        localStorage.setItem('currentUser', JSON.stringify(user));
        showMainApp();
    } else {
        showError('Email ou senha incorretos');
    }
}

function register(nome, email, senha) {
    const users = getUsers();
    
    if (users.some(u => u.email === email)) {
        showError('Email já cadastrado');
        return;
    }

    const newUser = {
        id: Date.now().toString(),
        nome,
        email,
        senha,
        status: 'ATIVO',
        dataCadastro: new Date().toISOString()
    };

    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));
    
    currentUser = newUser;
    localStorage.setItem('currentUser', JSON.stringify(newUser));
    showMainApp();
}

function handleLogout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    document.getElementById('main-app').classList.remove('active');
    document.getElementById('login-page').classList.add('active');
    document.getElementById('email').value = '';
    document.getElementById('senha').value = '';
}

function toggleAuthMode() {
    isRegisterMode = !isRegisterMode;
    
    const title = document.getElementById('auth-title');
    const submitBtn = document.getElementById('auth-submit');
    const toggleBtn = document.getElementById('toggle-auth-btn');
    const nomeField = document.getElementById('nome-field');

    if (isRegisterMode) {
        title.textContent = 'Criar Conta';
        submitBtn.textContent = 'Cadastrar';
        toggleBtn.textContent = 'Já tem conta? Entre aqui';
        nomeField.classList.remove('hidden');
    } else {
        title.textContent = 'Entrar';
        submitBtn.textContent = 'Entrar';
        toggleBtn.textContent = 'Não tem conta? Cadastre-se';
        nomeField.classList.add('hidden');
    }
    
    document.getElementById('error-message').classList.add('hidden');
}

function showMainApp() {
    document.getElementById('login-page').classList.remove('active');
    document.getElementById('main-app').classList.add('active');
    
    document.getElementById('nav-user-name').textContent = currentUser.nome;
    navigateTo('dashboard');
}

// ==========================================
// NAVEGAÇÃO
// ==========================================

function navigateTo(page) {
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === page) {
            link.classList.add('active');
        }
    });

    // Update pages
    document.querySelectorAll('.content-page').forEach(p => {
        p.classList.remove('active');
    });
    document.getElementById(`${page}-page`).classList.add('active');

    // Render page content
    switch(page) {
        case 'dashboard':
            renderDashboard();
            break;
        case 'catalogo':
            renderCatalogo();
            break;
        case 'emprestimos':
            renderEmprestimos();
            break;
        case 'perfil':
            renderPerfil();
            break;
    }
}

// ==========================================
// DASHBOARD
// ==========================================

function renderDashboard() {
    const jogos = getJogos();
    const emprestimos = getEmprestimos();
    const penalidades = getPenalidades();

    document.getElementById('welcome-name').textContent = currentUser.nome;

    // Stats
    const meusJogos = jogos.filter(j => j.dono === currentUser.id);
    const meusEmprestimos = emprestimos.filter(e => 
        e.solicitante === currentUser.id || e.dono === currentUser.id
    );
    const emprestimosAtivos = meusEmprestimos.filter(e => e.status === 'ATIVO');
    const jogosDisponiveis = jogos.filter(j => j.status === 'DISPONIVEL' && j.dono !== currentUser.id);
    const multasPendentes = penalidades.filter(p => 
        p.usuario === currentUser.id && p.status === 'PENDENTE'
    );

    document.getElementById('stat-meus-jogos').textContent = meusJogos.length;
    document.getElementById('stat-emprestimos-ativos').textContent = emprestimosAtivos.length;
    document.getElementById('stat-jogos-disponiveis').textContent = jogosDisponiveis.length;
    document.getElementById('stat-multas-pendentes').textContent = multasPendentes.length;

    // Penalty alert
    const penaltyAlert = document.getElementById('penalty-alert');
    if (multasPendentes.length > 0) {
        document.getElementById('penalty-message').textContent = 
            `Você tem ${multasPendentes.length} multa(s) pendente(s).`;
        penaltyAlert.classList.remove('hidden');
    } else {
        penaltyAlert.classList.add('hidden');
    }

    // Meus jogos
    const jogosContainer = document.getElementById('dashboard-meus-jogos');
    if (meusJogos.length === 0) {
        jogosContainer.innerHTML = '<p class="empty-state">Nenhum jogo cadastrado</p>';
    } else {
        jogosContainer.innerHTML = meusJogos.slice(0, 5).map(jogo => `
            <div class="list-item">
                <h3>${jogo.nome}</h3>
                <p>${jogo.categoria}</p>
                <span class="badge ${jogo.status === 'DISPONIVEL' ? 'badge-success' : 'badge-warning'}">
                    ${jogo.status === 'DISPONIVEL' ? 'Disponível' : 'Emprestado'}
                </span>
            </div>
        `).join('');
    }

    // Empréstimos
    const emprestimosContainer = document.getElementById('dashboard-emprestimos');
    if (emprestimosAtivos.length === 0) {
        emprestimosContainer.innerHTML = '<p class="empty-state">Nenhum empréstimo ativo</p>';
    } else {
        emprestimosContainer.innerHTML = emprestimosAtivos.slice(0, 5).map(emp => {
            const jogo = jogos.find(j => j.id === emp.jogo);
            const prazo = new Date(emp.dataPrazo);
            const hoje = new Date();
            const diasRestantes = Math.ceil((prazo - hoje) / (1000 * 60 * 60 * 24));
            
            return `
                <div class="list-item">
                    <h3>${jogo?.nome || 'Jogo desconhecido'}</h3>
                    <p>Prazo: ${prazo.toLocaleDateString('pt-BR')}</p>
                    <p style="color: ${diasRestantes < 0 ? '#ef4444' : '#6b7280'};">
                        ${diasRestantes < 0 ? 'Atrasado' : `${diasRestantes} dias restantes`}
                    </p>
                </div>
            `;
        }).join('');
    }
}

// ==========================================
// CATÁLOGO
// ==========================================

function renderCatalogo(searchTerm = '') {
    const jogos = getJogos();
    const users = getUsers();
    const penalidades = getPenalidades();

    const isBlocked = currentUser.status === 'BLOQUEADO';
    const blockedAlert = document.getElementById('blocked-alert');
    
    if (isBlocked) {
        blockedAlert.classList.remove('hidden');
    } else {
        blockedAlert.classList.add('hidden');
    }

    let jogosDisponiveis = jogos.filter(j => j.dono !== currentUser.id);
    
    if (searchTerm) {
        jogosDisponiveis = jogosDisponiveis.filter(j => 
            j.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
            j.categoria.toLowerCase().includes(searchTerm.toLowerCase())
        );
    }

    const container = document.getElementById('catalogo-jogos');
    
    if (jogosDisponiveis.length === 0) {
        container.innerHTML = '<p class="empty-state">Nenhum jogo encontrado</p>';
        return;
    }

    container.innerHTML = jogosDisponiveis.map(jogo => {
        const dono = users.find(u => u.id === jogo.dono);
        
        return `
            <div class="game-card">
                <h3>${jogo.nome}</h3>
                <p>${jogo.descricao}</p>
                <div class="game-tags">
                    <span class="badge badge-secondary">${jogo.categoria}</span>
                    <span class="badge ${jogo.status === 'DISPONIVEL' ? 'badge-success' : 'badge-danger'}">
                        ${jogo.status === 'DISPONIVEL' ? 'Disponível' : 'Emprestado'}
                    </span>
                </div>
                <p style="font-size: 13px; color: #6b7280;">Dono: ${dono?.nome || 'Desconhecido'}</p>
                ${jogo.status === 'DISPONIVEL' && !isBlocked ? `
                    <button class="btn btn-primary btn-full" onclick="openEmprestimoModal('${jogo.id}')">
                        Solicitar Empréstimo
                    </button>
                ` : isBlocked ? `
                    <button class="btn btn-secondary btn-full" disabled>Conta Bloqueada</button>
                ` : ''}
            </div>
        `;
    }).join('');
}

function openEmprestimoModal(jogoId) {
    selectedJogoForEmprestimo = jogoId;
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('emprestimo-prazo').setAttribute('min', today);
    document.getElementById('emprestimo-modal').classList.add('active');
}

function closeEmprestimoModal() {
    selectedJogoForEmprestimo = null;
    document.getElementById('emprestimo-modal').classList.remove('active');
    document.getElementById('emprestimo-form').reset();
}

function handleSolicitarEmprestimo(e) {
    e.preventDefault();
    
    if (!selectedJogoForEmprestimo) return;

    const prazo = document.getElementById('emprestimo-prazo').value;
    if (!prazo) {
        showToast('Selecione uma data de devolução', 'error');
        return;
    }

    const jogos = getJogos();
    const jogo = jogos.find(j => j.id === selectedJogoForEmprestimo);
    
    if (!jogo || jogo.status !== 'DISPONIVEL') {
        showToast('Jogo indisponível', 'error');
        closeEmprestimoModal();
        return;
    }

    // Criar empréstimo
    const emprestimos = getEmprestimos();
    const novoEmprestimo = {
        id: Date.now().toString(),
        jogo: selectedJogoForEmprestimo,
        solicitante: currentUser.id,
        dono: jogo.dono,
        status: 'ATIVO',
        dataPrazo: new Date(prazo).toISOString(),
        dataCadastro: new Date().toISOString()
    };

    emprestimos.push(novoEmprestimo);
    localStorage.setItem('emprestimos', JSON.stringify(emprestimos));

    // Atualizar status do jogo
    jogo.status = 'EMPRESTADO';
    const allJogos = getJogos();
    const updatedJogos = allJogos.map(j => j.id === jogo.id ? jogo : j);
    localStorage.setItem('jogos', JSON.stringify(updatedJogos));

    showToast('Empréstimo solicitado com sucesso!', 'success');
    closeEmprestimoModal();
    renderCatalogo();
}

// ==========================================
// EMPRÉSTIMOS
// ==========================================

function renderEmprestimos() {
    const emprestimos = getEmprestimos();
    const jogos = getJogos();
    const users = getUsers();

    const comoSolicitante = emprestimos.filter(e => e.solicitante === currentUser.id);
    const comoDono = emprestimos.filter(e => e.dono === currentUser.id);

    // Jogos que peguei emprestado
    const solicitanteContainer = document.getElementById('emprestimos-solicitante');
    if (comoSolicitante.length === 0) {
        solicitanteContainer.innerHTML = '<p class="empty-state">Nenhum empréstimo realizado</p>';
    } else {
        solicitanteContainer.innerHTML = comoSolicitante.map(emp => {
            const jogo = jogos.find(j => j.id === emp.jogo);
            const dono = users.find(u => u.id === emp.dono);
            const prazo = new Date(emp.dataPrazo);
            const hoje = new Date();
            const diasRestantes = Math.ceil((prazo - hoje) / (1000 * 60 * 60 * 24));

            return `
                <div class="emprestimo-item">
                    <div class="emprestimo-header">
                        <div>
                            <h3>${jogo?.nome || 'Jogo desconhecido'}</h3>
                            <p>Dono: ${dono?.nome || 'Desconhecido'}</p>
                        </div>
                        <span class="badge ${
                            emp.status === 'ATIVO' ? 'badge-warning' : 
                            emp.status === 'DEVOLVIDO' ? 'badge-success' : 'badge-secondary'
                        }">
                            ${emp.status === 'ATIVO' ? 'Em andamento' : 
                              emp.status === 'DEVOLVIDO' ? 'Devolvido' : 'Cancelado'}
                        </span>
                    </div>
                    <p>Prazo: ${prazo.toLocaleDateString('pt-BR')}</p>
                    ${emp.status === 'ATIVO' ? `
                        <p style="color: ${diasRestantes < 0 ? '#ef4444' : '#6b7280'};">
                            ${diasRestantes < 0 ? `Atrasado ${Math.abs(diasRestantes)} dias` : `${diasRestantes} dias restantes`}
                        </p>
                    ` : ''}
                    ${emp.dataDevolvido ? `
                        <p>Devolvido em: ${new Date(emp.dataDevolvido).toLocaleDateString('pt-BR')}</p>
                    ` : ''}
                </div>
            `;
        }).join('');
    }

    // Jogos que emprestei
    const donoContainer = document.getElementById('emprestimos-dono');
    if (comoDono.length === 0) {
        donoContainer.innerHTML = '<p class="empty-state">Nenhum empréstimo ativo</p>';
    } else {
        donoContainer.innerHTML = comoDono.map(emp => {
            const jogo = jogos.find(j => j.id === emp.jogo);
            const solicitante = users.find(u => u.id === emp.solicitante);
            const prazo = new Date(emp.dataPrazo);
            const hoje = new Date();
            const prazoVencido = prazo < hoje && emp.status === 'ATIVO';

            return `
                <div class="emprestimo-item">
                    <div class="emprestimo-header">
                        <div>
                            <h3>${jogo?.nome || 'Jogo desconhecido'}</h3>
                            <p>Solicitante: ${solicitante?.nome || 'Desconhecido'}</p>
                        </div>
                        <span class="badge ${
                            emp.status === 'ATIVO' ? 'badge-warning' : 
                            emp.status === 'DEVOLVIDO' ? 'badge-success' : 'badge-secondary'
                        }">
                            ${emp.status === 'ATIVO' ? 'Em andamento' : 
                              emp.status === 'DEVOLVIDO' ? 'Devolvido' : 'Cancelado'}
                        </span>
                    </div>
                    <p>Prazo: ${prazo.toLocaleDateString('pt-BR')}</p>
                    ${prazoVencido ? `
                        <p style="color: #ef4444; font-weight: 500;">Prazo vencido! Confirme a devolução</p>
                    ` : ''}
                    ${emp.dataDevolvido ? `
                        <p>Devolvido em: ${new Date(emp.dataDevolvido).toLocaleDateString('pt-BR')}</p>
                    ` : ''}
                    ${emp.status === 'ATIVO' && prazoVencido ? `
                        <div class="emprestimo-actions">
                            <button class="btn btn-primary" onclick="confirmarDevolucao('${emp.id}', true)">
                                Devolvido
                            </button>
                            <button class="btn btn-secondary" onclick="confirmarDevolucao('${emp.id}', false)" 
                                    style="background: #ef4444; color: white;">
                                Não Devolvido
                            </button>
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');
    }
}

function confirmarDevolucao(emprestimoId, devolvido) {
    const emprestimos = getEmprestimos();
    const emprestimo = emprestimos.find(e => e.id === emprestimoId);
    
    if (!emprestimo) return;

    if (devolvido) {
        // Marcar como devolvido
        emprestimo.status = 'DEVOLVIDO';
        emprestimo.dataDevolvido = new Date().toISOString();
        
        // Liberar jogo
        const jogos = getJogos();
        const updatedJogos = jogos.map(j => 
            j.id === emprestimo.jogo ? { ...j, status: 'DISPONIVEL' } : j
        );
        localStorage.setItem('jogos', JSON.stringify(updatedJogos));
        
        showToast('Devolução confirmada com sucesso!', 'success');
    } else {
        // Aplicar penalidade
        const penalidades = getPenalidades();
        const novaPenalidade = {
            id: Date.now().toString(),
            usuario: emprestimo.solicitante,
            emprestimo: emprestimoId,
            valorMulta: 50,
            status: 'PENDENTE',
            dataCadastro: new Date().toISOString()
        };
        penalidades.push(novaPenalidade);
        localStorage.setItem('penalidades', JSON.stringify(penalidades));

        // Bloquear usuário
        const users = getUsers();
        const updatedUsers = users.map(u => 
            u.id === emprestimo.solicitante ? { ...u, status: 'BLOQUEADO' } : u
        );
        localStorage.setItem('users', JSON.stringify(updatedUsers));

        showToast('Multa aplicada e usuário bloqueado', 'warning');
    }

    localStorage.setItem('emprestimos', JSON.stringify(emprestimos));
    renderEmprestimos();
}

// ==========================================
// PERFIL
// ==========================================

function renderPerfil() {
    const jogos = getJogos();
    const penalidades = getPenalidades();

    document.getElementById('perfil-nome').textContent = currentUser.nome;
    document.getElementById('perfil-email').textContent = currentUser.email;

    const statusBadge = document.getElementById('perfil-status-badge');
    if (currentUser.status === 'ATIVO') {
        statusBadge.className = 'badge badge-success';
        statusBadge.textContent = 'Conta Ativa';
    } else if (currentUser.status === 'BLOQUEADO') {
        statusBadge.className = 'badge badge-danger';
        statusBadge.textContent = 'Conta Bloqueada';
    }

    // Penalidades
    const multasPendentes = penalidades.filter(p => 
        p.usuario === currentUser.id && p.status === 'PENDENTE'
    );

    const penalidadesCard = document.getElementById('perfil-penalidades');
    if (multasPendentes.length > 0) {
        penalidadesCard.classList.remove('hidden');
        document.getElementById('lista-penalidades').innerHTML = multasPendentes.map(pen => `
            <div class="penalty-item">
                <h3>Multa por Atraso</h3>
                <p>Valor: R$ ${pen.valorMulta.toFixed(2)}</p>
                <p>Data: ${new Date(pen.dataCadastro).toLocaleDateString('pt-BR')}</p>
                <button class="btn btn-primary" onclick="pagarMulta('${pen.id}')">
                    Pagar Multa
                </button>
            </div>
        `).join('');
    } else {
        penalidadesCard.classList.add('hidden');
    }

    // Jogos
    const meusJogos = jogos.filter(j => j.dono === currentUser.id);
    document.getElementById('perfil-total-jogos').textContent = meusJogos.length;

    const jogosContainer = document.getElementById('perfil-jogos');
    if (meusJogos.length === 0) {
        jogosContainer.innerHTML = '<p class="empty-state">Nenhum jogo cadastrado</p>';
    } else {
        jogosContainer.innerHTML = meusJogos.map(jogo => `
            <div class="game-card">
                <h3>${jogo.nome}</h3>
                <p>${jogo.descricao}</p>
                <div class="game-tags">
                    <span class="badge badge-secondary">${jogo.categoria}</span>
                    <span class="badge ${jogo.status === 'DISPONIVEL' ? 'badge-success' : 'badge-warning'}">
                        ${jogo.status === 'DISPONIVEL' ? 'Disponível' : 'Emprestado'}
                    </span>
                </div>
            </div>
        `).join('');
    }
}

function toggleAddJogo() {
    const form = document.getElementById('add-jogo-form');
    form.classList.toggle('hidden');
    
    if (!form.classList.contains('hidden')) {
        document.getElementById('jogo-nome').focus();
    }
}

function handleAddJogo(e) {
    e.preventDefault();
    
    const nome = document.getElementById('jogo-nome').value;
    const descricao = document.getElementById('jogo-descricao').value;
    const categoria = document.getElementById('jogo-categoria').value;

    if (!nome || !descricao || !categoria) {
        showToast('Preencha todos os campos', 'error');
        return;
    }

    const jogos = getJogos();
    const novoJogo = {
        id: Date.now().toString(),
        nome,
        descricao,
        categoria,
        dono: currentUser.id,
        status: 'DISPONIVEL',
        dataCadastro: new Date().toISOString()
    };

    jogos.push(novoJogo);
    localStorage.setItem('jogos', JSON.stringify(jogos));

    showToast('Jogo cadastrado com sucesso!', 'success');
    
    document.getElementById('jogo-form').reset();
    toggleAddJogo();
    renderPerfil();
}

function pagarMulta(penalidadeId) {
    const penalidades = getPenalidades();
    const penalidade = penalidades.find(p => p.id === penalidadeId);
    
    if (!penalidade) return;

    // Marcar multa como paga
    penalidade.status = 'PAGA';
    penalidade.dataPagamento = new Date().toISOString();
    localStorage.setItem('penalidades', JSON.stringify(penalidades));

    // Desbloquear usuário
    const users = getUsers();
    const updatedUsers = users.map(u => 
        u.id === currentUser.id ? { ...u, status: 'ATIVO' } : u
    );
    localStorage.setItem('users', JSON.stringify(updatedUsers));
    
    currentUser.status = 'ATIVO';
    localStorage.setItem('currentUser', JSON.stringify(currentUser));

    showToast('Multa paga com sucesso! Sua conta foi desbloqueada.', 'success');
    
    setTimeout(() => {
        renderPerfil();
        renderDashboard();
    }, 500);
}

// ==========================================
// HELPERS
// ==========================================

function getUsers() {
    return JSON.parse(localStorage.getItem('users') || '[]');
}

function getJogos() {
    return JSON.parse(localStorage.getItem('jogos') || '[]');
}

function getEmprestimos() {
    return JSON.parse(localStorage.getItem('emprestimos') || '[]');
}

function getPenalidades() {
    return JSON.parse(localStorage.getItem('penalidades') || '[]');
}

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}
