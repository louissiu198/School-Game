class Game {
    constructor() {
        this.websocket = new WebSocket("/ws");
    }

    initialize_websocket() {
        this.websocket.addEventListener("close", (event) => {
            console.log("- websocket closed", event);
        });

        this.websocket.addEventListener("error", (error) => {
            console.error("- websocket error:", error);
        });
    }

    receive_message() {
        this.websocket.addEventListener("open", (event) => {
            console.log("+ websocket connected");
            this.load_game_info(); // Load game info when the connection is open
        });
    }
    
    response_message() {
        this.websocket.addEventListener("message", (event) => {
            let data = JSON.parse(event.data);
            if (data["type"] === "game_info") {
                console.log("+ game_info:", data["content"]);
                a(data["content"], data["user"]);
            }
            else if (data["type"] === "message") {
                console.log("+ message:", data["content"]);
            }
        });
    }

    send_message(message_str) {
        const send_message_p = { type: "message", content: message_str }; 
        this.websocket.send(JSON.stringify(send_message_p));
    }

    load_game_info() { 
        const load_game_info_p = { type: "game_info", content: document.getElementById("hiddenID").value }; 
        console.log(JSON.stringify(load_game_info_p));
        this.websocket.send(JSON.stringify(load_game_info_p));
    }

}

function a(content, user_data) {
    document.getElementById("drop1").textContent = content["player_" + user_data]["character_stats"]["actions"][0]["name"];  
    document.getElementById("drop2").textContent = content["player_" + user_data]["character_stats"]["actions"][1]["name"];    
    document.getElementById("drop3").textContent = content["player_" + user_data]["character_stats"]["actions"][2]["name"];      
}

document.addEventListener("DOMContentLoaded", () => {
    const gameClient = new Game();
    gameClient.initialize_websocket();
    gameClient.receive_message();
    gameClient.response_message();
});