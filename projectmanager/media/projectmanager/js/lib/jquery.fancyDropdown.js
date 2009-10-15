/*

Example usage:

$('ul.dropdown').fancyDropdown();

(elements must have a 'title' attribute in order to populate the prompt)

*/
$.fn.fancyDropdown = (function(){
    this.each(function(i, item) {
        var TIMER = 200;
        var dropdown = $('<span>').addClass('fancy-dropdown');
        
        
        dropdown.append('<label>' + ($(item).find('.current').text() || $(item).attr('title') || "Choose") + '</label>');
        var wrapper = $('<div>').addClass('dropdown-wrapper');
        wrapper.append($(item).clone());
        dropdown.append(wrapper);
        
        
        wrapper.hide();
        
        dropdown.find('label').click(function(){
            var show = !$(this).parent().find('ul').is(':visible');
            $('.fancy-dropdown .dropdown-wrapper').slideUp(TIMER);
            if (show) {
                wrapper.slideDown(TIMER);
            }
            else {
                wrapper.slideUp(TIMER);
            }
            return false;
        });
        $('body').click(function() {
            $('.fancy-dropdown .dropdown-wrapper').slideUp(TIMER);
        });
        
        
        $(item).after(dropdown);
        $(item).remove();
    });
});

