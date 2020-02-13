$(window).scroll(function() {    
    var scroll = $(window).scrollTop();

    if (scroll >= 10) {
        $("body").addClass("scrolling"); 
    } else {
        $("body").removeClass("scrolling");
    }
});

$(window).load(function(){
    $(".loading.main").delay(300).fadeOut();
});

$(document).ready(function(){

  /*-----------------------[Start] Back to top-----------------------*/
 
  $('.btn-totop').click(function () {
      $("html, body").animate({
          scrollTop: 0
      }, 600);
      return false;
  });

  $('.backtotop').hide();
  $(window).scroll(function() {
      if ($(this).scrollTop() > 200) {
          $('.backtotop').fadeIn();
      } else {
          $('.backtotop').fadeOut();
      }
  });


  $(document).on('click', 'a[href="#collapseTableNote"]', function (event) {
      event.preventDefault();

      $('html, body').animate({
          scrollTop: $($.attr(this, 'href')).offset().top - 100
      }, 600);
  });

  /*-----------------------[Start] jquery.matchHeight-min.js-----------------------*/
  
  $('.matchHeight > div').matchHeight();

   /*-----------------------[Start] Bootstrap Tooltip-----------------------*/

  
  $('.business-icon').tooltip({ 
    trigger: "hover focus",
  });
  $('.img-tooltip').tooltip({ 
    trigger: "hover focus",
  });

  $('.info-tooltip').tooltip({ 
    trigger: "hover focus",
    html: true,
    placement: "right"
  });  
  
 
  /*-----------------------[Start] .search-option-----------------------*/

  $('.title-navToggle').click(function () {
       $('.title-navToggle').toggleClass("opened");
  });

  /*------------[Start] Menu------------*/ 

  $("body").removeClass("menu-opened");
  $('.navbar-toggle').click(function () {
      $("body").toggleClass("menu-opened");
  });
   $('.menu ul li a').click(function () {
      $("body").removeClass("menu-opened");
  }); 

  /*------------[Start] filter option------------*/

  $('.dropdown-menu [data-toggle=dropdown]').on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $('.dropdown-menu [data-toggle=dropdown]').parent().removeClass('open');
    $(this).parent().addClass('open');
  });


  $('.switch-status').each(function(){
    var $switchStatus = $(this);
    
    $switchStatus.find('li.switch-item').click(function () {
      $switchStatus.find('li.switch-item').removeClass('status-active');
      $(this).addClass('status-active');

      
    });
  });
 

  /*------------[Start] change color of SVG image using CSS ------------*/

  $('img.svg-js').each(function() {

      var $img = jQuery(this);
      var imgURL = $img.attr('src');
      var attributes = $img.prop("attributes");

      $.get(imgURL, function(data) {
   
          // Get the SVG tag, ignore the rest
          var $svg = jQuery(data).find('svg');

          // Remove any invalid XML tags
          $svg = $svg.removeAttr('xmlns:a');

          // Loop through IMG attributes and apply on SVG
          $.each(attributes, function() {
              $svg.attr(this.name, this.value);
          });

          // Replace IMG with SVG
          $img.replaceWith($svg);
      }, 'xml');
  });

});

  
  
$(window).load(function(){
 
 // preload 

 $(".preloader").delay(300).fadeOut(); 

  var isMobile = {
      Android: function() {
          return navigator.userAgent.match(/Android/i);
      },
      BlackBerry: function() {
          return navigator.userAgent.match(/BlackBerry/i);
      },
      iOS: function() {
          return navigator.userAgent.match(/iPhone|iPad|iPod/i);
      },
      Opera: function() {
          return navigator.userAgent.match(/Opera Mini/i);
      },
      Windows: function() {
          return navigator.userAgent.match(/IEMobile/i);
      },
      any: function() {
          return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
      }
  };

  if(isMobile.any()) {
      $("html").addClass("device");
  }else{
      $("html").addClass("pc");
  } 
});


 


 