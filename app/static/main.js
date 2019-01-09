function saveUsers(status) {
    var selectElements = $("input[type=checkbox]:checked");
    var eLength = selectElements.length;
    var selectUids = [];
    for (var i = 0; i < eLength; i++)
    {
        var elem = selectElements[i];
        var uid = elem.value;
        selectUids.push(uid);
    }
    var method = 'post';
    var msg = '录入'
    if (status == 0)
    {
        method = 'delete';
        msg = '还原'
    }
    $.ajax({
        type: method,
        url: "/api/users",
        contentType: "application/json;charset=utf-8",
        data: JSON.stringify({"uids": selectUids}),
        success: function(result, status, xhr){
            if (confirm(msg + "成功")){
                window.location.reload();
            }
        },
        error: function(xhr, status, error){
            console.log(JSON.stringify({"uids": selectUids}));
            alert(msg + "失败");
        }
    });
}

function selectAll(){
    var status = $("#selectA")[0].checked;
    console.log(status);
    $("input[name=box]").each(function () {
        this.checked = status;
    })
}