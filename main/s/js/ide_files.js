var openFile = {
    name: "N/A",
    owner: false, //indicates self
    shared: false,
    initVal: "",
    is_changed: function() {
        if ($("#editor").val() != this.initVal)
            return true;
        return false;
    }
}

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
        str += "<li"+((data.my_files[i]==openFile.name&&!openFile.owner)?" class=\"in-use\"":"")+"><a href=\"javascript:void(0)\" onclick=\"loadFileByName(this)\">"+data.my_files[i]+"</a></li>\n";
    }
    $("#sidebar #my-files").html(str);

    str = ""; //print the other files
    for (i in data.shared_with_me) {
        str += "<h2>"+ i.split(" | ").reverse()[0]+"</h2>\n<ul>\n";
        for (var j = 0; j < data.shared_with_me[i].length; j++) {
            str += "<li"+((data.shared_with_me[i][j]==openFile.name&&openFile.owner==i.split(" | ")[0])?" class=\"in-use\"":"")+"><a href=\"javascript:void(0)\" onclick=\"loadFileByName(this, '"+i.split(" | ")[0]+"')\">"+data.shared_with_me[i][j]+"</a></li>\n";
        }
        str += "</ul>";
    }
    $("#sidebar #shared-files").html(str);
}

function loadFileByName(obj, owner) {
    var name = $(obj).html();
    var is_shared = false;

    if (typeof owner !== 'undefined') {
        is_shared = true;
    }

    if (openFile.name != "N/A" && !openFile.owner && openFile.is_changed()) {
        if (confirm(gettext("Do you want to save the file before exit?")))
            saveFile();
    }

    $.ajax({
        url: (is_shared?("/ajax/file/"+owner+"/"+name+".json"):("/ajax/file/"+name+".json")),
        async: false
    }).success(function(msg){
        if(!msg.success) {
            var emsg = gettext("An error has occurred while trying to load the file.") + "\n" + gettext("Error: ") + msg.error_msg;
            alert(emsg);
        } else {
            openFile.name = msg.name;
            openFile.owner = is_shared?owner:false;
            openFile.shared = msg.shared;
            openFile.initVal = msg.data;
            $("#filename").html(msg.name+".pcs");
            $("#editor").val(msg.data);
            $('#to-share').prop("checked", msg.shared);
        }
    });

    updateFileList();
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
    if(openFile.name == "N/A")
        return;
    if(openFile.owner != false)
    {
        $('#to-share').prop("checked", !$('#to-share').prop("checked"));
        alert(gettext('You\'re not allowed to perform this action'));
        return;
    }

    var csrftoken = getCookie('csrftoken');
    var name = openFile.name;

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
        } else {
            alert(gettext("The file has been saved!"));
            openFile.initVal = $("#editor").val();
        }
    });
}

function shareFile() {
    if(openFile.name == "N/A") {
        alert(gettext("Please open a file first"));
        $('#to-share').prop("checked", false);
        return;
    }
    if(openFile.owner != false)
    {
        alert(gettext('You\'re not allowed to perform this action'));
        return;
    }

    var name = openFile.name;

    $.ajax({
        url: "/ajax/share/"+name+"/",
        async: false
    }).success(function(msg){
        if(!msg.success) {
            var emsg = gettext("An error has occurred while trying to share the file.") + "\n" + gettext("Error: ") + msg.error_msg;
            alert(emsg);
        } else {
            alert(msg.message);
        }
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
            openFile.name = fname;
            openFile.owner = false;
            $("#filename").html(fname+".pcs");
            $("#editor").val("");
            $('#to-share').prop("checked", false);
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
            openFile.name = "N/A";
            openFile.owner = false;
            $("#filename").html("N/A");
            $("#editor").val("");
            $('#to-share').prop("checked", false);
        }
    });

    updateFileList();
}