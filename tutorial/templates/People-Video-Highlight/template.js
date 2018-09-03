require(['jquery-noconflict'], function(jQuery) {


    Window.implement('$', function(el, nc){
        return document.id(el, nc, this.document);
    });
    var $ = window.jQuery;
    $('.hiddeninput').first().parent().parent().css("display","none");
    
                
    
    var color = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f','#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928','#fbb4ae','#b3cde3','#ccebc5','#decbe4','#fed9a6','#ffffcc'];

    var backgroundcolor = ["#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","","#ccebc5","#ffed6f","#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","","#cab2d6","#6a3d9a","#ffff99","#b15928","#fbb4ae","#fbb4ae","#ccebc5","#decbe4","#fed9a6","#ffffcc"];
    var bordercolor = ["#4d9387","#bfbf73","#7e7a9a","#bb4032","#407193","#bd7422","#73be29","#bc8da5","#999999","#7c407d","","#ccebc5","#ffed6f","#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","","#cab2d6","#6a3d9a","#ffff99","#b15928","#fbb4ae","#fbb4ae","#ccebc5","#decbe4","#fed9a6","#ffffcc"];

    $().ready(function(){
        var description = $('#videodescription').html();
           // var desctags = descdata.split('_###_');
            var totaloffset = parseInt(0);

            //newsplit
            var splitdesc = description.split(/\s+/);
            description = "";
            var descoffset = 0;
            var termnumber = 0;
            $(splitdesc).each(function(index,value){
                if (value.length == 0) return true;

                var pretext = "<span startchar='"+(descoffset+index)+"' class='word' termnumber='"+index+"'>";
                var posttext = "</span>";
                descoffset += parseInt(parseInt(value.length) + parseInt(index));
                description = description +" "+ pretext + value + posttext;
                termnumber = index;
            });
            $('#videodescription').html(description);

            var subtitles = $('#videosubtitles').html();

            var totaloffset = parseInt(0);
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

    // all events that can be captured. log everything a worker does
    var events = ['abort', // Fires when the loading of an audio/video is aborted
        'canplay', // Fires when the browser can start playing the audio/video
        'canplaythrough', // Fires when the browser can play through the audio/video without stopping for buffering
        'durationchange', // Fires when the duration of the audio/video is changed
        'emptied', // Fires when the current playlist is empty
        'ended', // Fires when the current playlist is ended
        'error', //  Fires when an error occurred during the loading of an audio/video
        'loadeddata', // Fires when the browser has loaded the current frame of the audio/video
        'loadedmetadata', // Fires when the browser has loaded meta data for the audio/video
        'loadstart', // Fires when the browser starts looking for the audio/video
        'pause', // Fires when the audio/video has been paused
        'play', // Fires when the audio/video has been started or is no longer paused
        'playing', // Fires when the audio/video is playing after having been paused or stopped for buffering
        'progress', //  Fires when the browser is downloading the audio/video
        'ratechange', // Fires when the playing speed of the audio/video is changed
        'seeked', // Fires when the user is finished moving/skipping to a new position in the audio/video
        'seeking', // Fires when the user starts moving/skipping to a new position in the audio/video
        'stalled', // Fires when the browser is trying to get media data, but data is not available
        'suspend', // Fires when the browser is intentionally not getting media data
        'timeupdate', //  Fires when the current playback position has changed
        'volumechange', // Fires when the volume has been changed
        'waiting' // Fires when the video stops because it needs to buffer the next frame
    ];

    $('.submit').attr('disabled',true);
    
  
     for(e=0; e < events.length; e++) {
        $('.video').on(events[e], function(event) {
            $(this).parents('.jsawesome').find('input.e_' + event.type).val( function(i, v) {
                return parseInt(v) + 1;
            });
            
            if(event.type == 'ended' && $(".e_ended").filter(function() { return  $(this).val() >= 1; }).length == $('.e_ended').length) {
              
                $('.submit').attr('disabled',false);
            }
        });
    }

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

        $('#videodescription').find('.term').each(function(index,value)
        {
            var tempa = new Array();
            var temps = "";
            $(value).find(".word").each(function(index,value){
                if (index != 0) temps += " ";
                temps+= $(value).text();
            });

            var selector = $(value).attr("class");
            var findin = '#videodescription';
            selector = "." + selector.split(" ").join(".");
            tempa.push(selector);
            tempa.push(temps);
            tempa.push(findin);

            found.push(tempa);
        });

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


        var subdata = new Array();
        var descdata = new Array();
        var allData = new Array();

        $(found).each(function (index,value){

            var orig = $(value[2]).find(value[0]).first();
            var newit = "<span findin='"+value[2]+"'tagselector='"+value[0]+"' class='tags_list_span' style='border: "+ $(orig).css("border") +";background-color: "+$(orig).css("background-color")+"'><span class='deletetag'>[x]</span> "+value[1]+"</span><br />";
            if (value[2].indexOf("subtitle") > -1)
            {
                subdata.push(value[1]);
                allData.push(value[1]);
            } else if (value[2].indexOf("description") > -1) {
                descdata.push(value[1]);
                allData.push(value[1]);
            }
            $('#tags_list').append(newit);
        });
        console.log(descdata);
        console.log(subdata);
        console.log(allData);
        $(".hidden.cml_field > .taggedindescription").attr("value",JSON.stringify(descdata));
        $(".hidden.cml_field > .taggedinsubtitles").attr("value",JSON.stringify(subdata));
        
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