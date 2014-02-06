function printf(str) {
    var cur = $("#console").val();
    console.log(cur);
    if (cur != "") cur += "\n";
    $("#console").val(cur + str);
    $("#console").animate({ scrollTop: $(document).height() }, "fast");
}

function scanf(title, defaultval) {
    var out = prompt(title, defaultval);
    out = out==null?"":out;
    printf(">>> "+out);
    return out;
}