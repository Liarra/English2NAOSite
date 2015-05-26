var changelist={
    actions_to_add:[],
    actions_to_remove:[],
    change_in_actions:[],

    conditions_to_add:[],
    conditions_to_remove:[],
    change_in_conditions:[],

    clear:function(){
        this.actions_to_add=[];
        this.actions_to_remove=[];
        this.change_in_actions=[];
        this.conditions_to_add=[];
        this.conditions_to_remove=[];
        this.change_in_conditions=[];
    },


    addAction:function(new_class,new_params){
        var new_action={class: new_class, params:new_params};
        this.actions_to_add.push(new_action);
    },

    addCondition:function(new_class,new_params){
        var new_condition={class: new_class, params:new_params};
        this.conditions_to_add.push(new_condition);
    },

    changeAction:function(index,new_params){
        this.change_in_actions[index]=new_params;
    },

}

var i=0
function addAllNewActions(){
}

function addNewActionTemplate(senderIcon){
    i=i+1;
    new_class=senderIcon.attr('command');
    class_glyphicon="glyphicon-question";

    if (new_class=="say_command")
    class_glyphicon="glyphicon-comment";
    if (new_class=="move_command")
    class_glyphicon="glyphicon-move";
    if (new_class=="wait_command")
    class_glyphicon="glyphicon-time";

    $(" <span class='program-box glyphicon "+class_glyphicon+" program-box-clickable new-action added-action' about='a"+i+"' command='"+new_class+"'></span>").insertBefore("#empty-action-box");
    $(".active-box").removeClass("active-box");
    $(".new-action").addClass("active-box");
    $(".new-action").removeClass("new-action");

    $.ajax({
            url: "/translator/editor-class-params/",
            type:"POST",
            data: {
                class_name: new_class
            },

            success: function( data ) {
                $(".action-params-div").hide();
                new_div="<div class='action-params-div' id='a"+i+"'>"+data+"</div>"
                $("#substep_editor_library").show();
                $("#substep_editor_library").append(new_div);
                assign_substep_actions_icons()
            },

            fail:function(data){
                throw_exception;
            }
        });
}
