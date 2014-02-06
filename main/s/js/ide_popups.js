var cData = null;

$(document).ready(function () {
    $('#dialog-close-btn, #dialog-overlay').click(function () {
        cData = null;
        $('#dialog-overlay, #dialog-box').fadeOut(50);
        $('#data').html("");
        return false;
    });
    
    $(window).resize(function () {
        
        //only do it if the dialog box is not hidden
        if (!$('#dialog-box').is(':hidden')) popup();        
    });     
});

function popup(title, message) {
    var maskHeight = $(document).height();
    var maskWidth = $(window).width();
    var dialogTop =  100;
    var dialogLeft = (maskWidth/2) - ($('#dialog-box').width()/2);

    if(cData == null) {
        cData = {"title": title, "message": message};
        /*$.ajax({
            url: "/ajax/get_data_for_"+id+".json",
            async: false
        }).success(function(data){
            cData = data;
        }).fail(function(data){
            console.log("ERROR: Invalid ID - got 404");
        });*/
    }
    if(cData == null)
        return;

    $('#dialog-overlay').css({height:maskHeight, width:maskWidth}).fadeIn(50);
    $('#dialog-box').css({top:dialogTop, left:dialogLeft}).fadeIn(200);
    $('#title').html(title);
    $('#message').html(message);
}