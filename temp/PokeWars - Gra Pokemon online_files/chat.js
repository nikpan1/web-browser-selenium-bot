$(document).ready(function(){
	
	setInterval(checkMessages, 2000);

	setInterval(count_down_timer, 1000);

	var last_msg_id = getCookie('last_message');
	var last_msg_timestamp = 0;
	var last_user_active = Math.round(new Date().getTime()/1000);
	var active_refresh_lock = false;

	var time_counter = 0;

	var chat_otwarty = getCookie('chat');
	
	var active_tab = getCookie('chat_tab');


	$(window).mousemove(function(){
		last_user_active = Math.round(new Date().getTime()/1000);
	});

	$(window).keydown(function(){
		last_user_active = Math.round(new Date().getTime()/1000);
	});


	$('#chat_input').keydown(function(event) 
	{
 		if (event.which == 13) 
    		send_message();
	});

	$('#chat_submit').click(function(){send_message()});


	$(".login_picker").click(function(){
		var login = $(this).attr("login");
		$("#chat_input").val(login+", ");
	});



	$(".chat_tab").click(function()
	{
		var t = $(this).attr('tab_id');
		select_tab(t);
	});

	$('#chat_hide_btn').click(function(){
		if(getCookie('chat') == 1)
		{
			$(this).empty();
			close_chat(true);
			chat_otwarty = 0;
		}
		else
		{
			$(this).empty();
			open_chat(true);
			chat_otwarty = 1;
		}
	});
	

	if(typeof active_tab === "undefined")
	{
		active_tab = 0;
		setCookie('chat_tab',active_tab,10);
	}
	
	if(chat_otwarty == 1)
		open_chat(false);
	else
		close_chat(false);


	$(".chat_message_box").hide();
	$(".chat_tab[tab_id="+active_tab+"]").addClass( "active" );
	$(".chat_message_box[tab_id="+active_tab+"]").show();
	$(".chat_message_box[tab_id="+active_tab+"]").scrollTop($(".chat_message_box[tab_id="+active_tab+"]")[0].scrollHeight);

	function open_chat(animate) {
		if(animate)
			$("#chat_window").animate({ bottom: 40 }, "fast");
		else
			$("#chat_window").css('bottom', 40);
		$('#chat_hide_btn').html("&#8595;");
		setCookie('chat',1,1);
	}

	function close_chat(animate) {
		if(animate)
			$("#chat_window").animate({ bottom: -200 }, "fast");
		else
			$("#chat_window").css('bottom', -200);
		$('#chat_hide_btn').html("&#8593;");
		setCookie('chat',0,1);
	}

	function select_tab(tab_id)
	{
		if(tab_id != active_tab) {
			$(".chat_tab").removeClass( "active" );
			$(".chat_tab[tab_id="+tab_id+"]").addClass( "active" );

			$(".chat_message_box").hide();
			$(".chat_message_box[tab_id="+tab_id+"]").show();
				
			active_tab = tab_id;
			setCookie('chat_tab',active_tab,1);

			loadMessages(false);
		}

		if(getCookie('chat') == 0 || chat_otwarty == 0)
		{
			$('#chat_hide_btn').empty();
			open_chat(true);
			chat_otwarty = 1;
		}
	}



	function zgloszono()
	{
		var NewDialog = $('<div id="zgloszono_chat_dialog">\
	        <p>Wiadomość została zgłoszona do administracji.</p>\
	    </div>');
	    NewDialog.dialog({
	        modal: true,
	        title: "Zgłoś gracza",
	        hide: 'puff',
	        buttons: [
	         {text: "OK", click: function() {$(this).dialog("close")}}
	        ]
	    });
	}

	function start_counting()
	{
		var time_now = Math.round(new Date().getTime() / 1000);
		time_counter = last_msg_timestamp + 3 - time_now;
		$('#chat_input_mask').html('Nie tak szybko <img src="img/smilies/smile.png" border="0" height="17">&nbsp;&nbsp;&nbsp;&nbsp;Odczekaj: '+time_counter);
		$('#chat_input_mask').show();
	}

	function count_down_timer()
	{
		$('#chat_input_mask').empty();
		if(time_counter > 0)
		{
			$('#chat_input_mask').html('Nie tak szybko <img src="img/smilies/smile.png" border="0" height="17">&nbsp;&nbsp;&nbsp;&nbsp;Odczekaj: '+time_counter);
			time_counter--;
		}
		else
			$('#chat_input_mask').hide();
	}



	function send_message()
	{
		var text = $('#chat_input').val();
		
		var time_now = Math.round(new Date().getTime() / 1000);

		if(text == '') return 0;
		
		if(chat_otwarty == 0) return 0;
		
		if(last_msg_timestamp + 3 > time_now) {
			start_counting();
			return 0;
		}	

		if((text.indexOf('/targ/oferta/') != -1 || (text.indexOf('/profil') != -1 && text.indexOf('/oferty') != -1)) && active_tab == 0) {
		    pokazOstrzezenieUniwersalne("Na chacie ogólnym nie można umieszczać ofert sprzedaży.");
			return 0;
		}


		if(text.length > 400) {
			gameAlert('Twoja wiadomość jest za długa (max 400 znaków).');
			return 0;
		}

		$.ajax({
			url: '/ajax_chat',
			data: {method: 'chat_send',
				   message:  text,
				   group: active_tab},
			type: 'post',
			success: function(output) { 
				last_msg_timestamp = time_now;
				checkMessages();
				$("#chat_input").val('');
				$(".no-messages-info").remove();
				if(output == 2)
					gameAlert("Nie powtarzaj swoich wiadomości.");

				if(output == 3)
					pokazOstrzezenieCenzora();

				if(output == 4)
					pokazOstrzezenieUniwersalne("Na chacie handlowym można wysyłać jedną wiadomość na 5 minut.");
			},
			error: function(output) {
				gameAlert("Brak połączenia z serwerem. Spróbuj jeszcze raz lub odśwież stronę.");
			}
		});

	}





	function checkMessages()
	{

		if(getCookie('chat') == 0 || chat_otwarty == 0) return;

		if(last_user_active + 60 < Math.round(new Date().getTime()/1000) && active_refresh_lock == false && chat_active_refresh_lock == true) {
			$(".chat_message_box[tab_id="+active_tab+"]").empty();
			$(".chat_message_box[tab_id="+active_tab+"]").append('<div style="text-align:center; width:100%; margin-top:100px;" class="chat_active_info">Z powodu braku Twojej aktywności odświeżanie chatu zostało wyłączone.</div>');
			active_refresh_lock = true;
			return;
		}

		if(last_user_active + 60 > Math.round(new Date().getTime()/1000) && active_refresh_lock == true) {
			loadMessages();
			active_refresh_lock = false;
		}
		else
		{
			$.ajax({
				url: '/ajax_chat',
				data: {method: 'chat_update',	
					   group: active_tab,
					   last_id: last_msg_id,
				       mobile: false},
				type: 'post',
				success: function(output) { 
					var data = jQuery.parseJSON(output);
					if(data.count > 0) {
						$.each( data.messages, function( index, dane) {
						  	$(".chat_message_box[tab_id="+active_tab+"]").append(messageFromData(dane));
						});

					 	if($(".chat_message_box[tab_id="+active_tab+"]")[0].scrollHeight/1.55 < $(".chat_message_box[tab_id="+active_tab+"]").scrollTop())
							$(".chat_message_box[tab_id="+active_tab+"]").scrollTop($(".chat_message_box[tab_id="+active_tab+"]")[0].scrollHeight);

					}

				}
			});
		}
	}

	function loadMessages()
	{	

		$(".chat_message_box[tab_id="+active_tab+"]").empty();
		$(".chat_message_box[tab_id="+active_tab+"]").append('<div style="text-align:center; width:100%; margin-top:100px;"><img src="img/icons/loading.gif"/></div>');
		$.ajax({
			url: '/ajax_chat',
			data: {method: 'chat_load',	
				   group: active_tab,
				   mobile: false},
			type: 'post',
			success: function(output) { 

				$(".chat_message_box[tab_id="+active_tab+"]").empty();
			
				var data = jQuery.parseJSON(output);
				
				if(data.count > 0) {
					$.each( data.messages, function( index, dane) {
	
					  	$(".chat_message_box[tab_id="+active_tab+"]").append(messageFromData(dane));
					});
					$(".chat_message_box[tab_id="+active_tab+"]").scrollTop($(".chat_message_box[tab_id="+active_tab+"]")[0].scrollHeight);
				}
				else
					$(".chat_message_box[tab_id="+active_tab+"]").append('<div class="no-messages-info" style="width: 100%;  text-align:center; margin-top: 10px;">Brak wiadomości</div>');
			},
			error: function(output) {
				$(".chat_message_box[tab_id="+active_tab+"]").empty();
				$(".chat_message_box[tab_id="+active_tab+"]").append('<div class="no-messages-info" style="width: 100%;  text-align:center; margin-top: 10px;">Brak połączenia z serwerem. Odśwież stronę.</div>');
			}
		});
	}

	function curHeight(element){
	   return $(element).height();
	}





	function messageFromData(data) {
		switch(data.type) {

			case '0':
				var status = '';
				var color = '';
				var login = data.login;
				var timestamp = Math.floor(Date.now() / 1000);

				if(data.color != '')
					var color = 'style="background: ' + data.color + '"';
				else 
					var color = '';


				if(data.user_id == getCookie('user_id')) {
					var message = '<div class="chat_message" post_id="' + data.id + '" time="' + data.time + '">';
						message +='<div class="text you"><div class="time"> ' + data.time + '</div>' + data.text + '</div><div class="clear"></div></div>';
				}
				else
				{
					if(data.user_id == 1) color = '#f3fff4';
					
					if(data.rang != 0)
						login = data.login_code.replace('{login}', login);

									
					if(data.last_active >= timestamp - 300 && data.offline_mode == false)
						var icons = '<img src="img/icons/icon_online.png" title="Online" width="10" height="10" class="login_picker" login="' + data.login + '"/>';
					else
						var icons = '<img src="img/icons/icon_offline.png" title="Online" width="10" height="10" class="login_picker" login="' + data.login + '"/>';

					icons += '<img src="/img/icons/report_icon.png" width="12" height="12" onclick="chat_report(' + data.id + ');" class="report_icon"/> ';

					var message = '<div class="chat_message" user_id="' + data.user_id + '" post_id="' + data.id + '" '+ color + ' time="' + data.time + '">';
						message +='<div class="info-box">' + icons + '</div>';
						message +='<div class="text other"><div class="time"> ' + data.time + '</div><div class="title"><a href="/profil/' + data.user_id + '" title="Przejdź do profilu" >' + login +'</a></div>' + data.text + '</div><div class="clear"></div></div>';
				}

			break;

			case '1':
				var message = '<div class="chat_ad">'+data.text+'</div>';
			break;

			case '2':
				if(data.timestamp >= timestamp - 60)
					show_contest_question(data.id, data.type, data.text);
				var message = '<div class="chat_ad">'+data.text+'</div>';
			break;

			case '3':
				if(data.timestamp >= timestamp - 60)
					show_contest_answer(data.id, data.type, data.text);
				var message = '<div class="chat_ad">'+data.text+'</div>';
			break;

			case '4':
				var message = '<div class="chat_ph_offert">'+data.text+'</div>';
			break;

			case '5':
				var message = '<div class="chat_fanpage">'+data.text+'<div class="clear" style="margin-top: 5px;"></div><a href="https://www.facebook.com/PokeWarsPL" class="niceButton" target="_blank">Wejdź na FanPage</a></div>';
			break;

		}

		if(data.to_you)
			message = '<strong>' + message + '</strong>';

		return message;
	}



});

