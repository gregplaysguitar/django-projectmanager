/*

Example usage:

$('form.titleprompt input, form input.titleprompt').formPrompt();

(elements must have a 'title' attribute in order to populate the prompt)

*/
$.fn.formPrompt = (function(){
    this.each(function(i, item) {
        var input = $(item), promptRemoved = false, removePromptFunc;
		//console.log(item);
		
		var removePromptFunc = function(){
            //console.log(input.val(), input.attr("title"));
            input.removeClass("prompt-visible");
            if (!promptRemoved && input.val() == input.attr("title")){
                input.val("");
                promptRemoved = true;
            }
        };
		
		var addPromptFunc = function() {
            if (input.attr("type") == "text" && input.attr("title") && !input.val()) {
                input.addClass("prompt-visible");
                input.val(input.attr("title"));
                
                input.change(removePromptFunc);
                input.focus(removePromptFunc);
                input.parents("form").submit(removePromptFunc);
                promptRemoved = false;
            }
        };
        
        addPromptFunc();
        input.blur(addPromptFunc);
        
    });
});


