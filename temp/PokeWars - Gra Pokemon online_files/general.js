
var col_hide = getCookie("col_hide");
var night = getCookie("night");
var pdx_loaded = false;
var pdx_opened = false;
var game_modifier_open = false;
var global_timestamp = 0;
var displayed_special_msg = [];
var displayed_voting_msg = [];

var last_full_refresh = Math.floor(Date.now() / 1000);

var time_quest_interval;
var time_quest_page_interval;
var time_quest_page_interval_enabled = false;
var assoc_quest_interval;


$(document).ready(function(){

	setCookie('ps','');
	start();
	time_tick();
	

	setInterval(time_tick, 1000);	
	setInterval(check_for_news, 10000);
	setDbgPage();

	initRequestHandler();
	showElementsNotificationIndicators(elementsNotificationIndicatorsMap);

	$("body a").live( "click", function(e){
		if(!dynamic_pages) return;
		if($(this).attr('link') != undefined) return;
		if($(this).closest("#pdx_window").length) return;

		var href = $(this).attr('href');
		var target = $(this).attr('target');

		if(href == undefined) return;
		if(target == '_blank') return;
		if(href.substr(0, 4) == 'http') return;
		if(href.substr(0, 10) == 'javascript') return;
		if(href.substr(0, 1) == '#') return;
		if(last_full_refresh + refresh_time < Math.floor(Date.now() / 1000)) return;

		e.preventDefault();

		var get_href = '';

		if(href.indexOf('?') != -1)
			get_href = href + "&only_content=1";
		else
			get_href = href + "?only_content=1";

		$('#content_loader').animate({ top: '30px' }, 200);
		$.get( get_href, function( data ) {
			refreshInfoCol(function(){
		  		$( "#content" ).html( data);
		  		if(col_hide == 1)
					fast_hide_col();
		 		$('#content_loader').animate({ top: '0px' }, 200);
		 		hideComunicates();
		 		setTimeout(function() { hide_popups(); }, 5000);
		  		window.history.pushState(href, data.pageTitle, href);
		  	});
		});
	});


	$("form").live("submit", function(e) {
		performDynamicSubmit(e, this, null);
	});

	$(".inputChanger").live("input focusout", function(e){


		var element_id = $(this).attr('id');
		var amount = $(this).val();
		
		if(amount.length){
			$("#"+element_id+"_changer").text( parseInt($(this).val()).numberFormat(0,'.','.'));
		}
		else{
			$("#"+element_id+"_changer").text("0");
		}
	});

	$("input:submit").live("click", function(e) {
		var btn = $(this);
		var form = btn.parent("form");
		performDynamicSubmit(e, form, btn);
	});



	$(".msg-important-btn").live("click", function(e) {

		var object = $(this);

		var user_id = object.attr('user-id');


		$.ajax({
			url: '/ajax',
			data: {method: 'msg',
				   user_id: user_id,
				   func: 'mark_conversation_as_important'},
			type: 'post',
			success: function(output) { 

				if(object.hasClass('on')) {

					object.removeClass("on");
					object.addClass("off");
				} else {

					object.removeClass("off");
					object.addClass("on");
				}
			}
		});
	});

/*
	$(".inputChanger").change(function(){
		$(this).val(parseInt($(this).val()).numberFormat(0,'.','.'));
	});

	$(".inputChanger").click(function(){
		var inputed = $(this).val();

		if(inputed.length == 0) return;

		$(this).val(inputed.replace(/\./g,""));
	}); */

	function performDynamicSubmit(e, that, btn) {
		if(!dynamic_pages) return;
	    var url = $(that).attr('action');

	    if(url == undefined)
	    	url = window.location.href;
	   	else if(url.substr(0, 4) == 'http') return;

		if(last_full_refresh + refresh_time < Math.floor(Date.now() / 1000)) return;

		e.preventDefault();

	    var get_href = '';

		if(url.indexOf('?') != -1)
			get_url = url + "&only_content=1";
		else
			get_url = url + "?only_content=1";

		if(btn == null)
			btn = $(that).find('input:submit');
		var formData = $(that).serialize();

		formData += "&" + btn.attr('name') + "=" + btn.attr('value');

		$('#content_loader').animate({ top: '30px' }, 200);
	    $.ajax({
           type: "POST",
           url: get_url,
           data: formData, 
           success: function(data)
           {
           		refreshInfoCol(function(){
		  			$( "#content" ).html( data);
		  			if(col_hide == 1)
						fast_hide_col();
		 			$('#content_loader').animate({ top: '0px' }, 200);
		 			hideComunicates();
		 			setTimeout(function() { hide_popups(); }, 5000);
               		window.history.pushState(url, data.pageTitle, url);
               	});
           }
        });
	}



	if($(".msg_new_count").html() == '')
		$(".msg_new_count").hide();

	if(getCookie('friends_box') == 0)
		$('#friends_box').css('right', -220);
	else
		$('#friends_box').css('right', 0);

	$('#friends_box_btn').click(function(){
		if(getCookie('friends_box') == 0)
		{
			$('#friends_box').animate({ right: 0 }, "fast");
			setCookie('friends_box',1,1);
		}
		else
		{
			$('#friends_box').animate({ right: -220 }, "fast");
			setCookie('friends_box',0,1);
		}
	});

	$('input.only_number').keyup(function() {
		this.value = this.value.replace(/[^0-9\.]/g,'');
	});

	$( "#search_icon" ).toggle(
	  function() {
	  	$(this).parent('li').addClass('active');
	  	$('#search_input_box').show();
	  	$('#search_input').focus();

	  }, function() {
	  	$(this).parent('li').removeClass('active');
	    $('#search_input_box').hide();
	  }
	);

	$('#search_input').keyup(function(event) {
		var text = $(this).val();
		if(text.length >= 3) {

			if (event.keyCode == '13') {
				event.preventDefault();
               window.location.href = $("#search_result_list .result_row:first-child a").attr('href');
               
            }
            else
            {
				$.ajax({
					url: '/ajax',
					data: {method: 'user_search',
						   fraza: text},
					type: 'post',
					success: function(output) { 
						if(output.length != 0) {
							$("#search_result_list").html(output);
						}
					}
				});
			}
		}
		else
			$("#search_result_list").empty();
	});	


	$(".online_status").click(function() {
		$.ajax({
			url: '/ajax',
			data: {method: 'change_online_status'},
			type: 'post',
			success: function(output) { 
	
				if(output == 0) {
					$(".online_status.online").show();
					$(".online_status.offline").hide();
				} 
				else
				{
					$(".online_status.online").hide();
					$(".online_status.offline").show();
				}
			}
		});
	});


	$( ".cross_icon" ).click(function(){
		var infoBar = $(this).parent(".infoBar");

		infoBar.animate({
		    height:"0px"
		  }, 200, function() {
		    infoBar.remove();
		  });
	});

	$(".news_information").click(function() {
		var c_name = 'hide_new_' + $(this).attr('new_id');
		setCookie(c_name,1,100);
		$(this).parent(".col").remove();
	});

	hideComunicates();

	$( "#pdx_btn" ).click(function() {
	  	if(!pdx_opened) {
	  		pdxOpen();
	  		var page_name = getCookie("pdx_active_page");
	  		if(typeof page_name == 'undefined')
	  			page_name = 'start';
	  		pdxLoad(page_name);
	  	}
	  	else
	  	{
	  		pdxHide();
	  	}
	});

	$( "#game_modifier_btn" ).click(function() {
		if(!game_modifier_open) {
			gameModifierOpen();
		}
		else
		{
			gameModifierClose();
		}
	});


	$("#pdx_copy_btn").live("click", function(event) {
		$("#pdx_adress").show().select();
	});


	$("#pdx_window a").live( "click", function(event)  {
		var page_name = $(this).attr('href');
		if(page_name.substr(0,1) == '/' || page_name.substr(0,4) == 'http') return;

		event.preventDefault();
		
		if(page_name == null) return;
 		pdxLoad(page_name);
	});

	$( "#dbg_btn" ).toggle(
	  function() {
	  	dbgOpen();
	  }, function() {
	   	dbgHide()
	  }	
	);

	$(".night_btn").live('click', function(){
		if(night == 1) {
			$('body').removeClass('night');
			night = 0;
			setCookie("night", 0, 1);
		}else {
			$('body').addClass('night');
			night = 1;
			setCookie("night", 1, 1);
		}
	});


	$('.poke_view_btn').live('click', function(){
		var p_id = $(this).attr('poke_id');
		var that = $(this);

		$.ajax({
			url: '/ajax',
			data: {method: 'load_info_box',
				   closed: col_hide, 
				   tab:  0,
				   p_id:p_id},
			type: 'post',
			success: function(output) { 
				if(output != 'error') {
					$('.team_member').removeClass('active');
					that.addClass('active');
					if(col_hide == 0) {
						changePanelTab("team", false);
						$('#info-box-content').html(output);
					}
					else
						$('.small_controll_box .content').html(output);
				}
			}
		});
	});

	$('.dbg_menu_item').click(function(){
		var id = $(this).attr('id');
		$(".dbg_content").hide();
		$(".dbg_content#dbgc_"+id).show();
		setCookie("dbg_content", id, 1);
	});


	var prevent_multiclick = false;

	$('.prevent_multiclick').click(function(e){

		if(prevent_multiclick) {
			e.stopImmediatePropagation();
			e.preventDefault();
		}

		$(this).prop('onclick',null);
		prevent_multiclick = true;
	});

});


$(document).ready(setTimeout(hide_popups, 5000));


