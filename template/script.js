document.addEventListener("DOMContentLoaded", function () {
    function predictPC() {
        const budget = document.getElementById("budget").value;
        const use_case = document.getElementById("use_case").value;
        const category = document.getElementById("category").value;

        fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ budget: Number(budget), use_case, category })
        })
        .then(response => response.json())
        .then(data => {
            // Display the prediction result or error message in the <pre> tag
            const resultText = JSON.stringify(data, null, 2); // Pretty print JSON
            document.getElementById("result").innerText = resultText;
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }

    window.predictPC = predictPC;
});
