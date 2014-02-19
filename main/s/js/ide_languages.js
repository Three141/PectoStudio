function inIframe () {
    try {
        return window.self !== window.top;
    } catch (e) {
        return true;
    }
}

function changeLanguage() {
    var langCode = $("#langSelect").val();
    $.cookie("ps-lang", langCode, {expires: 7, path: '/'});
    if (inIframe())
        window.parent.location.reload();
    else location.reload();
}