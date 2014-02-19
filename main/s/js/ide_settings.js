function cancel() {
    window.parent.hideSettings();
}

function apply() {
    // 1st setting - lang
    changeLanguage();
    cancel();
}