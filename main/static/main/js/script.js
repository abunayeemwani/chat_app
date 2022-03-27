const USER_ID = $('#loggedin-user').val()
let input_message = $('#message')
let message_body = $('.right-body')
let message_form = $('#message-form')


let loc = window.location
let wsPre = 'ws://'

if(loc.protocol === 'https'){
    wsPre = 'wss://'
}

let wsURL = wsPre + loc.host + loc.pathname

var socket = new WebSocket(wsURL)

socket.onopen = async function(e){
    console.log("open")
    message_form.on('submit', function(e){
        console.log("submit")
        e.preventDefault()
        let message = input_message.val()
        let sent_by = USER_ID
        let send_to = get_other_user_id()
        let thread_id = get_active_thread_id()

        let data = {
            'message': message,
            'sent_by': sent_by,
            'send_to': send_to,
            'thread_id': thread_id
        }
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}

socket.onmessage = async function(e){
    console.log("on message")
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by = data['sent_by']
    let thread_id = data['thread_id']

    newMessage(message, sent_by, thread_id)
}

socket.onerror = async function(e){
    console.log('Error', e)
}

socket.onclose = async function(e){
    console.log('Close', e)
}

function newMessage(message, sent_by, thread_id){
    console.log("New message")
    console.log(message)
    if($.trim(message) === ''){
        return false
    }

    let currentDate = new Date()
    let currentTime = currentDate.getHours() + ":" + currentDate.getMinutes();

    let message_element;
    if(sent_by == USER_ID){
        message_element = `
        <div class="message sent">
            <p>${message}</p>
            <span>Today, ${currentTime}</span>
        </div>
        `;
    }
    else{
        message_element = `
        <div class="message received">
            <p>${message}</p>
            <span>Today, ${currentTime}</span>
        </div>
        `;
    }

    let message_body = $('.right-container[thread-id="' + thread_id + '"] .right-body')
    message_body.append(message_element)
    message_body.animate({
        scrollTop: $(document).height()
    }, 300);
	input_message.val(null);
}



function showFriends(){
    document.getElementById("friends").classList.add("active")
    document.getElementById("connect").classList.remove("active")
}

function showConnect(){
    document.getElementById("friends").classList.remove("active")
    document.getElementById("connect").classList.add("active")
}

$('.friend').on('click', function(){
    $('.friend.active-friend').removeClass('active-friend')
    $(this).addClass('active-friend')

    let thread_id = $(this).attr('thread-id')
    $('.right-container.active').removeClass('active')
    $('.right-container[thread-id="' + thread_id + '"]').addClass('active')
})

function get_other_user_id(){
    let other_user_id = $.trim($('.right-container.active').attr('other-user-id'))
    return other_user_id
}

function get_active_thread_id(){
    let active_thread_id = $.trim($('.right-container.active').attr('thread-id'))
    return active_thread_id
}