function assign_remove_buttons(){
$(".btn-remove-substep").click(function() {

    var substep_div = $(this).parent().parent();
    var substep_number=substep_div.children(".glyphicon-step").first().attr("uid");
    var substep_name=substep_div.children(".glyphicon-step").first().html();

    var conditions=substep_div.children(".condition-box");
    if (conditions.length){
    substep_name+=" ("
        for (var i=0;i<conditions.length;i++){
            substep_name+=conditions[i].innerHTML;
        }
        substep_name+=")"
    }

    bootbox.confirm("Removing step "+substep_name+". Is it OK?", function(result) {
        if(result){
            remove_substep(substep_div);
        }
    });
});


$(".btn-edit-substep").click(function(){
 var substep_div = $(this).parent().parent();
 var substep_number=substep_div.attr("uid");
 changelist.clear();
 edit_substep(substep_div);
});
}



function assignDoneButton(){
    $(".btn-done").click(
        function(){
        collectAdditions();
        collectConditionsAdditions();
        collectModifications();
        sendSubstepUpdate();
        }
    );
}

function remove_substep(substep_div){
    $("#btn-save").addClass("btn-info");

    $.ajax({
            url: remove_state_URL,
            type:"POST",
            data: {
                substep_id: substep_div.attr("uid"),
            },

            success: function( data ) {
                meta=substep_div.parent();
                substep_div.remove();
                if (meta.hasClass("metastate-container")){
                 if (meta.children().length==0){
                    meta.parent().remove();
                 }
                }

            },

            fail:function(data){
                throw_exception;
            }
        });
}


function edit_substep(substep_div){
 $("#btn-save").addClass("btn-info");

 $.ajax({
            url: edit_state_URL,
            type:"POST",
            data: {
                substep_id: substep_div.attr("uid"),
            },

            success: function( data ) {
                bootbox.dialog({
                message:data,

                 buttons: {

                    success: {
                      label: "Done!",
                      className: "btn-done",
                    }
                 }
                });
                assign_substep_actions_icons();
                assignDoneButton();
            },

            fail:function(data){
                throw_exception;
            }
        });
}


function h(e) {
  $(e).css({'height':'auto'}).height(e.scrollHeight);
}

$('textarea').each(function () {
  h(this);
}).on('input', function () {
  h(this);
});

function throw_exception(){
    alert("Something went wrong");
}

assign_remove_buttons();