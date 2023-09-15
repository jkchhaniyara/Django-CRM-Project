function fetchDataAndUpdateTable2() {
    showLoading();
    fetch('record-ajax/1/') // Replace with your actual URL for data fetching
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#data-table-2 tbody');
            tableBody.innerHTML = ''; // Clear existing rows
            var i = 1;
            data.forEach(item => {
                const createdAtDateTime = new Date(item.created_at);
                const formattedDateTime = createdAtDateTime.toLocaleString(); // Formats both date and time
                const newRow = document.createElement('tr');
                newRow.innerHTML = `<td><a href="${item.id}">${i++}</a></td><td>${item.first_name}</td><td>${item.last_name}</td><td>${item.email}</td><td>${item.phone}</td><td>${item.city}</td><td>${item.state}</td><td>${formattedDateTime}</td>`;
                tableBody.appendChild(newRow);
            });
            hideLoading();
        })
        .catch(error => {
            console.error('Fetch error:', error);
            hideLoading();
        });
}