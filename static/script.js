fetch("/reset", { method: "POST" }).catch(() => {});

const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("input");
const btn = document.getElementById("btn");
const fileInput = document.getElementById("file-input");
const preview = document.getElementById("preview");
const attachBtn = document.querySelector(".attach-btn");

let pendingImages = [];
let visionEnabled = true;

fetch("/config")
    .then((r) => r.json())
    .then((cfg) => {
        visionEnabled = cfg.vision_enabled !== false;
        if (!visionEnabled && attachBtn) {
            attachBtn.style.display = "none";
            const hello = document.querySelector(".message.bot p");
            if (hello) {
                hello.textContent =
                    "¡Hola! Soy el asistente de reglas de Riftbound. Preguntame por nombre de carta (Defy, Hidden Blade) o por número (OGN-045). En esta versión publicada no se adjuntan fotos.";
            }
        }
    })
    .catch(() => {});

let pendingImages = [];

const loadingMessages = [
    "Pensando...",
    "Consultando el grimorio...",
    "Canalizando runas...",
    "Revisando el reglamento...",
    "Inventando reglas nuevas... mentira",
    "Preguntandole al Head Judge...",
    "Shuffleando el Rune Deck...",
    "Buscando en el Rift...",
    "Leyendo la letra chica...",
    "Haciendo DAMAYC...",
    "Resolviendo la cadena...",
    "Pasando prioridad...",
    "Pagando costos de poder...",
    "Exhaust, tap, listo...",
    "Checkeando interacciones...",
];

const statusLabels = {
    searching: "Buscando reglas y cartas...",
    draft: "Generando respuesta...",
    draft_retry: "Reintentando con más contexto...",
    verify: "Verificando ruling...",
};

function showLoading() {
    const div = document.createElement("div");
    div.className = "loading";
    div.id = "loading-indicator";

    const spinner = document.createElement("div");
    spinner.className = "spinner";
    div.appendChild(spinner);

    const text = document.createElement("span");
    text.className = "loading-text";
    text.textContent = loadingMessages[0];
    div.appendChild(text);

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;

    let idx = 0;
    const interval = setInterval(() => {
        idx = (idx + 1) % loadingMessages.length;
        // Solo rotar si no hay un status fijo del servidor
        const el = document.getElementById("loading-indicator");
        if (el && !el.dataset.serverStatus) {
            text.textContent = loadingMessages[idx];
        }
        chat.scrollTop = chat.scrollHeight;
    }, 3000);

    return interval;
}

function setLoadingStatus(status) {
    const el = document.getElementById("loading-indicator");
    if (!el) return;
    const label = statusLabels[status];
    if (label) {
        el.dataset.serverStatus = "1";
        const text = el.querySelector(".loading-text");
        if (text) text.textContent = label;
        chat.scrollTop = chat.scrollHeight;
    }
}

