//code for button to open n close images
$(document).ready(function() {
    var showChar = 400;
 
    var View = "View";
    var Close = "Close";
   
    $('.more').each(function() {
        var content = $(this).html();

       

            var html = '<span class="moreelipses">'+'</span><span class="morecontent"><span>' + content + '</span><div class="text-center margin_top_10"><a href="" class="morelink">'+View+'</a></div></span>';

            $(this).html(html);
        

    });

    $(".morelink").click(function(){
        if($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(View);
        } else {
            $(this).addClass("less");
            $(this).html(Close);
        }
        $(".moreelipses").toggle();
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });
});