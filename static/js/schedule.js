const Update = (id) => {
    let spanUpdate = document.querySelector(`.spanUpdate${id}`);
    let spanSubmit = document.querySelector(`.spanSubmit${id}`);
    let spanUpdateCancel = document.querySelector(`.spanUpdateCancel${id}`);
    let selectDate = document.querySelector(`.selectDate${id}`);
    let selectTime = document.querySelector(`.selectTime${id}`);
  
    console.log(spanUpdate);
    spanUpdate.style.display = 'none';
    selectDate.style.display = 'inline-block';
    selectTime.style.display = 'inline-block';
    spanSubmit.style.display = 'inline-block';
    spanUpdateCancel.style.display = 'inline-block';
}

const UpdateCancel = (id) => {
    let spanUpdate = document.querySelector(`.spanUpdate${id}`);
    let spanSubmit = document.querySelector(`.spanSubmit${id}`);
    let spanUpdateCancel = document.querySelector(`.spanUpdateCancel${id}`);
    let selectDate = document.querySelector(`.selectDate${id}`);
    let selectTime = document.querySelector(`.selectTime${id}`);
  
    console.log(spanUpdateCancel);
    spanUpdate.style.display = 'inline-block';
    selectDate.style.display = 'none';
    selectTime.style.display = 'none';
    spanSubmit.style.display = 'none';
    spanUpdateCancel.style.display = 'none';
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
const csrftoken = getCookie('csrftoken');
