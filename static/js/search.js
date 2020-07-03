function sortByRelevance(a, b) {
    if (a["value"] < b["value"]) return 1;
    else if (a["value"] == b["value"]) return 0;
    else return -1;
};

function simpleTemplating(search_results) {


    var div = []



    search_results.forEach(entry => {
        var tmp = $(".template").clone(false);
        tmp.removeClass("template");
        tmp.find(".link").text(entry.title);
        tmp.find(".url").text(entry.page)
        tmp.find(".excerpt").html(entry.desc)
            //tmp.find(".link").text(entry.value);
        tmp.find(".link").attr("href", entry.page);
        tmp.find(".relevance").text(entry.value);
        if (entry["resultType"] == "new")
            tmp.addClass("red");
        else if (entry["resultType"] == "original")
            tmp.addClass("blue");
        else
            tmp.addClass("green");
        div.push(tmp);


    });
    return div;
}

var i = 0,
    j = 0;
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
    if (i == 0) {
        $("#showcase").css("display", "none");
        $("#newsletter").css("display", "block");
        $("#projects").css("display", "block");
        query = $("#search").val();
        $('#search2').val(query);
        i = 1;
    } else {
        query = $("#search2").val();
    }

    $("#results").empty();
    $("#no-results").empty();

    var request = $.ajax({
        url: "http://127.0.0.1:5000/search/" + query
    });
    request.success((results_for_ajax) => {

        var search_results = [];
        // obj = JSON.parse(results_for_ajax);

        obj = JSON.parse(results_for_ajax["results"]);
        if (results_for_ajax["new_keywords"])
            newKeywords = results_for_ajax["new_keywords"];

        obj.forEach(json_object => {
            search_results.push(json_object);
        });
        if (search_results.length < 1) {
            var tmp = $(".no-result-template").clone(false);
            tmp.removeClass("no-result-template");
            tmp.find("#query-value").text(" " + query + " ");
            $("#no-results").append(tmp);
            $('#pagination-container').empty();
            $("#description_col").addClass("hidden");
            $("#results").removeClass("min_height");
            $("#profile_col").find("h5").empty();
        } else {
            var start = new Date().getTime();
            search_results.sort(sortByRelevance);
            var testHTML = simpleTemplating(search_results);
            var desc = $("#description_col");
            desc.removeClass("hidden");
            desc.find("h3").text(testHTML[0].find(".link").text());
            desc.find("p").text(testHTML[0].find(".excerpt").text());
            desc.find(".find_more").text(testHTML[0].find(".url").text());
            desc.find(".find_more").attr("href", testHTML[0].find(".url").text());

            $('#pagination-container').pagination({
                dataSource: search_results,
                pageSize: 5,

                className: 'paginationjs-theme-blue',

                callback: function(data, pagination) {
                    console.log(pagination);
                    $("#results").empty();
                    var html = simpleTemplating(data);
                    $("#results").append(html);

                    $("#results").addClass("min_height");

                    var time_elapsed = (new Date().getTime()) - start;

                    $("#profile_col").find("h5").text("About " + search_results.length + " results (" + (time_elapsed / 1000)+ ' seconds)');
                    $("#profile_col").find('h5').append('<br/>');
                    if (results_for_ajax["new_keywords"]) {
                        $("#profile_col").find("h5").append("Color Key: <span class='color-box' style='background-color: #311b92;'></span> for original results and <span class='color-box' style='background-color: #dd2c00;'></span> for reformulated query results.");
                        $("#profile_col").find("h5").append("<br>New Keywords: " + newKeywords);
                    }

                }
            })

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
