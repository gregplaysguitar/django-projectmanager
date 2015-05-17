

$.fn.SelectCustomizer = (function(){
    // Select Customizer jQuery plug-in
	// based on customselect by Ace Web Design http://www.adelaidewebdesigns.com/2008/08/01/adelaide-web-designs-releases-customselect-with-icons/
	// modified by David Vian http://www.ildavid.com/dblog
	// and then modified AGAIN be Dean Collins http://www.dblog.com.au
    // console.log(this, $);
    return this.each(function(){
        var obj = $(this);
		var name = obj.attr('id');
		var id_slc_options = name+'_options';
		var id_icn_select = name+'_iconselect';
		var id_holder = name+'_holder';
		var custom_select = name+'_customselect';
		var container = $('<div class=\"customselect\">');
		var clickable = obj.hasClass('clickable');
		obj.after(container);
        container.append("<div id=\""+id_slc_options+"\" class=\"optionswrapper\"> </div>");


        obj.find('option').each(function(i, item){
            $("#"+id_slc_options).append("<div title=\"" + $(this).attr("value") + "\" class=\"selectitems\"><span>" + $(this).html() + "</span></div>");
            
        });
        container.append("<input type=\"hidden\" value =\"" + $(this).val() + "\" name=\"" + this.name + "\" id=\""+custom_select+"\"/><div id=\""+id_icn_select+"\" class=\"iconselect\">" + $(this).find(':selected').text() + "</div><div id=\""+id_holder+"\" class=\"selectwrapper\"> </div>");
        
        if (clickable || obj.hasClass('titleprompt') && !$(this).find(':selected').attr('value')) {
            $("#"+id_icn_select).html(obj.attr('title')).addClass('prompt-visible');
        }
        obj.remove();
        
        
        $("#"+id_icn_select).click(function(a){
			if($("#"+id_holder).css('display') == 'none') {
				$("#"+id_holder).fadeIn(200);
				$("#"+id_holder).focus();
				a.stopPropagation();
				
				$('body').click(function(){
				    //console.log("dsfds");
					$("#"+id_holder).fadeOut(200);
					$('body').unbind('click');
				});
			} else {
				$("#"+id_holder).fadeOut(200);
				$('body').unbind('click');
			}
			
			
        });
        $("#"+id_holder).append($("#"+id_slc_options)[0]);
		$("#"+id_holder).append("<div class=\"selectfooter\"></div>");
		$("#"+id_slc_options+" > div:last").addClass("last");
        $("#"+id_holder+ " .selectitems").mouseover(function(){
            $(this).addClass("hoverclass");
        });
        $("#"+id_holder+" .selectitems").mouseout(function(){
            $(this).removeClass("hoverclass");
        });
        $("#"+id_holder+" .selectitems").click(function(){
            $("#"+id_holder+" .selectedclass").removeClass("selectedclass");
            $(this).addClass("selectedclass");
            var thisselection = $(this).html();
            $("#"+custom_select).val(this.title);
            if ($(obj).hasClass('titleprompt')) {
                if (this.title) {
                    $("#"+id_icn_select).html(thisselection).removeClass('prompt-visible');
                }
                else {
                    $("#"+id_icn_select).html(obj.attr('title')).addClass('prompt-visible');
                }
            }
            else {
                $("#"+id_icn_select).html(thisselection);
            }
            $("#"+id_holder).fadeOut(250);
			$('body').unbind('click');
			//console.log(clickable, this.title);
			if (clickable && this.title) {
			    window.location = this.title;
			}
        });
    });
});