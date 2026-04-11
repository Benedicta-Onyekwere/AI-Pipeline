let allMEPs = [];
let filteredMEPs = [];
let currentIndex = 0;

// Elements
const loadingEl = document.getElementById('loading');
const cardEl = document.getElementById('reviewer-card');
const counterEl = document.getElementById('counter');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const searchInput = document.getElementById('searchInput');

// Data Elements
const nameEl = document.getElementById('mep-name');
const committeeRoleEl = document.getElementById('mep-committee-role');
const countryEl = document.getElementById('mep-country');
const politicalGroupEl = document.getElementById('mep-political-group');
const nationalPartyEl = document.getElementById('mep-national-party');
const roleEl = document.getElementById('mep-role');
const profileLinkEl = document.getElementById('link-profile');

// Social Links
const fbLink = document.getElementById('link-facebook');
const twLink = document.getElementById('link-twitter');
const instLink = document.getElementById('link-instagram');

// Load Data
async function loadData() {
    try {
        const response = await fetch('mep_details.csv');
        const csvText = await response.text();
        
        Papa.parse(csvText, {
            header: true,
            skipEmptyLines: true,
            complete: function(results) {
                allMEPs = results.data;
                filteredMEPs = [...allMEPs];
                initReviewer();
            }
        });
    } catch (error) {
        console.error('Error loading CSV:', error);
        loadingEl.innerHTML = '<p style="color: red;">Failed to load data. Please ensure mep_details.csv exists.</p>';
    }
}

function initReviewer() {
    loadingEl.classList.add('hidden');
    cardEl.classList.remove('hidden');
    updateCard();
}

function updateCard() {
    if (filteredMEPs.length === 0) {
        showEmptyState();
        return;
    }

    const mep = filteredMEPs[currentIndex];
    
    // Fill text
    nameEl.textContent = mep.Name;
    committeeRoleEl.textContent = mep['Committee Role'];
    countryEl.textContent = mep.Country;
    politicalGroupEl.textContent = mep['Political Group'];
    nationalPartyEl.textContent = mep['National Party'];
    roleEl.textContent = mep.Role;
    profileLinkEl.href = mep['Profile URL'];

    // Handle Social Links
    handleSocialLink(fbLink, mep.Facebook);
    handleSocialLink(twLink, mep.Twitter);
    handleSocialLink(instLink, mep.Instagram);

    // Update Counter & Buttons
    counterEl.textContent = `${currentIndex + 1} of ${filteredMEPs.length}`;
    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex === filteredMEPs.length - 1;
}

function handleSocialLink(element, value) {
    if (value && value !== 'Not found' && value !== 'Error') {
        element.href = value;
        element.classList.remove('hidden');
    } else {
        element.classList.add('hidden');
    }
}

function showEmptyState() {
    nameEl.textContent = "No results found";
    committeeRoleEl.textContent = "";
    countryEl.textContent = "-";
    politicalGroupEl.textContent = "-";
    nationalPartyEl.textContent = "-";
    roleEl.textContent = "-";
    counterEl.textContent = "0 of 0";
    prevBtn.disabled = true;
    nextBtn.disabled = true;
}

// Navigation
prevBtn.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
        updateCard();
    }
});

nextBtn.addEventListener('click', () => {
    if (currentIndex < filteredMEPs.length - 1) {
        currentIndex++;
        updateCard();
    }
});

// Search
searchInput.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    filteredMEPs = allMEPs.filter(mep => 
        mep.Name.toLowerCase().includes(term) || 
        mep.Country.toLowerCase().includes(term) ||
        mep['National Party'].toLowerCase().includes(term)
    );
    currentIndex = 0;
    updateCard();
});

// Start
loadData();
