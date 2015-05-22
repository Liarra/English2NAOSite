var changelist={
    actions_to_add:[],
    actions_to_remove:[],
    change_in_actions:[],

    conditions_to_add:[],
    conditions_to_remove:[],
    change_in_conditions:[],

    clear:function(){
        actions_to_add=[];
        actions_to_remove=[];
        change_in_actions=[];
        conditions_to_add=[];
        conditions_to_remove=[];
        change_in_conditions=[];
    },


    addAction:function(new_class,new_params){
        var new_action={class: new_class, params:new_params};
        actions_to_add.push(new_action);
    },

    addCondition:function(new_class,new_params){
        var new_condition={class: new_class, params:new_params};
        conditions_to_add.push(new_condition);
    }




}


function addAllNewActions(){
}

function addNewActionTemplate(senderIcon){
    new_class=senderIcon.attr('command');
    $(" <span class='program-box glyphicon glyphicon-move program-box-clickable new-action added-action'></span>").insertBefore("#empty-action-box");
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
                $("#substep_editor_library").html(data);
            },

            fail:function(data){
                throw_exception;
            }
        });
}
