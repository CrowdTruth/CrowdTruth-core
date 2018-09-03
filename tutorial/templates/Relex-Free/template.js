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
  
  //Ensure MooTools is where it must be
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
    var spans = $(".word_split").find("span").each(function() {
      if ($(this).text() == "-" || $(this).text() == "/") {
        startOffset = startOffset - 1;
      }
      
      var idNumber = $(this).attr("class").slice(4);
      $(this).attr("id", idNumber);
      
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
    
  
  $('.hiddeninput').first().parent().parent().css("display","none");

  $('.submit').attr('disabled',true);
    
  var sentence = $('.people').html();
  $('.people').html("");
  
  jQuery.fn.reverse = [].reverse;
 
 

    // sort the inserts reversed, otherwise adding text will screw up the index positions.
  function sort_by_column(a,b) {
    return ((a[0] > b[0]) ? -1 : ((a[0] < b[0]) ? 1 : 0));
  }
  
  
  $('.placeholder').click(function() {
      
      if ($(this).attr("tagid") == "no_causal_relation") {
        $('.clickbutton').each(function(){
          var tagid = $(this).attr('tagid');
          console.log(tagid);
          if (tagid == 'no_causal_relation') {
            if ($(this).hasClass('btn-error'))
              $(this).removeClass('btn-error');
            else {
              $(this).addClass('btn-error');
              $('.clickbutton.btn-success').each(function(){
                $(this).removeClass('btn-success');
              });
              
            }
          }
        });
        $(".container #text_container").html(sentence);
      }
      else {
        if ($(this).find('.clickbutton').hasClass('btn-success'))
        {
          $(this).find('.clickbutton').removeClass('btn-success');
        } else {
          $(this).find('.clickbutton').addClass('btn-success');
          $('.clickbutton.btn-error').each(function(){
            $(this).removeClass('btn-error');
          });
          
        }
      }
      updateSelected();
    });
    
  $('.placeholder').on("hover", function() {
    console.log("faf");
    // highlight words in the sentence when mouse over an option
    var tagid = $(this).attr('tagid');
    console.log(tagid);
    if (tagid != 'no_causal_relation') {
      var events = tagid.split("--");
      
      if (events.length == 1) {
        events = tagid.split("-r-");
      }
      var event1 = events[0].split("_");
      var event2 = events[1].split("_");
    
  
  // Preprocess
  // load and parse the clusters

      var eventList = [];
      eventList.push([parseInt(event1[1]),'<b id="' + event1[0] + '" range="' + event1[1] + '-' + event1[2] + '" >']);
      eventList.push([parseInt(event1[2]),'</b>']);
      eventList.push([parseInt(event2[1]),'<b id="' + event2[0] + '" range="' + event2[1] + '-' + event2[2] + '" >']);
      eventList.push([parseInt(event2[2]),'</b>']);
     
      eventList.sort(sort_by_column);
     
      $(".container #text_container").html(sentence);
     
      $(".container #text_container").html(function(i, val) {
        var output = val;
        for(i = 0; i < eventList.length; i++) {
          output = [output.slice(0, eventList[i][0]), eventList[i][1], output.slice(eventList[i][0])].join('');
        }
        return output;
      });
    }
    else {
      $(".container #text_container").html(sentence);
    }
  });
  
  function updateSelected() {
    var relations = Array();
    var no_relations = Array();
    $('.clickbutton.btn-success').each(function(){
      var tagid = $(this).attr('tagid');
      relations.push(tagid);
    });
    
    $('.clickbutton.btn-error').each(function(){
      var tagid = $(this).attr('tagid');
      relations.push(tagid);
    });
    
    console.log(relations);
        
    $(".hidden.cml_field > .relations").attr("value",JSON.stringify(relations));
    
    console.log($(".hidden.cml_field > .relations").val() );
    if ($(".hidden.cml_field > .relations").val() == '["no_causal_relation"]') {

      $('#laststep').removeClass("hidden");
      $(".hidden.cml_field > .explanation").attr("value","");
      $('.submit').attr('disabled',true);
    }
    else if ($(".hidden.cml_field > .relations").val() != "[]"){
          $('#laststep').addClass("hidden");;
          $(".hidden.cml_field > .explanation").attr("value","");
          $('.submit').attr('disabled',false);
      }
      else {
        $('.submit').attr('disabled',true);
        $('#laststep').addClass("hidden");
        $(".hidden.cml_field > .explanation").attr("value","");
      }
    /*    if ($(".hidden.cml_field > .relations").val() != "[]")
          $('.submit').attr('disabled',false);
        else
          $('.submit').attr('disabled',true);
    */
  }
  
  
  $('#notpossible').on("change keyup blur focus keydown", function() {
    var explanation = $(this).val().trim();
    
    if (explanation.length < 2) {
      $('.submit').attr('disabled',true);
    }
    else {
      $('.submit').attr('disabled',false);
    }
    
    $(".hidden.cml_field > .explanation").attr("value",explanation);
  });
  
  
/*  
  $('.clickbutton').on("hover", function() {

    //var currentSentence = $(".alignment #people").text();
    console.log(currentSentence);
    var tagid = $(this).attr('tagid');
    if (tagid != 'no_event') {
      var events = tagid.split("_");
    //  console.log(events);
      var eventList = [];
      eventList.push([parseInt(events[1]),'<span id="' + events + '" class="term hover" range="' + events[1] + '-' + events[2] + '" >']);
      eventList.push([parseInt(events[2]),'</span>']);
      eventList.sort(sort_by_column);
    //  console.log(eventList);
      
      $('.clickbutton.btn-success').each(function(){
        var tagid = $(this).attr('tagid');
        var events = tagid.split("_");
        console.log(events);
                
        eventList.push([parseInt(events[1]),'<span id="' + events + '" class="term selected" range="' + events[1] + '-' + events[2] + '" >']);
        eventList.push([parseInt(events[2]),'</span>']);
        eventList.sort(sort_by_column);
        console.log(eventList);
      });  
            
      $(".alignment #people").html(currentSentence);
      
      $(".alignment #people").html(function(i, val) {
      //  console.log(i);
      //  console.log(val);
        var output = val;
        for(i = 0; i < eventList.length; i++) {
          output = [output.slice(0, eventList[i][0]), eventList[i][1], output.slice(eventList[i][0])].join('');
        }
        $(".alignment #people").html(output);
        //return output;
      }); 
    }
    else {
      var eventList = [];
      $('.clickbutton.btn-success').each(function(){
        var tagid = $(this).attr('tagid');
        var events = tagid.split("_");
        console.log(events);
                
        eventList.push([parseInt(events[1]),'<span id="' + events + '" class="term selected" range="' + events[1] + '-' + events[2] + '" >']);
        eventList.push([parseInt(events[2]),'</span>']);
        eventList.sort(sort_by_column);
        console.log(eventList);
      });  
            
      $(".alignment #people").html(currentSentence);
      
      $(".alignment #people").html(function(i, val) {
      //  console.log(i);
      //  console.log(val);
        var output = val;
        for(i = 0; i < eventList.length; i++) {
          output = [output.slice(0, eventList[i][0]), eventList[i][1], output.slice(eventList[i][0])].join('');
        }
        $(".alignment #people").html(output);
        //return output;
      }); 
    }
  });
  */
  
  $('.hiddeninput').first().parent().parent().css("display","none");
    $('.submit').attr('disabled',true);

    $().ready(function(){
        
    });
    
    $('#button_addnewtag').click(function(){  f_addnewtag();  return false;});
    $(document).on('keydown', '#addnewtags', function(ev) {
        if(ev.which === 13) {
          f_addnewtag();
        }
    });
    
    var addcounter = 0;
    function f_addnewtag()
    {
      var tagval = $('#addnewtags').val();
      if (tagval == "") return;
      var v = tagval;
      if(v.length > 0 && v != " ") {
        if(v.length < (15 * v.split(' ').length) && v.split(' ').length < 4 && v.match(/^([a-zA-Z0-9 _-]+)$/)) {
          $('#newtags > .tags').append('<button type="button" class="clickbutton btn btn-success" tagtype="newlyadded" tagid="manual_'+addcounter+'">'+tagval+'</button>');
        } else {
          $('#newtags > .tags').append('<button type="button" class="clickbutton btn btn-danger" tagtype="newlyadded" tagid="manual_'+addcounter+'">'+tagval+'</button>');
        }
      }

       $('#addnewtags').val("");
       $('#newtags > .tags > button').click( function() {
         $(this).remove();
         updateSelected();
       });
       updateSelected();
       addcounter = addcounter + 1;
       
    }
    

    
    
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

    //$('.submit').attr('disabled',true);
    
  
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

    $('.clickbutton').click(function() {
      
      if ($(this).hasClass('btn-success'))
      {
        $(this).removeClass('btn-success');
      } else {
        $(this).addClass('btn-success');
      }
      updateSelected();
    });



    function updateSelected()
    {
        var descdata = Array();
        var subsdata = Array();
        var tagsdata = Array();
        var manualdata = Array();
        var allData = Array();
        
        $('.clickbutton.btn-success').each(function(){
          var tagid = $(this).attr('tagid');
          switch($(this).attr("tagtype"))
          {
            case "description":
              descdata.push(tagid+'_###_'+$(this).text());
              allData.push(tagid+'_###_'+$(this).text());
              break;
            
            case "subtitles":
              subsdata.push(tagid+'_###_'+$(this).text());
              allData.push(tagid+'_###_'+$(this).text());
              break;
              
            case "image":
              tagsdata.push(tagid+'_###_'+$(this).text());
              allData.push(tagid+'_###_'+$(this).text());
              break;
            
            case "newlyadded":
              manualdata.push(tagid+'_###_'+$(this).text());
              allData.push(tagid+'_###_'+$(this).text());
              break;
          }
        });
        
        
        console.log(descdata);
        console.log(subsdata);
        console.log(tagsdata);
        console.log(manualdata);
        
        $(".hidden.cml_field > .selectedtags_desc").attr("value",JSON.stringify(descdata));
        $(".hidden.cml_field > .selectedtags_subs").attr("value",JSON.stringify(subsdata));
        $(".hidden.cml_field > .selectedtags_tags").attr("value",JSON.stringify(tagsdata));
        $(".hidden.cml_field > .selectedtags_manual").attr("value",JSON.stringify(manualdata));
        
        if (allData.length != 0) {
          $('.submit').attr('disabled',false);
        }
        else {
          $('.submit').attr('disabled',true);
        }
    }

});