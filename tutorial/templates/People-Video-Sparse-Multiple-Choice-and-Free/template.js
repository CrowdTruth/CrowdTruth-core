require(['jquery-noconflict'], function(jQuery) {
    

    Window.implement('$', function(el, nc){
        return document.id(el, nc, this.document);
    });
    var $ = window.jQuery;
    $('.hiddeninput').first().parent().parent().css("display","none");
    $('.submit').attr('disabled',true);

    var finished = false;
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
    
    $().ready(function(){
        
    });
    
    for(e=0; e < events.length; e++) {
        $('.video').on(events[e], function(event) {
            $(this).parents('.jsawesome').find('input.e_' + event.type).val( function(i, v) {
                return parseInt(v) + 1;
            });
            
            if(event.type == 'ended' && $(".e_ended").filter(function() { return  $(this).val() >= 1; }).length == $('.e_ended').length) {
                finished = true;
                updateSelected();
                
            }
        });
    }
    
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

        var manualdata = Array();
        var allData = Array();
        
        $('.clickbutton.btn-success').each(function(){
          var tagid = $(this).attr('tagid');
          switch($(this).attr("tagtype"))
          {
            case "description":
              allData.push(tagid+'_###_'+$(this).text());
              break;
            
            case "subtitles":
              allData.push(tagid+'_###_'+$(this).text());
              break;
              
            case "image":
              allData.push(tagid+'_###_'+$(this).text());
              break;
            
            case "newlyadded":
              manualdata.push(tagid+'_###_'+$(this).text());
              allData.push(tagid+'_###_'+$(this).text());
              break;
          }
        });
        
        console.log(manualdata);
        
        $(".hidden.cml_field > .selected_answer").attr("value",JSON.stringify(allData));
        $(".hidden.cml_field > .selectedtags_manual").attr("value",JSON.stringify(manualdata));
        
        if (allData.length != 0) {
          if (finished){
            $('.submit').attr('disabled',false);
          } else{
            $('.submit').attr('disabled',true);
          }
        }
        else {
          $('.submit').attr('disabled',true);
        }
    }
});