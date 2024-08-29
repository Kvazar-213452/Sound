// Function to handle menu item click
function yhg(url, color) {
    $("#musx").attr("src", url);
    $("#musx").attr("name", url);
    
    color_ch(color);
}

function color_ch(name) {
    $(".section").removeClass('color_a').addClass('color_n');
    
    $(name).removeClass('color_n').addClass('color_a');
}

$(document).ready(function() {
    yhg('/mu_m', '#div_url_b1');
});