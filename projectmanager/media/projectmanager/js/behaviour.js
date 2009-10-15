(function ($) {
    
    
    $(function() {

        // Kill links to self
        $('a').each(function(i, item) {
            if (item.href == ('' + window.location).replace(/#.*$/, '')) {
                $(item).addClass('current');
            }
        });
        
          
        // facilitate zebra striping in uls and tables
        $('ul li:even, table tr:even').addClass('alt');

        // fix checkboxes
        $('input[type=checkbox]').addClass('checkbox');                
                
        
        /*
        // Add stars to required form fields
        $(function() {
            $('input.required, select.required, textarea.required').parent('li, tr').find('label, th').append("*").addClass('required');
        });
    
        // add prompts to form elements
        $('form.titleprompt input, form input.titleprompt').formPrompt();
        
        // datepicker activation
        $('input.datepicker').datepicker({dateFormat: 'yy-mm-dd'});

        */
        
    });

// END
}) ($);
