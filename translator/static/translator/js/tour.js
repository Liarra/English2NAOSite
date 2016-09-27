tutorial_screen=0;
$(".tutorial").click(
function(){
if (tutorial_screen==5){
tutorial_screen=0;
$(this).hide();
}

tutorial_screen=tutorial_screen+1;
$(this).css("background-image", "url('../static/translator/img/tour/"+tutorial_screen+".png')")

});

$(".help").click(
function(){
$(".tutorial").show();
});