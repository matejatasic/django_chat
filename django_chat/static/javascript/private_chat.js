const userAnchors = document.querySelectorAll(".user");
const websocketUrl = `ws://${window.location.host}/ws/private-chat-server`;
const privateChatSocket = new WebSocket(websocketUrl);
const form = document.getElementById("private-chat-form");
const messageInput = document.getElementById("message");

document.addEventListener("DOMContentLoaded", () => {
    privateChatSocket.onmessage = (e) => onReceivedMessageShowIt(e);
    userAnchors.forEach(user => {
        user.addEventListener("click", (e) => {
            e.preventDefault();

            let classes = e.target.className.split(" ");
            otherUserId =  classes[1].split("-")[1];
            otherUserUsername = e.target.textContent;

            getMessages(otherUserId);
        });
    });
    form.addEventListener("submit", (e) => sendMessage(e));
    messageInput.addEventListener("keypress", (e) => {
        if(e.key === "Enter" && !e.shiftKey) {
            sendMessage(e);
        }
    })

    getMessages(otherUserId);

    function getMessages(toUserId) {
        clearMessageBox();

        axios.get(`${privateChatApiUrl}?user2=${toUserId}`)
        .then(response => {
            if(response.data.length === 0) {
                showNoMessagesParagraph();

                return;
            }

            showMessages(response.data);
        })
        .catch(error => {
            showNoMessagesParagraph();
        });
    }

    function showMessages(messages) {
        for(let message of messages) {
            addMessageToHtml(message);
        }
    }

    function onReceivedMessageShowIt(e) {
        removeNoMessagesParagraph();

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
        let messageRowType;
        let username;

        if(message.sender == loggedinUserId) {
            messageRowType = "loggedin-user-message-row";
            username = "You";
        }

        else {
            messageRowType = "other-user-message-row";
            username = otherUserUsername;
        }

        let messageHtml = `
            <div class="col-md-12 d-flex message-row ${messageRowType} my-3">
                <div class="d-flex justify-content-center align-items-center user-avatar-div">
                    <img src="${profileImage}" alt="default-profile-image">
                </div>
                <div class="message-div">
                    <div class="message-box">
                        <p>
                            ${message.message}
                        </p>
                    </div>
                    <small class="float-right my-2">${username} ${timestamp}</small>
                </div>
            </div>
        `;

        messagesDiv.insertAdjacentHTML("beforeend", messageHtml);
    }

    function formatTimestamp(timestamp) {
        timestamp = timestamp.replace(/Z/, "").replace(/T/, " ").replace(/\.\d{3}/, "").replace(/:\d{5}/, "");

        return timestamp;
    }

    function sendMessage(e) {
        e.preventDefault();

        removeNoMessagesParagraph();

        let message = messageInput.value;

        if(message.trim().length === 0) {
            showWarning("Message box cannot be empty!");

            return;
        }

        let csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;

        let body = {
            "user2": otherUserId,
            "message": message,
        };
        let header = {
            headers: {
                "X-CSRFToken": csrf
            },
        };

        axios.post(privateChatApiUrl, body, header)
        .then(response => {
            if(response.statusText === "Created") {
                response.data["user2"] = otherUserId;
                let json_body = JSON.stringify(response.data);

                addMessageToHtml(response.data);

                privateChatSocket.send(json_body);
            }
        })
        .catch((error) => {
            showWarning("There was an error while trying to send the message!")
        });

        form.reset();
    }

    function showNoMessagesParagraph() {
        let messagesDiv = document.getElementById("messages-div");

        messagesDiv.innerHTML = "<p class=\"ml-3\" id=\"no-messages-paragraph\">No messages with this user</p>";
    }

    function removeNoMessagesParagraph() {
        let noMessagesParagraph = document.getElementById("no-messages-paragraph");

        if(noMessagesParagraph !== null) {
            noMessagesParagraph.remove();
        }
    }

    function clearMessageBox() {
        let messagesDiv = document.getElementById("messages-div");

        messagesDiv.innerHTML = "";
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
});