function buildProblemTable(tableData) {
    jQuery("#problemTable").append("<tbody>");
    let tbodyNode = jQuery("#problemTable").find("tbody")[0];
    const rowClass = {true: "even", false: "odd"};
    parity = true;
    for (const row of tableData) {
        parity = !parity;
        let rowNode = jQuery("<tr>");
        for (const cell of row) {
            rowNode.append(
                jQuery('<td class=></td>').addClass(rowClass[parity]).html(cell)
            );
        }
        rowNode.appendTo(tbodyNode);
    }
}


function searchProblems(arg) {
    jQuery("#suchButton").css("background-color", "maroon");
    let selectedData = [];
    let selectedIndexes;
    selectedIndexes = $("#gebieteTree").jstree("get_selected", true);
    jQuery.each(selectedIndexes, function (index, value) {
        selectedData.push(selectedIndexes[index].id);
    });
    selectedIndexes = $("#methodenTree").jstree("get_selected", true);
    jQuery.each(selectedIndexes, function (index, value) {
        selectedData.push(selectedIndexes[index].id);
    });
    // alert(selectedData);

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        const tableData = JSON.parse(this.response);
        buildProblemTable(tableData);
        // let dataTableJSON = {};
        // dataTableJSON["data"] = tableData;
        // jQuery("#problemTable").dataTable(dataTableJSON);
    }
    getURL = "../getProbleme.php?themen=" + JSON.stringify(selectedData);
    xhttp.open("GET", getURL, true);
    // xhttp.open("GET", "https://www.mathematik-olympiaden.de/aufgaben/metadaten/store/getThemen.php", true);
    xhttp.send();

    jQuery("#suchButton").css("background-color", "forestgreen");
}