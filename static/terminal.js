const terminalDiv = document.getElementById("terminal");
const input = document.getElementById("cmdInput");

input.addEventListener("keydown", async (event) => {
  if (event.key === "Enter") {
    const command = input.value.trim();
    terminalDiv.innerHTML += "\n$ " + command;

    if (!command) {
      input.value = "";
      return;
    }

    try {
      let response;

      if (command === "sysinfo") {
        response = await fetch("/sysinfo");
        const j = await response.json();
        terminalDiv.innerHTML += `\nCPU: ${j.cpu_percent}% | MEM: ${j.memory_percent}% | PROCESSES: ${j.process_count}`;
        input.value = "";
        terminalDiv.scrollTop = terminalDiv.scrollHeight;
        return;
      }
       else if (command.startsWith("!py")) {
        const code = command.replace("!py", "").trim();
        response = await fetch("/local_run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ language: "python", code })
        });
      } else {
        response = await fetch("/terminal", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ command })
        });
      }

      const data = await response.json();
      if (data.stdout) {
        terminalDiv.innerHTML += "\n" + data.stdout;
      }
      if (data.stderr) {
        terminalDiv.innerHTML += "\nError: " + data.stderr;
      }
    } catch (err) {
      terminalDiv.innerHTML += "\n[Error contacting server]";
    }

    input.value = "";
    terminalDiv.scrollTop = terminalDiv.scrollHeight;
  }
});
