function color_b_type (type_n) {
    if (type_n === 0) {
        $("#button_type_1").removeClass('type_n').addClass('type_a');
        $("#button_type_2").removeClass('type_a').addClass('type_n');
    }
    if (type_n === 1) {
        $("#button_type_1").removeClass('type_a').addClass('type_n');
        $("#button_type_2").removeClass('type_n').addClass('type_a');
    }
}





function Stop_sound() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/stop_def", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = xhr.responseText;
                if (response === '0') {
                    list("Type_0");
                }
            } else {
                console.error("Помилка при відправці повідомлення!");
            }
        }
    };
    xhr.send("jsonData");
}
 


