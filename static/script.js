const citizenModal = document.getElementById('citizenModal');
const adminModal = document.getElementById('adminModal');

const landingPage = document.getElementById('landingPage');
const dashboardSection = document.getElementById('dashboardSection');
const navAuthBtns = document.getElementById('navAuthBtns');

function openCitizenModal() {
    citizenModal.classList.add('active');
    resetForm();
}

function openAdminModal() {
    adminModal.classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

document.getElementById('citizenLoginBtn').addEventListener('click', openCitizenModal);
document.getElementById('adminLoginBtn').addEventListener('click', openAdminModal);

// Form Validation & OTP Send
function sendOTP() {
    const name = document.getElementById('regName').value.trim();
    const mobile = document.getElementById('regMobile').value.trim();
    const idNumber = document.getElementById('regIdNumber').value.trim();

    if (!name) {
        alert('Please enter your Full Name.');
        return;
    }
    if (mobile.length !== 10 || isNaN(mobile)) {
        alert('Please enter a valid 10-digit Mobile Number.');
        return;
    }
    if (idNumber.length !== 12 || isNaN(idNumber)) {
        alert('Please enter a valid 12-digit ID Number.');
        return;
    }

    document.getElementById('sentNumber').innerText = "+91 " + mobile;
    document.getElementById('otpStep1').style.display = 'none';
    document.getElementById('otpStep2').style.display = 'block';
}

// Auto move input focus for OTP
function moveNext(elem, index) {
    if (elem.value.length === 1 && index < 4) {
        document.querySelectorAll('.otp-input')[index].focus();
    }
}

// Verify OTP and populate user details in dashboard
function verifyOTPAndLogin() {
    const inputs = document.querySelectorAll('.otp-input');
    let otpVal = "";
    inputs.forEach(input => otpVal += input.value);

    if (otpVal.length === 4) {
        closeModal('citizenModal');

        const name = document.getElementById('regName').value;
        const mobile = document.getElementById('regMobile').value;

        // Set dynamic details in User Dashboard
        document.getElementById('dispUserName').innerText = name;
        document.getElementById('dispUserMobile').innerText = mobile;

        // Show Dashboard
        landingPage.style.display = 'none';
        dashboardSection.style.display = 'block';

        navAuthBtns.innerHTML = `
            <button class="btn btn-outline"><i class="fa-solid fa-user-check"></i> ${name}</button>
            <button class="btn btn-primary" onclick="logoutUser()"><i class="fa-solid fa-right-from-bracket"></i> Logout</button>
        `;
    } else {
        alert('Please enter a valid 4-digit OTP.');
    }
}

function handleAdminLogin(event) {
    event.preventDefault();
    const badgeId = document.getElementById('adminId').value;
    alert(`Officer ${badgeId} authenticated successfully. (Admin Dashboard simulation)`);
    closeModal('adminModal');
}

function logoutUser() {
    dashboardSection.style.display = 'none';
    landingPage.style.display = 'block';
    navAuthBtns.innerHTML = `
        <button class="btn btn-outline" id="citizenLoginBtn" onclick="openCitizenModal()"><i class="fa-regular fa-user"></i> Citizen Registration / Login</button>
        <button class="btn btn-primary" id="adminLoginBtn" onclick="openAdminModal()"><i class="fa-solid fa-user-shield"></i> Admin Login</button>
    `;
    // Re-bind listeners
    document.getElementById('citizenLoginBtn').addEventListener('click', openCitizenModal);
    document.getElementById('adminLoginBtn').addEventListener('click', openAdminModal);
}

function showLandingPage() {
    dashboardSection.style.display = 'none';
    landingPage.style.display = 'block';
}

function resetForm() {
    document.getElementById('otpStep1').style.display = 'block';
    document.getElementById('otpStep2').style.display = 'none';
    document.getElementById('regName').value = '';
    document.getElementById('regMobile').value = '';
    document.getElementById('regIdNumber').value = '';
    document.querySelectorAll('.otp-input').forEach(input => input.value = '');
}

window.addEventListener('click', function(event) {
    if (event.target === citizenModal) closeModal('citizenModal');
    if (event.target === adminModal) closeModal('adminModal');
});