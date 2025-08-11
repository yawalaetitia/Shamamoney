const apiUrl = "http://localhost:8000"; // adapte selon ton API
let token = "";

// Login function
async function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const errorEl = document.getElementById("login-error");
  errorEl.textContent = "";

  if (!username || !password) {
    errorEl.textContent = "Veuillez remplir tous les champs.";
    return;
  }

  try {
    const response = await fetch(`${apiUrl}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        username,
        password,
        grant_type: "password",
      }),
    });


    if (!response.ok) {
      throw new Error("Identifiants incorrects");
    }

    const data = await response.json();
    token = data.access_token;

    document.getElementById("login-section").classList.add("hidden");
    document.getElementById("dashboard").classList.remove("hidden");

    await loadSelects();
    showTab("transactions");
  } catch (err) {
    errorEl.textContent = err.message;
  }
}

// Switch tab function
function showTab(tab) {
  document.getElementById("transactions-tab").classList.add("hidden");
  document.getElementById("new-transaction-tab").classList.add("hidden");
  document.getElementById("tab-transactions").classList.remove("active");
  document.getElementById("tab-new").classList.remove("active");

  if (tab === "transactions") {
    document.getElementById("transactions-tab").classList.remove("hidden");
    document.getElementById("tab-transactions").classList.add("active");
    getTransactions();
  } else if (tab === "new-transaction") {
    document.getElementById("new-transaction-tab").classList.remove("hidden");
    document.getElementById("tab-new").classList.add("active");
    document.getElementById("creation-message").textContent = "";
  }
}

// Get transactions list
async function getTransactions() {
  try {
    const res = await fetch(`${apiUrl}/transactions/archive`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const transactions = await res.json();
    const list = document.getElementById("transaction-list");
    list.innerHTML = "";

    if (!transactions.length) {
      list.innerHTML = "<li>Aucune transaction trouvée.</li>";
      return;
    }

    transactions.forEach((item) => {
      list.innerHTML += `
      <li>Id Transaction: ${item.id}</li></br>
      <li>Montant: ${item.amount}</li></br>
      <li>phone_number: ${item.phone_number}</li></br>
      <li>operator: ${item.operator_id}</li></br>
      <li>transaction_type: ${item.transaction_type_id}</li></br>

      <li>transaction_time: ${item.tansaction_time}</li></br>

`


      
    })
    
  } catch {
    alert("Erreur lors de la récupération des transactions");
  }
}

// Load select options for type, operator, user
async function loadSelects() {
  try {
    const [typesRes, opsRes, usersRes] = await Promise.all([
      fetch(`${apiUrl}/transaction_types`, { headers: { Authorization: `Bearer ${token}` } }),
      fetch(`${apiUrl}/operators`, { headers: { Authorization: `Bearer ${token}` } }),
      fetch(`${apiUrl}/users`, { headers: { Authorization: `Bearer ${token}` } }),
    ]);

    const types = await typesRes.json();
    const operators = await opsRes.json();
    const users = await usersRes.json();

    fillSelect("transaction_type_select", types);
    fillSelect("operator_select", operators);
    fillSelect("user_select", users);
  } catch {
    alert("Erreur lors du chargement des listes");
  }
}

function fillSelect(selectId, items) {
  const select = document.getElementById(selectId);
  select.innerHTML = "";
  items.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = item.name || item.username || "Inconnu";
    select.appendChild(option);
  });
}

// Create new transaction
async function createTransaction() {
  const amount = parseFloat(document.getElementById("amount").value);
  const phone_number = document.getElementById("phone_number").value.trim();
  const transaction_type_id = parseInt(document.getElementById("transaction_type_select").value);
  const operator_id = parseInt(document.getElementById("operator_select").value);
  const user_id = parseInt(document.getElementById("user_select").value);
  const messageEl = document.getElementById("creation-message");

  messageEl.className = "";
  messageEl.textContent = "";

  if (isNaN(amount) || amount <= 0) {
    messageEl.className = "error";
    messageEl.textContent = "Montant invalide.";
    return;
  }
  if (!phone_number) {
    messageEl.className = "error";
    messageEl.textContent = "Numéro de téléphone requis.";
    return;
  }

  try {
    const res = await fetch(`${apiUrl}/transactions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        amount,
        phone_number,
        transaction_type_id,
        operator_id,
        user_id,
      }),
    });

    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || "Erreur lors de la création");
    }

    const data = await res.json();
    messageEl.className = "success";
    messageEl.textContent = `✅ Transaction créée ! Reçu n°: ${data.receipt.receipt_number}`;

    // Reset form
    document.getElementById("amount").value = "";
    document.getElementById("phone_number").value = "";

    getTransactions();
  } catch (err) {
    messageEl.className = "error";
    messageEl.textContent = err.message;
  }
}
