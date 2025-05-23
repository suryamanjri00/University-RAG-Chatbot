// app/static/script.js

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("chat-form");
  const chatBody = document.getElementById("chat-body");
  const input = document.getElementById("question-input");
  const userTyping = document.getElementById("user-typing-indicator");
  const botThinking = document.getElementById("bot-thinking-indicator");

  // Ensure both indicators start hidden
  userTyping.style.display = "none";
  botThinking.style.display = "none";

  // 1) Show "User is typing..." when input has text
  input.addEventListener("input", () => {
    if (input.value.trim().length > 0) {
      userTyping.style.display = "block";
    } else {
      userTyping.style.display = "none";
    }
  });

  // 2) Handle form submit
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    // Hide user‑typing indicator and append user message
    userTyping.style.display = "none";
    appendMessage("user", question);
    input.value = "";

    // Show bot‑thinking indicator
    botThinking.style.display = "block";

    try {
      const fd = new FormData();
      fd.append("question", question);
      fd.append("model_name", "mistral");

      const res = await fetch("/ask", {
        method: "POST",
        body: fd
      });
      const data = await res.json();

      botThinking.style.display = "none";
      if (data.answer) {
        appendMessage("bot", data.answer);
      } else if (data.error) {
        appendMessage("bot", "Error: " + data.error);
      } else {
        appendMessage("bot", "No response from server.");
      }
    } catch (err) {
      botThinking.style.display = "none";
      appendMessage("bot", "Network error: " + err.message);
    }
  });

  // Utility to add a message bubble
  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.textContent = text;
    chatBody.appendChild(msg);
    chatBody.scrollTop = chatBody.scrollHeight;
  }
});
