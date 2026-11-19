function bindCampaignCombo() {
  const suggestions = document.getElementById("campaign-suggestions");
  const hiddenId = document.getElementById("keitaro_campaign_id");
  const queryInput = document.getElementById("campaign_query");
  const previewBtn = document.getElementById("open-campaign-preview");
  if (!suggestions || !hiddenId || !queryInput) return;

  function syncPreviewButton() {
    if (!previewBtn) return;
    const hasId = Boolean(hiddenId.value.trim()) || /^\d+/.test(queryInput.value.trim());
    previewBtn.disabled = !hasId;
  }

  function setSelection(id, label) {
    hiddenId.value = id;
    queryInput.value = `#${id} · ${label}`;
    suggestions.innerHTML = "";
    syncPreviewButton();
  }

  suggestions.addEventListener("click", (event) => {
    const btn = event.target.closest(".combo-option");
    if (!btn) return;
    const id = btn.dataset.keitaroId;
    const label = btn.dataset.label || "";
    setSelection(id, label);
    openCampaignPreviewModal(id, label);
  });

  queryInput.addEventListener("input", () => {
    hiddenId.value = "";
    syncPreviewButton();
  });

  previewBtn?.addEventListener("click", () => {
    let id = hiddenId.value.trim();
    if (!id) {
      const raw = queryInput.value.trim();
      const match = raw.match(/^#?(\d+)/);
      if (match) id = match[1];
      else if (/^\d+$/.test(raw)) id = raw;
    }
    if (!id) return;
    const label = queryInput.value.replace(/^#\d+\s*·\s*/, "").trim() || `Campaign #${id}`;
    hiddenId.value = id;
    openCampaignPreviewModal(id, label);
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".combo-wrap--campaign")) {
      suggestions.innerHTML = "";
    }
  });

  syncPreviewButton();
}

function openCampaignPreviewModal(keitaroId, name) {
  const params = new URLSearchParams({
    keitaro_campaign_id: String(keitaroId),
    name: name || "",
  });
  if (typeof htmx !== "undefined") {
    htmx.ajax("GET", `/campaigns/open/panel?${params.toString()}`, {
      target: "#app-modal-body",
      swap: "innerHTML",
    });
  }
}

function legkoLoadModalPanel(url) {
  if (typeof htmx === "undefined") return;
  htmx.ajax("GET", url, { target: "#app-modal-body", swap: "innerHTML" });
}

function legkoOpenRecent(localId) {
  legkoLoadModalPanel(`/campaigns/${localId}/recent/panel`);
}

function legkoOpenCreate() {
  legkoLoadModalPanel("/campaigns/new/panel");
}

window.legkoOpenRecent = legkoOpenRecent;
window.legkoOpenCreate = legkoOpenCreate;
window.legkoLoadModalPanel = legkoLoadModalPanel;

document.addEventListener("DOMContentLoaded", bindCampaignCombo);