function showElementsNotificationIndicators(indicators)
{
	Object.keys(indicators).forEach(function(key, index) {
		$("." + key).append(' <span class="notification-indicator red">' + indicators[key] + '</span>');
	}, indicators);
}



function initRequestHandler()
{
	$('body').on('click', "a[data-request], input[type=submit][data-request], input[type=button][data-request]", function() {

		let request = $(this).data('request');
		let data = $(this).data('request-data');
		let successClosure = $(this).data('request-success');
		let errorClosure = $(this).data('request-error');
		let completeClosure = $(this).data('request-complete');
		let formSelector = $(this).data('request-form');
		let confirmQuestion = $(this).data('request-confirm');

		if (data === undefined) {
			data = {};
		}

		if (formSelector !== undefined) {
			let formData = $(formSelector).serializeArray();
			formData.forEach(function(field) {
				data[field.name] = field.value;
			});
		}

		let requestData = {
			request: request,
			data: data,
			successClosure: successClosure,
			errorClosure: errorClosure,
			completeClosure: completeClosure
		};

		if (confirmQuestion !== undefined) {

			vex.dialog.open({
				message: confirmQuestion,
				buttons: [
					$.extend({}, vex.dialog.buttons.YES, {text: 'Tak'}),
					$.extend({}, vex.dialog.buttons.NO, {text: 'Nie'})
				],
				callback: function (data) {
					if (data) {
						makeAjaxRequest(requestData);
					}
				}
			});
		} else {
			makeAjaxRequest(requestData);
		}
	});
}


function makeAjaxRequest(requestData)
{
	$.ajax({
		url: requestData.request,
		data: requestData.data,
		type: 'post',
		success: function(output) {

			if (isObject(output)) {

				if (output.content !== undefined) {
					putHtmlFromResponse(output.content);
				}

				if (output.content.redirect !== undefined) {
					window.location.href = output.content.redirect;
				}

				if (output.messages !== undefined) {
					showMessages(output.messages);
				}

				if (output.popups !== undefined) {
					showPopups(output.popups);
				}
			}

			if (requestData.successClosure !== undefined) {
				runClosure(requestData.successClosure);
			}
		},
		error: function(output) {
			if (requestData.errorClosure !== undefined) {
				runClosure(requestData.errorClosure);
			}
		},
		complete: function(output) {
			if (requestData.completeClosure !== undefined) {
				runClosure(requestData.completeClosure);
			}
		}
	});
}

function isObject(obj) {
  return obj === Object(obj);
}

function runClosure(dataClosure)
{
	var x = eval(dataClosure);
    if (typeof x == 'function') {
        x()
    }
}

function putHtmlFromResponse(response)
{
	for (let k in response){
		if (typeof response[k] !== 'function') {
			if (k == '*') {
				$('body').append(response[k]);
			} else {
				$(k).html(response[k]);
			}
		}
	}
}

function showMessages(messages)
{
	messages.forEach(function(message) {
		showInfo(message.type, message.msg);
	});
}

function showPopups(popups)
{
	popups.forEach(function(popup) {
		add_popup(popup.img, popup.text);
	});
}

function isJsonString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

function objectifyForm(formArray) {

  var returnArray = {};
  for (var i = 0; i < formArray.length; i++){
    returnArray[formArray[i]['name']] = formArray[i]['value'];
  }
  return returnArray;
}


function sendCaptchaToken(token) {

	$.ajax({
		url: '/ajax',
		data: {method: 'captchaToken',
			   token: token},
		type: 'post'
	});
}


Number.prototype.numberFormat = function(c, d, t){
var n = this, 
    c = isNaN(c = Math.abs(c)) ? 2 : c, 
    d = d == undefined ? "." : d, 
    t = t == undefined ? "," : t, 
    s = n < 0 ? "-" : "", 
    i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", 
    j = (j = i.length) > 3 ? j % 3 : 0;
   return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
 };


function hideComunicates() {
	$( ".infoBar.autoHide" ).delay(5000).animate({
    	height:"0px"
  	}, 200, function() {
    	$(this).remove();
  	});
}

function refreshInfoCol(callback) {
	$.ajax({
		url: '/ajax',
		data: {method: 'get_infocol'},
		type: 'post',
		success: function(output) { 
			if(output != '')
				$('#info_col_container').html(output);
			callback();
		}
	});
}

function setDbgPage() {
	if(getCookie('dbg_open') == 1)
		dbgOpen();
	else
		dbgHide();

	var page = getCookie('dbg_content');
	if(page !== null) {
		$(".dbg_content").hide();
		$(".dbg_content#dbgc_"+page).show();
	}
}

function showTemplateList() {
	$.ajax({
		url: '/ajax',
		data: {method: 'msg',
			   func: 'get_template_list'},
		type: 'post',
		success: function(output) { 
			if(output != '')
				$('#template_list').html(output);
		}
	});
}




function useTemplate(id) {
	var text = $("#template-id-"+id).html();

	$("#msg_text").val(rehtmlEntities(text));
}

function showAdTemplateList() {
	$.ajax({
		url: '/ajax',
		data: {method: 'association',
			   func: 'get_ad_template_list'},
		type: 'post',
		success: function(output) { 
			if(output != '')
				$('#ad_template_list').html(output);
		}
	});
}

function useAdTemplate(id) {

	$.ajax({
		url: '/ajax',
		data: {method: 'association',
			   func: 'get_ad_template_text',
			   id: id},
		type: 'post',
		success: function(output) { 
			if(output != '')
				$("#msg_text").val(output);
		}
	});
}


function removeAdTemplate(id) {

	$.ajax({
		url: '/ajax',
		data: {method: 'association',
			   func: 'remove_ad_template',
			   id: id},
		type: 'post',
		success: function(output) { 
			
			$("#ad-template-id-"+id).remove();
		}
	});
}


function showInfo(type, message) {
	switch(parseInt(type))
	{
		case 1: type = 'success'; break;
		case 2: type = 'warning'; break;
		case 3: type = 'error'; break;
	}

	$("#content").prepend('<div class="infoBar ' + type + ' autoHide">'+ message +'</div><div class="clear"></div>');
	$(".infoBar").delay(5000).animate({
	    height:"0px"
	  }, 200, function() {
	    $(this).remove();
	  });
}


function hide_popups() {

	$('.popup_item').each(function(index) {
        setTimeout(function(el) {
            el.slideUp(300);
        }, index * 280, $(this));
    });
}

function add_popup(img, text) {

	var res = '<div class="popup_item">';
	if(img.length != 0)
		res +='<div class="img"><img src="/img/' + img + '" height="50"/></div>';
	res +='<div class="text">' + text + '</div></div>';

	$(res).appendTo('#popup_list').delay(5000).slideUp(300);
}


function start()
{
	global_timestamp = parseInt($("#global_timestamp").text());


	if(col_hide == 1)
		fast_hide_col();

	if(night == 1)
		$('body').addClass('night');

	money_anim();

	 
}

function money_anim() {
	var anim_box = $("#money_anim");
	var diff = parseInt(anim_box.attr('moneydiff'));
	if(diff == 0 || col_hide == 1) return;

	if(diff > 0) 
		anim_box.html('<span style="color:green;">+' + diff.numberFormat(0,'.','.') + '&yen;</span>');
	else 
		anim_box.html('<span style="color:red;">' + diff.numberFormat(0,'.','.') + '&yen;</span>');

	anim_box.animate({
	    right: "-=80"
	}, 500,function() {
		anim_box.animate({
	    	opacity: 0
		}, 800);
	});
}

function show_col()
{
	col_hide = 0;
	setCookie("col_hide", 0, 1);
  	$('.small_controll_box').animate({
    	left:"-125px"
  	}, 200, function(){
  		$('body, #top_bar, #bottom_bar').removeClass('small-body');
  		$('#container').removeClass('full-width');
  		$('#info_col').css({'top': "45px"});
	  	$('#info_col').animate({
		    marginLeft:"0px",
		  }, 200);
  	});
}


function hide_col()
{
	col_hide = 1;
	setCookie("col_hide", 1, 1);
	$('#info_col').animate({
	    marginLeft:"-350px",
	    
	  }, 200, function() {
	  	$('.controll_box').addClass('no-shadow');
	  	$('body, #top_bar, #bottom_bar').addClass('small-body');
	  	$('#container').addClass('full-width');
	  	$('.small_controll_box').animate({
	    	left:"0px"
	  	});
	  	
	  });
}

function fast_hide_col()
{
	$('#info_col').css({'marginLeft': "-350px",
						'top': "205px"});
	$('.controll_box').addClass('no-shadow');
	$('body, #top_bar, #bottom_bar').addClass('small-body');
	$('#container').addClass('full-width');
	$('.small_controll_box').css('left', '0px');
	col_hide = 1;
}

function time_tick()
{
	global_timestamp++;
	$("#game_time").text(getTime(global_timestamp));
}

function getTime(seconds) {

 	var currentdate = new Date(global_timestamp*1000); 
	var datetime =  (currentdate.getHours() < 10 ? "0"+currentdate.getHours() : currentdate.getHours()) + ":"  
            + (currentdate.getMinutes() < 10 ? "0"+currentdate.getMinutes() : currentdate.getMinutes()) + ":" 
            + (currentdate.getSeconds() < 10 ? "0"+currentdate.getSeconds() : currentdate.getSeconds());
    return datetime;
}


