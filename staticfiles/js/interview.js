document.getElementById('search-button').addEventListener('click', () => {
    const query = document.getElementById('applicant-search-input').value;
    const url = `${searchApplicantUrl}?search_txt=${encodeURIComponent(query)}`;

    const requestUserSearch = new XMLHttpRequest();
    requestUserSearch.open('GET', url, true);
    requestUserSearch.onreadystatechange = () => {
        if (requestUserSearch.readyState === XMLHttpRequest.DONE) {
            if (requestUserSearch.status < 400) {
                const data = JSON.parse(requestUserSearch.responseText);
                const userSearchResults = document.getElementById('applicant-search-results');
                userSearchResults.innerHTML = '';
                data.forEach(user => {
                    const li = document.createElement('li');
                    li.textContent = user.name;
                    li.addEventListener('click', () => {
                        window.location.href = `/applicants/document/profile/${user.id}`;
                    });
                    userSearchResults.appendChild(li);
                });
            }
        }
    };
    requestUserSearch.send();
});




const draggables = document.querySelectorAll('.each_applicant');
const droppables = document.querySelectorAll('.scroll_section');
var applicant_id = '0';
var status_zone_id = '0';

draggables.forEach((applicant) => {
    applicant.addEventListener("dragstart", () => {
        applicant.classList.add("is-dragging");
    });
    applicant.addEventListener("dragend", () => {
        applicant.classList.remove("is-dragging");

        statusUpdate(applicant_id, status_zone_id);
    });
});

droppables.forEach((status_zone) => {
    status_zone.addEventListener("dragover", (e) => {
        e.preventDefault();

        const bottomApplicant = insertAboveApplicant(status_zone, e.clientY);
        const curApplicant = document.querySelector(".is-dragging");

        if (!bottomApplicant) {
            status_zone.appendChild(curApplicant);
        } else {
            status_zone.insertBefore(curApplicant, bottomApplicant);
        }
        applicant_id = curApplicant.id;
        status_zone_id = status_zone.id;
    });
});

const insertAboveApplicant = (status_zone, mouseY) => {
    const els = status_zone.querySelectorAll(".each_applicant:not(.is-dragging");

    let closestApplicant = null;
    let closestOffset = Number.NEGATIVE_INFINITY;

    els.forEach((applicant) => {
        const { top } = applicant.getBoundingClientRect();

        const offset = mouseY - top;

        if (offset < 0 && offset > closestOffset) {
            closestOffset = offset;
            closestApplicant = applicant;
        }
    });

    return closestApplicant;
}

function statusUpdate(applicant_id, status_zone_id) {
    const url = `interview/change_status/${status_zone_id}/${applicant_id}/`;
    
    const xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    updateStatus(applicant_id, status_zone_id)
    const data = {
        'applicant_id': applicant_id,
        'status_zone_id': status_zone_id
    }
    xhr.send(JSON.stringify(data));
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateStatus(applicant_id, status_zone_id) {
    const applicantElement = document.getElementById(applicant_id);

    applicantElement.classList.remove('scheduled', 'in_progress', 'completed');

    if (status_zone_id === '1') {
        applicantElement.classList.add('scheduled');
    } else if (status_zone_id === '2') {
        applicantElement.classList.add('in_progress');
    } else if (status_zone_id === '3') {
        applicantElement.classList.add('completed');
    }
}