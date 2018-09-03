function capitalizeTerm(sentence, b, e) {
  var res = sentence.trim().split(" "); 
  var newSen = "";
  
  //alert(res);
  
  for (var i = 0; i < res.length; i++) {
    if (b <= i && i < e) {
      newSen += res[i].toUpperCase();
    }
    else {
      newSen += res[i];
    }
    
    if (i != res.length - 1) newSen += " ";
  }
  
  
  //return sentence.substring(0, b) + sentence.substring(b, e).toUpperCase() + sentence.substring(e, sentence.length - 1);
  return newSen;
}

function getSeedTermSpan(sentence, termsInFactor, noWords, b) {
  var index = new Array();
  index.push(b);
  
  if (noWords > 1) {
    for (i = 1; i < noWords; i ++) {
      index.push(parseInt(parseInt(index[i - 1])) + termsInFactor[i - 1].length + 1);
    }
  }
  
  return index;
}

require(['jquery-noconflict'], function(jQuery) {


    Window.implement('$', function(el, nc){
        return document.id(el, nc, this.document);
    });
    var $ = window.jQuery;
    
    
    selectedIds = new Array();
checkboxes = new Array();

inputElements = document.getElementsByTagName('input');
sentence = document.getElementsByClassName("word_split");
b1 = document.getElementsByClassName('b1val');
b2 = document.getElementsByClassName('b2val');
e1 = document.getElementsByClassName('e1val');
e2 = document.getElementsByClassName('e2val');
hiddenFieldFactor1 = document.getElementsByClassName('factor1');
hiddenFieldFactor2 = document.getElementsByClassName('factor2');
  
$(".word_split").text(capitalizeTerm($(".word_split").text(), parseInt(b1[0].value), parseInt(e1[0].value)));
$(".word_split").text(capitalizeTerm($(".word_split").text(), parseInt(b2[0].value), parseInt(e2[0].value)));

hiddenFieldFactor1[0].value = hiddenFieldFactor1[0].value.toUpperCase();
hiddenFieldFactor2[0].value = hiddenFieldFactor2[0].value.toUpperCase();
    
noWordsFactor1 = hiddenFieldFactor1[0].value.split(/-| /).length;
termsInFactor1 = hiddenFieldFactor1[0].value.split(/-| /);
noWordsFactor2 = hiddenFieldFactor2[0].value.split(/-| /).length;
termsInFactor2 = hiddenFieldFactor2[0].value.split(/-| /);

  
    (function($){function injector(t,splitter,klass,after){var a=t.text().split(splitter),inject='';if(a.length){$(a).each(function(i,item){inject+='<span class="'+klass+(i+1)+'">'+item+'</span>'+after});t.empty().append(inject)}}var methods={init:function(){return this.each(function(){injector($(this),'','char','')})},words:function(){return this.each(function(){injector($(this),' ','word',' ')})},lines:function(){return this.each(function(){var r="eefec303079ad17405c889e092e105b0";injector($(this).children("br").replaceWith(r).end(),r,'line','')})}};$.fn.lettering=function(method){if(method&&methods[method]){return methods[method].apply(this,[].slice.call(arguments,1))}else if(method==='letters'||!method){return methods.init.apply(this,[].slice.call(arguments,0))}$.error('Method '+method+' does not exist on jQuery.lettering');return this}})(jQuery);
   
Array.prototype.remove = function(x) {
    for(i in this){
        if(this[i].toString() == x.toString()){
            this.splice(i,1)
        }
    }
};
  
Array.prototype.clear = function() {
    this.splice(0, this.length);
};
  
String.prototype.trim = function () {
  return this.replace(/^\s*/, "").replace(/\s*$/, "");
}

 $(".word_split").lettering('words');
    
    sentenceText = $(".word_split").text();
    index1 = getSeedTermSpan(sentenceText, termsInFactor1, noWordsFactor1, parseInt(b1[0].value));
    index2 = getSeedTermSpan(sentenceText, termsInFactor2, noWordsFactor2, parseInt(b2[0].value));
    
    var startOffset = 0;
    
    $('.hiddeninput').first().parent().parent().css("display","none");
    
    var color = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f','#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928','#fbb4ae','#b3cde3','#ccebc5','#decbe4','#fed9a6','#ffffcc'];

    var backgroundcolor = ["#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","","#ccebc5","#ffed6f","#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","","#cab2d6","#6a3d9a","#ffff99","#b15928","#fbb4ae","#fbb4ae","#ccebc5","#decbe4","#fed9a6","#ffffcc"];
    var bordercolor = ["#4d9387","#bfbf73","#7e7a9a","#bb4032","#407193","#bd7422","#73be29","#bc8da5","#999999","#7c407d","","#ccebc5","#ffed6f","#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","","#cab2d6","#6a3d9a","#ffff99","#b15928","#fbb4ae","#fbb4ae","#ccebc5","#decbe4","#fed9a6","#ffffcc"];
    
    var selectedtags = new Array();
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
                
                var elem_css = "";
            
                if (parseInt(b1[0].value) < parseInt(index) && parseInt(index) <= parseInt(e1[0].value)) {
                  elem_css += "color:#00B9FF;";
                  elem_css += "font-size:medium;";
                  elem_css += "font-weight:bold;";
                  elem_css += "text-transform: uppercase;"
                }
                
                if (parseInt(b2[0].value) < parseInt(index) && parseInt(index) <= parseInt(e2[0].value)) {
                  elem_css += "color:#00B9FF;";
                  elem_css += "font-size:medium;";
                  elem_css += "font-weight:bold;";
                  elem_css += "text-transform: uppercase;"
                }
                

                var pretext = "<span class='word' termnumber='"+parseInt(parseInt(index)+parseInt(termnumber))+"' style='" + elem_css + "'>";
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
    
    
    var spans = $("#videosubtitles.passage").find("span").each(function() {
      if ($(this).text() == "-" || $(this).text() == "/") {
        startOffset = startOffset - 1;
      }
      
    /*  var idNumber = $(this).attr("class").slice(4);
      $(this).attr("id", idNumber);*/
      var idNumber = $(this).attr("termnumber") - 1;
      alert($(this).text());
      
      var i = sentenceText.indexOf($(this).text(), startOffset);
      
     /* for (j = 0; j < index1.length; j ++) {
        if (i == index1[j]) {
          $(this).css("color", "darkred");
        }
      }
      
      for (j = 0; j < index2.length; j ++) {
        if (i == index2[j]) {
          $(this).css("color", "darkred");
        }
      }*/
      
      if (parseInt(b1[0].value) < idNumber && idNumber <= parseInt(e1[0].value)) {
        $(this).css("color", "#00B9FF");
        $(this).css("font-size", "medium");
        $(this).css("font-weight", "bold");
      }
      
      if (parseInt(b2[0].value) < idNumber && idNumber <= parseInt(e2[0].value)) {
        $(this).css("color", "#00B9FF");
        $(this).css("font-size", "medium");
        $(this).css("font-weight", "bold");
      }
      
    });


    var counterId = 0;
    function highlightTerm(passage, start) {


        var id  = counterId++;

        if(!$(start).parents('#selection').length) { // if no selection is made and maximum matches is not reached

            start.wrapAll("<span style='background-color: "+backgroundcolor[id]+"; border: 1px solid "+bordercolor[id]+";' class='term rel" + id + "term' id='selection' />");

            $(passage).find('span:not(#selection)').bind('mouseover', function(e) {
                highlightMultiple(start, $(e.target), passage, id);
            });

        } else {

            $(passage).find('#selection').removeAttr('id');

        }
    }

    // highlight range of terms
    function highlightMultiple(start, end, passage, id) {


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
            $(start).nextUntil(end.next()).andSelf().wrapAll("<span style='background-color: "+backgroundcolor[id]+"; border: 1px solid "+bordercolor[id]+";' class='term rel" + id + "term' id='selection' />");

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
          $('.submit').attr('disabled',false);
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