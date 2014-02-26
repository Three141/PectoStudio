function printf(str) {
    var cur = $("#console").val();
    console.log(cur);
    if (cur != "") cur += "\n";
    $("#console").val(cur + str);
    $("#console").animate({ scrollTop: $(document).height() }, "fast");
}

function scanf(title) {
    title = title==undefined?"":title;
    var out = prompt(title, "");
    out = out==null?"":out;
    printf(">>> "+out);
    return isNumeric(out)?parseFloat(out):out;
}

function runCode() {
    if (openFile.name == "N/A") {
        alert(gettext("Please open a file first"));
        return;
    }

    var program;

    try {
        program = newpecto.parse($("#editor").val());
        printf("-----"+gettext("Program starts")+"-----");
        eval(program.print("", "  "));
        printf("-----"+gettext("Program ended")+"-----");
    } catch (exception) {
        alert(exception.name + ":  " + exception.message);
    }
}