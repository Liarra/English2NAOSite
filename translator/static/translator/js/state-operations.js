var changelist={
    actions_to_add:[],
    actions_to_remove:[],
    change_in_actions:[],

    conditions_to_add:[],
    conditions_to_remove:[],
    change_in_conditions:[],

    next_id:0,

    clear:function(){
        this.actions_to_add=[];
        this.actions_to_remove=[];
        this.change_in_actions=[];
        this.conditions_to_add=[];
        this.conditions_to_remove=[];
        this.change_in_conditions=[];
        this.next_id=0;
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

    changeCondition:function(index,new_params){
        this.change_in_conditions[index]=new_params;
    },

    removeAction:function(index){
        this.actions_to_remove.push(index);
    },

    removeCondition:function(index){
        this.conditions_to_remove.push(index);
    },

    setNext:function(nextID){
        this.next_id=nextID;
    }
}

var i=0


function assign_substep_actions_icons(){
    $(".program-box-clickable").click(
        function(){
        $(".active-box").removeClass("active-box");
        $(this).addClass("active-box");
        state_div=$(this).parent().parent();
        state_id=state_div.children(".glyphicon-step").first().attr("uid");
        load_component_params($(this).attr('about'), state_id,'a');
        }
    );

    $(".condition-box").click(
        function(){
        $(".active-box").removeClass("active-box");
        $(this).addClass("active-box");
        state_div=$(this).parent().parent();
        state_id=state_div.children(".glyphicon-step").first().attr("uid");
        load_component_params($(this).attr('about'), state_id,'c');
        }
    );

    $(".state-id-clickable").click(
        function(){
        $(".active-box").removeClass("active-box");
        $(this).addClass("active-box");
        load_next_params($(this));
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

    $(".added-next").click(
        function(){
        $(".active-box").removeClass("active-box");
        $(this).addClass("active-box");
        load_next_params($(this));
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

     $("#empty-next-box").click(
        function(){
            $(".active-box").removeClass("active-box");
            $(this).addClass("active-box");
            load_next_params(null);
        }
    );

    $(".btn-remove-component").click(
        function(){
         var component = $(this).parent().parent().children(".program-box").first();
         var component_index=component.attr("about");

         component.parent().remove();

         //If component was added in this dialogue, just remove the icon
         if (component.hasClass("added-action") || component.hasClass("added-condition")){
            return;
         }

        else {
            if (component.hasClass("condition-box"))
                changelist.removeCondition(component_index);
            else if (component.hasClass("existing-action"))
                changelist.removeAction(component_index);
            else if (component.hasClass("existing-next"))
                changelist.setNext(-1);
        }
        }
    );
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


function load_component_params(index, state_id, letter){
//If it's already there, just show it

    if($("#"+letter+index).length ){
        $(".action-params-div").hide();
        $("#"+letter+index).show();
        return
    }

    if (letter=='a'){
        ajax_data={
            substep_id: state_id,
            substep_action_index: index,
        }
    }
    else{
        ajax_data={
            substep_id: state_id,
            substep_condition_index: index
        }
    }
    $.ajax({
            url: "/translator/editor-substep-params/",
            type:"POST",

            data: ajax_data,

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

function load_next_params(senderIcon){

    //If it's already there, just show it

    if($("#n").length ){
        $(".action-params-div").hide();
        $("#n").show();
        return
    }

    if (senderIcon)
    next_id=senderIcon.html();
    else
    {
    $(" <div class='component'>"+
    " <span class='program-box glyphicon glyphicon-step new-next added-next' about='n'>?</span>"+
    "<div class='component-buttons'><button type='button' class='btn btn-remove-component' title='Remove'>x</button></div></div>").insertBefore("#empty-next-box");
    $("#empty-next-box").hide();
    $(".active-box").removeClass("active-box");
    $(".new-condition").addClass("active-box");

    senderIcon=$(".new-next").first();
    $(".new-next").removeClass("new-next");
    }

    next_id="";

    data="<b>Next ID</b><br/><input type='text' name='next_id' id='next_id' value="+next_id+">"

    $(".action-params-div").hide();
    new_div="<div class='action-params-div' id='n'>"+data+"</div>"

    $("#substep_editor_library").show();
    $("#substep_editor_library").append(new_div);

    $("#next_id").on("input propertychange paste",function(){
        senderIcon.html($("#next_id").val());
    });

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

    $(" <div class='component'>"+
    "<span class='program-box glyphicon "+class_glyphicon+" program-box-clickable new-action added-action' about='a"+i+"' command='"+new_class+"'>"+
    "</span><div class='component-buttons'><button type='button' class='btn btn-remove-component' title='Remove this action'>x</button></div></div>").insertBefore("#empty-action-box");

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


    $(" <div class='component'>"+
    " <span class='program-box glyphicon "+class_glyphicon+" program-box-clickable new-condition added-condition' about='c"+i+"' command='"+new_class+"'>?</span>"+
    "<div class='component-buttons'><button type='button' class='btn btn-remove-component' title='Remove this condition'>x</button></div></div>").insertBefore("#empty-condition-box");
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

next_id_field=$("#next_id");
if (next_id_field.length)
    changelist.setNext(next_id_field.val());
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
                change_conditions : JSON.stringify(changelist.change_in_conditions),
                change_next_id: JSON.stringify(changelist.next_id),
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


