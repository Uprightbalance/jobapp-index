async function submitForm(event) {
  event.preventDefault(); // stop page reload

  const statusDiv = document.getElementById("status");
  statusDiv.innerText = "Submitting application...";

  const payload = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    position: document.getElementById("position").value
  };

  try {
    const response = await fetch(
      "https://m6o5e6i67i.execute-api.us-east-1.amazonaws.com/prod/submit",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Submission failed");
    }

    statusDiv.style.color = "green";
    statusDiv.innerText = "Application submitted successfully!";
    console.log("Response:", data);

  } catch (error) {
    statusDiv.style.color = "red";
    statusDiv.innerText = "Error submitting application.";
    console.error("Error:", error);
  }
}
