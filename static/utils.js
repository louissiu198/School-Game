async function register_account(event) {
    event.preventDefault();

    const p = {
        username: document.getElementsByName("username")[0].value, // change it to ID is better
        password: document.getElementsByName("password")[0].value,
    };

    const j = JSON.stringify(p);
    const r = await fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: j,
    });


    const data = await r.json();
    if (data["message"] == "account created") { // add success animation
        window.location.href = '/lobby';
    } else {
        alert(data["message"]); // fail animation
    }
    console.log('Registeration:', data);
}

async function login_account(event) {
    event.preventDefault();

    const p = {
        username: document.getElementsByName("username")[0].value, // change it to ID is better
        password: document.getElementsByName("password")[0].value,
    };

    const j = JSON.stringify(p);
    const r = await fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: j,
    });


    const data = await r.json();
    if (data["message"] == "account created") { // add success animation
        window.location.href = '/lobby';
    } else {
        alert(data["message"]); // fail animation
    }
    console.log('Login:', data);
}

async function lobby_create_game(event) {
    event.preventDefault();

    const p = {
        gamename: document.getElementsByName("gamename")[0].value,
    };

    const j = JSON.stringify(p);
    const r = await fetch('/api/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: j,
    });


    const data = await r.json();
    if (data["status"] == "success") { // add success animation
        document.getElementById('lobby_create_game').style.display = 'none';
        document.getElementById('game_response_button').innerText = 'Join';
        document.getElementById('game_response_button').onclick = function() {
            window.location.href = '/lobby/' + data["message"].replace(/-/g, '');  // - doesnt work how-can-i-remove-a-character-from-a-string-using-javascript
        };
        document.getElementById('game_response_button').style.display = 'block';

    } else {
        alert(data["message"]); // fail animation
    }
    console.log('Lobby:', data);
}