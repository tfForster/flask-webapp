// static/js/admin.js

async function updateStats() {
  try {
    const response = await fetch("/admin/stats", { credentials: "include" });
    const data = await response.json();

    // Update Zahlen auf der Seite
    document.getElementById("user-count").textContent = data.user_count;
    document.getElementById("message-count").textContent = data.message_count;
  } catch (err) {
    console.error("Fehler beim Abrufen der Daten:", err);
  }
}

// Alle 10 Sekunden aktualisieren
setInterval(updateStats, 10000);

// Sofort beim Laden ausführen
updateStats();
