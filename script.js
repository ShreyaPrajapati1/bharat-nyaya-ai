function checkStatus() {
    let firNumber = document.getElementById("firNumber").value;
    let result = document.getElementById("result");

    if (firNumber === "FIR-001") {
        result.innerHTML = `
        <div class="status-card">
            <h2>FIR Details</h2>
            <p><b>FIR Number:</b> FIR-001</p>
            <p><b>Status:</b> ${localStorage.getItem("FIR-001-status") || "Under Verification"}</p>
            <p><b>Police Station:</b> Gorakhpur</p>
            <p><b>Complaint Type:</b> Theft</p>
<p><b>Incident Date:</b> 28 September 2026</p>
<p><b>Complaint Description:</b> Mobile phone reported stolen near Gorakhpur Market.</p>

            <h3>Case Progress</h3>
            <p>✓ Complaint Submitted</p>
            <p>✓ AI Analysis Completed</p>
            <p>✓ User Verification Completed</p>
            <p>● Under Police Verification</p>
            <p>○ Case Investigation</p>
            <p>○ Case Closure</p>
        </div>`;
    }

    else if (firNumber === "FIR-002") {
        result.innerHTML = `
        <div class="status-card">
            <h2>FIR Details</h2>
            <p><b>FIR Number:</b> FIR-002</p>
            <p><b>Status:</b> Accepted</p>
            <p><b>Police Station:</b> Gorakhpur</p>
            <p><b>Complaint Type:</b> Online Fraud</p>
<p><b>Incident Date:</b> 25 September 2026</p>
<p><b>Complaint Description:</b> User reported an online transaction-related complaint.</p>
        </div>`;
    }

    else if (firNumber === "FIR-003") {
        result.innerHTML = `
        <div class="status-card">
            <h2>FIR Details</h2>
            <p><b>FIR Number:</b> FIR-003</p>
            <p><b>Status:</b> Case in Progress</p>
            <p><b>Police Station:</b> Gorakhpur</p>
            <p><b>Complaint Type:</b> Cyber Harassment</p>
<p><b>Incident Date:</b> 20 September 2026</p>
<p><b>Complaint Description:</b> User reported receiving threatening messages online.</p>
        </div>`;
    }

    else if (firNumber === "") {
        result.innerHTML = "<p>Please Enter FIR Number</p>";
    }

    else {
        result.innerHTML = "<p>Invalid FIR Number</p>";
    }
}


// Admin: Update FIR Status

function updateStatus() {
    let status = document.getElementById("status1");
    let selectedStatus = document.getElementById("statusSelect").value;

    status.innerHTML = selectedStatus;

    localStorage.setItem("FIR-001-status", selectedStatus);
}


// Admin: View FIR Details

function viewFIR(firNumber) {

    let details = document.getElementById("firDetails");

    if (firNumber === "FIR-001") {

        details.innerHTML = `
        <div class="status-card">
            <h2>FIR-001 Details</h2>

            <p><b>FIR Number:</b> FIR-001</p>
            <p><b>Status:</b> ${localStorage.getItem("FIR-001-status") || "Under Verification"}</p>
            <p><b>Police Station:</b> Gorakhpur</p>
            <p><b>Complaint Type:</b> Theft</p>
<p><b>Incident Date:</b> 28 September 2026</p>
<p><b>Complaint Description:</b> Mobile phone reported stolen near Gorakhpur Market.</p>

            <h3>Case Progress</h3>

            <p>✓ Complaint Submitted</p>
            <p>✓ AI Analysis Completed</p>
            <p>✓ User Verification Completed</p>
            <p>● Under Police Verification</p>
            <p>○ Case Investigation</p>
            <p>○ Case Closure</p>
        </div>`;
    }

    else if (firNumber === "FIR-002") {

        details.innerHTML = `
        <div class="status-card">
            <h2>FIR-002 Details</h2>

            <p><b>FIR Number:</b> FIR-002</p>
            <p><b>Status:</b> Accepted</p>
            <p><b>Police Station:</b> Gorakhpur</p>

            <h3>Case Progress</h3>

            <p>✓ Complaint Submitted</p>
            <p>✓ AI Analysis Completed</p>
            <p>✓ User Verification Completed</p>
            <p>✓ Police Verification</p>
            <p>● Case Investigation</p>
            <p>○ Case Closure</p>
        </div>`;
    }

    else if (firNumber === "FIR-003") {

        details.innerHTML = `
        <div class="status-card">
            <h2>FIR-003 Details</h2>

            <p><b>FIR Number:</b> FIR-003</p>
            <p><b>Status:</b> Case in Progress</p>
            <p><b>Police Station:</b> Gorakhpur</p>

            <h3>Case Progress</h3>

            <p>✓ Complaint Submitted</p>
            <p>✓ AI Analysis Completed</p>
            <p>✓ User Verification Completed</p>
            <p>✓ Police Verification</p>
            <p>● Case Investigation</p>
            <p>○ Case Closure</p>
        </div>`;
    }
}


// Go back to FIR Tracking page

function goToTracking() {
    window.location.href = "index.html";
}


// Open Google Maps

function openMap() {
    window.open(
        "https://www.google.com/maps/search/?api=1&query=Gorakhpur+Police+Station",
        "_blank"
    );
}