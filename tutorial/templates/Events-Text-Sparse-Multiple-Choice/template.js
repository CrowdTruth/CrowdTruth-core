require(['jquery-noconflict'], function(jQuery) {
  
  //Ensure MooTools is where it must be
  Window.implement('$', function(el, nc){
    return document.id(el, nc, this.document);
  });
  
  var $ = window.jQuery;
  
  
  $('.hiddeninput').first().parent().parent().css("display","none");
  $('.submit').attr('disabled',true);
  
  
  
  jQuery.fn.reverse = [].reverse;
  
    // sort the inserts reversed, otherwise adding text will screw up the index positions.
  function sort_by_column(a,b) {
    return ((a[0] > b[0]) ? -1 : ((a[0] < b[0]) ? 1 : 0));
  }
  
  var originalSentence = $('div.passage').text();
  var currentSentence = $(".alignment #people").text();
  
  
  $('.clickbutton').on("hover", function() {
    //var currentSentence = $(".alignment #people").text();
    console.log(currentSentence);
    var tagid = $(this).attr('tagid');
    if (tagid != 'no_event') {
      var events = tagid.split("__");
    //  console.log(events);
      var eventList = [];
      eventList.push([parseInt(events[1]),'<span id="' + events + '" class="term hover" range="' + events[1] + '-' + events[2] + '" >']);
      eventList.push([parseInt(events[2]),'</span>']);
      eventList.sort(sort_by_column);
    //  console.log(eventList);
      
      $('.clickbutton.btn-success').each(function(){
        var tagid = $(this).attr('tagid');
        var events = tagid.split("__");
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
        var events = tagid.split("__");
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
  
  
  $('.clickbutton').click(function() {
      
      if ($(this).attr("tagid") == "no_event") {
        if ($(this).hasClass('btn-error'))
        {
          $(this).removeClass('btn-error');
          updateSelected("3");
        } else {
          $(this).addClass('btn-error');
          $(".alignment #people").html(originalSentence);
          updateSelected("2");
        }
      }
      else {
        if ($(this).hasClass('btn-success'))
        {
          $(this).removeClass('btn-success');
        } else {
          $(this).addClass('btn-success');
        }
        updateSelected("1");
      }
    });



    function updateSelected(case_number)
    {
        var descdata = Array();

        switch(case_number)
        {
          case "1":
            var eventList = [];
            $('.clickbutton.btn-success').each(function(){
                var tagid = $(this).attr('tagid');
                descdata.push(tagid);
                var events = tagid.split("__");
                console.log(events);
                
                eventList.push([parseInt(events[1]),'<span id="' + events + '" class="term selected" range="' + events[1] + '-' + events[2] + '" >']);
                eventList.push([parseInt(events[2]),'</span>']);
                eventList.sort(sort_by_column);
                console.log(eventList);
            });  
                $(".alignment #people").html(originalSentence);
                console.log(originalSentence);
                $(".alignment #people").html(function(i, val) {
                //  console.log(i);
                //  console.log(val);
                  var output = val;
                  for(i = 0; i < eventList.length; i++) {
                    output = [output.slice(0, eventList[i][0]), eventList[i][1], output.slice(eventList[i][0])].join('');
                  }
                  $(".alignment #people").html(output);
                  console.log("1")
                  console.log($(".alignment #people").text());
                  console.log("2");
                  currentSentence = $(".alignment #people").text();
                  //return output;
              }); 
          
            $('.clickbutton.btn-error').each(function(){
              $(this).removeClass('btn-error');
            });
            break;
          case "2":
            $('.clickbutton.btn-success').each(function(){
              $(this).removeClass('btn-success');
            });
            $('.clickbutton.btn-error').each(function(){
              var tagid = $(this).attr('tagid');
              descdata.push(tagid);
              //$(".alignment #people").html(currentSentence);
            });
            break;
            
          case "3":
            
            break;
        }
        
        console.log(descdata);

        $(".hidden.cml_field > .selectedtags_desc").attr("value",JSON.stringify(descdata));
        if ($(".hidden.cml_field > .selectedtags_desc").val() != "[]")
          $('.submit').attr('disabled',false);
        else
          $('.submit').attr('disabled',true);
    }
    
});