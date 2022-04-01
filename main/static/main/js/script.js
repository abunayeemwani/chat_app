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
    // Click user
    $('.friend').on('click', function(){
        $('.friend.active-friend').removeClass('active-friend')
        $(this).addClass('active-friend')
        
        let user_id = $(this).attr('user-id')
        let data_type = "user"
        
        let data = {
            'data_type': data_type,
            'user_id': user_id
        }
        data = JSON.stringify(data)
        socket.send(data)
    })

    // Submit form
    message_form.on('submit', function(e){
        e.preventDefault()
        let message = input_message.val()
        let sent_by = USER_ID
        let send_to = $('.right-body').attr('other-user-id')
        let data_type = "message"

        let data = {
            'data_type': data_type,
            'message': message,
            'sent_by': sent_by,
            'send_to': send_to
        }
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })

}

socket.onmessage = async function(e){
    let data = JSON.parse(e.data)

    if(data['data_type'] === "message"){
        let message = data['message']
        let sent_by = data['sent_by']

        newMessage(message, sent_by)
    }
    else{
        let id = data['id']
        let image = data['image']
        let name = data['name']
        showUser(id, image, name)

        if(data['messages'] != ""){
            for(let i=0; i<data['messages'].length; i++){
                newMessage(data['messages'][i][1], data['messages'][i][0], data['messages'][i][2])
            }
        }
    }
}

socket.onerror = async function(e){
    console.log('Error', e)
}

socket.onclose = async function(e){
    console.log('Close', e)
}





function newMessage(message, sent_by, date="Today, "+new Date().getHours()+":"+new Date().getMinutes()){
    if($.trim(message) === ''){
        return false
    }

    let message_element;
    let message_body;
    if(sent_by == USER_ID){
        message_element = `
        <div class="message sent">
            <p>${message}</p>
            <span>${date}</span>
        </div>
        `
        message_body = $('.right-body')
    }
    else{
        message_element = `
        <div class="message received">
            <p>${message}</p>
            <span>${date}</span>
        </div>
        `
        message_body = $('.right-body[other-user-id="' + sent_by + '"]')
    }

    message_body.append(message_element)
    message_body.animate({
        scrollTop: message_body.get(0).scrollHeight
    }, 10);
	input_message.val(null);
}





function showUser(id, image, name){
    let user_element = `
    <div class="right-top" other-user-id="${id}">
        <img src="media/${image}" />
        <h4>${name}</h4>
    </div>
    <div class="right-body" other-user-id="${id}">
        
    </div>
    `

    $('.right-container').html(user_element)

}





function showFriends(){
    document.getElementById("friends").classList.add("active")
    document.getElementById("connect").classList.remove("active")
    document.getElementById("menu").classList.remove("active")
}

function showConnect(){
    document.getElementById("friends").classList.remove("active")
    document.getElementById("menu").classList.remove("active")
    document.getElementById("connect").classList.add("active")
}

function showMenu(x) {
    x.classList.toggle("change");

    if(document.getElementById("menu").classList.contains("active")){
        document.getElementById("friends").classList.add("active")
        document.getElementById("connect").classList.remove("active")
        document.getElementById("menu").classList.remove("active")
    }
    else{
        document.getElementById("friends").classList.remove("active")
        document.getElementById("connect").classList.remove("active")
        document.getElementById("menu").classList.add("active")
    }
}