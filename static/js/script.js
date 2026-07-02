document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll(".nav-menu .nav-item");
    let matched = false;

    navItems.forEach(item => {
        const href = item.getAttribute("href");
        if (href && currentPath.endsWith(href)) {
            item.classList.add("active");
            matched = true;
        } else {
            item.classList.remove("active");
        }
    });

    if (!matched) {
        const dashboardLink = document.getElementById("nav-index");
        if (dashboardLink) dashboardLink.classList.add("active");
    }

    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("qrFileInput");
    const analyzerForm = document.getElementById("analyzerForm");

    if (dropZone && fileInput) {
        dropZone.addEventListener("click", () => fileInput.click());

        dropZone.addEventListener("dragover", (event) => {
            event.preventDefault();
            dropZone.classList.add("dragover");
        });

        dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));

        dropZone.addEventListener("drop", (event) => {
            event.preventDefault();
            dropZone.classList.remove("dragover");
            const file = event.dataTransfer.files[0];
            if (file) {
                handleFileUpload(file);
            }
        });

        fileInput.addEventListener("change", () => {
            if (fileInput.files.length > 0) {
                handleFileUpload(fileInput.files[0]);
            }
        });
    }

    if (analyzerForm) {
        analyzerForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const urlInput = document.getElementById("targetUrlInput").value.trim();
            if (urlInput) {
                handleTextAnalysis(urlInput);
            }
        });
    }

    function escapeHtml(value) {
        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
    }

    function setStatus(text) {
        const statusText = document.getElementById("statusText");
        if (statusText) {
            statusText.textContent = text;
        }
    }

    function showReport() {
        const report = document.getElementById("analysisReport");
        if (report) {
            report.classList.remove("hidden");
        }
    }

    function displayResult(result) {
        const reportResults = document.getElementById("reportResults");
        const verdictBox = document.getElementById("verdictBox");
        const verdictTitle = document.getElementById("verdictTitle");
        const verdictDescription = document.getElementById("verdictDescription");
        const resUrl = document.getElementById("resUrl");
        const resRep = document.getElementById("resRep");
        const resSsl = document.getElementById("resSsl");

        if (!reportResults || !verdictBox || !verdictTitle || !verdictDescription || !resUrl || !resRep || !resSsl) {
            return;
        }

        const verdict = result.verdict || "Safe";
        const score = Number.isFinite(result.score) ? result.score : 0;
        const transport = (result.analysis && result.analysis.transport) ? result.analysis.transport : "Unknown";

        verdictTitle.textContent = verdict === "Malicious" ? "CRITICAL THREAT IDENTIFIED" : verdict === "Suspicious" ? "Potential Threat Detected" : "SECURE VERDICT: SAFE PAYLOAD";
        verdictDescription.textContent = (result.analysis && result.analysis.notes) ? result.analysis.notes.join(" ") : "No suspicious traits were detected.";
        resUrl.innerHTML = `<code>${escapeHtml(result.payload)}</code>`;
        resRep.innerHTML = `<span class='score ${verdict === "Malicious" ? "score-high" : verdict === "Suspicious" ? "score-mid" : "score-low"}'>${verdict} (${score}/100)</span>`;
        resSsl.innerHTML = `<span class='score ${transport === "HTTPS" ? "score-low" : "score-high"}'>${escapeHtml(transport)}</span>`;

        verdictBox.className = `result-verdict ${verdict === "Malicious" ? "danger" : verdict === "Suspicious" ? "warning" : "safe"}`;
        reportResults.classList.remove("hidden");
    }

    function runAnalysis(fetcher) {
        const progressBar = document.getElementById("progressBar");
        const spinner = document.getElementById("statusSpinner");
        const reportResults = document.getElementById("reportResults");

        if (!progressBar || !spinner || !reportResults) return;

        showReport();
        reportResults.classList.add("hidden");
        spinner.classList.add("fa-spin");
        progressBar.style.width = "0%";

        const stages = [
            { pct: 20, text: "VALIDATING PAYLOAD..." },
            { pct: 45, text: "INSPECTING THREAT MARKERS..." },
            { pct: 70, text: "ANALYZING TRANSPORT AND REDIRECTS..." },
            { pct: 95, text: "FINALIZING VERDICT..." }
        ];

        let stageIndex = 0;
        const timer = setInterval(() => {
            if (stageIndex >= stages.length) {
                clearInterval(timer);
                return;
            }
            const stage = stages[stageIndex];
            progressBar.style.width = `${stage.pct}%`;
            setStatus(stage.text);
            stageIndex += 1;
        }, 400);

        return fetcher()
            .then((response) => response.json())
            .then((json) => {
                clearInterval(timer);
                progressBar.style.width = "100%";
                spinner.classList.remove("fa-spin");
                setStatus("ANALYSIS COMPLETE.");

                if (!json.success) {
                    setStatus(json.message || "Analysis failed.");
                    return;
                }

                displayResult(json.result);
            })
            .catch((error) => {
                clearInterval(timer);
                spinner.classList.remove("fa-spin");
                progressBar.style.width = "100%";
                setStatus("Analysis failed.");
                console.error(error);
            });
    }

    function handleTextAnalysis(payload) {
        runAnalysis(() => fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ payload })
        }));
    }

    function handleFileUpload(file) {
        const formData = new FormData();
        formData.append("file", file);

        runAnalysis(() => fetch("/api/upload", {
            method: "POST",
            body: formData
        }));
    }
});
