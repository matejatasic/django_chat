const websocketUrl = `ws://${window.location.host}/ws/chat-server`;
const publicChatSocket = new WebSocket(websocketUrl);
const form = document.getElementById("public-chat-form");
const messageInput = document.getElementById("message");

document.addEventListener("DOMContentLoaded", () => {
    publicChatSocket.onmessage = (e) => onReceivedMessageShowIt(e);
    form.addEventListener("submit", (e) => sendMessage(e));
    messageInput.addEventListener("keypress", (e) => {
        if(e.key === "Enter" && !e.shiftKey) {
            sendMessage(e);
        }
    })

    getMessages();

    function getMessages() {
        axios.get(publicChatApiUrl)
        .then((response) => {
            showMessages(response.data);
        })
        .catch((error) => {
            showWarning("There was an error while trying to fetch the messages!");
        });
    }

    function showMessages(messages) {
        for(let message of messages) {
            addMessageToHtml(message);
        }
    }

    function onReceivedMessageShowIt(e) {
        let data = e.data
        let response = JSON.parse(data)

        if(response.type === "new_message") {
            let message = response["message"];

            addMessageToHtml(message);
        }
    }

    function addMessageToHtml(message) {
        let messagesDiv = document.getElementById("messages-div");
        let timestamp = formatTimestamp(message.timestamp);

        let messageHtml = `
            <div class="col-md-12 d-flex message-row my-3">
                <div class="d-flex justify-content-center align-items-center">
                    <img src="${profileImage}" alt="default-profile-image">
                </div>
                <div>
                    <div class="message-box">
                        <p>
                            ${message.message}
                        </p>
                    </div>
                    <small class="float-right my-2">${message.user} ${timestamp}</small>
                </div>
            </div>
        `;

        messagesDiv.insertAdjacentHTML("beforeend", messageHtml);
    }

    function formatTimestamp(timestamp) {
        timestamp = timestamp.replace(/Z/, "").replace(/T/, " ").replace(/\.\d{3}/, "");

        return timestamp;
    }

    function sendMessage(e) {
        e.preventDefault();

        let message = messageInput.value;

        if(message.trim().length === 0) {
            showWarning("Message box cannot be empty!");

            return;
        }

        let csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        let body = {
            "message": message,
            "user_id": userId
        };
        let header = {
            headers: {
                'X-CSRFToken': csrf
            },
        };

        axios.post(publicChatApiUrl, body, header)
        .then(response => {
            if(response.statusText === "Created") {
                let json_body = JSON.stringify(response.data);

                publicChatSocket.send(json_body);
            }
        })
        .catch((error) => {
            showWarning("There was an error while trying to send the message!")
        });

        form.reset();
    }

    function showWarning(message) {
        let warningDiv = document.getElementById("warning-div");
        warningDiv.innerHTML = `
            <div class="alert alert-danger">${message}</div>
        `;

        setTimeout(() => {
            warningDiv.innerHTML = "";
        }, 4000);
    }
})