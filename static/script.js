fetchEvents();
setInterval(fetchEvents, 15000);

function fetchEvents() {
    fetch("/webhook/events")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("events");
            container.innerHTML = "";

            data.forEach(event => {
                const div = document.createElement("div");
                let text = "";

                if (event.event === "push") {
                    text = `${event.author} pushed to ${event.to_branch} on ${formatTime(event.timestamp)}`;
                }
                else if (event.event === "pull_request") {
                    text = `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${formatTime(event.timestamp)}`;
                }
                else if (event.event === "merge") {
                    text = `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${formatTime(event.timestamp)}`;
                }

                div.innerText = text;
                container.appendChild(div);
            });
        });
}

function formatTime(ts) {
    return new Date(ts).toUTCString();
}
