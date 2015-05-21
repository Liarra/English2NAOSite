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

function assign_substep_actions_icons(){
$(".program-box-clickable").click(
    function(){
    $(".active-box").removeClass("active-box");
    $(this).addClass("active-box");
    substep_div=$(this).parent()
    substepid=substep_div.children(".glyphicon-step").first().html()
        load_component_params($(this).attr('about'), substepid)
    }
);

$(".empty-program-box").click(
    function(){
        $(".active-box").removeClass("active-box");
        $(this).addClass("active-box");
        load_actions_library();
    }
);
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
                      label: "Done!",
                      className: "btn-success",
                    }
                 }
                });
                assign_substep_actions_icons();
            },

            fail:function(data){
                throw_exception;
            }
        });
}


function load_actions_library(){
    $.ajax({
            url: "/translator/editor-substep-actions/",
            type:"GET",

            success: function( data ) {
                $("#substep_editor_library").show();
                $("#substep_editor_library").html(data);
            },

            fail:function(data){
                throw_exception;
            }
        });
}


function load_component_params(index, substepid){
    $.ajax({
            url: "/translator/editor-substep-params/",
            type:"POST",

            data: {
                substep_id: substepid,
                substep_action_index: index,
            },

            success: function( data ) {
                $("#substep_editor_library").show();
                $("#substep_editor_library").html(data);
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