function setCookie(cookieName,cookieValue,nDays) {
 var today = new Date();
 var expire = new Date();
 if (nDays==null || nDays==0) nDays=1;
 expire.setTime(today.getTime() + 3600000*24*nDays);
 document.cookie = cookieName+"="+escape(cookieValue)
                 + ";expires="+expire.toGMTString()
                 + "; path=/";
}

function getCookie(c_name)
{
    var i,x,y,ARRcookies=document.cookie.split(";");

    for (i=0;i<ARRcookies.length;i++)
    {
        x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
        y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
        x=x.replace(/^\s+|\s+$/g,"");
        if (x==c_name)
        {
            return unescape(y);
        }
     }
}



function pdxOpen()
{
	gameModifierClose();
	if(!pdx_loaded)
		$("#top_bar").append('<div id="pdx_window"></div>');

	$('#pdx_btn').parent('li').addClass('active');
	var pdx_window = $('#pdx_window');
	pdx_window.show();
	pdx_loaded = true;
	pdx_opened = true;
	pdx_window.animate({
	    height:"600px",
	  }, 200, function() {

	  });

}

function pdxHide()
{
	var pdx_window = $('#pdx_window');
	pdx_window.animate({
	    height:"0px",
	  }, 200, function() {
	  	pdx_window.hide();
	  	pdx_opened = false;
	  	$('#pdx_btn').parent('li').removeClass('active');
	  });
}

function pdxSearch(e) {

	var key = e.value;

	if(key.length < 2) {
		$("#pdx_search_list").empty();
		return;
	}

	$.ajax({
		url: '/pokedex',
		data: {
			method: 'search',
			key: key
		},
		type: 'post',
		success: function(wynik) { 
			if(wynik != '') {
				$("#pdx_search_list").empty();
				$("#pdx_search_list").html(wynik);
			}
		}
	});
}

function dbgOpen()
{
	$('#dbg_btn').parent('li').addClass('active');
	$('#dbg_window').show();
	setCookie("dbg_open", 1, 1);
}

function dbgHide()
{
	$('#dbg_window').hide();
	$('#dbg_btn').parent('li').removeClass('active');
	setCookie("dbg_open", 0, 1);
}


function drinkOak()
{	
	$.ajax({
		url: '/ajax',
		data: {
			method: 'drink_oak'
		},
		type: 'post',
		success: function(wynik) 
		{ 
			wynik = JSON.parse(wynik);
			if(wynik['w'] == 0)
			{
				gameAlert(wynik['t']);
			}
			else
			{
				$("#action_points_count").text($("#max_action_points_count").text());
				$("#action_points_progress").css('width', '100%');
				$("#dr_oak_drink_count").text(wynik['c']);
				showInfo(1, "Wypiłeś napój Profesora Oaka.");
			}
		}
	});
}


function drinkJuniper()
{	
	$.ajax({
		url: '/ajax',
		data: {
			method: 'drink_juniper'
		},
		type: 'post',
		success: function(wynik) 
		{ 
			wynik = JSON.parse(wynik);
			if(wynik['w'] == 0)
			{
				gameAlert(wynik['t']);
			}
			else
			{
				$("#action_points_count").text(wynik['ap']);
				$("#action_points_progress").css('width', wynik['percent'] + "%");
				$("#prof_juniper_drink_count").text(wynik['c']);
				showInfo(1, "Wypiłeś napój Profesora Junipera.");
			}
		}
	});
}


function depositIn()
{	
	$.ajax({
		url: '/ajax',
		data: {
			method: 'deposit_in'
		},
		type: 'post',
		success: function(wynik) 
		{ 
			wynik = JSON.parse(wynik);
			if(wynik['w'] == 0)
			{
				gameAlert(wynik['t']);
			}
			else
			{
				$("#money_anim").attr("moneydiff",-wynik['taken']);
				money_anim();
				$("#money").text('0 ¥');

				$("#money_deposit").text(wynik['c']+' ¥');

				$("#deposit_out_button").css('display','inline');
				$("#deposit_in_button").css('display','none');
				

				showInfo(1, "Wpłaciłeś wszystko do Depozytu.");
			}
		}
	});
}

function depositOut()
{	
	$.ajax({
		url: '/ajax',
		data: {
			method: 'deposit_out'
		},
		type: 'post',
		success: function(wynik) 
		{ 
			wynik = JSON.parse(wynik);
			if(wynik['w'] == 0)
			{
				gameAlert(wynik['t']);
			}
			else
			{
				$("#money_anim").attr("moneydiff",wynik['c']);
				money_anim();
				$("#money").text(wynik['money']+' ¥');


				$("#money_deposit").text("0 ¥");

				$("#deposit_out_button").css('display','none');
				$("#deposit_in_button").css('display','inline');

				showInfo(1, "Wypłaciłeś wszystko z Depozytu.");
			}
		}
	});
}

function healAll()
{	
	$.ajax({
		url: '/ajax',
		data: {
			method: 'heal_all'
		},
		type: 'post',
		success: function(wynik) 
		{ 
			wynik = JSON.parse(wynik);
			if(wynik['w'] == 0)
			{
				gameAlert(wynik['t']);
			}
			else
			{
				$("#money_anim").attr("moneydiff",-wynik['p']);
				money_anim();
				$("#money").text(wynik['money'] +' ¥');

				$(".not-full-health").each(function(){
					$(this).removeClass('gray')
						   .removeClass('not-full-health')
						   .addClass('light-blue')
						   .addClass('poke-select');

					var poke_id = $(this).attr('poke_id');
					$(this).attr('onclick',"poke_"+poke_id+".submit()");
					$(this).css('cursor','pointer');

					$(this).find('.poke-hp').text($(this).find('.poke-max-hp').text());
					$(this).find('.health').css('width','100%');
				});

				var hp = parseInt(wynik['hp']).numberFormat(0,'.','.');
				$("#pokemon_health_bar").css('width','100%');
				$("#pokemon_health_text").text('Życie: '+hp+' / '+hp);

				showInfo(1, "Wyleczyłeś wszystkie swoje pokemony.");

				if(wynik['done'])
					showInfo(1, "Wypełniłeś część zadania od Profesora Elma.");
			}
		}
	});
}

function healLider()
{	
	$.ajax({
		url: '/ajax',
		data: {
			method: 'heal_lider'
		},
		type: 'post',
		success: function(wynik) 
		{ 
			wynik = JSON.parse(wynik);
			if(wynik['w'] == 0)
			{
				gameAlert(wynik['t']);
			}
			else
			{
				$("#money_anim").attr("moneydiff",-wynik['p']);
				money_anim();
				$("#money").text(wynik['money'] +' ¥');
				
				showInfo(1, "Wyleczyłeś lidera.");

				var poke_id = wynik['poke_id'];

				$(".not-full-health").each(function(){

					if(poke_id == $(this).attr('poke_id')){ //jeżeli jest liderem

						$(this).removeClass('gray')
						   	   .removeClass('not-full-health')
						  	   .addClass('light-blue')
						  	   .addClass('poke-select');

						$(this).attr('onclick',"poke_"+poke_id+".submit()");
						$(this).css('cursor','pointer');

						$(this).find('.poke-hp').text($(this).find('.poke-max-hp').text());
						$(this).find('.health').css('width','100%');
					} 				
				});


				var hp = parseInt(wynik['hp']).numberFormat(0,'.','.');
				$("#pokemon_health_bar").css('width','100%');
				$("#pokemon_health_text").text('Życie: '+hp+' / '+hp);

				if(wynik['done'])
					showInfo(1, "Wypełniłeś część zadania od Profesora Elma.");
			}
		}
	});
}

function drinkFavourite()
{
	$.ajax({
		url: '/ajax',
		data: {
			method: 'drink_favourite'
		},
		type: 'post',
		success: function(wynik) 
		{ 
			wynik = JSON.parse(wynik);

			if(wynik['w'] == 0){
				gameAlert(wynik['t']);
			}
			else{
				$("#pokemon_health_bar").css('width', wynik['p'] + '%');
				$("#pokemon_health_text").text("Życie: " + wynik['h'] + " / " + wynik['mh']);
				$("#favourite_drink_count").text(wynik['fdc']);

				var poke_id = wynik['poke_id'];
				var pokemon = $("form[name='poke_"+poke_id+"']");

				pokemon.find('.box').removeClass('gray')
							  	   .addClass('light-blue')
							  	   .addClass('poke-select');

				if(wynik['remove_full_health'])
					pokemon.find('.box').removeClass('not-full-health');

				pokemon.attr('onclick',"poke_"+poke_id+".submit()");
				pokemon.css('cursor','pointer');

				pokemon.find('.poke-hp').text(wynik['h']);
				pokemon.find('.health').css('width',wynik['p']+'%');
					

				showInfo(1, "Wyleczyłeś Liderowi 50 punktów zdrowia.");
			}
		}
	});
}

function drinkFavouriteAndFight()
{
	$.ajax({
		url: '/ajax',
		data: {
			method: 'drink_favourite'
		},
		type: 'post',
		success: function(wynik) 
		{ 
			wynik = JSON.parse(wynik);

			if(wynik['w'] == 0){
				gameAlert(wynik['t']);
			}
			else{
				$("#pokemon_health_bar").css('width', wynik['p'] + '%');
				$("#pokemon_health_text").text("Życie: " + wynik['h'] + " / " + wynik['mh']);

				var pokemon_id = wynik['pokemon_id'];

				$("form[name='poke_"+pokemon_id+"']").submit();
				
				showInfo(1, "Wyleczyłeś Liderowi 50 punktów zdrowia.");
			}
		}
	});
}

