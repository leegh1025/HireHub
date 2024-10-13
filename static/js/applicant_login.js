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

// 로그인 함수
function login(email, password) {
   const csrfToken = getCSRFToken();
   return fetch('/applicants/login/', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json',
         'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
         'email': email,
         'password': password
      }),
      credentials: 'same-origin'
   })
   .then(response => {
      if (response.ok) {
         return response.json();
      } else {
         throw new Error('Login failed');
      }
   });
}

// 이벤트 리스너
document.getElementById('login_btn').addEventListener('click', function(event) {
   event.preventDefault(); // 기본 form 제출 방지
   
   const email = document.getElementById('email').value;
   const password = document.getElementById('password').value;

   login(email, password)
       .then(data => {
           if (data.success) {
               window.location.href = data.redirect_url;
           } else {
               alert(data.message);
           }
       })
       .catch(error => {
           console.error('Login error: ', error);
           alert("로그인 중 오류가 발생했습니다. 다시 시도해주세요.");
       });
});