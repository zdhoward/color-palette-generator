function copycell(id) {
    var text = document.getElementById(id).innerHTML;
    navigator.clipboard.writeText(text);
};
