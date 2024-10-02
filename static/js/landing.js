document.addEventListener('DOMContentLoaded', function () {
    const titleBoxes = document.querySelectorAll('#title_box, #final_btn');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (entry.target.id === 'final_btn') {
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, 600); 
                } else {
                    entry.target.classList.add('visible');
                }
                observer.unobserve(entry.target); // 애니메이션이 한 번만 적용되도록 관찰 중지
            }
        });
    });

    titleBoxes.forEach(box => {
        observer.observe(box);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const images = document.querySelectorAll('.left, .right, #info');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (entry.target.id === 'info') {
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, 500); 
                } else {
                    entry.target.classList.add('visible');
                }

                observer.unobserve(entry.target); // 애니메이션이 한 번만 적용되도록 관찰 중지
            }
        });
    });

    images.forEach(image => {
        observer.observe(image);
    });
});



document.addEventListener('DOMContentLoaded', function() {
    const animatedElement = document.getElementById('arrow');
    const elementsToShow = [
        document.getElementById('section_img_1'),
        document.getElementById('section_img_2'),
        document.getElementById('section_img_3'),
        document.getElementById('section_img_4'),
    ];

  // IntersectionObserver 설정
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (!animatedElement.classList.contains('animate-on-focus')) {
                    animatedElement.classList.add('animate-on-focus');

                    elementsToShow.forEach((element, index) => {
                        // 각 요소에 다른 지연 시간을 적용
                        const delay = (index + 1) * 500; // 첫 번째 요소 500ms, 두 번째 1000ms, 세 번째 1500ms, 네 번째 2000ms
                        setTimeout(() => {
                            element.classList.add('show');
                        }, delay); // 지연 시간 적용

                    });

                    // 애니메이션이 끝난 후 'done' 클래스를 추가하여 상태를 유지
                    animatedElement.addEventListener('transitionend', function() {
                        animatedElement.classList.add('done');
                    }, { once: true });
                }
            }
        });
    }, {
        threshold: 0.1 
    });

    observer.observe(animatedElement);
});

document.addEventListener('DOMContentLoaded', function() {
    const animatedElement = document.getElementById('interview_img');

    // IntersectionObserver 설정
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (!animatedElement.classList.contains('interview-on-focus')) {
                    animatedElement.classList.add('interview-on-focus'); 

                    animatedElement.addEventListener('transitionend', function() {
                        animatedElement.classList.add('done');
                    }, { once: true });
                }
            }
        });
    }, {
        threshold: 0.1 // 10% 이상 보일 때 트리거
    });

    // 관찰할 요소를 지정
    observer.observe(animatedElement);
});