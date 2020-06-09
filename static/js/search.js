function sortByRelevance(a, b) {
    if (a["value"] < b["value"]) return 1;
    else if (a["value"] == b["value"]) return 0;
    else return -1;
};
$(".btn").click(() => {

    var query = $("#search").val();
    $("#results").empty()




    var request = $.ajax({
        url: "http://127.0.0.1:5000/search/" + query
    });
    request.success((results_for_ajax) => {
        var search_results = [];
         obj = JSON.parse(results_for_ajax);

        obj.forEach(json_object => {
            search_results.push(json_object);
        });
        
        search_results.sort(sortByRelevance);
        
            search_results.forEach(entry => {
                var tmp = $(".template").clone(false);
                tmp.removeClass("template");
                tmp.find(".link").text(entry["page"]);
                //tmp.find(".link").text(entry.value);
                tmp.find(".url").attr("href", entry.page);
                tmp.find(".relevance").text(entry.value);
                $("#results").append(tmp);
            });

        
    });
        



    return false;
});