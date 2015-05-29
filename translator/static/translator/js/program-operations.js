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

$(".empty-program-box").click(
    function(){
        $(".active-box").removeClass("active-box");
        $(this).addClass("active-box");
        load_actions_library();
    }
);
}

function assignDoneButton(){
    $(".btn-done").click(
        function(){
        collectAdditions();
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
            type:"GET",

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

function collectAdditions(){
added_icons=$(".added-action");
for (index = 0; index < added_icons.length; ++index) {
    console.log(added_icons[index]);
    var className=added_icons[index].attributes["command"].nodeValue;
    var params_div_id=added_icons[index].attributes["about"].nodeValue;
    var params_div=$("#"+params_div_id);
    var param_textboxes=params_div.children("div").first().children("input");
    var params = {};

    for (jindex = 0; jindex < param_textboxes.length; ++jindex) {
        name=param_textboxes[jindex].attributes["name"].nodeValue;
        value=param_textboxes[jindex].value;
        params[name]=value;
    }

    changelist.addAction(className,params);
}
}

function collectModifications(){
added_icons=$(".existing-action");
for (index = 0; index < added_icons.length; ++index) {
    console.log(added_icons[index]);
    var params_div_id=added_icons[index].attributes["about"].nodeValue;
    var params_div=$("#s"+params_div_id);
    var param_textboxes=params_div.children("div").first().children("input");
    var params = {};

    for (jindex = 0; jindex < param_textboxes.length; ++jindex) {
        name=param_textboxes[jindex].attributes["name"].nodeValue;
        value=param_textboxes[jindex].value;
        params[name]=value;
    }

    changelist.changeAction(index,params);
}

}

function sendSubstepUpdate(){
$.ajax({
            url: "/translator/editor-substep-update/",
            type:"POST",

            data: {
                substep_id: $("#current-substep-edit span").first().html(),
                actions_to_add : JSON.stringify(changelist.actions_to_add),
                conditions_to_add : JSON.stringify(changelist.conditions_to_add),
                actions_to_remove: JSON.stringify(changelist.actions_to_remove),
                conditions_to_remove: JSON.stringify(changelist.conditions_to_remove),
                change_actions : JSON.stringify(changelist.change_in_actions),
                change_conditions : JSON.stringify(changelist.change_in_conditions)
            },

            success: function( data ) {
                $("#program" ).html(data);
                assign_balloons();
                alignTextWithProgram();
                assign_remove_buttons();
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