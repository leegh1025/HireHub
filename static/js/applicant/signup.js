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

// 회원가입 함수
document.getElementById('signup_btn').addEventListener('click', function(event) {
   event.preventDefault(); // 기본 form 제출 방지

   var email = document.getElementById('email').value;
   var name = document.getElementById('applicant_name').value;
   var phone_number = document.getElementById('phone_number').value;
   var password = document.getElementById('password').value;
   var password_confirm = document.getElementById('password_confirm').value;
   var verification_code = document.getElementById('code').value;

   const csrfToken = getCSRFToken();

   fetch('/applicants/signup/', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json',
         'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
         'email': email,
         'name': name,
         'phone_number': phone_number,
         'password': password,
         'password_confirm': password_confirm,
         'code': verification_code
      })
   }).then(response => response.json())
   .then(data => {
      console.log('응답 데이터:', data);  // 응답 데이터를 콘솔에 출력
      if (data.success) {
         window.location.href = data.redirect_url;
      } else {
         alert(data.message);  // 실패 시 메시지 alert로 출력
      }
   })
   .catch(error => {
      console.error('Fetch 에러:', error);
      alert('오류가 발생했습니다. 다시 시도해주세요.');
   });
});

document.getElementById('send_code_btn').addEventListener('click', function() {
   var email = document.getElementById('email').value;
   const csrfToken = getCSRFToken();
   fetch(window.location.origin + '/applicants/send_verification_code/', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json',
         'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ 'email': email })
   }).then(response => response.json())
   .then(data => {
      if (data.success) {
         alert('인증코드가 이메일로 전송되었습니다.');
      } else {
         alert(data.message);
      }
   });
});

document.getElementById('verify_code_btn').addEventListener('click', function() {
   var email = document.getElementById('email').value;
   var code = document.getElementById('code').value;
   const csrfToken = getCSRFToken();
   fetch(window.location.origin + '/applicants/verify_code/', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json',
         'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ 'email': email, 'code': code })
   }).then(response => response.json())
   .then(data => {
      var statusDiv = document.getElementById('verification_status');
      if (data.success) {
         statusDiv.innerHTML = '<p style="color: green;">🎉 인증 성공! 🎉</p>';
         document.getElementById('signup_btn').disabled = false; // 회원가입 버튼 활성화
      } else {
         statusDiv.innerHTML = '<p style="color: red;">😅 인증 실패 😅</p>';
         alert(data.message);
      }
   });
});

// 전화번호에 숫자만 입력되도록 차단
document.getElementById('phone_number').addEventListener('input', function(e) {
   this.value = this.value.replace(/[^0-9]/g, ''); // 숫자가 아닌 문자는 제거
})