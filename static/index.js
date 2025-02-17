function initialize_websocket() {
    const websocket = new WebSocket("ws://localhost:3333/ws");

    websocket.addEventListener("open", (event) => {
        console.log("WebSocket connection established.");
        websocket.send("Hello Server!"); 
    });

    websocket.addEventListener("message", (event) => {
        console.log("Message from server:", event.data);
    });

    websocket.addEventListener("close", (event) => {
        console.log("WebSocket connection closed:", event);
    });

    websocket.addEventListener("error", (error) => {
        console.error("WebSocket error observed:", error);
    });
}

initialize_websocket();

// function recieve_commands() {

// }