$(document).ready(function () {
    $("#jobForm input").change(function (e) {
        console.log("ady feh elhagys");
        let table = {"jobID": jobID, "type": "editJob"};
        let input = $(this);
        let attrName = input.attr("name");
        let val = 1;
        val = input.val();
        if (val.isEmpty()) {
            return;
        }
        table[attrName] = val;
        $.ajax({
            url: "../requests/jobs.php",
            method: "POST",
            data: table,
            success: function (response) {
                console.log(response);
            },
            error: function (err) {
                console.log(err.responseText);
                alert("Failed to update: " + attrName)
            }
        });
    });
    $("#startForm").submit(function (e) {
        e.preventDefault();
        let form = $(this);
        let actionUrl = form.attr('action');
        $.ajax({
            type: "POST",
            url: actionUrl,
            data: form.serialize(), // serializes the form's elements.
            success: function (data) {
                console.log(data);
                alert("Job Started Successfully");
                location.reload();
            },
            error: function (error) {
                console.log(error.responseText);
                let message = JSON.parse(error.responseText);
                if (message["errorCode"] === -1) {
                    window.location.href = "login.php";
                }
                alert(message["message"]);
            }
        });
    });
    let editButtonPressed = false;
    let parts = $("#parts");
    let table = parts.DataTable({searching: false});
    parts.on('click', 'tbody tr button', function (e) {
        if (editButtonPressed) {
            return;
        }
        e.preventDefault();
        //getting the row
        let parent = $(this).parent().parent();
        let button = $(this);
        let partID = button.attr('dms');
        let actionType = $(this).attr('action-type');
        if (actionType === "edit") {

            editButtonPressed = true;
            let html = button.html();
            button.html("<span class=\"spinner-border spinner-border-sm\" role=\"status\" aria-hidden=\"true\"></span>");
            button.attr("disabled", "");
            let doneFunction = function () {
                button.html(html);
                button.attr("disabled", null);
                editButtonPressed = false;
            };
            getPartModal("edit", doneFunction, doneFunction, partID);

        } else if (actionType === "remove") {
            deletePart(parent, table, partID);
        }

    });
    $("#newJob").on('click', function (e) {
        console.log("Hi");
        if (editButtonPressed) return;
        editButtonPressed = true;
        let button = $(this);
        let html = button.html();
        button.html("<span class=\"spinner-border spinner-border-sm\" role=\"status\" aria-hidden=\"true\"></span>");
        button.attr("disabled", "");
        let doneFunction = function () {
            console.log("Done")
            button.html(html);
            button.attr("disabled", null);
            editButtonPressed = false;
        };
        getPartModal("new", doneFunction, doneFunction);
    })

});
var a = null;

function getPartModal(type, success, error, partID = null) {
    var url = `../requests/getPartModal.php?type=${type}`;
    if (partID) {
        url += `&partID=${partID}`;
    }
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'text',
        success: function (res) {
            console.log(res);
            $("#editModalHolder").html(res);
            $("#partEditor").modal("show");
            success();
        },
        error: function (e) {
            let message = JSON.parse(error.responseText);
            if (message["errorCode"] === -1) {
                window.location.href = "login.php";
                return;
            }
            alert(message["message"]);
            error();
        }
    });
}

function deletePart(row, table, id) {
    $("#deletePartButton").click(function () {

        $.ajax({
            url: '../requests/jobs.php',
            type: 'POST',

            data: {"partID": id, "type": "remove"},
            success: function (res) {
                console.log(res);
                table.row(row).remove().draw();
                $("#deleteModal").modal("hide")
                addToTotalParts(-1);
            },
            error: function (error) {
                console.log(error.responseText);
                let message = JSON.parse(error.responseText);
                if (message["errorCode"] === -1) {
                    window.location.href = "login.php";
                }
                alert(message["message"]);
            }
        });
    })
}

function addToTotalParts(addition) {
    var totalParts = $("#totalParts");
    totalParts.val(Number(totalParts.val()) + addition);
}

String.prototype.isEmpty = function () {
    return (this.length === 0 || !this.trim());
};
