const Auth = {
  mostrarLogin() {
    document.getElementById("form-login").classList.remove("hidden");
    document.getElementById("form-cadastro").classList.add("hidden");
    document.getElementById("tab-login").classList.add("active");
    document.getElementById("tab-cadastro").classList.remove("active");
  },

  mostrarCadastro() {
    document.getElementById("form-login").classList.add("hidden");
    document.getElementById("form-cadastro").classList.remove("hidden");
    document.getElementById("tab-login").classList.remove("active");
    document.getElementById("tab-cadastro").classList.add("active");
  },

  async login(e) {
    e.preventDefault();
    const email = document.getElementById("login-email").value;
    const senha = document.getElementById("login-senha").value;
    const erroEl = document.getElementById("login-erro");
    erroEl.classList.add("hidden");
    const res = await Api.post("/auth/login", { email, senha });
    if (res.erro) {
      erroEl.textContent = res.erro;
      erroEl.classList.remove("hidden");
    } else {
      Api.setToken(res.token);
      localStorage.setItem("usuario", JSON.stringify(res.usuario));
      App.iniciarSessao(res.usuario);
    }
  },

  async cadastrar(e) {
    e.preventDefault();
    const nome = document.getElementById("cad-nome").value;
    const email = document.getElementById("cad-email").value;
    const senha = document.getElementById("cad-senha").value;
    const erroEl = document.getElementById("cad-erro");
    erroEl.classList.add("hidden");
    const res = await Api.post("/auth/cadastrar", { nome, email, senha });
    if (res.erro) {
      erroEl.textContent = res.erro;
      erroEl.classList.remove("hidden");
    } else {
      Api.setToken(res.token);
      localStorage.setItem("usuario", JSON.stringify(res.usuario));
      App.iniciarSessao(res.usuario);
    }
  },
};