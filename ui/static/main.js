document.getElementById("runBtn").addEventListener("click", async () => {
  const teamAName = document.getElementById("teamAName").value || "Team A";
  const teamBName = document.getElementById("teamBName").value || "Team B";
  const teamAStr = Number(document.getElementById("teamAStr").value) || 5;
  const teamBStr = Number(document.getElementById("teamBStr").value) || 5;
  const setsTo = Number(document.getElementById("setsTo").value) || 3;

  const payload = {
    teamA: { name: teamAName, strength: teamAStr },
    teamB: { name: teamBName, strength: teamBStr },
    sets_to: setsTo
  };

  const resultDiv = document.getElementById("result");
  const eventsPre = document.getElementById("events");
  resultDiv.textContent = "Running...";
  eventsPre.textContent = "";

  try {
    const resp = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await resp.json();
    if (!resp.ok || !data.ok) {
      resultDiv.textContent = "Error: " + (data.error || JSON.stringify(data));
      return;
    }

    const res = data.result;
    const sets = res.sets || [];
    const winner = res.winner || "Unknown";
    resultDiv.innerHTML = `<strong>Winner:</strong> ${winner}<br/><strong>Sets:</strong> ${sets.map(s => s.a + '-' + s.b).join(', ')}`;

    if (Array.isArray(res.events)) {
      eventsPre.textContent = res.events.join("\n");
    } else {
      eventsPre.textContent = JSON.stringify(res.events, null, 2);
    }
  } catch (err) {
    resultDiv.textContent = "Network error: " + err;
  }
});
