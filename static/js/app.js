let i = 0;

$('.carousel').carousel();

function onClick(){
    if(i == 0){
        $("#main").hide();
        i = 1;
    }else{
        $("#main").show();
        i = 0;
    }
}

$('#btn').click(function(){
    $('#info').removeClass('invisible');
})