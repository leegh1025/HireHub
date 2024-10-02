$(document).ready(function() {
    $('#question-form').submit(function(e) {
        e.preventDefault();
        // 기존 폼 데이터를 가져옴
        var formData = $('#question-form').serializeArray();

        // 폼 데이터에 question_submit 항목 추가
        formData.push({ name: 'question_submit', value: 'Add Question' });

        $.ajax({
            type: 'POST',
            url: $('#question-form').attr('action'),
            data: $.param(formData),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                if (response.success) {
                    $('#question_list').append(
                        '<li class="individualquestion" data-question-id="' + response.question.id + '">' +
                        '<div class="question" data-question-id="' + response.question.id + '">' +
                        '질문: ' + response.question.text +'<div class="question_btn">'+
                        '<button class="deleteQuestionBtn" data-question-id="' + response.question.id + '">삭제</button>' +
                        '</div></div></li>'
                    );
                    $('#question-form')[0].reset();
                } else {
                    alert('Failed to add question: ' + response.error);
                    console.error(response.form_errors);  // 폼 오류 메시지 출력
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred: ' + error);
                console.error('AJAX request failed:', error);
            }
        });
    });
});

$(document).ready(function() {
    // 질문 삭제
    $(document).on('click', '.deleteQuestionBtn', function() {
        if (!confirm('정말로 이 질문을 삭제하시겠습니까?')) {
            return;
        }

        var questionId = $(this).data('question-id');
        var applicantId = $('#load-question').data('applicant-id');
        var url = applicantId + "/question/" + questionId + "/delete/";

        $.ajax({
            url: url,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(data) {
                if (data.success) {
                    $('.individualquestion[data-question-id="' + questionId + '"]').remove();
                } else {
                    alert('Failed to delete question: ' + data.error);
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred: ' + error);
                console.error('AJAX request failed:', error);
            }
        });
    });
});

// $(document).ready(function() {
//     // 답변 폼 생성
//     $(document).on('submit', '.answerForm', function(event){
//         event.preventDefault();
//         var questionId = $(this).data('question-id');
//         var applicantId = $('#load-question').data('applicant-id');
//         var url = applicantId + "/question/";
//         var formData = $('.answerForm').serializeArray();

//         formData.push({ name: 'answer_submit', value: 'Add Answer' });
//         console.log(formData);
//         formData.push({ name: 'question_id', value: questionId});
//         console.log(formData);

//         $.ajax({
//             url: url,
//             type: 'POST',
//             data: $.param(formData),
//             headers: {
//                 'X-CSRFToken': csrftoken
//             },
//             success: function(data) {
//                 console.log('Server response:', data);
//                 if (data.success) {
//                     $('.answerForm').closest('li').find('ul.answerList').append('<li class="individualanswer" data-answer-id="'+ data.answer.id +'"> 답변: ' + data.answer.text + 
//                         '<button class="deleteAnswerBtn" data-answer-id="'+ data.answer.id +'">삭제</button>'+'</li>');
//                     $('.answerForm')[0].reset();
//                 } else {
//                     alert('Failed to add question: ' + data.error);
//                     console.error(data.form_errors);  // 폼 오류 메시지 출력
//                 }
//             },
//             error: function(xhr, status, error) {
//                 alert('An error occurred: ' + error);
//                 console.error('AJAX request failed:', error);
//             }
//         });
//     });
// });

// $(document).ready(function() {
//     // 답변 삭제
//     $(document).on('click', '.deleteAnswerBtn', function() {
//         if (!confirm('정말로 이 답변을 삭제하시겠습니까?')) {
//             return;
//         }

//         var answerId = $(this).data('answer-id');
//         var applicantId = $('#load-question').data('applicant-id');
//         var url = applicantId + "/question/" + answerId + "/answer_delete/";

//         $.ajax({
//             url: url,
//             type: 'POST',
//             headers: {
//                 'X-CSRFToken': csrftoken
//             },
//             success: function(data) {
//                 if (data.success) {
//                     $('.individualanswer[data-answer-id="' + answerId + '"]').remove();
//                 } else {
//                     alert('Failed to delete question: ' + data.error);
//                 }
//             },
//             error: function(xhr, status, error) {
//                 alert('An error occurred: ' + error);
//                 console.error('AJAX request failed:', error);
//             }
//         });
//     });
// });