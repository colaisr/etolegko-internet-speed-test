const CREATOR_FIELD_IDS = {
  campaign_name: "campaign_name",
  geo_code: "geo_code",
  offer_query: "offer_query",
};

function setErrorSlot(errEl, message) {
  if (!errEl) return;
  if (message) {
    errEl.textContent = message;
    errEl.classList.add("field-error--active");
  } else {
    errEl.textContent = "";
    errEl.classList.remove("field-error--active");
  }
}

function clearCreatorValidation() {
  Object.values(CREATOR_FIELD_IDS).forEach((id) => {
    const input = document.getElementById(id);
    const err = document.getElementById(`${id}-error`);
    input?.classList.remove("field--invalid");
    input?.removeAttribute("aria-invalid");
    setErrorSlot(err, "");
  });
  document.getElementById("template-preview")?.classList.remove("preview-box--warn");
}

function setFieldError(fieldId, message) {
  const input = document.getElementById(fieldId);
  const err = document.getElementById(`${fieldId}-error`);
  if (!input || !err) return;
  input.classList.add("field--invalid");
  input.setAttribute("aria-invalid", "true");
  setErrorSlot(err, message);
  if (fieldId === "offer_query") {
    document.getElementById("template-preview")?.classList.add("preview-box--warn");
  }
}

