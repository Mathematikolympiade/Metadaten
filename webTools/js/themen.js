
function buildThemenTrees () {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        const allData = JSON.parse(this.responseText);
        let jsTreeJSON = {"core": {"themes": {"dots": false, "stripes": true}}};
        jsTreeJSON['core']['data'] = allData["gebiete"];
        jQuery("#gebieteTree").jstree(jsTreeJSON);
        jsTreeJSON['core']['data'] = allData["methoden"];
        jQuery("#methodenTree").jstree(jsTreeJSON);
    }
    // xhttp.open("GET", "data/store/getThemen.php", true);
    xhttp.open("GET", "https://www.mathematik-olympiaden.de/aufgaben/MetaDaten/store/getThemen.php", true);
    xhttp.send();
}
