(function($){
 $(window).on("load", function () {
	var basepath = "info/";


	var w = 740;
	var h = 600;

 	var r = Raphael('map',w,h),

        attributes = {
            fill: '#d5b08e',
            stroke: '#ccc',
            'stroke-width': 2,
            'stroke-linejoin': 'round'
        },

        arr = new Array();

	$(".mapPoint").mouseenter(function(){
		$(this).children("span").show();
	}).mouseleave(function(){
		$(this).children("span").hide();
	});

        var id = 0;

	var showTitle = function (obj) {
		//console.log(this.data('wert'));
		//console.log(obj);
		var box = obj.getBBox();
		var cls = obj.data('name') == ''?'class="empty"':'';
		var $title = $('<div id="mapTitle" ' + cls + ' style="position: absolute;">' + obj.data('hoverName') + '<\/div>');
		$('#map').append($title);
		$title.css({
			top: box.y + box.height/2 + (obj.data('offy') || 0),
			left: (box.x + box.width/2) - $title.innerWidth() + (obj.data('offx') || 0)
		});
	}

	var hideTitle = function () {
		$('#mapTitle').remove();
	};
	for (var region in paths) {
		var obj = r.path(paths[region].path);
		var regionColor = paths[region].color;
		obj.attr(attributes);
		obj.attr('fill', regionColor);
		arr[obj.id] = region;
		obj.data('name', paths[region].name);
		obj.data('hoverName', paths[region].hoverName);
		obj.data('offx', paths[region].offx);
		obj.data('offy', paths[region].offy);
		obj
			.hover(function(){
				if (paths[arr[this.id]].name != '') {
					this.animate({fill: '#d09962'}, 300)
				};
                		showTitle(this);
			}, function() {
			this.animate({
				fill: paths[arr[this.id]].color
				}, 300);
				hideTitle();
			})
			.click(function(){
				if (paths[arr[this.id]].name == '') return false;
				window.location = basepath + paths[arr[this.id]].name + "/";
			});
		};
	});
})(jQuery);