function validateCreatorFields() {
  const hiddenOffer = document.getElementById("offer_id");
  const offerInput = document.getElementById("offer_query");
  const geoInput = document.getElementById("geo_code");
  const nameInput = document.getElementById("campaign_name");

  if (hiddenOffer && offerInput && !hiddenOffer.value.trim()) {
    const raw = offerInput.value.trim();
    const match = raw.match(/^#?(\d+)/);
    if (match) hiddenOffer.value = match[1];
    else if (/^\d+$/.test(raw)) hiddenOffer.value = raw;
  }
  if (geoInput) geoInput.value = geoInput.value.trim().toUpperCase().slice(0, 2);

  const issues = [];
  if (!nameInput?.value.trim()) {
    issues.push({
      field: "campaign_name",
      message: "Введите название",
    });
  }
  if (!geoInput?.value.trim() || geoInput.value.trim().length !== 2) {
    issues.push({
      field: "geo_code",
      message: "Две латинские буквы, например DE",
    });
  }
  if (!hiddenOffer?.value.trim()) {
    issues.push({
      field: "offer_query",
      message: "Выберите оффер из списка или укажите ID",
    });
  }
  return issues;
}

function applyCreatorValidation(issues) {
  clearCreatorValidation();
  if (!issues.length) return true;
  issues.forEach((issue) => setFieldError(issue.field, issue.message));
  const first = document.getElementById(issues[0].field);
  first?.focus();
  if (issues.some((i) => i.field === "offer_query")) {
    const offerInput = document.getElementById("offer_query");
    if (offerInput && typeof htmx !== "undefined") {
      htmx.trigger(offerInput, "focus");
    }
  }
  return false;
}

function bindCreatorForm() {
  const form = document.getElementById("creator-form");
  const offerSuggestions = document.getElementById("offer-suggestions");
  const geoSuggestions = document.getElementById("geo-suggestions");
  const hiddenOffer = document.getElementById("offer_id");
  const offerInput = document.getElementById("offer_query");
  const geoInput = document.getElementById("geo_code");
  const nameInput = document.getElementById("campaign_name");
  const previewGeo = document.getElementById("preview-stream-geo");
  const previewOffer = document.getElementById("preview-stream-offer");
  if (!form || !previewGeo || !previewOffer) return;
  if (form.dataset.legkoBound === "1") return;
  form.dataset.legkoBound = "1";

  function clearFieldValidation(fieldId) {
    const input = document.getElementById(fieldId);
    const err = document.getElementById(`${fieldId}-error`);
    input?.classList.remove("field--invalid");
    input?.removeAttribute("aria-invalid");
    setErrorSlot(err, "");
    if (fieldId === "offer_query") {
      document.getElementById("template-preview")?.classList.remove("preview-box--warn");
    }
  }

  function updatePreview() {
    const geo = (geoInput?.value || "…").trim().toUpperCase() || "…";
    const offerLabel =
      (offerInput?.value || "").trim() ||
      (hiddenOffer?.value ? `#${hiddenOffer.value}` : "…");
    previewGeo.innerHTML = `Поток 1: <strong>${geo}</strong> → Google`;
    previewOffer.innerHTML = `Поток 2: остальной трафик → оффер <strong>${offerLabel}</strong>`;
    if (hiddenOffer?.value.trim()) {
      clearFieldValidation("offer_query");
    }
  }

  [nameInput, geoInput, offerInput].forEach((el) => {
    el?.addEventListener("input", () => {
      clearFieldValidation(el.id);
      updatePreview();
    });
  });
  updatePreview();

  function pickGeo(code) {
    if (!geoInput || !code) return;
    geoInput.value = code.toUpperCase().slice(0, 2);
    if (geoSuggestions) geoSuggestions.innerHTML = "";
    clearFieldValidation("geo_code");
    updatePreview();
  }

  document.querySelectorAll(".geo-chip").forEach((chip) => {
    chip.addEventListener("click", () => pickGeo(chip.dataset.geoCode));
  });

  if (geoSuggestions && geoInput) {
    geoSuggestions.addEventListener("click", (event) => {
      const btn = event.target.closest(".combo-option");
      if (!btn?.dataset.geoCode) return;
      pickGeo(btn.dataset.geoCode);
    });

    geoInput.addEventListener("input", () => {
      const raw = geoInput.value.toUpperCase();
      if (raw.length <= 2) geoInput.value = raw;
      else geoInput.value = raw.slice(0, 2);
    });
  }

  if (offerSuggestions && hiddenOffer && offerInput) {
    offerSuggestions.addEventListener("click", (event) => {
      const btn = event.target.closest(".combo-option");
      if (!btn) return;
      hiddenOffer.value = btn.dataset.offerId || "";
      offerInput.value = `#${btn.dataset.offerId} · ${btn.dataset.label || ""}`;
      offerSuggestions.innerHTML = "";
      clearFieldValidation("offer_query");
      updatePreview();
    });
  }

  if (geoSuggestions || offerSuggestions) {
    document.addEventListener("click", (event) => {
      if (!event.target.closest(".combo-wrap--geo") && geoSuggestions) {
        geoSuggestions.innerHTML = "";
      }
      if (!event.target.closest(".combo-wrap--offer") && offerSuggestions) {
        offerSuggestions.innerHTML = "";
      }
    });
  }
}

function prepareCreatorFields() {
  const issues = validateCreatorFields();
  if (!issues.length) return null;
  applyCreatorValidation(issues);
  return issues[0].message;
}

function setCreatorLoading(active) {
  const panel = document.getElementById("creator-form-panel");
  const overlay = document.getElementById("creator-loading");
  const btn = document.getElementById("creator-submit-btn");
  const cancelBtn = panel?.querySelector("[data-modal-close]");
  if (active) {
    panel?.classList.add("modal-panel--busy");
    if (overlay) overlay.hidden = false;
    if (btn) {
      btn.disabled = true;
      btn.setAttribute("aria-busy", "true");
    }
    if (cancelBtn) cancelBtn.disabled = true;
  } else {
    panel?.classList.remove("modal-panel--busy");
    if (overlay) overlay.hidden = true;
    if (btn) {
      btn.disabled = false;
      btn.removeAttribute("aria-busy");
    }
    if (cancelBtn) cancelBtn.disabled = false;
  }
}

function legkoSubmitCreator() {
  const form = document.getElementById("creator-form");
  const err = prepareCreatorFields();
  if (err) return;
  if (!form || typeof htmx === "undefined") {
    applyCreatorValidation([
      {
        field: "campaign_name",
        message: "Форма недоступна. Обновите страницу.",
      },
    ]);
    return;
  }
  setCreatorLoading(true);
  htmx
    .ajax("POST", "/campaigns/new", {
      source: form,
      target: "#app-modal-body",
      swap: "innerHTML",
    })
    .catch(() => {
      setCreatorLoading(false);
      applyCreatorValidation([
        {
          field: "campaign_name",
          message: "Ошибка сети. Попробуйте снова.",
        },
      ]);
    });
}

window.legkoSubmitCreator = legkoSubmitCreator;

document.addEventListener("DOMContentLoaded", bindCreatorForm);