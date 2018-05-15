const templates =
	{
	 'utter_goodbye': "Auf Wiedersehn",
	 'utter_frage_zugangdaten_bekannt': "Sind Ihre Zugangdaten noch bekannt?",
	 'utter_entsperrung_nicht_erlaubt': "Leider ist die Entsperrung Ihres Kontos über den Chat nicht erlaubt",
	 'utter_frage_name_geburtsdatum': "Bitte nennen Sir mir Ihren Namen und Ihr Geburtsdatum. Bitte beginnen Sie Ihren Vor- und Nachnamen mit Großbuchstaben.",
	 'utter_frage_name': "Bitte nennen Sie mir Ihren Namen. Bitte beginnen Sie Ihren Vor- und Nachnamen mit Großbuchstaben.",
	 'utter_frage_geburtsdatum': "Bitte nennen Sie mir Ihr Geburtsdatum",
	 'utter_frage_kw': "Bitte nennen Sir mir Ihr bevorzugte KW",
	 'utter_frage_zeit': "Bitte nennen Sir mir Ihre bevorzugte Zeit",
	 'utter_ob_selfservice_link': "Sie koennen die Link www.sb.de abrufen, und Onlinebanking dort eigenständig einrichten",
	 'utter_uew_storno_nicht_moeglich': "Ein Überweisungsrückruf ist nicht moeglich, bitte wenden Sie sich an den Zahlungsempfänger.",
	 'utter_tv_optional_wishes': "Haben Sie ein Terminwunsch (KW und Zeit)?",
	 'action_transfer_to_agent': "Ich leite Sie diesbezüglich an einem Berater weiter"
	}


var message_side = 'right';
var sId = new Date().getTime();
var global_mandant_id = Math.floor(Math.random() * 100) + 1

class Message {
    constructor(arg) {
        this.text = arg.text;
        this.message_side = arg.message_side;
    }

    draw(){
        var $message, $message_agent;
        $message = $($('.message_template').clone().html());
        $message.addClass(this.message_side).find('.text').html(this.text);

        $message_agent = $message.clone();
        $('#agent .messages').append($message_agent);
        $message_agent.addClass('appeared');

        $('#user .messages').append($message);
        $message.addClass('appeared');
    }
}

function getMessageText(who) {
    var $message_input;
    text = $(who + ' .message_input').val();
    console.log(who + text);
    return text;
};

function sendMessage(text, message_side) {
    var message;
    if (text.trim() === '') {
        return;
    }
    $('.message_input').val('');
    message = new Message({
        text: text,
        message_side: message_side
    });
    message.draw();

    // auto scroll up:
    $('.messages').each(function(){
        $this = $(this);
        $this.animate({ scrollTop: $this.prop('scrollHeight')}, 300);
    })
};

//- curl -i -H 'Content-type:application/json; charset=UTF-8' -XPOST localhost:5005/conversations/101/parse -d '{"query":"/account_number{\"account_number\":\"456700\"}"}'
function rasaParse(text){
    rasa_url = "http://localhost:5005/conversations/"+ sId +"/parse";
    rasa_post_data = JSON.stringify({query:text});
    $.post(rasa_url, rasa_post_data)
    .done(function(data){
        console.log(data);
        $tr = $("<tr></tr>");
        $pre = $("<pre>"+JSON.stringify(data, undefined, 2)+"</pre>");
        $tr.append($pre)
        $('#rasa tbody').append($tr);
        $('.table-scroll').animate({ scrollTop: $('.table-scroll').prop('scrollHeight')}, 300);
        if (data.next_action != 'action_listen')
            $('#agent .message_input').val(data.next_action)
    }).
    fail(function(){
        console.log('failed');
    });
}

function falconParse(text){
    rasa_url = "/api/parse";
    rasa_post_data = JSON.stringify({query:text, sender_id:sId, mandant:global_mandant_id});
    $.ajax({
        url: rasa_url,
        data: rasa_post_data,
        method: 'POST',
        contentType: 'application/json; charset=UTF-8',
        success: function(data){
            console.log(data);
            if($.isArray(data)){
                data.forEach(function(el){
                    console.log(el)
                    $tr = $("<tr></tr>");
                    $pre = $("<pre>"+JSON.stringify(el, undefined, 2)+"</pre>");
                    $tr.append($pre);
                    $('#rasa tbody').append($tr);
                    if (el.next_action != 'action_listen')
                        $('#agent .message_input').val(el.next_action);
                });
            }else{
                console.log('Parse result is not an array')
                $tr = $("<tr></tr>");
                $pre = $("<pre>"+JSON.stringify(data, undefined, 2)+"</pre>");
                $tr.append($pre);
                $('#rasa tbody').append($tr);
                if (data.next_action != 'action_listen')
                    $('#agent .message_input').val(data.next_action);
            }

            $('.table-scroll').animate({ scrollTop: $('.table-scroll').prop('scrollHeight')}, 300);

        }
    });
}

//- curl -i -H 'Content-type:application/json; charset=UTF-8' -XPOST localhost:5005/conversations/101/continue -d '{"executed_action": "utter_yr_account_number", "events": []}'
function rasaContinue(text){
    rasa_url = "http://localhost:5005/conversations/"+ sId +"/continue";
    rasa_post_data = JSON.stringify({executed_action: text});
    $.post(rasa_url, rasa_post_data)
    .done(function(data){
        console.log(data);
        $tr = $("<tr></tr>");
        $pre = $("<pre>"+JSON.stringify(data, undefined, 2)+"</pre>");
        $tr.append($pre)
        $('#rasa tbody').append($tr);
        $('.table-scroll').animate({ scrollTop: $('.table-scroll').prop('scrollHeight')}, 300);
        if (data.next_action != 'action_listen')
            $('#agent .message_input').val(data.next_action)
    }).
    fail(function(){
        console.log('failed');
    });
}

//- curl -i -H 'Content-type:application/json; charset=UTF-8' -XPOST localhost:5005/conversations/101/continue -d '{"executed_action": "utter_yr_account_number", "events": []}'
function falconContinue(text){
    rasa_url = "/api/continue";
    rasa_post_data = JSON.stringify({executed_action: text, sender_id:sId});
    $.ajax({
        url: rasa_url,
        data: rasa_post_data,
        method: 'POST',
        contentType: 'application/json; charset=UTF-8',
        success: function(data){
            console.log(data);
            $tr = $("<tr></tr>");
            $pre = $("<pre>"+JSON.stringify(data, undefined, 2)+"</pre>");
            $tr.append($pre);
            $('#rasa tbody').append($tr);
            $('.table-scroll').animate({ scrollTop: $('.table-scroll').prop('scrollHeight')}, 300);
            if (data.next_action != 'action_listen')
                $('#agent .message_input').val(data.next_action);
        }
    });
}

$(document).ready(function(){
    $('#user .send_message').click(function (e) {
        text = getMessageText('#user');
        //rasaParse(text);
        falconParse(text);
        return sendMessage(text, 'left');

    });

    $('#agent .send_message').click(function (e) {
        text = getMessageText('#agent');
        //rasaContinue(text)
        falconContinue(text);
        var sendtext = text;
    	for (var template in templates){
    		if (template == text){
        		console.log(template)
        		sendtext = templates[template]
    		}
    	}
    	return sendMessage(sendtext, 'right');
        
    });

    sendMessage('MandantID: '+ global_mandant_id +', SessionID: '+sId, 'right');
});
