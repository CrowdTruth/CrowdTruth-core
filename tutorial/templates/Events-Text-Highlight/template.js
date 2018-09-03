require(['jquery-noconflict'], function(jQuery) {


    Window.implement('$', function(el, nc){
        return document.id(el, nc, this.document);
    });
    var $ = window.jQuery;
    $('.hiddeninput').first().parent().parent().css("display","none");
    
                
    
    var color = ['#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7'];

    var backgroundcolor = ['#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7'];
    
    var bordercolor = ['#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7','#8dd3c7'];

    $().ready(function(){
        
           // var desctags = descdata.split('_###_');
            var totaloffset = parseInt(0);
            var descoffset = 0;
            var termnumber = 0;


            var subtitles = $('#videosubtitles').html();

            termnumber++;
            //newsplit
            var splitsubs = subtitles.split(/\s+/);
            subtitles = "";
            $(splitsubs).each(function(index,value){
                if (value.length == 0) return true;



                var pretext = "<span class='word' termnumber='"+parseInt(parseInt(index)+parseInt(termnumber))+"'>";
                var posttext = "</span>";

                subtitles = subtitles +" "+ pretext + value + posttext;

            });
            $('#videosubtitles').html(subtitles);


            $("#videodescription > .word").mousedown(function(e) {

                highlightTerm('#videodescription', $(e.target));

            }).mouseup(function() {
                $('span').unbind('mouseover');

                if($('#videodescription > #selection').length) {
                    endSelection($(this).parents('.alignment'));
                }
                updateSelected();
            });

            $("#videosubtitles > .word").mousedown(function(e) {

                highlightTerm('#videosubtitles', $(e.target));

            }).mouseup(function() {
                $('span').unbind('mouseover');

                if($('#videosubtitles > #selection').length) {
                    endSelection('#videosubtitles');
                }
                updateSelected();
            });
    });

    $('.keywords').on('input',function(e){
            var tags = $.map($(this).val().split(","), $.trim);
    
            var result = [];
            var error = 0;
            $.each(tags, function(i, v) {
                if(v.length > 0 && v != " ") {
                    if(v.length < (15 * v.split(' ').length) && v.split(' ').length < 4 && v.match(/^([a-zA-Z0-9 _-]+)$/)) {
                        result += "<span class='tag btn btn-success btn-xs'>" + v + "</span>";
                    } else {
                        result += "<span class='tag btn btn-danger btn-xs'>" + v + "</span>";
                        error = 1;
                    }
                }
            });
            if(error == 1) {
                $(this).parents('.jsawesome').find('.instructions').show();
            } else {
                $(this).parents('.jsawesome').find('.instructions').hide();
            }
            $(this).parents('.jsawesome').find('.tags').html(result);
        });



    var counterId = 0;
    function highlightTerm(passage, start) {


        var id  = counterId++;

        if(!$(start).parents('#selection').length) { // if no selection is made and maximum matches is not reached

            start.wrapAll("<span style='background-color: white; border: 1px solid "+bordercolor[id]+";' class='term rel" + id + "term' id='selection' />");

            $(passage).find('span:not(#selection)').bind('mouseover', function(e) {
                highlightMultiple(start, $(e.target), passage, id);
            });

        } else {

            $(passage).find('#selection').removeAttr('id');

        }
    }

    // highlight range of terms
    function highlightMultiple(start, end, passage, id) {
        // ignore margins between elements

        $(passage).find('#selection').contents().unwrap();
        if(start.is(end)) { // single element
            $(start).wrapAll("<span class='term rel" + id + "term' id='selection'/>");
        } else { // if range of elements
            if($(passage).find('span').index(start) > $(passage).find('span').index(end)) { // swap if end is before start
                var temp = end;
                end = start;
                start = temp;
            }


            if(!start.parent().not($('#selection')).is(end.parent().not($('#selection')))) {
                // common parent element
                var common = end.parents().not($('#selection')).has(start).first();

                if(start.parent('.term').not(common).length) { // if word has a parent term
                    start = $(common).children().has(start);
                    // $(start).parent('.term');
                }

                if(end.parent('.term').not(common).length) {
                    end = $(common).children().has(end);
                    //end = $(end).parent('.term');
                }
            }
            // highlight range
            $(start).nextUntil(end.next()).andSelf().wrapAll("<span style='background-color: white; border: 1px solid "+bordercolor[id]+";' class='term rel" + id + "term' id='selection' />");

        }
    }



    // get word range index
    function selectionIndex(passage) {
        var selection = $(passage).find('#selection .word');
        var startId = $(passage).find('.word').index(selection.first());
        if(selection.length == 1) { // single word
            return startId;
        } else { // range of words
            return startId + "-" + (startId + selection.length - 1);
        }
    }

    // finish selection and link terms
    function endSelection(alignment) {
        var relId = $(alignment)[0].relId;


        $(alignment).find('.rel' + relId + 'a').val(selectionIndex($(alignment).find('#passage1')));

        $(alignment).find('.rel' + relId).before('<span class=\'term rel' + relId + 'term\'>' + $(alignment).find('#passage1 #selection .word').not(":last").append(" ").end().text() + '</span>');

        $(alignment).find('.rel' + relId).removeClass('hidden').parent().parent().removeClass('hidden');


        $(alignment).find('#selection').removeAttr('id');
        //   updateSelected();

    }

    function updateSelected()
    {
        var found = new Array();
        $('#videosubtitles').find('.term').each(function(index,value)
        {
            var tempa = new Array();
            var temps = "";
            $(value).find(".word").each(function(index,value){
                if (index != 0) temps += " ";
                temps+= $(value).text();
            });

            var selector = $(value).attr("class");
            var findin = '#videosubtitles';
            selector = "." + selector.split(" ").join(".");
            tempa.push(selector);
            tempa.push(temps);
            tempa.push(findin);

            found.push(tempa);
        });
        $('#tags_list').html("");

        var allData = new Array();

        $(found).each(function (index,value){

            var orig = $(value[2]).find(value[0]).first();
            var newit = "<span findin='"+value[2]+"'tagselector='"+value[0]+"' class='tags_list_span' style='border: "+ $(orig).css("border") +";background-color: "+$(orig).css("background-color")+"'><span class='deletetag'>[x]</span> "+value[1]+"</span><br />";

                allData.push(value[1]);
            
            $('#tags_list').append(newit);
        });

        console.log(allData);
        $(".hidden.cml_field > .tagged_events").attr("value",JSON.stringify(allData));

        if (allData.length != 0) {
          $('.notPossible').hide();
        }
        else {
          $('.notPossible').show();
        //  $('.submit').attr('disabled',true);
        }

        $('.deletetag').click(function(){
            var selector = $(this).parent().attr("tagselector");
            var findin = $(this).parent().attr("findin");
            $(findin).find(selector).first().contents().unwrap();
            updateSelected();
        });
        

    }
});