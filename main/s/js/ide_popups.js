function reloadSettings() {
    document.getElementById('setting-iframe').contentWindow.location.reload();
}

function showSettings() {
    var maskHeight = $(window).height();
    var maskWidth = $(window).width();
    var dialogTop =  (maskHeight/2.0) - ($('#dialog-box').height()/2.0);
    var dialogLeft = (maskWidth/2.0) - ($('#dialog-box').width()/2.0);

    $('#dialog-overlay').css({height:maskHeight, width:maskWidth}).fadeIn(50);
    $('#dialog-box').css({top:dialogTop, left:dialogLeft}).fadeIn(200);
}

function hideSettings() {
    $('#dialog-overlay, #dialog-box').fadeOut(50);
    reloadSettings();
    return false;
}

$(document).ready(function () {
    $('#dialog-close-btn, #dialog-overlay').click(hideSettings);
    
    $(window).resize(function () {
        
        //only do it if the dialog box is not hidden
        if (!$('#dialog-box').is(':hidden')) showSettings();
    });     
});