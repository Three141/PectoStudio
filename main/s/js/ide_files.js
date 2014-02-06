function updateFileList() {
    var data = null;
    $.ajax({
        url: "/ajax/all_files.json",
        async: false
    }).success(function(msg){
        data = msg;
    });

    var str = "";
    for (var i = 0; i < data.files.length; i++) {
        str += "<li><a href=\"#\" onclick=\"loadFileByName(this)\">"+data.files[i]+"</a></li>\n";
    }
    $("#sidebar ul").html(str);
}

function loadFileByName(obj) {
    var data = null;
    var name = $(obj).html();
    $.ajax({
        url: "/ajax/file/"+name+".json",
        async: false
    }).success(function(msg){
        data = msg;
    });

    $("#filename").html(data.name+".pcs");
    $("#editor").val(data.data);
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
        if(!msg.success)
            alert("שגיאה התרחשה בתהליך השמירה");
        else alert("השמירה בוצעה בהצלחה!");
    });
}

function newFile() {
    var fname = null;
    while(!(fname = prompt("אנא בחר שם לקובץ החדש", "no_name")));

    $.ajax({
        url: "/ajax/new/"+fname+"/",
        async: false
    }).success(function(msg){
        if(!msg.success) {
            alert("שגיאה התרחשה בפתיחת הקובץ");
        } else  {
            alert("הקובץ נפתח בהצלחה!");
            $("#filename").html(fname+".pcs");
            $("#editor").val("");
        }
    });

    updateFileList();
}

function deleteFile() {
    var ans = confirm("האם אתה בטוח שאתה רוצה למחוק קובץ זה?");
    if(ans === false || $("#filename").html() == "N/A")
        return
    var name = $("#filename").html();
    name = name.substring(0, name.lastIndexOf("."));

    $.ajax({
        url: "/ajax/delete/"+name+"/",
        async: false
    }).success(function(msg){
        if(!msg.success) {
            alert("שגיאה התרחשה במחיקת הקובץ");
        } else  {
            alert("הקובץ נמחק בהצלחה!");
            $("#filename").html("N/A");
            $("#editor").val("");
        }
    });

    updateFileList();
}