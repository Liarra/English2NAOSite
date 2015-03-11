var steps_counter=2;
$("#steps-column")
    .on("click focus", ".step-div.inactive .step-description", function(e) {
        var curRow = $(".step-div.inactive");
        var newRow=curRow.clone();

        newRow.find(".step-number:first").html(steps_counter+".");
        newRow.find("input:first").val("");
        newRow.appendTo("#steps-column");

        steps_counter+=1;

        curRow.removeClass("inactive").find("textarea:last").focus();
    })
    .on("click", ".step-div .row .step-delete", function(e) {
        $(this).closest(".step-div").remove();
        renumber_steps();
        steps_counter--;
    });


function renumber_steps(){
    var i=0
    $( ".step-div" ).each(function( index ) {
        $(this).find(".step-number").html(index+1+".");
    });

}