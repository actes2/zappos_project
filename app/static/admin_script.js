function dropButtonAction(id) {
    return document.getElementById('txt_curtable').value = document.getElementById(id).textContent;
}

function submitChangesToDB(){

    let t_headers = document.getElementById('t_headref').children;
    let t_cnt = t_headers.length;

    let key_record = 0;
    let key_index = -1;

    for (let x = 0; x < t_cnt; x++){
        if (t_headers[x].textContent === 'key') {
            key_index = x;
        }
    }
    if (key_index === -1) return console.log("Can't continue as there's no key for reference in this table!");


    for (let x = 0; x < t_cnt; x++){
        if (x != key_index) {
            query_Self_with_Ret('query_self', 'updateRecord¬' + t_headers[x].textContent + '¬' + document.getElementById('dynamic_mod_txt' + x).value + '¬' + document.getElementById('dynamic_mod_txt' + key_index).value);
        }
    }

}

function deleteFromDB(){

    let key_index = -1;

    let t_headers = document.getElementById('t_headref').children;
    let t_cnt = t_headers.length;

    for (let x = 0; x < t_cnt; x++){
        if (t_headers[x].textContent === 'key') {
            key_index = x;
        }
    }
    if (key_index === -1) return console.log("Can't continue as there's no key for reference in this table!");

    query_Self_with_Ret('query_self', 'deleteRecord¬' + document.getElementById('dynamic_mod_txt' + key_index).value);
}

function createNewRcDB(){

    let key_index = -1;

    let t_headers = document.getElementById('t_headref').children;
    let t_cnt = t_headers.length;

    for (let x = 0; x < t_cnt; x++){
        if (t_headers[x].textContent === 'key') {
            key_index = x;
        }
    }
    if (key_index === -1) return console.log("Can't continue as there's no key for reference in this table!");

    request = "createRecord";


    for (let x = 0; x < t_cnt; x++){
        if (x != key_index){
            request = request + "¬" + document.getElementById('dynamic_mod_txt' + x).value
        }
    }

    query_Self_with_Ret('query_self', request);

}

function swapTables(){
    let swap_to = document.getElementById("txt_curtable").value

    query_Self_with_Ret('query_self', "swapTables¬" + swap_to);
}

function createTable(){
    let table = new DataTable('#table_reference');

    table.on('click', 'tbody tr', function () {
        let data = table.row(this).data();

        let t_headers = document.getElementById('t_headref').children;


        for (let x = 0; x < data.length; x++){
            console.log(t_headers[x].textContent + ': ' + data[x]);

            document.getElementById('dynamic_mod_txt' + x).value = data[x]
            // fill our on-screen elements with this
        }
    });
}