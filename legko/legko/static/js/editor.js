function bindEditorAddOffer() {
  const suggestions = document.getElementById("editor-offer-suggestions");
  const hiddenId = document.getElementById("editor_offer_id");
  const queryInput = document.getElementById("editor_offer_query");
  if (!suggestions || !hiddenId || !queryInput) return;
  if (queryInput.dataset.legkoBound === "1") return;
  queryInput.dataset.legkoBound = "1";

  suggestions.addEventListener("click", (event) => {
    const btn = event.target.closest(".combo-option");
    if (!btn) return;
    hiddenId.value = btn.dataset.offerId || "";
    queryInput.value = `#${btn.dataset.offerId} · ${btn.dataset.label || ""}`;
    suggestions.innerHTML = "";
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".combo-wrap--editor-add")) {
      suggestions.innerHTML = "";
    }
  });

  const form = document.querySelector(".editor-add-form");
  form?.addEventListener("submit", () => {
    if (hiddenId.value.trim()) return;
    const raw = queryInput.value.trim();
    const match = raw.match(/^#?(\d+)/);
    if (match) hiddenId.value = match[1];
    else if (/^\d+$/.test(raw)) hiddenId.value = raw;
  });
}

function bindEditorCopyUrl() {
  const btn = document.getElementById("editor-copy-url");
  if (!btn || btn.dataset.legkoBound === "1") return;
  btn.dataset.legkoBound = "1";
  btn.addEventListener("click", async () => {
    const id = btn.getAttribute("data-copy-target");
    const input = id ? document.getElementById(id) : null;
    const text = input?.value?.trim();
    if (!text) return;
    try {
      await navigator.clipboard.writeText(text);
      const prev = btn.textContent;
      btn.textContent = "Скопировано";
      window.setTimeout(() => {
        btn.textContent = prev;
      }, 1600);
    } catch {
      input.select();
      document.execCommand("copy");
    }
  });
}

function bindEditorFetchLoading() {
  document.querySelectorAll(".editor-fetch-form, .editor-empty-fetch-form").forEach((form) => {
    if (form.dataset.legkoFetchBound === "1") return;
    form.dataset.legkoFetchBound = "1";
    form.addEventListener("submit", () => {
      const btn = form.querySelector('button[type="submit"]');
      if (!btn || btn.disabled || btn.classList.contains("is-loading")) return;
      btn.disabled = true;
      btn.classList.add("is-loading");
      btn.setAttribute("aria-busy", "true");
      btn.innerHTML =
        '<span class="btn-spinner" aria-hidden="true"></span>' +
        '<span class="btn-loading-text">Загружаем потоки…</span>';
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  bindEditorAddOffer();
  bindEditorCopyUrl();
  bindEditorFetchLoading();
});