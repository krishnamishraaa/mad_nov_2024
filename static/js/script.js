document
  .getElementById("campaignForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const data = {
      name: document.getElementById("name").value,
      description: document.getElementById("description").value,
      start_date: document.getElementById("start_date").value,
      end_date: document.getElementById("end_date").value,
      budget: document.getElementById("budget").value,
      visibility: document.getElementById("visibility").value,
      goals: document.getElementById("goals").value,
    };

    fetch("/api/campaign", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        loadCampaigns(); // Load campaigns after creating one
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

// Function to load campaigns from the API
function loadCampaigns() {
  fetch("/api/campaign")
    .then((response) => response.json())
    .then((data) => {
      const campaignsDiv = document.getElementById("campaigns");
      campaignsDiv.innerHTML = "<h2>Campaigns</h2>"; // Clear previous campaigns
      data.forEach((campaign) => {
        const campaignElement = document.createElement("div");
        campaignElement.innerText = `ID: ${campaign.campaign_id}, Name: ${campaign.name}`;
        campaignsDiv.appendChild(campaignElement);
      });
    });
}

// Load campaigns on page load
window.onload = loadCampaigns;
