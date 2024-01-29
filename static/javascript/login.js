console.clear();
if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {


    ready()
}

function ready() {

	// JWT token obtained after successful authentication
	var jwtToken = "your_jwt_token_here";

	const loginBtn = document.getElementById('login');
	const signupBtn = document.getElementById('signup');
	const registerBtn = document.getElementById('registerBtn');
	const loginInBtn = document.getElementById('loginInBtn')
	const regName = document.getElementById('regName')
	const regSurname = document.getElementById('regSurname')
	const regEmail = document.getElementById('regEmail')
	const regPassword = document.getElementById('regPassword')
	const logEmail = document.getElementById('logEmail')
	const logPassword = document.getElementById('logPassword')
	const alertElement = document.getElementById('myAlert');

	loginBtn.addEventListener('click', (e) => {
		let parent = e.target.parentNode.parentNode;
		Array.from(e.target.parentNode.parentNode.classList).find((element) => {
			if (element !== "slide-up") {
				parent.classList.add('slide-up')
			} else {
				signupBtn.parentNode.classList.add('slide-up')
				parent.classList.remove('slide-up')
			}
		});
	});

	signupBtn.addEventListener('click', (e) => {
		let parent = e.target.parentNode;
		Array.from(e.target.parentNode.classList).find((element) => {
			if (element !== "slide-up") {
				parent.classList.add('slide-up')
			} else {
				loginBtn.parentNode.parentNode.classList.add('slide-up')
				parent.classList.remove('slide-up')
			}
		});
	});
	registerBtn.addEventListener('click',(e) =>{


		var userData = {
			"name" : regName.value,
			"surname" : regSurname.value,
			"email" : regEmail.value,
			"password" : regPassword.value
		}
		// Fetch API to make a POST request with JSON body
		fetch('/register', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(userData)
		})
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.then(data => {
			message = data['message']
			if (message === "User successfully registered"){
				successAlert(alertElement, message)
			}
			else if (message === "Email already registered") {
				errorAlert(alertElement, message)
			}
		})
		.catch(error => {
			console.error('Error:', error);
		});
	})
	loginInBtn.addEventListener('click',(e) =>{

		var userData = {
			"email" : logEmail.value,
			"password" : logPassword.value
		}
		// Fetch API to make a POST request with JSON body
		fetch('/login', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(userData)
		})
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.then(data => {
			message = data['message']
			if (message === "User successfully registered"){
				successAlert(alertElement, message)
			}
			else if (message === "Invalid email or password") {
				errorAlert(alertElement, message)
			}
		})
		.catch(error => {
			console.error('Error:', error);
		});
	})
}

function errorAlert(alertElement, message) {
	if (alertElement) {
		alertElement.style.display = 'block';
		alertElement.style.backgroundColor = '#DC143C';
		alertElement.innerText = message;

		setTimeout(function () {
			if (alertElement) {
				alertElement.style.display = 'none';
			}
		}, 2000); // 2000 milliseconds = 2 seconds
	}
}

function successAlert(alertElement, message) {
	if (alertElement) {
		alertElement.style.display = 'block';
		alertElement.style.backgroundColor = 'lightgreen';
		alertElement.innerText = message;

		setTimeout(function () {
			if (alertElement) {
				alertElement.style.display = 'none';
			}
		}, 2000); // 2000 milliseconds = 2 seconds
	}
}