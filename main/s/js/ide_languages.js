function changeLanguage(e) {
    var langCode = $(e).val();
    console.log(langCode);
    $.cookie("ps-lang", langCode);
    location.reload();
}