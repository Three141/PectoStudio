function updateFileList() {
    var data = null;
    $.ajax({
        url: "/ajax/all_files.json",
        async: false
    }).success(function(msg){
        data = msg;
    });

    var str = ""; //print the user's files
    for (var i = 0; i < data.my_files.length; i++) {
        str += "<li><a href=\"#\" onclick=\"loadFileByName(this)\">"+data.my_files[i]+"</a></li>\n";
    }
    $("#sidebar #my-files").html(str);

    str = ""; //print the other files
    for (i in data.shared_with_me) {
        str += "<h2>"+i+"</h2>\n<ul>\n";
        for (var j = 0; j < data.shared_with_me[i].length; j++) {
            str += "<li><a href=\"#\" onclick=\"loadFileByName(this)\">"+data.shared_with_me[i][j]+"</a></li>\n";
        }
        str += "</ul>";
    }
    $("#sidebar #shared-files").html(str);
}

function loadFileByName(obj) {
    var name = $(obj).html();

    if ($("#filename").html() != "N/A") {
        if (confirm(gettext("Do you want to save the file before exit?")))
            saveFile();
    }

    $.ajax({
        url: "/ajax/file/"+name+".json",
        async: false
    }).success(function(msg){
        if(!msg.success) {
            var emsg = gettext("An error has occurred while trying to load the file.") + "\n" + gettext("Error: ") + msg.error_msg;
            alert(emsg);
        } else {
            $("#filename").html(msg.name+".pcs");
            $("#editor").val(msg.data);
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function saveFile() {
    if($("#filename").html() == "N/A")
        return;

    var csrftoken = getCookie('csrftoken');
    var name = $("#filename").html();
    name = name.substring(0, name.lastIndexOf("."));

    $.ajax({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr) { xhr.setRequestHeader("X-CSRFToken", csrftoken); },
        type: "POST",
        url: "/ajax/save/"+name+"/",
        data: { data: $("#editor").val() },
        async: false
    }).success(function(msg){
        if(!msg.success) {
            var emsg = gettext("An error has occurred while trying to save the file.") + "\n" + gettext("Error: ") + msg.error_msg;
            alert(emsg);
        } else alert(gettext("The file has been saved!"));
    });
}

function newFile() {
    var fname = null;
    fname = prompt(gettext("Please pick a name:"), "no_name");
    if (fname == null)
        return;

    $.ajax({
        url: "/ajax/new/"+fname+"/",
        async: false
    }).success(function(msg){
        if(!msg.success) {
            var emsg = gettext("An error has occurred while trying to create the file.") + "\n" + gettext("Error: ") + msg.error_msg;
            alert(emsg);
        } else  {
            alert(gettext("The file has been created!"));
            $("#filename").html(fname+".pcs");
            $("#editor").val("");
        }
    });

    updateFileList();
}

function deleteFile() {
    var ans = confirm(gettext("Are you sure you want to delete this file?"));
    if(ans === false || $("#filename").html() == "N/A")
        return
    var name = $("#filename").html();
    name = name.substring(0, name.lastIndexOf("."));

    $.ajax({
        url: "/ajax/delete/"+name+"/",
        async: false
    }).success(function(msg){
        if(!msg.success) {
            var emsg = gettext("An error has occurred while trying to delete the file.") + "\n" + gettext("Error: ") + msg.error_msg;
            alert(emsg);
        } else  {
            alert(gettext("The file has been removed!"));
            $("#filename").html("N/A");
            $("#editor").val("");
        }
    });

    updateFileList();
}