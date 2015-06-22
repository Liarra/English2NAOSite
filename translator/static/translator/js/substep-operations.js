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


function addNewConditionTemplate(senderIcon){
    i=i+1;
    new_class=senderIcon.attr('command');
    class_glyphicon="glyphicon-question";

    if (new_class=="button_press")
    class_glyphicon="glyphicon-button-input";


    $(" <span class='program-box glyphicon "+class_glyphicon+" program-box-clickable new-condition added-condition' about='c"+i+"' command='"+new_class+"'>&nbsp;</span>").insertBefore("#empty-condition-box");
    $("#empty-condition-box").hide();
    $(".active-box").removeClass("active-box");
    $(".new-condition").addClass("active-box");
    $(".new-condition").removeClass("new-condition");

    $.ajax({
            url: "/translator/editor-class-params/",
            type:"POST",
            data: {
                class_name: new_class
            },

            success: function( data ) {
                $(".action-params-div").hide();
                new_div="<div class='action-params-div' id='c"+i+"'>"+data+"</div>"
                $("#substep_editor_library").show();
                $("#substep_editor_library").append(new_div);
                assign_substep_actions_icons()
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

function collectConditionsAdditions(){
added_icons=$(".added-condition");
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

    changelist.addCondition(className,params);
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
                substep_id: $("#current-substep-edit span").first().attr("uid"),
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


