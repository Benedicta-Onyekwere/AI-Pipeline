// --- VARIABLES ---
let allMEPs = [];
let filteredMEPs = [];

// Elements
const tableBody = document.getElementById('mepTableBody');
const loadingEl = document.getElementById('loading');
const searchInput = document.getElementById('searchInput');
const exportBtn = document.getElementById('exportBtn');

// --- LOAD MEP DATA ---
async function loadData() {
    try {
        const response = await fetch('mep_details.csv');
        const csvText = await response.text();
        
        Papa.parse(csvText, {
            header: true,
            skipEmptyLines: true,
            complete: function(results) {
                // Add default status
                allMEPs = results.data.map(mep => ({
                    ...mep,
                    ReviewStatus: 'Pending'
                }));
                filteredMEPs = [...allMEPs];
                renderTable();
                loadingEl.style.display = 'none';
            }
        });
    } catch (error) {
        console.error('Error loading CSV:', error);
        loadingEl.innerHTML = '<p style="color: red;">Error: Could not find "mep_details.csv".</p>';
    }
}

// --- RENDER TABLE ---
function renderTable() {
    tableBody.innerHTML = '';
    
    filteredMEPs.forEach((mep, index) => {
        const row = document.createElement('tr');
        
        // 1. MEP Info Columns
        ['Name', 'Country', 'Political Group', 'National Party', 'Committee Role', 'Role'].forEach(key => {
            const cell = document.createElement('td');
            cell.textContent = mep[key] || '-';
            row.appendChild(cell);
        });

        // 2. Social Links Column
        const socialCell = document.createElement('td');
        const links = [];
        if (mep.Facebook && mep.Facebook !== 'Not found') links.push(`<a href="${mep.Facebook}" target="_blank">FB</a>`);
        if (mep.Twitter && mep.Twitter !== 'Not found') links.push(`<a href="${mep.Twitter}" target="_blank">TW</a>`);
        if (mep.Instagram && mep.Instagram !== 'Not found') links.push(`<a href="${mep.Instagram}" target="_blank">IG</a>`);
        socialCell.innerHTML = links.join(' | ') || '-';
        row.appendChild(socialCell);

        // 3. Status Column (Now before Actions)
        const statusCell = document.createElement('td');
        statusCell.textContent = mep.ReviewStatus;
        statusCell.className = `status-${mep.ReviewStatus.toLowerCase()}`;
        row.appendChild(statusCell);

        // 4. Actions Column (Using Symbols)
        const actionCell = document.createElement('td');
        
        const approveBtn = document.createElement('button');
        approveBtn.innerHTML = '✔'; // Symbol for approve
        approveBtn.className = 'btn-approve';
        approveBtn.title = 'Approve';
        approveBtn.onclick = () => updateStatus(index, 'Approved');
        
        const rejectBtn = document.createElement('button');
        rejectBtn.innerHTML = '✖'; // Symbol for reject
        rejectBtn.className = 'btn-reject';
        rejectBtn.title = 'Reject';
        rejectBtn.onclick = () => updateStatus(index, 'Rejected');

        actionCell.appendChild(approveBtn);
        actionCell.appendChild(rejectBtn);
        row.appendChild(actionCell);

        tableBody.appendChild(row);
    });
}

// --- UPDATE STATUS ---
function updateStatus(filteredIndex, newStatus) {
    const mep = filteredMEPs[filteredIndex];
    const originalMep = allMEPs.find(m => m.Name === mep.Name && m['Profile URL'] === mep['Profile URL']);
    if (originalMep) {
        originalMep.ReviewStatus = newStatus;
        renderTable();
    }
}

// --- SEARCH ---
searchInput.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    filteredMEPs = allMEPs.filter(mep => 
        mep.Name.toLowerCase().includes(term) || 
        mep.Country.toLowerCase().includes(term) ||
        mep['National Party'].toLowerCase().includes(term)
    );
    renderTable();
});

// --- EXPORT ---
exportBtn.addEventListener('click', () => {
    const approved = allMEPs.filter(m => m.ReviewStatus === 'Approved');
    const csv = Papa.unparse(approved);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'approved_meps.csv');
    link.click();
});

loadData();
