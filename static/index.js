class Game {
    constructor() {
        this.websocket = new WebSocket("/ws");
    }

    initialize_websocket() {
        this.websocket.addEventListener("close", (event) => {
            console.log("WebSocket connection closed:", event);
        });

        this.websocket.addEventListener("error", (error) => {
            console.error("WebSocket error observed:", error);
        });
    }

    receive_message() {
        this.websocket.addEventListener("open", (event) => {
            console.log("WebSocket connection established.");
            this.load_game_info(); // Load game info when the connection is open
        });
    }
    
    response_message() {
        this.websocket.addEventListener("message", (event) => {
            console.log("Message from server:", event.data);
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

document.addEventListener("DOMContentLoaded", () => {
    const gameClient = new Game();
    gameClient.initialize_websocket();
    gameClient.receive_message();
    gameClient.response_message();
});