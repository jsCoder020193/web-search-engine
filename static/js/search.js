function sortByRelevance(a, b) {
    if (a["value"] < b["value"]) return 1;
    else if (a["value"] == b["value"]) return 0;
    else return -1;
};

var i=0, j=0;
$(".btn").click(() => {

    // if (j == 0) {
    //     j = 1;
    //     var elem = document.getElementById("progress");
    //     var elem2 = document.getElementById("progressbar");
    //     var width = 1;
    //     elem2.style.width = "100%";
    //     var id = setInterval(frame, 8);
    //     function frame() {
    //       if (width >= 100) {
    //         clearInterval(id);
    //         j = 0;
    //       } else {
    //         width++;
    //         elem.style.width = width + "%";
    //       }
    //     }
    //   }

    var query;
    if(i==0){
        $("#showcase").css("display", "none");
        $("#newsletter").css("display", "block");
        $("#projects").css("display", "block");
        query = $("#search").val();
        $('#search2').val(query); 
        i = 1;
    }else{
        query = $("#search2").val();
    }
    
    $("#results").empty();
    $("#no-results").empty();

    var request = $.ajax({
        url: "http://127.0.0.1:5000/search/" + query
    });
    request.success((results_for_ajax) => {

            var search_results = [];
            obj = JSON.parse(results_for_ajax);

            obj.forEach(json_object => {
                search_results.push(json_object);
            });
        if(search_results.length < 1){
                var tmp = $(".no-result-template").clone(false);
                tmp.removeClass("no-result-template");
                tmp.find("#query-value").text(" "+query+" ");
                $("#no-results").append(tmp);
        }else{
            search_results.sort(sortByRelevance);
            
                search_results.forEach(entry => {
                    var tmp = $(".template").clone(false);
                    tmp.removeClass("template");
                    tmp.find(".link").text(entry.title);
                    tmp.find(".url").text(entry.page)
                    tmp.find(".excerpt").text(entry.desc)
                    //tmp.find(".link").text(entry.value);
                    tmp.find(".link").attr("href", entry.page);
                    tmp.find(".relevance").text(entry.value);
                    $("#results").append(tmp);
                });
        }

        });

    return false;
});

function init() {
    // Clear forms here
    $('#search').val("");
    $('#search2').val("");
}

$(window).ready(init) 
