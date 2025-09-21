async function runPython() {
    const code = document.getElementById("codeInput").value;
    const outEl = document.getElementById("outputBox");
    outEl.textContent = "Running…";
  
    try {
      const res = await fetch("/local_run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language: "python", code })
      });
  
      const data = await res.json();
  
      let output = "";
      if (data.stdout) output += data.stdout;
      if (data.stderr) output += (output ? "\n" : "") + "[stderr]\n" + data.stderr;
      output += `\n(return code ${data.returncode})`;
  
      outEl.textContent = output;
    } catch (err) {
      outEl.textContent = "Network error: " + err;
    }
  }
  
  // Attach to the Run button
  document.getElementById("runBtn").addEventListener("click", runPython);
  