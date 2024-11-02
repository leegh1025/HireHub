// CSRF 토큰을 쿠키에서 가져오는 함수
function getCSRFToken() {
   const name = 'csrftoken=';
   const decodedCookie = decodeURIComponent(document.cookie);
   const cookieArray = decodedCookie.split(';');
   for(let i = 0; i < cookieArray.length; i++) {
       let cookie = cookieArray[i].trim();
       if (cookie.indexOf(name) == 0) {
           return cookie.substring(name.length, cookie.length);
       }
   }
   return "";
}

document.getElementById('password_reset_btn').addEventListener('click', function(event) {
   event.preventDefault();

   var email = document.getElementById('id_email').value;
   const csrfToken = getCSRFToken();

   fetch('/applicants/password_reset/', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json',
         'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({'email': email})
   })
   .then(response => response.json())
   .then(data => {
      if (data.success) {
         alert(data.message)
      } else {
         alert(data.message)
      }
   })
   .catch(error => {
      console.error("에러 발생", error);
      alert("오류가 발생했습니다. 다시 시도해주세요.");
   });
});