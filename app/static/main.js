function selectUsers() {
    var selectElements = $("input[type=checkbox]:checked");
    var eLength = selectElements.length;
    var selectUids = [];
    for (var i = 0; i < eLength; i++)
    {
        var elem = selectElements[i];
        var uid = elem.value;
        selectUids.push(uid);
    }
    $.ajax({
        type: "post",
        url: "/api/users",
        contentType: "application/json;charset=utf-8",
        data: JSON.stringify({"uids": selectUids}),
        success: function(result, status, xhr){
            alert("录入成功");
        },
        error: function(xhr, status, error){
            console.log(JSON.stringify({"uids": selectUids}));
            alert("录入失败");
        }
    });
}