function pokazFormularzCenzora() {


	vex.dialog.open({
		message: "Jesteś pewny, że nie użyłeś w tej wiadomości wulgaryzmu?",
		buttons: [
			$.extend({}, vex.dialog.buttons.YES,{text:'Tak, wyślij zgłoszenie'}),
			$.extend({}, vex.dialog.buttons.NO,{text: 'Nie'})
		],
		callback: function(data){
			if(data){

				$.ajax({
					url: '/ajax_chat',
					data: {method: 'add_exception'},
					type: 'post',
					success: function(output) { 

						if(output == 1)
							gameAlert("Dziękujemy za wysłanie zgłoszenia. Jeśli nie użyłeś wulgaryzmu to zgłoszone słowa zostaną dodane do słownika wyjątków.");

						$(".chat_info_mask").remove();
					}
				});
				
			}
		}
	});
}


function pokazOstrzezenieCenzora() {

	var html = "<div class='chat_info_mask'>"
					+ "<div class='chat_jenny'></div>"
					+ "<div class='chat_info_content'>"
						+ "<div class='jenny_text'>"
							+ "Nieładnie!<br/>W PokeWars nie wolno używać wulgaryzmów."
						+ "</div>"
						+ "<div class='control_box'>"
							+ "<a class='niceButton' onclick='$(\".chat_info_mask\").remove();'>Ok, rozumiem</a>"
						+ "</div>"
						+ "<div class='control_box'>"
							+ "<a style='font-size:12px;' onclick='pokazFormularzCenzora();'>Nie użyłem wulgaryzmu, <br/>Cenzor się pomylił.</a>"
						+ "</div>"
					+ "</div>"
				+ "</div>";

	$("#chat_window").append(html);
}

