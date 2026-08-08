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

let questionField=document.querySelector("#question");
questionField.addEventListener("keydown", (evt)=>{
    if(evt.key==="Enter"){
        evt.preventDefault();
        askQuestion();
    }
});

async function askQuestion() {
    const question = questionField.value.trim();
    const answerElement = document.querySelector("#answer");

    if (!question) {
        answerElement.textContent = "Please enter a question.";
        return;
    }

    answerElement.textContent = "Thinking...";

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

        // Display the answer
        answerElement.textContent = data.answer;

    } catch (error) {

        console.error("Ask Error:", error);

        answerElement.textContent =
            error.message || "Sorry, I couldn't generate an answer.";
    }
}