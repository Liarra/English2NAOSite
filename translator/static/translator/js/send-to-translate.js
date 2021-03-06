// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){

    assign_balloons();
    alignTextWithProgram();


    $(".step-name-text").focus(function(){
        $("#btn-save").addClass("btn-info");
    });

    $(".step-description").focus(function(){
        $("#btn-save").addClass("btn-info");
    });

    $("#btn-save").click(function(){
        var url_to_go=$(this).attr("to");
        var text_values = $('.step-description').map(function() {
            return this.value;
        }).get()

        var headers_values = $('.step-name-text').map(function() {
            return this.value;
        }).get()

        $.ajax({
            url: url_to_go,
            type:"POST",
            data: {
                text: text_values,
                headers: headers_values
            },

            success: function( data ) {
                $("#btn-save").removeClass("btn-info");
                assign_balloons();
                alignTextWithProgram();
            }
        });
    });

    $(".btn-translate").click(function(){
        var url_to_go=$(this).attr("to");
        bootbox.confirm("Doing this will replace an existing program on the left with a translation. Any changes you made to the program will be lost. Is it OK?", function(result) {
        if(result){

        $("#btn-save").addClass("btn-info");

        var text_values = $('.step-description').map(function() {
            return this.value;
        }).get()

        var headers_values = $('.step-name-text').map(function() {
            return this.value;
        }).get()

        $.ajax({
            url: url_to_go,
            type:"POST",
            data: {
                text: text_values,
                headers: headers_values
            },

            success: function( data ) {
//                var json_data=jQuery.parseJSON(data);
//                $("#program" ).html(make_program(json_data));
                $("#program").html(data);
                assign_balloons();
                alignTextWithProgram();
                assign_remove_buttons();
            }
        });
        }
        });


    });


    $('.application-form').submit(function(e)
    {
        e.preventDefault();

        $.cookie(getCookie('csrftoken'));
    });

    $("#btn-download").click(function(){
        var url_to_go=$(this).attr("to");
        var values = $('.step-description').map(function() {
            return this.value;
        }).get()

        var params={};
        var i=0;

        for(v of values){
            params["text["+i+"]"]=v;
            i++;
        }

        $.ajax({
            url: url_to_go,
            type:"POST",
            data: params,

            success: function( response, status, request ) {
                var disp = request.getResponseHeader('Content-Disposition');
                if (disp && disp.search('attachment') != -1) {

                var form = $('<form method="POST" class="application-form" action="/translator/csv/">{% csrf_token %}');
                $.each(params, function(k, v) {
                    form.append($("<input type='hidden' name='text[]' value='" + v + "'>"));
                });
                form.append($('<input type="hidden" name="csrfmiddlewaretoken" class="csrf" value="' + csrftoken + '">'));
                $('body').append(form);
                form.submit();
                }
            }
        });
    });

});

function assign_balloons() {
  $('.program-box').balloon({position: "bottom",minLifetime: 0, css: {'max-width':'200px'}});
}

function alignTextWithProgram(){
    var numItems = $('.program-step').length
    var programItems = $('.program-step')
    var textItems=$('.step-div')


    for(var i=0;i<numItems;i++){
        ProgramItem=programItems.eq(i);
        TextItem=textItems.eq(i);
        var nameHeight=TextItem.children(".row").first().height()+4;

        difference=ProgramItem.height()-TextItem.height();
        if (difference>0){
            difference=difference+62;
            TextItem.css({"margin-bottom":difference+"px"});
            ProgramItem.css({"margin-bottom":"30px"});
        }

        else{
            difference=-1*difference;
            ProgramItem.css({"margin-bottom":difference+"px"});
            TextItem.css({"margin-bottom":"20px"});
        }


    }
}