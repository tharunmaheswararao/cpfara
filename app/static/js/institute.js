let instituteHeader = document.getElementsByClassName("institute-name-header")[0];
let fromDateElement = document.getElementById("from-date");
let toDateElement = document.getElementById("to-date");
let fromDateValue;
let toDateValue;
let instituteName;
let data;


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