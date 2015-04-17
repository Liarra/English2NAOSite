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
    $(".btn-translate").click(function(){

        var values = $('.step-description').map(function() {
            return this.value;
        }).get()

        $.ajax({
            url: "translate/",
            type:"POST",
            data: {
                text: values,
            },

            success: function( data ) {
//                var json_data=jQuery.parseJSON(data);
//                $("#program" ).html(make_program(json_data));
                $("#program" ).html(data);
                assign_balloons();
                alignTextWithProgram();
            }
        });
    });


    $('.application-form').submit(function(e)
    {
        e.preventDefault();

        $.cookie(getCookie('csrftoken'));
    });

    $("#btn-download").click(function(){

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
            url: "csv/",
            type:"POST",
            data: params,

            success: function( response, status, request ) {
                var disp = request.getResponseHeader('Content-Disposition');
                if (disp && disp.search('attachment') != -1) {

                var form = $('<form method="POST" class="application-form" action="csv/">{% csrf_token %}');
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

function make_program(json_data){
    var count = Object.keys(json_data).length;
    var htmlString="";

    for(var i=1; i<=count;i++){
        var step_data=jQuery.parseJSON(json_data[i+""]);
        htmlString+="<div class='program-step'>";

        var inner_count = Object.keys(step_data).length;
        if(inner_count==0){
            htmlString+="<center>(EMPTY STEP)</center>"
        }

        else
        for (var substep of step_data){
            //SubstepID
            htmlString+="<span class='program-box glyphicon glyphicon-step'>"+substep["stepID"]+"</span>";

            var conditions=substep["conditions"];
            if (conditions!=undefined){
                for (var condition of conditions){
                    if (condition.indexOf("key[")==0){
                    htmlString+="<span class='program-box glyphicon glyphicon-button-input' title='"+condition+"'>"+condition.charAt(4).toUpperCase()+"</span>"
                    }
                }
//                htmlString+="<span class='arrow-box glyphicon glyphicon-arrow-right'></span>"
                }

          htmlString+="<span class='arrow-box glyphicon glyphicon-arrow-right'></span>"

            var actions=substep["actions"]
            if (actions!=undefined)
                for (var action of actions){
                    if (action.indexOf("_UNRECOGNISED_")==0){
                        htmlString+="<span class='program-box glyphicon glyphicon-question-sign' title='"+action+"'></span> "
                    }

                    if (action.indexOf("say(")==0){
                        htmlString+="<span class='program-box glyphicon glyphicon-comment' title='"+action+"'></span> "
                    }

                    if (action.indexOf("wait(")==0){
                        htmlString+="<span class='program-box glyphicon glyphicon-time' title='"+action+"'></span> "
                    }
                    if (action.indexOf("stiff")==0){
                        htmlString+="<span class='program-box glyphicon glyphicon-move' title='"+action+"'></span> "
                    }
                    if (action.indexOf(" | ")==0){
                        htmlString+="<span class='program-box' title='"+action+"'>|</span>"
                    }

                    if (action.indexOf(" & ")==0){
                        htmlString+="<span class='program-box' title='"+action+"'>&</span>"
                    }
                }



                nextID=substep["nextID"]
                if(nextID>-1){
                    htmlString+="<span class='arrow-box glyphicon glyphicon-arrow-right'></span>";
                    htmlString+="<span class='program-box glyphicon glyphicon-step'>"+nextID+"</span>";
                }
                htmlString+="<br/>"
//
        }
//        htmlString+=json_data[i+""];
        htmlString+="</div>";
    }

    return htmlString;
}

function alignTextWithProgram(){
    var numItems = $('.program-step').length
    var programItems = $('.program-step')
    var textItems=$('.step-div')

    for(var i=0;i<numItems;i++){
        ProgramItem=programItems.eq(i)
        TextItem=textItems.eq(i)

        difference=ProgramItem.height()-TextItem.height()+61

        TextItem.css({"margin-bottom":difference+"px"});
    }
}