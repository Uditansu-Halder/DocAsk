const BACKEND_URL = "http://127.0.0.1:8000";

async function uploadPDF() {
    const fileInput = document.querySelector("#pdfFile");
    const statusElement = document.querySelector("#uploadStatus");

    if (!fileInput.files.length) {
        alert("Please select a PDF, image, DOCX,TXT or md file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    statusElement.textContent = "Uploading...";

    try {
        const response = await fetch(`${BACKEND_URL}/upload`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || data.message || "Upload failed.");
        }

        statusElement.textContent = `${data.message} (${data.filename})`;
        document.querySelector("#question").disabled = false;
        document.querySelector("#askButton").disabled = false;
        document.querySelector("#question").placeholder ="Ask something about your document...";
    } catch (error) {
        statusElement.textContent = error.message;
    }
}

let questionField = document.querySelector("#question");
questionField.addEventListener("keydown", (evt) => {
    if (evt.key === "Enter") {
        evt.preventDefault();
        askQuestion();
    }
});

function renderCitations(citations) {
    const citationsList = document.querySelector("#citations");
    const citationSummary = document.querySelector("#citationSummary");
    const citationPreview = document.querySelector("#citationPreview");

    citationsList.innerHTML = "";

    if (!citations.length) {
        citationSummary.textContent = "No citations yet.";
        citationPreview.textContent = "Select a citation to preview the relevant source excerpt.";
        return;
    }

    citationSummary.textContent = `${citations.length} citation${citations.length > 1 ? "s" : ""}`;

    citations.forEach((citation, index) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "citation-item";
        button.innerHTML = `
            <span class="citation-index">${index + 1}</span>
            <span class="citation-meta">${citation.type} • ${citation.location}</span>
        `;

        button.addEventListener("click", () => {
            citationPreview.innerHTML = `
                <strong>Citation ${index + 1}</strong>
                <p>${citation.preview || "No preview available."}</p>
            `;
        });

        citationsList.appendChild(button);
    });

    if (citations[0]) {
        citationPreview.innerHTML = `
            <strong>Citation 1</strong>
            <p>${citations[0].preview || "No preview available."}</p>
        `;
    }
}

async function askQuestion() {
    const question = questionField.value.trim();
    const answerElement = document.querySelector("#answer");

    if (!question) {
        answerElement.textContent = "Please enter a question.";
        return;
    }

    answerElement.textContent = "Thinking...";
    renderCitations([]);

    try {
        const response = await fetch(`${BACKEND_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Failed to get answer."
            );
        }

        answerElement.textContent = data.answer;
        renderCitations(data.citations || data.sources || []);
    } catch (error) {
        console.error("Ask Error:", error);

        answerElement.textContent =
            error.message || "Sorry, I couldn't generate an answer.";
        renderCitations([]);
    }
}