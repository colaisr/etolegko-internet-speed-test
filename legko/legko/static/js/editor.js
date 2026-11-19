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

function bindEditorPushModal() {
  const openBtn = document.getElementById("editor-open-push");
  const backdrop = document.getElementById("editor-push-backdrop");
  const body = document.getElementById("editor-push-modal-body");
  if (!openBtn || !backdrop || !body || openBtn.dataset.legkoBound === "1") return;
  openBtn.dataset.legkoBound = "1";

  const closeModal = () => {
    backdrop.hidden = true;
    backdrop.classList.remove("modal-backdrop--open");
    document.body.classList.remove("modal-open");
    body.innerHTML = "";
  };

  const bindCloseHandlers = () => {
    backdrop.querySelectorAll("[data-editor-push-close]").forEach((el) => {
      el.addEventListener("click", closeModal);
    });
  };

  backdrop.addEventListener("click", (event) => {
    if (event.target === backdrop) closeModal();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !backdrop.hidden) closeModal();
  });

  openBtn.addEventListener("click", async () => {
    const url = openBtn.getAttribute("data-push-preview-url");
    if (!url || openBtn.disabled) return;
    body.innerHTML = '<p class="text-muted">Загружаем diff…</p>';
    backdrop.hidden = false;
    backdrop.classList.add("modal-backdrop--open");
    document.body.classList.add("modal-open");
    try {
      const response = await fetch(url, { headers: { Accept: "text/html" } });
      const htmlText = await response.text();
      if (!response.ok) {
        body.innerHTML = htmlText;
        bindCloseHandlers();
        return;
      }
      body.innerHTML = htmlText;
      bindCloseHandlers();
      const form = body.querySelector(".push-confirm-form");
      form?.addEventListener("submit", () => {
        const submit = form.querySelector('button[type="submit"]');
        if (submit) submit.disabled = true;
      });
    } catch {
      body.innerHTML = '<p class="alert alert-error">Не удалось загрузить diff</p>';
      bindCloseHandlers();
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  bindEditorAddOffer();
  bindEditorCopyUrl();
  bindEditorFetchLoading();
  bindEditorPushModal();
});