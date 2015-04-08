
var time_init;
(function () {

var start_y = null, end_y = null, ghost = null,
	  params = {};

time_init = function(p) {
	params = p;
	params.snap_pixels = params.snap_hours / (params.end_hour - params.start_hour) * $('#time_list')[0].offsetHeight;
};


$('#time_list').mousedown(function(e) {
	start_y = snap(getClickCoords(e).y - getElementCoords($('#time_list')[0]).y, params.snap_pixels);
});
$('#time_list').mousemove(function(e) {
	if (start_y) {
		end_y = snap(getClickCoords(e).y - getElementCoords($('#time_list')[0]).y, params.snap_pixels);
//		console.log(end_y);
	 	if (start_y < end_y) {
			makeGhost(start_y, end_y);
		}
	}
});

$(document).mouseup(function(e) {
	if (start_y && end_y && start_y < end_y) {
		prefillForm(start_y, end_y);
	}
	start_y = end_y = null;
	setTimeout(clearGhost, 100);
});

function makeGhost(start_y, end_y) {
	if (!ghost) {
		ghost = $('<li>');
		ghost.addClass('ghost');
		$('#time_list ul').append(ghost);
	}
	ghost.css({
		top: start_y + 'px',
		height: (end_y - start_y) + 'px'
	}).show();
};
function clearGhost() {
	ghost.hide();
};

function prefillForm(start_y, end_y) {
	var 	start = getDatetimeFromOffset(Math.min(start_y, end_y)),
			end = getDatetimeFromOffset(Math.max(start_y, end_y));
	
	$('#add_time #id_start').val(start);
	$('#add_time #id_end').val(end);
	$('#add_time #id_project').focus();
	$.scrollTo($('#add_time #id_project'), 200);
	
};

function getDatetimeFromOffset(offset) {
	var hours = (params.end_hour - params.start_hour) * offset / $('#time_list')[0].offsetHeight + params.start_hour;
	var getHours = function(t) {
		return Math.floor(Math.round(t / params.snap_hours) * params.snap_hours);
	};
	var getMinutes = function(t) {
		t = (t - getHours(t))
		t = Math.round(t / params.snap_hours) * (60 * params.snap_hours);
		if (parseInt(t) < 10) {
			t = '' + t + '0';
		}
		return t;
	};
	
	return params.current_day + ' ' + getHours(hours) + ':' + getMinutes(hours);
	
};


function snap(value, snap) {
//	console.log(value, snap, Math.round(value / snap) * snap);
	return Math.round(value / snap) * snap;
};


function getClickCoords(e) {
	var coords = {'x' : 0, 'y' : 0};
	if (!e) {
		var e = window.event;
	}
	if (e.pageX || e.pageY) {
		coords.x = e.pageX;
		coords.y = e.pageY;
	}
	else if (e.clientX || e.clientY) {
		coords.x = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
		coords.y = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
	}
	return coords;
};

function getElementCoords(el) {
	var coords = {'x' : 0, 'y' : 0};
	do {
		coords.x += el.offsetLeft;
		coords.y += el.offsetTop;
	}
	while (el = el.offSetParent);
	return coords;
};


})();




