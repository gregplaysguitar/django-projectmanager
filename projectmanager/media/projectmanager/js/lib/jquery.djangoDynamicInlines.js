/* 

jQuery plugin to add dynamic inlines to the django admin, specified per model. Uses 
some hackery to work out which model is which on the page because the django admin
doesn't provide hooks for identifying a model inline via selectors.


Example usage:

$('.inline-group').dynamicInlines(); // makes all inlines on the page dynamic

$('.inline-group').dynamicInlines({filter: ['my_model', 'another_model']}); // only affects inlines for the MyModel and AnotherModel

$('.inline-group').dynamicInlines({exclude: ['my_model', 'another_model']}); // affects all inlines except MyModel and AnotherModel


Adapted from 
http://www.arnebrodowski.de/blog/507-Add-and-remove-Django-Admin-Inlines-with-JavaScript.html
and
http://www.djangosnippets.org/snippets/1594/

*/



(function($) {


    function increment_form_ids(el, to, name) {
        var from = to-1;
        $(':input', $(el)).each(function(i,e){
            var old_name = $(e).attr('name');
            var old_id = $(e).attr('id');
            $(e).attr('name', old_name.replace(from, to));
            $(e).attr('id', old_id.replace(from, to));
            $(e).val('');
        });
    };
    
    function add_inline_form(name) {
        var first = $('#id_'+name+'-0-id').parents('.inline-related');
        // check to see if this is a stacked or tabular inline
        if (first.hasClass("tabular")) {
            var field_table = first.parent().find('table > tbody');
            var count = field_table.children().length;
            var copy = $('tr:last', field_table).clone(true);
            copy.removeClass("row1 row2");
            copy.addClass("row"+((count % 2) == 0 ? 1 : 2));
            field_table.append(copy);
            increment_form_ids($('tr:last', field_table), count, name);
        }
        else {
            var last = $(first).parent().children('.last-related');
            var copy = $(last).clone(true);
            var count = $(first).parent().children('.inline-related').length;
            $(last).removeClass('last-related');
            var header = $('h3', copy);
            header.html(header.html().replace("#"+count, "#"+(count+1)));
            $(last).after(copy);
            increment_form_ids($(first).parents('.inline-group').children('.last-related'), count, name);
        }
        $('input#id_'+name+'-TOTAL_FORMS').val(count+1);
        return false;
    };


    var html_template = '<ul class="tools">'+
        '<li>'+
            '<a class="add">Add another</a>'+
        '</li>'+
    '</ul>';
    
    $.djangoDynamicInlines = (function(args){
        $('.inline-group').each(function() {
            var me = $(this), validFlag = true;
            console.log(args);
            if (args) {
                // test if we're looking at the right model/s
                var inputName = me.find('input[type=hidden][name$=TOTAL_FORMS]').attr('name');
                var modelName = inputName.split('_set-')[0];
                
                if (
                    (args['filter'] && $.inArray(modelName, args['filter']) == -1) ||
                    $.inArray(modelName, args['exclude'] || []) > -1
                ) {
                    validFlag = false;
                }
            }
            
            if (validFlag && me.find('input[type=hidden][name$=TOTAL_FORMS]').attr('value') > me.find('input[type=hidden][name$=INITIAL_FORMS]').attr('value')) {
                var prefix = $("input[type='hidden']", this).attr("name").split("-")[0];
                me.append(html_template);
                me.find('ul.tools a.add').click(function() {
                    add_inline_form(prefix);
                }).css({cursor: 'pointer'});
            }
        });
    });
    

})(jQuery);