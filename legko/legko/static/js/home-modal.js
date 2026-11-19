function getAppModal() {
  return document.getElementById("app-modal");
}

function openAppModal() {
  const backdrop = getAppModal();
  if (!backdrop) return;
  backdrop.classList.add("modal-backdrop--open");
  backdrop.setAttribute("aria-hidden", "false");
  document.body.classList.add("modal-open");
}

function closeAppModal() {
  const backdrop = getAppModal();
  if (!backdrop) return;
  backdrop.classList.remove("modal-backdrop--open");
  backdrop.setAttribute("aria-hidden", "true");
  document.body.classList.remove("modal-open");
  const body = document.getElementById("app-modal-body");
  if (body) body.innerHTML = "";
}

function bindModalChrome() {
  const backdrop = getAppModal();
  if (!backdrop) return;

  backdrop.addEventListener("click", (event) => {
    if (event.target === backdrop) closeAppModal();
  });

  document.addEventListener("click", (event) => {
    if (event.target.closest("[data-modal-close]")) {
      event.preventDefault();
      closeAppModal();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && backdrop.classList.contains("modal-backdrop--open")) {
      closeAppModal();
    }
  });
}

function bindModalHtmx() {
  document.body.addEventListener("htmx:afterSwap", (event) => {
    const target = event.detail?.target;
    if (!target || target.id !== "app-modal-body") return;
    openAppModal();
    if (typeof htmx !== "undefined") {
      htmx.process(target);
    }
    if (typeof bindCreatorForm === "function") bindCreatorForm();
    if (target.querySelector(".modal-panel--success")) {
      document.body.dispatchEvent(new Event("legkoRecentRefresh"));
      if (typeof htmx !== "undefined") {
        htmx.trigger(document.body, "legkoRecentRefresh");
      }
    }
    const title =
      document.getElementById("create-modal-title") || document.getElementById("open-modal-title");
    const dialog = title?.closest('[role="dialog"]');
    if (title && dialog) dialog.setAttribute("aria-labelledby", title.id);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  bindModalChrome();
  bindModalHtmx();
});

window.legkoOpenModal = openAppModal;
window.legkoCloseModal = closeAppModal;