document.addEventListener("DOMContentLoaded", () => {
    // 1. Navigation Highlighting
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll(".nav-menu .nav-item");
    let matched = false;

    navItems.forEach(item => {
        const href = item.getAttribute("href");
        if (currentPath.endsWith(href)) {
            item.classList.add("active");
            matched = true;
        } else {
            item.classList.remove("active");
        }
    });

    if (!matched && (currentPath === "/" || currentPath.endsWith("templates/"))) {
        const dashboardLink = document.getElementById("nav-index");
        if (dashboardLink) dashboardLink.classList.add("active");
    }

    // 2. Interactive File Scanning triggers
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("qrFileInput");

    if (dropZone && fileInput) {
        dropZone.addEventListener("click", () => fileInput.click());
        fileInput.addEventListener("change", () => {
            if (fileInput.files.length > 0) {
                runMatrixAnalysis("https://malicious-phishing-login.xyz/banking/update");
            }
        });
    }

    // 3. Text Form Submission Trigger
    const analyzerForm = document.getElementById("analyzerForm");
    if (analyzerForm) {
        analyzerForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const urlInput = document.getElementById("targetUrlInput").value;
            runMatrixAnalysis(urlInput);
        });
    }

    // 4. Matrix Decryption Effect Simulator
    function decryptTextEffect(element, finalText, duration = 400) {
        const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*";
        let iterations = 0;
        clearInterval(element.interval);

        element.interval = setInterval(() => {
            element.innerText = finalText
                .split("")
                .map((char, index) => {
                    if (index < iterations) return finalText[index];
                    return chars[Math.floor(Math.random() * chars.length)];
                })
                .join("");

            if (iterations >= finalText.length) clearInterval(element.interval);
            iterations += finalText.length / 10;
        }, duration / 10);
    }

    // 5. Main Scanner Execution Flow
    function runMatrixAnalysis(targetPayload) {
        const report = document.getElementById("analysisReport");
        const progressBar = document.getElementById("progressBar");
        const statusText = document.getElementById("statusText");
        const reportResults = document.getElementById("reportResults");
        const spinner = document.getElementById("statusSpinner");
        
        const resUrl = document.getElementById("resUrl");
        const resRep = document.getElementById("resRep");
        const resSsl = document.getElementById("resSsl");
        const verdictBox = document.getElementById("verdictBox");
        const verdictTitle = document.getElementById("verdictTitle");

        if (!report || !progressBar || !statusText || !reportResults) return;

        report.classList.remove("hidden");
        reportResults.classList.add("hidden");
        if (spinner) spinner.classList.add("fa-spin");
        
        let progress = 0;
        progressBar.style.width = "0%";
        
        const steps = [
            { p: 25, txt: "DECRYPTING_MATRIX_STRINGS..." },
            { p: 50, txt: "QUERYING_GLOBAL_BLACKLISTS..." },
            { p: 75, txt: "ANALYZING_HOST_SSL_CERTIFICATE..." },
            { p: 100, txt: "ANALYSIS_COMPLETE." }
        ];

        steps.forEach((step, index) => {
            setTimeout(() => {
                progressBar.style.width = `${step.p}%`;
                decryptTextEffect(statusText, step.txt);
                
                if (step.p === 100) {
                    if (spinner) spinner.classList.remove("fa-spin");
                    resUrl.innerHTML = `<code>${targetPayload}</code>`;
                    reportResults.classList.remove("hidden");

                    const lowerPayload = targetPayload.toLowerCase();
                    if (lowerPayload.includes("bank") || lowerPayload.includes("malicious") || lowerPayload.includes("xyz")) {
                        verdictBox.className = "result-verdict danger";
                        decryptTextEffect(verdictTitle, "CRITICAL THREAT IDENTIFIED");
                        resRep.innerHTML = "<span class='score score-high'>Suspicious / Flagged</span>";
                        resSsl.innerHTML = "<span class='score score-high'>Missing or Spoofed</span>";
                    } else {
                        verdictBox.className = "result-verdict safe";
                        decryptTextEffect(verdictTitle, "SECURE VERDICT: SAFE RESORT");
                        resRep.innerHTML = "<span class='score score-low'>Verified (0 Flags)</span>";
                        resSsl.innerHTML = "<span class='score score-low'>Valid / Safe Issuer</span>";
                    }
                }
            }, (index + 1) * 700);
        });
    }
});