function hideLoading(interval) {
    clearInterval(interval);
    const el = document.getElementById("loading-indicator");
    if (el) el.remove();
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

function renderBotMarkdown(text) {
    let html = escapeHtml(text);
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/^#{1,3}\s+(.+)$/gm, "<strong>$1</strong>");
    return html;
}

function addMessage(text, type, sources, imageUrls, ruling) {
    const div = document.createElement("div");
    div.className = `message ${type}`;

    if (imageUrls && imageUrls.length > 0) {
        for (const url of imageUrls) {
            const img = document.createElement("img");
            img.src = url;
            div.appendChild(img);
        }
    }

    if (type === "bot" && ruling?.verdict) {
        const summary = document.createElement("div");
        summary.className = "ruling-summary";

        const verdict = document.createElement("span");
        verdict.className = `verdict verdict-${ruling.verdict.toLowerCase()}`;
        const verdictLabels = {
            INFORMATIVO: "Información",
            NO_RESUELTO: "No resuelto",
            RESUELTO: "Resuelto",
        };
        verdict.textContent =
            verdictLabels[ruling.verdict] || `Veredicto: ${ruling.verdict}`;
        summary.appendChild(verdict);

        const confidence = document.createElement("span");
        confidence.className = `confidence confidence-${(ruling.confidence || "BAJA").toLowerCase()}`;
        confidence.textContent = `Confianza ${ruling.confidence || "BAJA"}`;
        summary.appendChild(confidence);
        div.appendChild(summary);
    }

    const p = document.createElement("p");
    if (type === "bot") {
        p.innerHTML = renderBotMarkdown(text);
    } else {
        p.textContent = text;
    }
    div.appendChild(p);

    if (type === "bot" && ruling?.citations?.length > 0) {
        const evidence = document.createElement("div");
        evidence.className = "evidence";

        const title = document.createElement("div");
        title.className = "evidence-title";
        title.textContent = "Evidencia";
        evidence.appendChild(title);

        for (const citation of ruling.citations) {
            const item = document.createElement("details");
            item.className = "citation";

            const heading = document.createElement("summary");
            heading.textContent = `${citation.title} · ${citation.source}`;
            item.appendChild(heading);

            const quote = document.createElement("p");
            quote.textContent = citation.text;
            item.appendChild(quote);
            evidence.appendChild(item);
        }
        div.appendChild(evidence);
    } else if (sources && sources.length > 0) {
        const s = document.createElement("div");
        s.className = "sources";
        s.textContent = "Fuentes: " + sources.join(", ");
        div.appendChild(s);
    }

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function addImageToPreview(file) {
    pendingImages.push(file);
    const thumb = document.createElement("div");
    thumb.className = "thumb";

    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    thumb.appendChild(img);

    const removeBtn = document.createElement("button");
    removeBtn.className = "remove";
    removeBtn.textContent = "\u00d7";
    removeBtn.addEventListener("click", () => {
        const idx = pendingImages.indexOf(file);
        if (idx > -1) pendingImages.splice(idx, 1);
        thumb.remove();
    });
    thumb.appendChild(removeBtn);

    preview.appendChild(thumb);
}

function clearPreview() {
    pendingImages = [];
    preview.innerHTML = "";
}

// File input
fileInput.addEventListener("change", (e) => {
    if (!visionEnabled) return;
    for (const file of e.target.files) {
        addImageToPreview(file);
    }
    fileInput.value = "";
});

// Ctrl+V paste
document.addEventListener("paste", (e) => {
    if (!visionEnabled) return;
    const items = e.clipboardData?.items;
    if (!items) return;
    for (const item of items) {
        if (item.type.startsWith("image/")) {
            e.preventDefault();
            const file = item.getAsFile();
            if (file) addImageToPreview(file);
        }
    }
});

// Auto-resize textarea
input.addEventListener("input", () => {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 150) + "px";
});

// Enter envía, Shift+Enter nueva línea
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        form.requestSubmit();
    }
});

// Submit
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = input.value.trim();
    if (!query && pendingImages.length === 0) return;

    const imageUrls = pendingImages.map((f) => URL.createObjectURL(f));
    addMessage(query || "(imagen adjunta)", "user", null, imageUrls);

    const formData = new FormData();
    formData.append("query", query || "\u00bfQu\u00e9 hace esta carta?");
    for (const img of pendingImages) {
        formData.append("images", img);
    }

    input.value = "";
    input.style.height = "auto";
    clearPreview();
    btn.disabled = true;

    const loadingInterval = showLoading();

    try {
        const res = await fetch("/ask-stream", {
            method: "POST",
            body: formData,
        });
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let data = null;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            // Parsear eventos SSE del buffer
            const parts = buffer.split("\n\n");
            buffer = parts.pop(); // lo que queda incompleto
            for (const part of parts) {
                const eventMatch = part.match(/^event:\s*(.+)$/m);
                const dataMatch = part.match(/^data:\s*(.*)$/m);
                if (!eventMatch) continue;
                const eventName = eventMatch[1].trim();
                const eventData = dataMatch ? dataMatch[1].trim() : "";

                if (eventName === "status") {
                    setLoadingStatus(eventData);
                } else if (eventName === "result") {
                    data = JSON.parse(eventData);
                }
            }
        }

        hideLoading(loadingInterval);
        if (data) {
            addMessage(data.answer, "bot", data.sources, null, {
                verdict: data.verdict,
                confidence: data.confidence,
                citations: data.citations,
                missingInfo: data.missing_info,
            });
        } else {
            addMessage("No se recibió respuesta del servidor.", "bot");
        }
    } catch (err) {
        hideLoading(loadingInterval);
        addMessage("Error al conectar con el servidor.", "bot");
    }

    btn.disabled = false;
    input.focus();
});