function phToPa()
{	
	$.ajax({
		url: '/ajax',
		data: {
			method: 'ph_to_pa'
		},
		type: 'post',
		success: function(wynik) { 
			
			if(wynik == parseInt('-1'))
			{
				gameAlert("Nie posiadasz takiej ilości punktów honoru.");
			}
			else if(wynik == parseInt('-2'))
			{
				gameAlert("Nie możesz uzupełnić PA w Rezerwacie.");
			}
			else if(wynik == parseInt('-3'))
			{
				gameAlert("Nie możesz uzupełnić PA.");
			}
			else
			{
				var sum = parseInt($("#action_points_count").text()) + parseInt(wynik) * 5;
				var p = Math.round(parseInt($("#max_action_points_count").text()) / sum * 100);
				$("#action_points_count").text(sum);
				$("#action_points_progress").css('width', p + '%');
				showInfo(1, "Uzupełniłeś " + parseInt(wynik) * 5 + " punktów akcji, za " + wynik + "&pound.");
			}
			
			
		}
	});
}

function pdxLoad(page)
{	
	var pdx = $("#pdx_window");
	pdx.empty().html('<div id="loading"></div>');

	setCookie('pdx_last_page', getCookie('pdx_active_page'), 1);

	$.ajax({
		url: '/pokedex',
		data: {
			method: 'loadPage',
			page: page
		},
		type: 'post',
		success: function(wynik) { 
			if(wynik != '')
			{
				pdx.empty();
				pdx.html(wynik);
				setCookie('pdx_active_page', page, 1);
			}
		}
	});
}

function pdxAddToFavourite(page_id, btn) {
	$.ajax({
		url: '/pokedex',
		data: {
			method: 'add_to_favourite',
			page_id: page_id
		},
		type: 'post',
		success: function(wynik) { 
			if(wynik != '') {
				switch(parseInt(wynik)) {
					case 2: 
						$("#page_fav_btn").removeClass("no-fav");
						$("#page_fav_btn").addClass("fav");
					break;

					case 1: 
						gameAlert("Można mieć maksymalnie 8 ulubionych stron.");
					break;

					case 0: 
						$("#page_fav_btn").removeClass("fav");
						$("#page_fav_btn").addClass("no-fav");
					break;
				}
			}
		}
	});
}

function pdxVoteOnPokemon(pokemon_id) {
	$.ajax({
		url: '/pokedex',
		data: {
			method: 'vote_pokemon',
			pokemon_id: pokemon_id
		},
		type: 'post',
		success: function(wynik) { 
			if(wynik != '') {
				switch(parseInt(wynik)) {
					case 1: 
						$("#vote_poke_btn").addClass("blocked");
					break;

					case 0: 
						gameAlert("W tym tygodniu już głosowałeś na Pokemona.");
					break;
				}
			}
		}
	});
}

function pdxLoadLastPage() {
	var page = getCookie('pdx_last_page');
	if(page != null)
		pdxLoad(page);
}

function pdxOpenPage(page) {
	pdxOpen();
	pdxLoad(page);
}


function openItemList(p_id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'get_poke_item_list',
			   p_id: p_id},
		type: 'post',
		success: function(output) { 
			$('.new-item-list').html(output);
			$('.new-item-list').show();
		}
	});
}

function openResItemList(p_id){
	$.ajax({
		url: '/ajax',
		data: {method: 'get_poke_res_item_list',
			   p_id: p_id},
		type: 'post',
		success: function(output) { 
			$('.new-res-item-list').html(output);
			$('.new-res-item-list').show();
		}
	});
}

function close_poke_item_select(){
	$('.new-item-list').hide();
}

function close_poke_res_item_select(){
	$('.new-res-item-list').hide();
}


function addItem(item, p_id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'poke_items',
			   item: item,
			   type: 1,
			   p_id: p_id},
		type: 'post',
		success: function(output) { 
			
			if(output.trim() != '0' && output.trim() != '10') 
				$('.item-box').html(output);
			else if(output.trim() == '10') 
				showInfo(3, "Pokemon nie może trzymać dwóch takich samych przedmiotów.");
			else if(output.trim() == '0')
				showInfo(3,"Nie można dać przedmiotu Pokemonowi.");

			$('.new-item-list').hide();
		}
	});
}


function delItem(item, p_id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'poke_items',
			   item: item,
			   type: 0,
			   p_id: p_id},
		type: 'post',
		success: function(output) { 
			if(output != '0') {
				$('.item-box').html(output);
			}
		}
	});
}


function fastItemDel(item, p_id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'fast_item_del',
			   item: item,
			   p_id: p_id},
		type: 'post',
		success: function(output) { 
			if(output.trim() == "1")
				$('.item[name=' + item + '][poke_id='+p_id+']').remove();
			else
				showInfo(3, output);
		}
	});
}


function team_setLeader(id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'set_leader',
			   id: id},
		type: 'post',
		success: function(output) { 
			$('.poke-team-box').removeClass('leader');
			$('.poke-team-box[poke_id=' + id + ']').addClass('leader');
		}
	});
}

function team_setLeaderInfoCol(id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'set_leader',
			   id: id},
		type: 'post',
		success: function(output) { 
			$('.liderBtn').hide();
			$('.poke-team-box').removeClass('leader');
			$('.poke-team-box[poke_id=' + id + ']').addClass('leader');
		}
	});
}

function team_move(from, to, id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'move_to',
			   from: from,
			   to: to,
			   id: id},
		type: 'post',
		success: function(output) { 
			if(output.trim() != '') {
				showInfo(3, output);
			}
			else {
				if(from == 'druzyna') 
					$(".main_menu_poke[poke_id=" + id + "]").remove();

				team_get_poke_list(from, null, null);
				if(to == 'druzyna' || to == getCookie('active_poke_tab'))
					team_get_poke_list(to, null, null);
				else
				{
					var ilosc = parseInt($("span." + to + "-count-get").text());
					$("span." + to + "-count").text((ilosc + 1) + "");
				}
			}
		}
	});
}

function team_count_poke_group(name) {
	var ilosc = $("div#lista-" + name + " .p-counter").length;
	$("span." + name + "-count").text(ilosc);
}



function lock_unlock(id, pokebox) {
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'lock/unlock',
			   pokebox: pokebox,
			   id: id},
		type: 'post',
		success: function(output) { 
			var lock = $(".r-lock[poke_id=" + id + "]");
			var box = $(".rezerwa-box[poke_id=" + id + "]");
			
			if(output == 1) {
				lock.removeClass('unlocked');
				lock.addClass('locked');
				if(box.hasClass('orange') == false) {
					box.removeClass('light-blue');
					box.addClass('gray');
				}
			}
			else
			{
				lock.removeClass('locked');
				lock.addClass('unlocked');
				if(box.hasClass('orange') == false) {
					box.removeClass('gray');
					box.addClass('light-blue');
				}
			}
		}
	});
}

function ball_lock_unlock(id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'plecak',
			   func: 'lock/unlock',
			   id: id},
		type: 'post',
		success: function(output) { 
			var lock = $(".lock[item_id=" + id + "]");
			var locked_text = $("#lt_"+id);
			var locked_buttons = $("#li_"+id);
			
			if(output == 1) {
				lock.removeClass('unlocked');
				lock.addClass('locked');
				locked_text.show();
				locked_buttons.hide();
			}
			else
			{
				lock.removeClass('locked');
				lock.addClass('unlocked');
				locked_text.hide();
				locked_buttons.show();
			}
		}
	});
}

function evolve(id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'evolve',
			   id: id},
		type: 'post',
		success: function(output) { 
			if(output.trim() == '3') {
				team_get_poke_list('rezerwa', null, null);
				add_popup("icons/get_info.png", "Twój pokemon ewoluował!");
			}
			else if(output.trim() == '0') 
				add_popup("icons/error.png", "Ten pokemon nie posiada wyższych stadiów ewolucji.");
			else if(output.trim() == '1')
				add_popup("icons/error.png", "Tego pokemona można ewoluować tylko w zakładce stan drużny.");
			else if(output.trim() == '2')
				add_popup("icons/error.png", "Ten pokemon nie spełnia wszystkich wymagań do ewolucji.");
			else if(output.trim() == '4')
				add_popup("icons/error.png", "Nie można ewoluować zablokowanego Pokemona. Jeśli chcesz go ewoluować to odblokuj go klikając na kłódeczkę.");
			else if(output.trim() == '5')
				add_popup("icons/error.png", "Ten pokemon ma zablokowaną możliwość ewolucji. Odbokować tę możliwość możesz w zakładce Stan drużyny.");
			else if(output.trim() == '')
				add_popup("icons/error.png", "Błąd!");
			else
			{
				$("#info_window").remove();
				$('body').append(output);
			}
		}
	});
}


function evolve_advanced(id, next_id) {
	$.ajax({
		url: '/ajax',
		data: {
			method: 'team_poke',
			func: 'evolve_advanced',
			id: id,
			next_id: next_id
		},
		type: 'post',
		success: function (output) {
			if (output.trim() == '1') {
				team_get_poke_list('rezerwa', null, null);
				add_popup("icons/get_info.png", "Twój pokemon ewoluował!");
			} else if (output.trim() == '5')
				add_popup("icons/error.png", "Ten pokemon ma zablokowaną możliwość ewolucji. Odbokować tę możliwość możesz w zakładce Stan drużyny.");
			else
				add_popup("icons/get_info.png", "Błąd!");

			$("#info_window").remove();
			$('body').append(output);
		}
	});
}



