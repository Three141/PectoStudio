function ide_keydown(e) {
    if (e.ctrlKey) {
        if (e.keyCode == 'S'.charCodeAt(0)) {
            e.preventDefault();
            saveFile();
            return;
        }
        if (e.keyCode == 'Q'.charCodeAt(0)) {
            e.preventDefault();
            newFile();
            return;
        }
        if (e.keyCode == 'D'.charCodeAt(0)) {
            e.preventDefault();
            deleteFile();
            return;
        }
        if (e.keyCode == 'E'.charCodeAt(0)) {
            e.preventDefault();
            $('#to-share').prop("checked", !$('#to-share').prop("checked"));
            shareFile();
            return;
        }
        if (e.keyCode == 'R'.charCodeAt(0)) {
            e.preventDefault();
            runFile();
            return;
        }
    }
}

document.addEventListener('keydown', ide_keydown, true);