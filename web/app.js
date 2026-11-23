"use strict";
const $ = (id) => document.getElementById(id);
let busy = false;
let revision = -1;
let latest = null;
async function send(action, payload = {}) {
  if (busy) return;
  try {
    const response = await fetch("/api/actions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, payload }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error);
    busy = true;
    updateButtons();
    $("status").textContent = "Working…";
  } catch (error) {
    $("status").textContent = error.message;
  }
}
function updateButtons() {
  document.querySelectorAll("button[data-action]").forEach((button) => {
    button.disabled = busy;
  });
}
async function poll() {
  try {
    const response = await fetch("/api/state");
    if (!response.ok)
      throw new Error(
        "Could not reach the app. Open the address printed in its terminal.",
      );
    const state = await response.json();
    busy = state.busy;
    updateButtons();
    showInfo(state.application);
    if (revision !== state.revision) {
      revision = state.revision;
      if (state.error) $("status").textContent = state.error;
      else if (state.result) {
        latest = state.result;
        $("status").textContent =
          latest.error || (latest.kind === "error" ? latest.message : "Ready");
        render(latest);
      } else $("status").textContent = "Ready";
    }
    if (busy) $("status").textContent = "Working…";
  } catch (error) {
    $("status").textContent = error.message;
  } finally {
    setTimeout(poll, 750);
  }
}
function showInfo(app) {
  $("connection").textContent = "Local folder";
  $("folder").textContent = app.folder;
}
function render(r) {
  if (r.error) return;
  if (r.files) {
    $("files").replaceChildren();
    for (const file of r.files) {
      const label = document.createElement("label");
      label.className = "inline";
      const box = document.createElement("input");
      box.type = "checkbox";
      box.value = file.name;
      label.append(
        box,
        document.createTextNode(
          file.name + " · " + Math.ceil(file.bytes / 1024) + " KB",
        ),
      );
      $("files").append(label);
    }
    $("output").textContent = r.total + " files found. Showing up to 200.";
  } else if (r.outcomes) {
    for (const outcome of r.outcomes) {
      if (outcome.status === "moved") {
        for (const box of document.querySelectorAll("#files input")) {
          if (box.value === outcome.file) box.parentElement.remove();
        }
      }
    }
    $("output").textContent = r.outcomes
      .map(
        (o) =>
          o.file + " — " + o.status + "\n" + (o.destination || o.message || ""),
      )
      .join("\n\n");
  }
}
$("scan").addEventListener("click", () => send("scan"));
$("sort").addEventListener("click", () => {
  const names = Array.from(
    document.querySelectorAll("#files input:checked"),
    (box) => box.value,
  );
  if (!names.length) {
    $("status").textContent = "Select files to sort.";
    return;
  }
  if (
    confirm("Move " + names.length + " selected files into category folders?")
  )
    send("sort", { names });
});
poll();