function addNewPokeBoxGroup() {
	var name = $("#pb_group_name").val();
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'add_group',
			   name: name},
		type: 'post',
		success: function(output) { 
			if(output.trim() != '') 
				showInfo(3, output);
			else
				team_get_poke_list('pokebox', null, null);
		}
	});
}

function delPokeBoxGroup(group_id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'del_group',
			   group_id: group_id},
		type: 'post',
		success: function(output) { 
			if(output.trim() == '') 
				team_get_poke_list('pokebox', null, null);
		}
	});
}

function pb_search(t) {
	var sname = $(t).val();
	sname = sname.toLowerCase();

	if(sname.length <= 0) {
		$(".p-search").show();
		return;
	}

	$(".p-search").hide();
	$(".p-search[p_name^='"+sname+"']").each( function( index ) {
	  	$(this).show();
	});

}



function team_move_list(from, to) {

	 var list_id = $("input.check-" + from + ":checkbox:checked").map(function(){
      return $(this).attr('poke_id');
    }).get();
	 
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'move_to',
			   from: from,
			   to: to,
			   id: list_id},
		type: 'post',
		success: function(output) { 
			if(output.trim() != '') 
				showInfo(3, output);
			else
			{
				team_get_poke_list(from, null, null);
				if(to == 'druzyna')
					team_get_poke_list(to, null, null);
				else
				{
					var ilosc = parseInt($("span." + to + "-count-get").text());
					var plus = Object.keys(list_id).length;
					$("span." + to + "-count").text((ilosc + plus) + "");
				}
			}
		}
	});
}

function group_pokebox_move_list(selectbox) {

	var target_group = $(selectbox).val();

	var list_id = $("input.check-pokebox:checkbox:checked").map(function(){
      return $(this).attr('poke_id');
    }).get();
	 
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'group_move_to',
			   target_group: target_group,
			   id: list_id},
		type: 'post',
		success: function(output) { 
			if(output.trim() != '') 
				showInfo(3, output);
			else
				team_get_poke_list('pokebox', null, null);
		}
	});
}

function team_sort_poke_list(list_name, sort) {
	$("#sort-" + list_name+' a').removeClass('active');
	$("#sort-" + list_name+' a[sort_by=' + sort + ']').addClass('active');
	team_get_poke_list(list_name, sort, null);
}

function team_sort_poke_ord(list_name, dir) {
	$("#ord-" + list_name+' a').removeClass('active');
	$("#ord-" + list_name+' a[sort_ord=' + dir + ']').addClass('active');
	team_get_poke_list(list_name, null, dir);
}

function team_poke_list_pokebox_sort(group_id, sort) {
	$("#sort-pokebox-"+group_id+' a').removeClass('active');
	$("#sort-pokebox-"+group_id+' a[sort_by=' + sort + ']').addClass('active');

	$("#loader").show();
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'set_pokebox_sort',
			   group_id:group_id,
			   sort: sort},
		type: 'post',
		complete: function(output) {
			team_get_poke_list('pokebox', sort, null);
			$("#loader").hide();
		}
	});
	
}

function team_poke_list_pokebox_ord(group_id, dir) {
	$("#ord-pokebox-"+group_id+' a').removeClass('active');
	$("#ord-pokebox-"+group_id+' a[sort_ord=' + dir + ']').addClass('active');
	$("#loader").show();
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'set_pokebox_dir',
			   group_id:group_id,
			   dir: dir},
		type: 'post',
		complete: function(output) {
			team_get_poke_list('pokebox', null, null);
			$("#loader").hide();
		}
	});
	
}

function poke_change_tab(list_name) {
	team_get_poke_list(list_name, null, null);
	$(".tab_selector").removeClass('active');
	$(".tab_selector[tab="+list_name+"]").addClass('active');
	setCookie('active_poke_tab',list_name,1);
}

function team_get_poke_list(list_name, sort, dir) {
	$("#loader").show();
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'get_poke_list',
			   list_name: list_name,
			   sort: sort,
			   dir: dir},
		type: 'post',
		success: function(output) { 
			if(list_name == 'druzyna')
				$("#lista-druzyna").html(output);
			else
				$("#poke_content").html(output);
			team_count_poke_group(list_name);

		},
		complete: function(output) {
			$("#loader").hide();
		}
	});
	
}

function team_change_ord(dir, id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'change_ord',
			   dir: dir,
			   id: id},
		type: 'post',
		success: function(output) { 
			team_get_poke_list('druzyna', null, null);
		}
	});
}


function check_for_news() {
	$.ajax({
		url: '/ajax',
		data: {method: 'msg',
			   func: 'check_for_news'},
		type: 'post',
		success: function(output) { 

			if(output.trim() != '') {
				data = jQuery.parseJSON(output);

				$.each(data, function( id , d) {
					switch(d.type) {
						case 'new_msg': alert_new_msg(d); break;
						case 'warning_msg': show_warning_msg(d); break; 
						case 'voting': show_voting_msg(d); break; 
						case 'window': $("#info_window").remove();
									   $("body").append(d.html);
									   break;
					}
				});
			}
		}
	});
}

function show_voting_msg(output) {

	output.id = parseInt(output.id);
	if(displayed_voting_msg.indexOf(output.id) != -1) return;
	displayed_voting_msg.push(output.id);

	var msg = output.msg;
	gameAlert(msg);
}

function show_warning_msg(output) {

	output.id = parseInt(output.id);
	if(displayed_special_msg.indexOf(output.id) != -1) return;
	displayed_special_msg.push(output.id);
	

	var msg = output.msg;

	gameAlert(msg, function(data) {
		$.ajax({
			url: '/ajax',
			data: {method: 'msg',
				   func: 'special_msg_read',
				   id: output.id},
			type: 'post'
		});
	});
}

function alert_new_msg(output) {
	var msg_list = output.dane;
	var count = output.count;

	if(count > 0) {
		$("#message_count_info").text(count);
		$("#message_count_info").show();
	}

	$.each(msg_list, function( id , data) {

		if(data.text.length > 100)
			data.text = data.text.replace(/^(.{100}[^\s]*).*/, "$1") + '...';

		if(!data.login) {
			data.text += '<br/><br/><a href="/poczta/powiadomienia" class="niceButton" style="width: 100%;">Pokaż powiadomienie</a>';
			add_popup('icons/message-popup.png', data.text);
		}
		else {
			data.text += '<br/><br/><a href="/poczta/rozmowy/' + data.user_id + '" class="niceButton" style="width: 100%;">Pokaż rozmowę</a>';
	   		add_popup('icons/message-popup.png', '<strong>' + data.login + "</strong>: " + data.text);
		}
	});
}


function get_new_messages() {
	$.ajax({
		url: '/ajax',
		data: {method: 'msg',
			   func: 'get_new_messages'},
		type: 'post',
		success: function(output) { 

			if(output.trim() != '') {
				output = jQuery.parseJSON(output);

				var msg = output.dane;
				var count = output.count;

				if(count > 0) {
					$("#message_count_info").text(count);
					$("#message_count_info").show();
				}

				$.each(msg, function( id , data) {
					if(!data.login)
						add_popup('icons/message-popup.png', data.text);
					else
				   		add_popup('icons/message-popup.png', '<strong>' + data.login + "</strong>: " + data.text);
				});
				
			}
		}
	});
}



function htmlEntities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function rehtmlEntities(str) {
    return String(str).replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"');
}


function href_question(function_name,question){
	vex.dialog.open({
		message: question,
		buttons: [
			$.extend({}, vex.dialog.buttons.YES,{text:'Tak'}),
			$.extend({}, vex.dialog.buttons.NO,{text: 'Nie'})
		],
		callback: function(data){
			if(data){
				window[function_name]();
			}
		}
	});
}

function form_question(form_id, question, event) {

	if(event != null) {
		event.preventDefault();
		event.stopPropagation();
	}

    vex.dialog.open({
        message: question,
        buttons: [
            $.extend({}, vex.dialog.buttons.YES, { text: 'Tak' }),
            $.extend({}, vex.dialog.buttons.NO, { text: 'Nie' })
        ],
        callback: function (data) {
           if(data)
        		$('#'+form_id).submit();
        }
    });
}

function gameAlert(text, callback) {

    vex.dialog.open({
        message: text,
        buttons: [
            $.extend({}, vex.dialog.buttons.YES, { text: 'OK' }),
        ],
        callback: function (data) {
        	if(typeof callback === "function") 
           		callback();
        }
    });
}

function load_plecak(cat, format) {
	$.ajax({
		url: '/ajax',
		data: {method: 'plecak',
			   func: 'get_items',
				cat: cat,
				format: format},
		type: 'post',
		success: function(output) { 
			$("#item_"+cat+"_container").html(output);
		}
	});
}

function load_pokesklep(cat, format) {
	$.ajax({
		url: '/ajax',
		data: {method: 'pokesklep',
			   func: 'get_items',
				cat: cat,
				format: format},
		type: 'post',
		success: function(output) { 
			$("#item_"+cat+"_container").html(output);
		}
	});
}

function show_info_window(type, id) {

	$("#info_window").remove();

	$.ajax({
		url: '/ajax',
		data: {method: 'info_window',
			   func: type,
				id: id},
		type: 'post',
		success: function(output) { 
			if(output.length > 0)
				$("body").append(output);
		}
	});
}

function show_info_window(type, id, id2) {

	$("#info_window").remove();

	$.ajax({
		url: '/ajax',
		data: {method: 'info_window',
			   func: type,
				id: id,
				id2: id2},
		type: 'post',
		success: function(output) { 
			if(output.length > 0)
				$("body").append(output);
		}
	});
}



