(function($) {

var task_data;
function load_task_data(callback, reload) {
	if (reload || !task_data) {
		$.get(PROJECTMANAGER_URLS.TASK_DATA, function(data) {
			task_data = data;
			callback && callback(task_data);
		});
	}
	else {
		callback(task_data);
	}
};
// load_task_data();
function remove_from_task_data(project_id, task) {
	// var task = new Task(task_data);
	
	console.log('remove', task)
	var existing_tasks = task_data[project_id] || [];
	task_data[project_id] = [];
	for (var i = 0; i < existing_tasks.length; i++) {
		if (existing_tasks[i][0] !== task[0]) {
			task_data[project_id].push(existing_tasks[i]);
		}
	}
};
function add_to_task_data(project_id, task) {
	if (!task_data[project_id]) {
		task_data[project_id] = []
	}
	var index = null;
	for (var i = 0; i < task_data[project_id].length; i++) {
		if (task_data[project_id][i][0] === task[0]) {
			index = i;
			break;
		}
	}
	if (index !== null) {
		task_data[project_id][index] = task;
	}
	else {
		task_data[project_id].push(task);
	}
};


function time_form_init(form) {
	var project = form.find('#id_project'),
	    task = form.find('#id_task'),
			new_task = form.find('#id_new_task'),
			completed = form.find('#id_completed');
	
	
	function reset_form(new_task_data) {
		new_task.val('');
		form.find('#id_description').val('');
		form.find('#id_completed').attr('checked', false);
		if (new_task_data) {
			if (new_task_data.task[2]) {
				remove_from_task_data(new_task_data.project_id, new_task_data.task);
			}
			else {
				add_to_task_data(new_task_data.project_id, new_task_data.task);
			}
			update_tasks();
			// if (project.val() == new_task_data.project_id && !new_task_data.task[2]) {
			// 	task.val(new_task_data.task[0]);
			// }
		}
	};
	
	function add_optgroup(select, name, opts) {
		var optgroup = $('<optgroup>').attr('label', name).appendTo(select);
		 for (var i = 0; i < opts.length; i++) {
			 optgroup.append($('<option>').attr('value', opts[i][0])
															      .text(opts[i][1]));
		}
		return optgroup;
	};
	
	function update_tasks(reload, callback, additional_tasks) {
		var project_id = project.val();
		load_task_data(function(data) {
			task.html('');
			task.append('<option value="">[new task]</option>');
			var completed = [],
			    incomplete = [];
			
			function append_tasks(task_list) {
				for (var i = 0, list, in_list; i < task_list.length; i++) {
					list = (task_list[i][2] ? completed : incomplete);
					in_list = false
					// only add the task if it's not already in the list
					for (var j = 0; j < list.length; j++) {
						if (list[j][0] == task_list[i][0]) {
							in_list = true;
						}
					}
					if (!in_list) {
						list.push(task_list[i]);
					}
				}
			};
			
			// add tasks from the current project and any additional ones required
			append_tasks(data[project_id]);
			additional_tasks && append_tasks(additional_tasks);
			
			// add in progress and completed groups to the select
			incomplete.length && add_optgroup(task, 'In progress', incomplete);
			completed.length && add_optgroup(task, 'Completed', completed);
			
			task.change();
			callback && callback();
		}, reload);
	};
	project.change(function() {
		update_tasks()
	});
	
	task.change(function() {
		var task_id = $(this).val(),
				completed_val;
				
		if (task_id) {
			new_task.parents('tr').hide();
			completed_val = $(this).find('option:selected').parent('optgroup')
			                       .data('completed') || false;
		}
		else {
			new_task.parents('tr').show();
			new_task.focus();
			completed_val = false;
		}
		completed.attr('checked', completed_val);
	});
	
	project.change();
	task.change();
	
	return {
		'reset_form': reset_form,
		'update_tasks': update_tasks,
	};
};



$(document).ready(function() {

  var add_form = time_form_init($('#add_time'));
	
  var date = new Date();
	var d = date.getDate();
	var m = date.getMonth();
	var y = date.getFullYear();
	
	var calendar = $('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			//right: 'month,basicWeek,basicDay'
			right: 'month,agendaWeek,agendaDay'
		},
		editable: true,
		firstHour: 8,
		defaultView: 'agendaWeek',
		//contentHeight: 1500,
		firstDay: 1, // monday
		events: PROJECTMANAGER_URLS.PROJECT_TIME_LIST,
		loading: onCalendarLoading,
		select: onCalendarSelect,
		eventDrop: onCalendarEventUpdate,
		eventResize: onCalendarEventUpdate,
		eventClick: onCalendarEventClick,
		selectable: true,
		selectHelper: true,
		slotMinutes: 15
	});

	$("form.addtime").submit(onTimeFormSubmit);
	$("#add_time_cancel, #add_time_overlay").click(hideAddTimeForm);

	$(document).keydown(onDocumentKeyDown)


	function onCalendarLoading(bool)
	{
			if (bool) $('#loading').show();
			else $('#loading').hide();
	};

	function onCalendarSelect(start, end, allDay)
	{
		// Prefill the form.
		$('form.addtime #id_id').val('0');
		$('#add_time #id_start').val(formatDate(start));
		$('#add_time #id_end').val(formatDate(end));
		$('#add_time #id_description').val("");
		$('#add_time #id_project').focus();
		$('#add_time #id_completed').attr('checked', false);
		$("#add_time, #add_time_overlay").fadeIn(300);
		$('#add_time .delete').hide();
		
		add_form.update_tasks();
	};

	function onCalendarEventUpdate(event, delta)
	{
		_jQueryPost(PROJECTMANAGER_URLS.PROJECT_TIME_MOVE, 
			          _eventToPostVars(event), null);
	};

	function onCalendarEventClick(event) {
		// Prefill the form.
		$('form.addtime #id_id').val(event._id);
		$('#add_time #id_start').val(formatDate(event.start));
		$('#add_time #id_end').val(formatDate(event.end));
		$('#add_time #id_project').val(event._project_id);
		$('#add_time #id_description').val(event._description).focus();
		$("#add_time, #add_time_overlay").fadeIn(300);
		$('#add_time .delete').show().attr('href', $('#add_time .delete').attr('href').replace('/0/', '/' + event._id + '/'));
		
		// send the clicked task through in case it's already completed, and 
		// therefore not in the global task data
		add_form.update_tasks(false, function() {
			$('#add_time #id_task').val(event._task[0]).change();
			$('#add_time #id_completed').attr('checked', event._task[2]);
		}, [event._task]);
	};

	function onTimeFormSubmit(event)
	{
		event.preventDefault();
		var form = $("form.addtime");

		if( !parseInt(form[0].elements['id'].value) )
			_jQueryPost(PROJECTMANAGER_URLS.PROJECT_TIME_ADD, $("form.addtime").serialize(), onAddTimeResponse);
		else
			_jQueryPost(PROJECTMANAGER_URLS.PROJECT_TIME_EDIT, $("form.addtime").serialize(), onEditTimeResponse);
	};

	function onAddTimeResponse(data, status, xhr)
	{
		if( ! data.status )
		{
			displayFormErrors(data.errors);
			return;
		}

		calendar.fullCalendar('renderEvent', data.event, true); // third arg makes make the event "stick"
		hideAddTimeForm();  // hides the selection band.
		add_form.reset_form({task: data.event._task, 
			                   project_id: data.event._project_id});
	};

	function onEditTimeResponse(data, status, xhr)
	{
		if( ! data.status )
		{
			displayFormErrors(data.errors);
			return;
		}
		
		// Update the existing item with the new values.
		var newevent = calendar.fullCalendar('clientEvents', data.event._id)[0];
		for(var prop in data.event)
			newevent[prop] = data.event[prop];

		calendar.fullCalendar('updateEvent', newevent);
		hideAddTimeForm();  // hides the selection band.
		add_form.reset_form({task: data.event._task, 
			                   project_id: data.event._project_id});
	};

	function onAjaxError()
	{
		alert("Server error, unable to update database!");
	};

	function onDocumentKeyDown(event)
	{
		if( event.which == 27 ) {  // escape
			hideAddTimeForm();
		}
	};

	function displayFormErrors(errors)
	{
		var msg = '';
		for( var fieldname in errors )
			msg += fieldname + ": " + errors[fieldname];
		alert(msg);
	};


	function hideAddTimeForm()
	{
		$("#add_time, #add_time_overlay").fadeOut(500);
		calendar.fullCalendar('unselect');
	};

	function formatDate(date)
	{
		// JavaScript has no native format function.
		var hours = date.getHours().toString();
		var mins = date.getMinutes().toString();
		if( hours.length == 1 ) hours = "0" + hours;
		if( mins.length == 1 ) mins = "0" + mins;
		return date.getFullYear() + "-" + (date.getMonth()+1) + "-" + date.getDate() + " " + hours + ":" + mins;
	};


	// ---- Ajax posting ----

	function _jQueryPost(url, postdata, onsuccess)
	{
		jQuery.ajax(url, {
			'type': 'POST',
			'data': postdata,
			'dataType': 'json',
			'success': onsuccess,
			'error': onAjaxError
		});
	};

	function _eventToPostVars(event)
	{
		var postvars = {
			'id': event._id,
			'title': event.title,
			'start': formatDate(event.start),
			'end': formatDate(event.end),
			'project_id': event._project_id,
			'allDay': event.allDay
		};
		return jQuery.param(postvars);
	};

});

})(jQuery);
