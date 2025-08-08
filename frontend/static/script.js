const apiUrl = "http://localhost:8000"; // À adapter selon ton backend
let token = "";

function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  fetch(`${apiUrl}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      username,
      password,
      grant_type: "password"
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      token = data.access_token;
      document.getElementById("login-form").classList.add("hidden");
      document.getElementById("dashboard").classList.remove("hidden");

      getTransactions();
      loadUsers();      // Charger les utilisateurs dans le select
      loadOperators();  // Charger les opérateurs dans le select
    })
    .catch((err) => alert("Erreur de connexion"));
}

function getTransactions() {
  fetch(`${apiUrl}/transactions/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      const list = document.getElementById("transaction-list");
      list.innerHTML = "";
      data.forEach((tx) => {
        const item = document.createElement("li");
        item.textContent = `Montant: ${tx.amount} | Opérateur: ${tx.operator_id} | Type: ${tx.transaction_type_id}`;
        list.appendChild(item);
      });
    });
}

function createTransaction() {
  const amount = document.getElementById("amount").value;
  const transaction_type_id = document.getElementById("transaction_type_id").value;
  const operator_id = document.getElementById("operator_id").value;
  const user_id = document.getElementById("user_id").value;

  fetch(`${apiUrl}/transactions/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      amount: parseFloat(amount),
      transaction_type_id, // depot ou retrait (string)
      operator_id: parseInt(operator_id),
      user_id: parseInt(user_id),
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      alert("Transaction créée !");
      getTransactions();
    })
    .catch((err) => alert("Erreur lors de la création"));
}

function showTab(tab) {
  document.getElementById("transactions-tab").classList.add("hidden");
  document.getElementById("new-tab").classList.add("hidden");

  if (tab === "transactions") {
    document.getElementById("transactions-tab").classList.remove("hidden");
    getTransactions();
  } else if (tab === "new") {
    document.getElementById("new-tab").classList.remove("hidden");
  }
}

function loadUsers() {
  fetch(`${apiUrl}/users/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => res.json())
    .then((users) => {
      const select = document.getElementById("user_id");
      select.innerHTML = '<option value="" disabled selected>-- Sélectionnez un utilisateur --</option>';
      users.forEach((user) => {
        const option = document.createElement("option");
        option.value = user.id;
        option.textContent = user.username;
        select.appendChild(option);
      });
    });
}

function loadOperators() {
  fetch(`${apiUrl}/operators/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => res.json())
    .then((operators) => {
      const select = document.getElementById("operator_id");
      select.innerHTML = '<option value="" disabled selected>-- Sélectionnez un opérateur --</option>';
      operators.forEach((op) => {
        const option = document.createElement("option");
        option.value = op.id;
        option.textContent = op.name;
        select.appendChild(option);
      });
    });
}