function close_info_window() {
	$("#info_window").remove();
}



//zarządzanie graczami na chacie

function chat_user_menager(id) {
	vex.dialog.open({
        message: "Co chcesz zrobić?",
        buttons: [
            $.extend({}, vex.dialog.buttons.NO, { className: 'vex-dialog-button-primary', text: 'Wyślij ostrzeżenie', click: function($vexContent, event) {
	            $vexContent.data().vex.value = 'send_warning';
	            vex.close($vexContent.data().vex.id);
	        }}),
	        /*
            $.extend({}, vex.dialog.buttons.NO, { className: 'vex-dialog-button-primary', text: 'Zablokuj', click: function($vexContent, event) {
	            $vexContent.data().vex.value = 'ban_chat';
	            vex.close($vexContent.data().vex.id);
	        }}),*/
        ],
        callback: function (data) {
         	switch(data) {
         		case 'send_warning': show_warning_prompt(id); break;
         		case 'ban_chat': show_ban_prompt(id); break;
         	}
        }
    });
}


function changePanelTab(tab_name, update_content) {

	$.ajax({
		url: '/ajax_panel',
		data: {method: 'load_tab',
			   tab_name: tab_name,
			   update_content: (update_content ? 1 : 0)},
		type: 'post',
		success: function(output) { 

			stop_time_quest_interval();

			if(output.trim() != '') 
				$("#info_col").html(output);

			if(output.trim() != '' || update_content == false) {
				$(".panel_tab_box .panel_tab").removeClass('active');
				$(".panel_tab_box .panel_tab."+tab_name+"_icon").addClass('active');
			}
		}
	});
}

function removePanelButton(tab_name) {
	$(".panel_tab_box .panel_tab."+tab_name+"_icon").remove();
}

function setPanelEventQuest(quest_num) {

	$.ajax({
		url: '/ajax_panel',
		data: {method: 'set_event_quest',
			   quest_num: quest_num},
		type: 'post',
		success: function(output) { 
			if(output == 1)
				changePanelTab("event", true);
		}
	});
}

function setPanelAchievementQuest(achievementId) {

	$.ajax({
		url: '/ajax_panel',
		data: {method: 'setAchievementQuest',
			achievementId: achievementId},
		type: 'post',
		success: function(output) {
			if(output == 1)
				changePanelTab("achievement_quest", true);
		}
	});
}

function disablePanelAchievementQuest() {

	$.ajax({
		url: '/ajax_panel',
		data: {method: 'disableAchievementQuestPreview'},
		type: 'post',
		success: function(output) {
			if(output == 1)
				changePanelTab("team", true);
		}
	});
}


function resetPanelLocationDrop() {

	$.ajax({
		url: '/ajax_panel',
		data: {method: 'reset_location_drop'},
		type: 'post',
		success: function(output) { 
			if(output == 1)
				changePanelTab("catch", true);
		}
	});
}

function changeCurrentDailyAction(action_name) {

	$.ajax({
		url: '/ajax_panel',
		data: {method: 'change_current_daily_action',
			   action_name: action_name},
		type: 'post',
		success: function(output) { 
			if(output == 1){
				changePanelTab("daily", true);
			}

		}
	});
}




function show_warning_prompt(id) {

	vex.dialog.prompt({
	message: "Wpisz treść ostrzeżenia",

	  placeholder: 'Treść',
	  callback: function(value) {
	  	if(value == false) return;
	  	console.log(value);
	   	$.ajax({
			url: '/ajax',
			data: {method: 'chat_admin',
				   func: 'send_warning',
				   user_id: id,
				   message: value},
			type: 'post'
		});
	  }
	});
}


function dont_share(id) {
	$.ajax({
		url: '/ajax',
		data: {method: 'team_poke',
			   func: 'dont_share',
			   id: id},
		type: 'post',
		success: function(output) { 
			if(output.trim() != '') {
				showInfo(3, output);
			}
			else {
				team_get_poke_list('shared', null, null);
			}
		}
	});
}


function osada_bld(dzialanie, x, y) {

	$.ajax({
		url: '/stowarzyszenie/twoje/osada/?' + dzialanie + '&x=' + x + '&y=' + y,
		data: {only_content: true},
		type: 'post',
		success: function(output) { 
			$("#content").html(output);
		}
	});
}



function profil_pelna_lista_gablotek(id) {

	$.ajax({
		url: '/ajax',
		data: {method: 'lista_gablotek',
			   id: id},
		type: 'post',
		success: function(output) { 
			$(".profile_region_progress_box").prepend(output);
			$(".profile_region_full_box").fadeIn();
		}
	});
}

function refresh_time_quest_page() {
	$.ajax({
		url: '/wyzwania-czasowe/wyzwanie?only-view=1',
		type: 'get',
		success: function(output) {
			$("#content").html(output);
		}
	});
}

function start_time_quest_page_interval() {
	if (time_quest_page_interval_enabled) {
		return;
	}

	time_quest_page_interval_enabled = true;
	time_quest_page_interval = setInterval(refresh_time_quest_page, 1000);
}

function stop_time_quest_page_interval() {
	clearInterval(time_quest_page_interval);
	time_quest_page_interval_enabled = false;
}

function start_time_quest_interval() {

	stop_time_quest_interval();
	time_quest_interval = setInterval(refresh_time_quest, 1000);
}

function stop_time_quest_interval() {

	clearInterval(time_quest_interval);
}

function start_assoc_quest_interval(){

	stop_assoc_quest_interval();
	assoc_quest_interval = setInterval(refresh_time_assoc_quest, 1000);
}

function stop_assoc_quest_interval(){
	clearInterval(assoc_quest_interval);
}

function refresh_time_assoc_quest(){

	var time = $("#assoc-quest-left-time").text().split(":");

	var hours = parseInt(time[0]);
	var minutes = parseInt(time[1]);
	var seconds = parseInt(time[2]);

	seconds--;
	if(seconds < 0){
		seconds = 59;

		minutes--;
		if(minutes < 0){
			minutes = 59;

			hours--;
			if(hours < 0){

				setAssocQuestTime(0,0,0);
				stop_assoc_quest_interval();
				return;
			}
		}
	}

	setAssocQuestTime(hours, minutes, seconds);
}

function setAssocQuestTime(hours, minutes, seconds){
	
	if(seconds < 10 && seconds >= 0){
		seconds = "0" + seconds;
	}

	if(minutes < 10 && minutes >= 0){
		minutes = "0" + minutes;
	}

	var text = hours + ":" + minutes + ":" + seconds;

	$("#assoc-quest-left-time").text(text);
}


function refresh_time_quest() {
	$.ajax({
		url: '/wyzwanie-czasowe/widok',
		type: 'get',
		success: function(output) {

			if (isObject(output)) {
				if (output.content.active === false) {
					changePanelTab('team', true);
					removePanelButton('time-quest');
				}
			} else {
				$(".time-quest").html(output);
			}
		}
	});
}





function BotDetector() {
	var self = this;
	self.isBot = false;
	self.tests = {};

	var selectedTests = [];
	if (selectedTests.length == 0 || selectedTests.indexOf(BotDetector.Tests.SCROLL) != -1) {
		self.tests[BotDetector.Tests.SCROLL] = function() {
			var e = function() {
				self.tests[BotDetector.Tests.SCROLL] = true;
				self.update()
				self.unbindEvent(window, BotDetector.Tests.SCROLL, e)
				self.unbindEvent(document, BotDetector.Tests.SCROLL, e)
			};
			self.bindEvent(window, BotDetector.Tests.SCROLL, e);
			self.bindEvent(document, BotDetector.Tests.SCROLL, e);
		};
	}
	if (selectedTests.length == 0 || selectedTests.indexOf(BotDetector.Tests.MOUSE) != -1) {
		self.tests[BotDetector.Tests.MOUSE] = function() {
			var e = function() {
				self.tests[BotDetector.Tests.MOUSE] = true;
				self.update();
				self.unbindEvent(window, BotDetector.Tests.MOUSE, e);
			}
			self.bindEvent(window, BotDetector.Tests.MOUSE, e);
		};
	}
	if (selectedTests.length == 0 || selectedTests.indexOf(BotDetector.Tests.KEYUP) != -1) {
		self.tests[BotDetector.Tests.KEYUP] = function() {
			var e = function() {
				self.tests[BotDetector.Tests.KEYUP] = true;
				self.update();
				self.unbindEvent(window, BotDetector.Tests.KEYUP, e);
			}
			self.bindEvent(window, BotDetector.Tests.KEYUP, e);
		};
	}
	if (selectedTests.length == 0 || selectedTests.indexOf(BotDetector.Tests.SWIPE) != -1) {
		self.tests[BotDetector.Tests.SWIPE_TOUCHSTART] = function() {
			var e = function() {
				self.tests[BotDetector.Tests.SWIPE_TOUCHSTART] = true;
				self.update();
				self.unbindEvent(document, BotDetector.Tests.SWIPE_TOUCHSTART);
			}
			self.bindEvent(document, BotDetector.Tests.SWIPE_TOUCHSTART);
		}
	}
	if (selectedTests.length == 0 || selectedTests.indexOf(BotDetector.Tests.DEVICE_MOTION) != -1) {
		self.tests[BotDetector.Tests.DEVICE_MOTION] = function() {
			var e = function(event) {
				if(event.rotationRate.alpha || event.rotationRate.beta || event.rotationRate.gamma) {
					var userAgent = navigator.userAgent.toLowerCase();
					var isAndroid = userAgent.indexOf('android') != -1;
					var beta = isAndroid ? event.rotationRate.beta : Math.round(event.rotationRate.beta / 10) * 10;
					var gamma = isAndroid ? event.rotationRate.gamma : Math.round(event.rotationRate.gamma / 10) * 10;
					if (!self.lastRotationData) {
						self.lastRotationData = {
							beta: beta,
							gamma: gamma
						};
					}
					else {
						var movement = beta != self.lastRotationData.beta || gamma != self.lastRotationData.gamma;
						if (isAndroid) {
							movement = movement && (beta > 0.2 || gamma > 0.2);
						}
						var args = { beta: beta, gamma: gamma }
						self.tests[BotDetector.Tests.DEVICE_MOTION] = movement;
						self.update();
						if (movement) {
							self.unbindEvent(window, BotDetector.Tests.DEVICE_MOTION, e);
						}
					}
				}
				else {
					self.tests[BotDetector.Tests.DEVICE_MOTION] = false;
				}

			}
			self.bindEvent(window, BotDetector.Tests.DEVICE_MOTION, e);
		}
	}
	if (selectedTests.length == 0 || selectedTests.indexOf(BotDetector.Tests.DEVICE_ORIENTATION) != -1) {
		self.tests[BotDetector.Tests.DEVICE_ORIENTATION] = function() {
			var e = function() {
				self.tests[BotDetector.Tests.DEVICE_ORIENTATION] = true;
				self.update();
				self.unbindEvent(window, BotDetector.Tests.DEVICE_ORIENTATION, e);
			}
			self.bindEvent(window, BotDetector.Tests.DEVICE_ORIENTATION);
		}
	}
	if (selectedTests.length == 0 || selectedTests.indexOf(BotDetector.Tests.DEVICE_ORIENTATION_MOZ) != -1) {
		self.tests[BotDetector.Tests.DEVICE_ORIENTATION_MOZ] = function() {
			var e = function() {
				self.tests[BotDetector.Tests.DEVICE_ORIENTATION_MOZ] = true;
				self.update();
				self.unbindEvent(window, BotDetector.Tests.DEVICE_ORIENTATION_MOZ);
			}
			self.bindEvent(window, BotDetector.Tests.DEVICE_ORIENTATION_MOZ);
		}
	}


	self.cases = {};
	self.detected = false;
}

