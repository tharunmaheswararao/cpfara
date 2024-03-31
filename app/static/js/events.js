let fromDateElement = document.getElementById("from-date");
let toDateElement = document.getElementById("to-date");
let fromDateValue;
let toDateValue;
let data;
let checkedCheckboxes;
let checkedValues = [];
let selectedValue = "";

const checkboxes = document.querySelectorAll('input[name="checkboxes"]');
const selectElement = document.getElementById("domain");


window.onload = function() {
    fromDateValue = fromDateElement.value;
    toDateValue = toDateElement.value;
    
    data = {
        fromDateValue,
        toDateValue,
        checkedValues,
        selectedValue,
    }
    eventsApi(data);
}

fromDateElement.addEventListener("change", () => {
    fromDateValue = fromDateElement.value;
    toDateValue = toDateElement.value;
    data = {
        fromDateValue,
        toDateValue,
        checkedValues,
        selectedValue,
    }
    eventsApi(data);
})

toDateElement.addEventListener("change", () => {
    fromDateValue = fromDateElement.value;
    toDateValue = toDateElement.value;
    data = {
        fromDateValue,
        toDateValue,
        checkedValues,
        selectedValue,
    }
    eventsApi(data);
})

checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        checkedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
        checkedValues = checkedCheckboxes.map(checkbox => checkbox.value);
        console.log(checkedValues);
        data = {
            fromDateValue,
            toDateValue,
            checkedValues,
            selectedValue,
        }
        eventsApi(data);
    });
});

selectElement.addEventListener("change", function() {
    selectedValue = this.value;
    data = {
        fromDateValue,
        toDateValue,
        checkedValues,
        selectedValue,
    }
    eventsApi(data);
});

function eventsApi(data) {
    
    fetch('/api/events/kr-events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
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
            let optionsList = data.domains;
            optionsList.forEach(function(option) {
                let optionElement = document.createElement("option");
                optionElement.value = option;
                optionElement.textContent = option;
                selectElement.appendChild(optionElement);
            });
        } else if (data.error) {
            alert('Error signing up: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}