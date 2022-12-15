const loginForm = document.getElementById("login-form");

async function auth(intent) {


	let user = loginForm.username.value;
	let pass = loginForm.password.value;

	const data = {
		username: user,
		password: pass
	};

	await fetch(`/${intent}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
		})
		.then((response) => response.json()
			.then((resp) => {
				card.attr("class", "alert alert-danger");
				if (response.status == 200 && intent == "login") {
					card.attr("class", "alert alert-success");
					window.location.href = '/flagpage';
                    return;
				}
				else if(response.status == 200){
					card.text(resp.message);
					card.attr("class", "alert alert-success");
					card.show();
					return;
				}
				card.text(resp.message);
				card.show();
			}))
		.catch((error) => {
			card.text(error);
			card.attr("class", "alert alert-danger");
			card.show();
		});

	toggleInputs(false);
}