BotDetector.Tests = {
	KEYUP: 'keyup',
	MOUSE: 'mousemove',
	SWIPE: 'swipe',
	SWIPE_TOUCHSTART: 'touchstart',
	SWIPE_TOUCHMOVE: 'touchmove',
	SWIPE_TOUCHEND: 'touchend',
	SCROLL: 'scroll',
	GESTURE: 'gesture',
	GYROSCOPE: 'gyroscope',
	DEVICE_MOTION: 'devicemotion',
	DEVICE_ORIENTATION: 'deviceorientation',
	DEVICE_ORIENTATION_MOZ: 'MozOrientation'
};
BotDetector.prototype.update = function() {
	var self = this;
	var count = 0;
	var tests = 0;
	for(var i in self.tests) {
		if (self.tests.hasOwnProperty(i)) {
			self.cases[i] = self.tests[i] === true;
			if (self.cases[i] === true) {
				count++;
			}
		}
		tests++;
	}
	self.isBot = count ==  0;
	self.allMatched = count == tests;
}

BotDetector.prototype.bindEvent = function(e, type, handler) {
	if (e.addEventListener) {
		e.addEventListener(type, handler, false);
	}
	else if(e.attachEvent) {
		e.attachEvent("on" + type, handler);
	}
};

BotDetector.prototype.unbindEvent = function(e, type, handle) {
	if (e.removeEventListener) {
		e.removeEventListener(type, handle, false);
	}
	else {
		var evtName = "on" + type;
		if (e.detachEvent) {
			if (typeof e[evtName] === 'undefined') {
				e[type] = null
			}
			e.detachEvent(evtName)
		}
	}
};
BotDetector.prototype.monitor = function() {
	for(var i in this.tests) {
		if (this.tests.hasOwnProperty(i)) {
			this.tests[i].call();
		}
	}
	this.update();
};







var mouseSamplingInterval = 50;
var mouseSamples = [];
var clicksCount = 0;

var cursorPosition = {
	x: -1,
	y: -1,
}

let botDetector = new BotDetector();
botDetector.monitor();

function MouseSample(x, y, velocity) {
	this.x = x;
	this.y = y;
	this.velocity = velocity;
	this.deviation = 0;
	this.angle = 0;
}

document.addEventListener('mousemove', event => {
	cursorPosition.x = event.pageX;
	cursorPosition.y = event.pageY;
});

setInterval(function() {
	if (cursorPosition.x === -1) {
		return;
	}

	if (mouseSamples.length === 0) {
		let sample = new MouseSample(cursorPosition.x, cursorPosition.y, 0, 0);
		mouseSamples.push(sample);
		return;
	}

	let last = mouseSamples.slice(-1)[0];

	let diffX = cursorPosition.x - last.x;
	let diffY = cursorPosition.y - last.y;
	let distance = Math.sqrt(Math.pow(diffX, 2) + Math.pow(diffY, 2));
	let velocity = distance * 1000 / mouseSamplingInterval;
	let sample = new MouseSample(cursorPosition.x, cursorPosition.y, velocity);

	if (velocity <= 30) {
		return;
	}

	if (mouseSamples.length > 1) {
		let lastTwo = mouseSamples.slice(-2);

		let prevAngle    = getAngleBetweenSamples(lastTwo[0], lastTwo[1]);
		let currentAngle = getAngleBetweenSamples(lastTwo[1], cursorPosition);
		sample.deviation = getSmallestDiffBetweenAngles(prevAngle, currentAngle);
		sample.angle = currentAngle;
	}

	mouseSamples.push(sample);

}, mouseSamplingInterval);

function prepareSamplesResults(event)
{
	let samples = mouseSamples.slice(2);

	if (samples.length > 200) {
		samples = samples.slice(-200);
	}

	let sbd = false;
	if (navigator.webdriver == true || window.document.documentElement.getAttribute("webdriver") || window.callPhantom || window._phantom) {
		sbd = true;
	}

	let hiddenSelectors = [];
	const selectors = [
		['.loc-poke', '.loc-poke .half-white']
	];

	selectors.forEach(selectorPair => {
		if (document.querySelector(selectorPair[0])) {
			const element = document.querySelector(selectorPair[1]);
			let style = window.getComputedStyle(element);
			if (!element || element.hidden || style.display === 'none' || style.visibility === 'hidden') {
				hiddenSelectors.push(selectorPair[1]);
			}
		}
	});

	let data = {
		scroll: 	  botDetector.tests[BotDetector.Tests.SCROLL] === true,
		deviceMotion: botDetector.tests[BotDetector.Tests.DEVICE_MOTION] === true,
		gyroscope:    botDetector.tests[BotDetector.Tests.GYROSCOPE] === true,
		clicksCount:  clicksCount,
		sbd: 		  sbd,
		automationDetected: runBotDetection(),
		clickPosition: {
			x: event.pageX,
			y: event.pageY
		},
		movement: {
			samplesAmount: samples.length
		},
		hiddenSelectorsCount: hiddenSelectors.length,
		newProps: findNewProps()
	};

	if (samples.length === 0) {
		return data;
	}

	let avgDeviation = avgFromSamples(samples, 'deviation').toFixed(2);
	data.movement = {
		samplesAmount: samples.length,
		velocityMin:  samples.hasMin('velocity').velocity.toFixed(2),
		velocityMax:  samples.hasMax('velocity').velocity.toFixed(2),
		velocityAvg:  avgFromSamples(samples, 'velocity').toFixed(2),
		deviationMin: samples.hasMin('deviation').deviation.toFixed(2),
		deviationMax: samples.hasMax('deviation').deviation.toFixed(2),
		deviationAvg: avgDeviation,
		straightLine: parseInt(avgDeviation) === 0
	}

	return data;
}

function avgFromSamples(samples, variable)
{
	if (samples.length === 0) {
		return 0;
	}

	let sum = 0;
	samples.forEach(function(element, index){
		sum += element[variable];
	});

	return sum / samples.length;
}

function getAngleBetweenSamples(sampleA, sampleB)
{
	return Math.atan2(sampleB.y - sampleA.y, sampleB.x - sampleA.x) * 180 / Math.PI + 180;
}

function getSmallestDiffBetweenAngles(angleA, angleB)
{
	let diff1 = Math.abs(angleA - angleB);
	let diff2;

	if (angleA > angleB) {
		diff2 = Math.abs(360 - angleA + angleB);
	} else {
		diff2 = Math.abs(360 - angleB + angleA);
	}

	return diff1 < diff2 ? diff1 : diff2;
}

Array.prototype.hasMin = function(attrib) {
	return (this.length && this.reduce(function(prev, curr){
		return prev[attrib] < curr[attrib] ? prev : curr;
	})) || null;
}


Array.prototype.hasMax = function(attrib) {
	return (this.length && this.reduce(function(prev, curr){
		return prev[attrib] > curr[attrib] ? prev : curr;
	})) || null;
}

$(document).on('click touch', function (event) {
	clicksCount++
	let result = prepareSamplesResults(event);
	let base64 = window.btoa(JSON.stringify(result));

	setCookie('mdata',base64);
});