function pokazOstrzezenieUniwersalne(text) {

	var html = "<div class='chat_info_mask'>"
					+ "<div class='chat_jenny'></div>"
					+ "<div class='chat_info_content'>"
						+ "<div class='jenny_text'>"
							+ text
						+ "</div>"
						+ "<div class='control_box'>"
							+ "<a class='niceButton' onclick='$(\".chat_info_mask\").remove();'>Ok, rozumiem</a>"
						+ "</div>"
					+ "</div>"
				+ "</div>";

	$("#chat_window").append(html);
}


function show_contest_question(msg_id, msg_type, text) {

	if(msg_type!= 2) return;	

	var c = getCookie("chat_contest_id_tab");
	var tab = new Array(0);
	if(c != undefined)
		tab = JSON.parse(c);

	var msg_id = parseInt(msg_id);

	if(tab.indexOf(msg_id) != -1) return;

	tab.push(msg_id);

	var start_index = tab.length - 30;
	if(start_index < 0)
		start_index = 0;

	var tab = tab.slice(start_index, start_index + 30);

	setCookie('chat_contest_id_tab',JSON.stringify(tab),10);


 	$("#contest_box").empty();
	$("#contest_box").html(text);
	$("#contest_box").show(200);
}

function show_contest_answer(msg_id, msg_type, text) {
	if(msg_type != 3) return;

	var c = getCookie("chat_contest_id_tab");
	var tab = new Array(0);
	if(c != undefined)
		tab = JSON.parse(c);

	var msg_id = parseInt(msg_id);

	if(tab.indexOf(msg_id) != -1) return;

	tab.push(msg_id);

	var start_index = tab.length - 30;
	if(start_index < 0)
		start_index = 0;

	tab = tab.slice(start_index, start_index + 30);

	setCookie('chat_contest_id_tab',JSON.stringify(tab),10);

 	if(isEmpty($("#contest_box")))
		$("#contest_box").append(text);
	else
		$("#contest_box").append('<hr/>' + text);
	$("#contest_box").show(200).delay(5000).hide(200);
}


function chat_report(id) {
	
	vex.dialog.open({
        message: 'Czy na pewno chcesz zgłosić tą wiadomość?',
        buttons: [
            $.extend({}, vex.dialog.buttons.YES, { text: 'Tak' }),
            $.extend({}, vex.dialog.buttons.NO, { text: 'Nie' })
        ],
        callback: function (data) {
           if(data){
        		$.ajax({
					url: '/ajax_chat',
					data: {method: 'chat_report',
						   id: id},
					type: 'post',
					success: function(output) { 
						if(output == 0)
							gameAlert('Wystąpił nieznany błąd.');
						else if(output == 1)
							gameAlert('Ta wiadomość została już wcześniej zgłoszona do administracji przez innego gracza.');
						else
							gameAlert('Wiadomość została zgłoszona do administracji.');
					},
					error: function(output) {
						gameAlert('Błąd połączenia z serwerem. Odśwież stronę.');
					}
				});
        	}
        }
    });
}


function isEmpty( el ){
  return !$.trim(el.html())
}
















