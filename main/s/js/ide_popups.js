$(document).ready(function () {
    $('#dialog-close-btn, #dialog-overlay').click(function () {
        cData = null;
        $('#dialog-overlay, #dialog-box').fadeOut(50);
        $('#data').html("");
        return false;
    });
    
    $(window).resize(function () {
        
        //only do it if the dialog box is not hidden
        if (!$('#dialog-box').is(':hidden')) showSettings();
    });     
});

function showSettings() {
    var maskHeight = $(window).height();
    var maskWidth = $(window).width();
    var dialogTop =  (maskHeight/2.0) - ($('#dialog-box').height()/2.0);
    var dialogLeft = (maskWidth/2.0) - ($('#dialog-box').width()/2.0);

    console.log("Mask: " + maskHeight);
    console.log("Box: " + $('#dialog-box').height());

    $('#dialog-overlay').css({height:maskHeight, width:maskWidth}).fadeIn(50);
    $('#dialog-box').css({top:dialogTop, left:dialogLeft}).fadeIn(200);
}