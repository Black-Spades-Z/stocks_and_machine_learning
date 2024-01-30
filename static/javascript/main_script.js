
var lang = {
  "uzb": {
    "hi": "Salom, Chippi",
    "search": "Qidiruv...",
    "market_prices": "Bozor qiymatlari",
    "my_balance": "Mening hisobim",
    "balance": "Balans",
    "withdraw": "Yechib olish",
    "deposit": "Deposit",
    "my_portfolio": "Mening Portfoliom"
  },
  "ru": {
    "hi": "Привет, Чиппи",
    "search": "Поиск...",
    "market_prices": "Цены на акции",
    "my_balance": "Мой Баланс",
    "balance": "Баланс",
    "withdraw": "Снять",
    "deposit": "Депозит",
    "my_portfolio": "Мое Портфолио"
  },
  "eng": {
    "hi": "Welcome, Chippi",
    "search": "Search...",
    "market_prices": "Stock prices",
    "my_balance": "My Balance",
    "balance": "Balance",
    "withdraw": "Withdraw",
    "deposit": "Deposit",
    "my_portfolio": "My Portfolio"
  }
};

function showLanguages() {
  const languageList = document.getElementById('language-list');
  languageList.style.display = (languageList.style.display === 'block') ? 'none' : 'block';
}

function changeLanguage(languageCode) {
  const hi = document.getElementById('hi');
  const search = document.getElementById('search');
  const market_prices = document.getElementById('market_prices');
  const my_balance = document.getElementById('my_balance');
  const balance = document.getElementById('balance');
  const withdraw = document.getElementById('withdraw');
  const deposit = document.getElementById('deposit');
  const my_portfolio = document.getElementById('my_portfolio');
  

  // Replace the content based on the selected language
  if (languageCode === 'eng') {
    hi.textContent = 'Welcome, Chippi';
    search.textContent = 'Search...';
    market_prices.textContent = 'Stock prices';
    my_balance.textContent = 'My Balance';
    balance.textContent = 'Balance';
    withdraw.textContent = 'Withdraw';
    deposit.textContent = 'Deposit';
    my_portfolio.textContent = 'My Portfolio';

  } else if (languageCode === 'es') {
    heading.textContent = '¡Hola, Mundo!';
    description.textContent = 'Esto es una página de muestra.';
    inputField.placeholder = 'Escribe algo...';
    // Add more language translations as needed
  }

  // Hide the language menu after selecting a language
  document.getElementById('language-list').style.display = 'none';

  
}

function changeIcon(anchor) {   // should be added to html part in order to show/hide balance in the card
    var icon = anchor.querySelector("i");
    icon.classList.toggle('bx-show');
    icon.classList.toggle('bx-hide');
    anchor.querySelector("span").textContent = icon.matches('.bx-hide') ? "*********" : anchor.querySelector("span").dataset.text;
}