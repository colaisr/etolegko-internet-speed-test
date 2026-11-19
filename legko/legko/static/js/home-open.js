function bindCampaignCombo() {
  const suggestions = document.getElementById("campaign-suggestions");
  const hiddenId = document.getElementById("keitaro_campaign_id");
  const queryInput = document.getElementById("campaign_query");
  const form = document.getElementById("open-campaign-form");
  if (!suggestions || !hiddenId || !queryInput || !form) return;

  suggestions.addEventListener("click", (event) => {
    const btn = event.target.closest(".combo-option");
    if (!btn) return;
    const id = btn.dataset.keitaroId;
    const label = btn.dataset.label || "";
    hiddenId.value = id;
    queryInput.value = `#${id} · ${label}`;
    suggestions.innerHTML = "";
  });

  form.addEventListener("submit", () => {
    if (!hiddenId.value.trim()) {
      const raw = queryInput.value.trim();
      const match = raw.match(/^#?(\d+)/);
      if (match) hiddenId.value = match[1];
      else if (/^\d+$/.test(raw)) hiddenId.value = raw;
    }
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".combo-wrap")) {
      suggestions.innerHTML = "";
    }
  });
}

document.addEventListener("DOMContentLoaded", bindCampaignCombo);
document.body?.addEventListener("htmx:afterSwap", (event) => {
  if (event.detail?.target?.id === "campaign-suggestions") return;
});