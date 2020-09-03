function copycell(id) {
    var text = document.getElementById(id).innerHTML.replace(/\n|<.*?>/g,'');
    navigator.clipboard.writeText(text);
};
