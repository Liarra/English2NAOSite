function assign_remove_buttons(){
$(".btn-remove-substep").click(function() {

    var substep_div = $(this).parent().parent();
    var substep_number=substep_div.children(".glyphicon-step").first().html()

    bootbox.confirm("Removing step "+substep_number+". Is it OK?", function(result) {
        if(result){
            remove_substep(substep_div);
        }
    });

});

$(".btn-edit-substep").click(function(){

 var substep_div = $(this).parent().parent();
 var substep_number=substep_div.children(".glyphicon-step").first().html()
 edit_substep(substep_div)

});
}



function remove_substep(substep_div){
    $("#btn-save").addClass("btn-info");

    $.ajax({
            url: "/translator/remove-substep/",
            type:"POST",
            data: {
                substep_id: substep_div.children(".glyphicon-step").first().html(),
            },

            success: function( data ) {
                substep_div.remove();
            },

            fail:function(data){
                throw_exception;
            }
        });
}


function edit_substep(substep_div){
 $("#btn-save").addClass("btn-info");

 $.ajax({
            url: "/translator/editor-substep/",
            type:"POST",
            data: {
                substep_id: substep_div.children(".glyphicon-step").first().html(),
            },

            success: function( data ) {
                bootbox.dialog({
                message:data,

                 buttons: {

                    success: {

                      label: "Success!",

                      className: "btn-success",

                    }
                    }
                });
            },

            fail:function(data){
                throw_exception;
            }
        });
}

function throw_exception(){
    alert("Nope, baby");
}

assign_remove_buttons();