runBotDetection = function () {
	var documentDetectionKeys = [
		"__webdriver_evaluate",
		"__selenium_evaluate",
		"__webdriver_script_function",
		"__webdriver_script_func",
		"__webdriver_script_fn",
		"__fxdriver_evaluate",
		"__driver_unwrapped",
		"__webdriver_unwrapped",
		"__driver_evaluate",
		"__selenium_unwrapped",
		"__fxdriver_unwrapped",
	];

	var windowDetectionKeys = [
		"_phantom",
		"__nightmare",
		"_selenium",
		"callPhantom",
		"callSelenium",
		"_Selenium_IDE_Recorder",
	];

	for (const windowDetectionKey in windowDetectionKeys) {
		const windowDetectionKeyValue = windowDetectionKeys[windowDetectionKey];
		if (window[windowDetectionKeyValue]) {
			return true;
		}
	};
	for (const documentDetectionKey in documentDetectionKeys) {
		const documentDetectionKeyValue = documentDetectionKeys[documentDetectionKey];
		if (window['document'][documentDetectionKeyValue]) {
			return true;
		}
	};

	for (const documentKey in window['document']) {
		if (documentKey.match(/\$[a-z]dc_/) && window['document'][documentKey]['cache_']) {
			return true;
		}
	}

	if (window['external'] && window['external'].toString() && (window['external'].toString()['indexOf']('Sequentum') != -1)) return true;

	if (window['document']['documentElement']['getAttribute']('selenium')) return true;
	if (window['document']['documentElement']['getAttribute']('webdriver')) return true;
	if (window['document']['documentElement']['getAttribute']('driver')) return true;

	return false;
};

function findNewProps() {
	let allowed = [
		'location',
		'implementation',
		'URL',
		'documentURI',
		'compatMode',
		'characterSet',
		'charset',
		'inputEncoding',
		'contentType',
		'doctype',
		'documentElement',
		'xmlEncoding',
		'xmlVersion',
		'xmlStandalone',
		'pictureInPictureEnabled',
		'timeline',
		'fonts',
		'scrollingElement',
		'webkitFullscreenEnabled',
		'webkitFullscreenElement',
		'webkitIsFullScreen',
		'webkitFullScreenKeyboardInputAllowed',
		'webkitCurrentFullScreenElement',
		'domain',
		'referrer',
		'cookie',
		'lastModified',
		'readyState',
		'title',
		'dir',
		'body',
		'head',
		'images',
		'embeds',
		'plugins',
		'links',
		'forms',
		'scripts',
		'currentScript',
		'defaultView',
		'designMode',
		'onreadystatechange',
		'fgColor',
		'linkColor',
		'vlinkColor',
		'alinkColor',
		'bgColor',
		'anchors',
		'applets',
		'all',
		'hidden',
		'visibilityState',
		'onvisibilitychange',
		'oncopy',
		'oncut',
		'onpaste',
		'activeElement',
		'pictureInPictureElement',
		'styleSheets',
		'pointerLockElement',
		'onabort',
		'onblur',
		'oncancel',
		'oncanplay',
		'oncanplaythrough',
		'onchange',
		'onclick',
		'onclose',
		'oncontextmenu',
		'oncuechange',
		'ondblclick',
		'ondrag',
		'ondragend',
		'ondragenter',
		'ondragleave',
		'ondragover',
		'ondragstart',
		'ondrop',
		'ondurationchange',
		'onemptied',
		'onended',
		'onerror',
		'onfocus',
		'onformdata',
		'oninput',
		'oninvalid',
		'onkeydown',
		'onkeypress',
		'onkeyup',
		'onload',
		'onloadeddata',
		'onloadedmetadata',
		'onloadstart',
		'onmousedown',
		'onmouseenter',
		'onmouseleave',
		'onmousemove',
		'onmouseout',
		'onmouseover',
		'onmouseup',
		'onpause',
		'onplay',
		'onplaying',
		'onprogress',
		'onratechange',
		'onreset',
		'onresize',
		'onscroll',
		'onsecuritypolicyviolation',
		'onseeked',
		'onseeking',
		'onselect',
		'onslotchange',
		'onstalled',
		'onsubmit',
		'onsuspend',
		'ontimeupdate',
		'ontoggle',
		'onvolumechange',
		'onwaiting',
		'onwebkitanimationend',
		'onwebkitanimationiteration',
		'onwebkitanimationstart',
		'onwebkittransitionend',
		'onwheel',
		'onmousewheel',
		'onanimationstart',
		'onanimationiteration',
		'onanimationend',
		'onanimationcancel',
		'ontransitionrun',
		'ontransitionstart',
		'ontransitionend',
		'ontransitioncancel',
		'ongotpointercapture',
		'onlostpointercapture',
		'onpointerdown',
		'onpointermove',
		'onpointerup',
		'onpointercancel',
		'onpointerover',
		'onpointerout',
		'onpointerenter',
		'onpointerleave',
		'onselectstart',
		'onselectionchange',
		'children',
		'firstElementChild',
		'lastElementChild',
		'childElementCount',
		'rootElement',
		'getElementsByTagName',
		'getElementsByTagNameNS',
		'getElementsByClassName',
		'createElement',
		'createElementNS',
		'createDocumentFragment',
		'createTextNode',
		'createCDATASection',
		'createComment',
		'createProcessingInstruction',
		'importNode',
		'adoptNode',
		'createAttribute',
		'createAttributeNS',
		'createEvent',
		'createRange',
		'createNodeIterator',
		'createTreeWalker',
		'getOverrideStyle',
		'caretRangeFromPoint',
		'getCSSCanvasContext',
		'exitPictureInPicture',
		'webkitExitFullscreen',
		'webkitCancelFullScreen',
		'getElementsByName',
		'open',
		'close',
		'write',
		'writeln',
		'hasFocus',
		'execCommand',
		'queryCommandEnabled',
		'queryCommandIndeterm',
		'queryCommandState',
		'queryCommandSupported',
		'queryCommandValue',
		'clear',
		'captureEvents',
		'releaseEvents',
		'exitPointerLock',
		'getSelection',
		'hasStorageAccess',
		'requestStorageAccess',
		'elementFromPoint',
		'elementsFromPoint',
		'getAnimations',
		'getElementById',
		'prepend',
		'append',
		'replaceChildren',
		'querySelector',
		'querySelectorAll',
		'createExpression',
		'createNSResolver',
		'evaluate',
		'nodeType',
		'nodeName',
		'baseURI',
		'isConnected',
		'ownerDocument',
		'parentNode',
		'parentElement',
		'childNodes',
		'firstChild',
		'lastChild',
		'previousSibling',
		'nextSibling',
		'nodeValue',
		'textContent',
		'getRootNode',
		'hasChildNodes',
		'normalize',
		'cloneNode',
		'isEqualNode',
		'isSameNode',
		'compareDocumentPosition',
		'contains',
		'lookupPrefix',
		'lookupNamespaceURI',
		'isDefaultNamespace',
		'insertBefore',
		'appendChild',
		'replaceChild',
		'removeChild',
		'ELEMENT_NODE',
		'ATTRIBUTE_NODE',
		'TEXT_NODE',
		'CDATA_SECTION_NODE',
		'ENTITY_REFERENCE_NODE',
		'ENTITY_NODE',
		'PROCESSING_INSTRUCTION_NODE',
		'COMMENT_NODE',
		'DOCUMENT_NODE',
		'DOCUMENT_TYPE_NODE',
		'DOCUMENT_FRAGMENT_NODE',
		'NOTATION_NODE',
		'DOCUMENT_POSITION_DISCONNECTED',
		'DOCUMENT_POSITION_PRECEDING',
		'DOCUMENT_POSITION_FOLLOWING',
		'DOCUMENT_POSITION_CONTAINS',
		'DOCUMENT_POSITION_CONTAINED_BY',
		'DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC',
		'addEventListener',
		'removeEventListener',
		'dispatchEvent',
		"onpointerlockchange","onpointerlockerror","wasDiscarded","featurePolicy","webkitVisibilityState","webkitHidden","onbeforecopy","onbeforecut","onbeforepaste","onfreeze","onresume","onsearch","fullscreenEnabled","fullscreen","onfullscreenchange","onfullscreenerror","onwebkitfullscreenchange","onwebkitfullscreenerror","onbeforexrselect","onbeforeinput","oncontextlost","oncontextrestored","onauxclick","onpointerrawupdate","fullscreenElement","adoptedStyleSheets","exitFullscreen","oncontentvisibilityautostatechange","prerendering","onprerenderingchange","fragmentDirective","onbeforematch","ontouchcancel","ontouchend","ontouchmove","ontouchstart"
	];

	let newProps = [];
	for (let prop in document) {
		if (allowed.indexOf(prop) === -1 && !prop.includes('poke') && !prop.includes('poluj') && !prop.includes('jQuery')) {
			newProps.push(prop);
		}
	}

	return newProps;
}

function gameModifierOpen()
{
	pdxHide();
	$('#game_modifier_btn').parent('li').addClass('active');
	var modifierWindow = $('#game_modifier_window');
	modifierWindow.show();
	game_modifier_open = true;
	modifierWindow.animate({
		height:"300px",
	}, 200, function() {

	});
}

function gameModifierClose()
{
	$('#game_modifier_btn').parent('li').removeClass('active');
	var modifierWindow = $('#game_modifier_window');
	modifierWindow.animate({
		height:"0px",
	}, 200, function() {
		modifierWindow.hide();
		game_modifier_open = false;
		$('#pdx_btn').parent('li').removeClass('active');
	});
}