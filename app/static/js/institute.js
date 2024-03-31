let instituteHeader = document.getElementsByClassName("institute-name-header")[0];
let fromDateElement = document.getElementById("from-date");
let toDateElement = document.getElementById("to-date");
let fromDateValue;
let toDateValue;
let instituteName;
let data;
let events_data = [];

const downloadBtn = document.getElementById("download-btn");

window.onload = function() {
    instituteName = window.location.href.split('/');
    instituteName = instituteName[instituteName.length - 1];
    fromDateValue = fromDateElement.value;
    toDateValue = toDateElement.value;
    data = {
        fromDateValue,
        toDateValue,
    }

    instituteHeader.innerText = instituteName + " Events";
    institutionApi(data);
}

fromDateElement.addEventListener("change", () => {
    fromDateValue = fromDateElement.value;
    toDateValue = toDateElement.value;
    data = {
        fromDateValue,
        toDateValue,
    }
    institutionApi(data);
})

toDateElement.addEventListener("change", () => {
    fromDateValue = fromDateElement.value;
    toDateValue = toDateElement.value;
    data = {
        fromDateValue,
        toDateValue,
    }
    institutionApi(data);
})

function downloadExcel(filename) {
    try {
        $('#data-table').table2excel({
            exclude: ".no-export",
            filename: filename + ".xls",
            fileext: ".xls",
            exclude_links: true,
            exclude_inputs: true
        });
    } catch (e) {
        console.log(e);
    }
}

function institutionApi(data) {
    instituteName = window.location.href.split('/');
    instituteName = instituteName[instituteName.length - 1];
    
    fetch('/api/institute/'+instituteName+'-events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // console.log(data.events_data);
            events_data = data.events_data;
            const keys = Object.keys(data.events_data);
            const eventsContainer = document.getElementById("events-list-cards-container");
            eventsContainer.innerHTML = '';
            keys.forEach((index) => {
                const rowData = data.events_data[index];
                console.log(rowData);
                const row = document.createElement("div");
                row.innerHTML = `
                    <div class="events-card-container">
                        <div class="event-date-header">
                            <h2>EVENT DATE : <br/>${rowData[0]}</h2>
                        </div>
                        <div class="event-description-container">
                            <div class="event-description">
                                <h2>EVENT NAME : <br/>${rowData[1]}</h2>
                            </div>
                        </div>
                    </div>
                `;
                eventsContainer.appendChild(row);
            })
        } else if (data.error) {
            alert('Error signing up: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}


downloadBtn.style.cursor = "pointer";

function arrayToCSV(dataArray) {
    const headers = ["Event Date", "Event Description"];
    const csvRows = [headers.join(",")];
    for (const row of dataArray) {
        const rowStr = row.map(cell => `"${cell}"`).join(",");
        csvRows.push(rowStr);
    }
    return csvRows.join("\n");
}
  
  // Function to download CSV file
function downloadCSV(dataArray, fileName) {
    const csvContent = arrayToCSV(dataArray);
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8" });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

downloadBtn.onclick = function() {
    downloadCSV(events_data, `${window.location.href.split('/').pop() + "-" + fromDateValue + "-to-" + toDateValue}.csv`);
}