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
 var substep_number=substep_div.children(".glyphicon-step").first().attr("uid");
 changelist.clear();
 edit_substep(substep_div);
});
}

function assign_substep_actions_icons(){
$(".program-box-clickable").click(
    function(){
    $(".active-box").removeClass("active-box");
    $(this).addClass("active-box");
    substep_div=$(this).parent();
    substepid=substep_div.children(".glyphicon-step").first().attr("uid");
    load_component_params($(this).attr('about'), substepid,'s');
    }
);


$(".added-action").click(
    function(){
    $(".active-box").removeClass("active-box");
    $(this).addClass("active-box");
    load_component_params($(this).attr('about'), 0,'');
    }
);

$(".added-condition").click(
    function(){
    $(".active-box").removeClass("active-box");
    $(this).addClass("active-box");
    load_component_params($(this).attr('about'), 0,'');
    }
);

$("#empty-action-box").click(
    function(){
        $(".active-box").removeClass("active-box");
        $(this).addClass("active-box");
        load_actions_library();
    }
);

$("#empty-condition-box").click(
    function(){
        $(".active-box").removeClass("active-box");
        $(this).addClass("active-box");
        load_conditions_library();
    }
);
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
                substep_id: substep_div.children(".glyphicon-step").first().attr("uid"),
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


function load_actions_library(){

     if($("#library").length ){
        $(".action-params-div").hide();
        $("#library").show();
        return
    }

    $.ajax({
            url: "/translator/editor-substep-actions/",
            type:"POST",
            data:{
                components_type: "components",
            },

            success: function( data ) {
                $(".action-params-div").hide();
                new_div="<div class='action-params-div' id='library'>"+data+"</div>"
                $("#substep_editor_library").show();
                $("#substep_editor_library").append(new_div);
                $(".new-action-icon").click(
                    function(){
                    addNewActionTemplate($(this));
                    }
                );
            },

            fail:function(data){
                throw_exception;
            }
        });
}

function load_conditions_library(){

     if($("#library_conditions").length ){
        $(".action-params-div").hide();
        $("#library_conditions").show();
        return
    }

    $.ajax({
            url: "/translator/editor-substep-actions/",
            type:"POST",
            data:{
                components_type: "conditions",
            },

            success: function( data ) {
                $(".action-params-div").hide();
                new_div="<div class='action-params-div' id='library_conditions'>"+data+"</div>"
                $("#substep_editor_library").show();
                $("#substep_editor_library").append(new_div);
                $(".new-condition-icon").click(
                    function(){
                    addNewConditionTemplate($(this));
                    }
                );
            },

            fail:function(data){
                throw_exception;
            }
        });
}


function load_component_params(index, substepid,letter){
//If it's already there, just show it

    if($("#"+letter+index).length ){
        $(".action-params-div").hide();
        $("#"+letter+index).show();
        return
    }

    $.ajax({
            url: "/translator/editor-substep-params/",
            type:"POST",

            data: {
                substep_id: substepid,
                substep_action_index: index,
            },

            success: function( data ) {
                $(".action-params-div").hide();
                new_div="<div class='action-params-div' id='"+letter+index+"'>"+data+"</div>"
                $("#substep_editor_library").show();
                $("#substep_editor_library").append(new_div);
            },

            fail:function(data){
                throw_exception;
            }
        });
}

function throw_exception(){
    alert("Something went wrong");
}

assign_remove_buttons();