function buildThemenTrees() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        const allData = JSON.parse(this.responseText);
        let jsTreeJSON = {"core": {"themes": {"dots": false, "stripes": true}}};
        jsTreeJSON['core']['data'] = allData["gebiete"];
        jQuery("#gebieteTree").jstree(jsTreeJSON);
        jsTreeJSON['core']['data'] = allData["methoden"];
        jQuery("#methodenTree").jstree(jsTreeJSON);
    }
    xhttp.open("GET", "../getThemen.php", true);
    // xhttp.open("GET", "https://www.mathematik-olympiaden.de/aufgaben/metadaten/store/getThemen.php", true);
    xhttp.send();
}

function searchAction(arg) {
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
    alert(selectedData);
    jQuery("#suchButton").css("background-color", "forestgreen");
}