// $(document).on('submit', 'form', function(e) {
//     alert('clicked');
//     e.preventDefault()
    // var targetArray = $(this).serializeArray() 
    // targetArray.forEach(element => {
    //     if(element.name == 'var'){
    //         console.log(element.value)
//         }
        
//     });;
// });

// $(document).ready(function(){
//     $('#main-form').submit(function(event){
//         $.post("/static/js/getajax",{data:$(".container__title").val()},onResponse);
//         return false;
//     })
//     function onResponse(data){
//         $(".container__alert").text(data);
//     }
// })

$(document).ready(function(){
    $('#main-form').submit(function(event){
        event.preventDefault()
        var targetArray = $(this).serializeArray()
        answerChosen = targetArray[1].value
        $.ajax({
            type:"POST",
            url:document.location.pathname+'check_is_correct/',
            data:{
                'search_text' : answerChosen,
                'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
            $(".container__submit input").prop('value', data);
            if(data=="Верно"){
                $(".container__variants-field").animate({
                    backgroundColor: "#ace3a2",
                    color: "#000",
                  }, 500);
            }else{
                $(".container__variants-field").animate({
                    backgroundColor: "#f08e8e",
                    color: "#000",
                  }, 500);
            }

        },
            dataType: 'html'
        });
        return false
        })
})


// function checkAnswer(){
// setTimeout(answerVal, 250)
// }
// function answerVal(){
//     console.log($(".container_alert").val())
// }