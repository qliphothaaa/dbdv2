;
(function ($) {
	/*
	 * @Chayut 20/11/2018
	 */
	'use strict';
	var defaults = {
			elename : ".page-content",
			scale : 1,
			filename: "pdf.pdf",
			defaultPageSize : [595 , 842],
			filter : '.no-print'
	};
	var settings = {};
	
	function getRatio(pageSize,canvasSize){
		var ratio = 1;
		if(oriant(canvasSize)=="l"){
			//กว้าง น้อย กว่าสูง
			ratio = pageSize[0] / canvasSize[0];
			
		}else{
			ratio = pageSize[1] / canvasSize[1];
		}
		return ratio;
	};
	function printPdf(quality,elename,filename){
		// Chrome 1 - 68
		//var isChrome = !!window.chrome && !!window.chrome.webstore;
		// Firefox 1.0+
		//var isFirefox = typeof InstallTrigger !== 'undefined';
		var opts = {
				bgcolor: "#FFFFFF" ,
				ieDelay: 100,
		 };
		if(isIeEdge())
			opts.ieDelay = 10000;
		_printPdf(quality,elename,filename,opts);
	};
	function _printPdf(quality,elename,filename,opts){
		
		var filterFunc = function(node){
			return true;
		};
		var saveAsPdf = function(){
			
		};
		
		var current = $(elename).css('margin-left');
		$(elename).css('margin-left',0);
		var node = $(elename).get(0);
		domtoimage.toJpeg(node,opts).then(function (dataUrl) {
		    	$(elename).css('margin-left',current);
		    	var canvasSize = [1000,1000];
		    	var pageSize = canvasSize;
		    	var img = new Image();
		    	img.onload = function(){
		    		canvasSize[0] = img.width;
		    		canvasSize[1] = img.height;
			        pageSize = canvasSize;
			       /* if(isIeEdge())
			        	if(oriant(pageSize) == "p")
			        		pageSize[1] = pageSize[1] / 2;
			        	else
			        		pageSize[0] = pageSize[0] / 2;*/
			        var pdf = new jsPDF(oriant(pageSize), 'px', pageSize);
					pdf.addImage(dataUrl, 'JPEG', 10, 0, pageSize[0], pageSize[1]);
					pdf.save(filename);
					if(isIeEdge())
						$("#tmpRender").remove();
		    	};
		    	img.src = dataUrl;
		    	
		    }).catch(function (error) {
		        console.error('oops, something went wrong!', error);
		});
		
	};
	function isIeEdge(){
    	// Internet Explorer 6-11
    	var isIE = /*@cc_on!@*/false || !!document.documentMode;

    	// Edge 20+
    	var isEdge = !isIE && !!window.StyleMedia;
    	
    	if(isIE || isEdge)
    		return true;
    	return false;
    }
	function svg2img(_node){
	    var svg = _node;
	    var xml = new XMLSerializer().serializeToString(svg);
	    var svg64 = btoa(unescape(encodeURIComponent(xml)));//btoa(xml); //for utf8: btoa(unescape(encodeURIComponent(xml)))
	    var b64start = 'data:image/svg+xml;base64,';
	    var image64 = b64start + svg64;
	    return image64;
	};

	
	function oriant(pageSize){
		if(pageSize[0] > pageSize[1] )
			return "l";
		return "p";
	}
	$.fn.htmlToPdf = function (options) {
		settings = $.extend(defaults, options );
	    this.each(function (index, el) {
	      $(el).on('click',function(e){e.preventDefault();printPdf(settings.scale,settings.elename,settings.filename);});
	    });
	    return this;
	}
})(jQuery);