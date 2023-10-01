function query_Self_with_Ret(_index, _data, _ret="", _type="") {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // We POST then receive here:

            // I could do a case-switch condition here but to be frank, it's better without in this context.
            if (_ret !== "") {
                //console.log(xhttp.responseText);
                if (_type === "txt") document.getElementById(_ret).innerHTML = xhttp.responseText;
                else if (_type === "img") document.getElementById(_ret).src = xhttp.responseText;
                else if (_type === "") console.log(xhttp.responseText);

            }
            if (xhttp.responseText === "relog"){
                window.location.href = '/';
            }
            return true;
        }
        return false;
    };

    xhttp.open("POST", _index);


    xhttp.send(_data);
}