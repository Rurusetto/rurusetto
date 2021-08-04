window.onload = function() {arrangeWIki()};

function arrangeWIki() {
    if (document.documentElement.clientWidth <= 991) {
        document.getElementById("infobox").classList.remove('col-sm-3');
        document.getElementById("wiki").classList.remove('col-sm-9');
    } else {
        document.getElementById("infobox").classList.add('col-sm-3');
        document.getElementById("wiki").classList.add('col-sm-9');
    }
}