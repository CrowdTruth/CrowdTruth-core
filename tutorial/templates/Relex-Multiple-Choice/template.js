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

});