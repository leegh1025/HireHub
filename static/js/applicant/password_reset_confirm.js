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

document.getElementById('password_reset_confirm_btn').addEventListener('click', function(event) {
   event.preventDefault();

   var new_password1 = document.getElementById('new_password1').value;
   var new_password2 = document.getElementById('new_password2').value;

   const csrfToken = getCSRFToken();

   const pathParts = window.location.pathname.split('/').filter(Boolean);
   const uidb64 = pathParts[2];
   const token = pathParts[3];

   fetch(`/applicants/reset/${uidb64}/${token}/`, {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json',
         'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
         'new_password1': new_password1,
         'new_password2': new_password2
      })
   }).then(response => response.json())
   .then(data => {
      if (data.success) {
         alert(data.message);
         window.location.href = data.redirect_url;
      } else {
         alert(data.message);
      }
   })
   .catch(error => {
      console.error('Fetch 에러:', error);
      alert('오류가 발생했습니다. 다시 시도해주세요');
   })
})