"use strict"

// Sends a new request to update the to-do list
function getGlobal() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("GET", "/socialnetwork/get-global", true)
    xhr.send()
}

function loadPosts() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("GET", "/socialnetwork/get-global", true)
    xhr.send()
}

function loadFollowerPosts(){
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("GET", "/socialnetwork/get-follower", true)
    xhr.send()

}


function updatePage(xhr) {
    console.log("going into updatepage")
    if (xhr.status == 200) {
        console.log("parsing")
        let response = JSON.parse(xhr.responseText)
        console.log("in update page", response)
        updatePosts(response["posts"])
        updateComments(response["comments"])
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('Content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    /*
    let response = JSON.parse(xhr.responseText)
    console.log(response)
    if (response.hasOwnProperty('error')) {
        
        displayError(response.error)
        return
    }

    displayError(response)
    */
}
/*
function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}
*/


function addComment(post_id){
    //console.log("entering addComment")
    console.log(post_id)
    let itemTextElement = document.getElementById("id_comment_input_text_" + post_id)

    if (itemTextElement == null){
        return ;
    }
    let itemTextValue   = itemTextElement.value
    console.log("itemVal", itemTextValue)
    console.log("itemElement", itemTextElement)
    // Clear input box and old error message (if any)
    itemTextElement.value = ''

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        console.log("updating here")
        updatePage(xhr)
    }
    console.log("before going into views")
    xhr.open("POST", "socialnetwork/add-comment", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("comment_text="+itemTextValue+"&post_id=" + post_id + "&csrfmiddlewaretoken="+getCSRFToken());

}


function updatePosts(items) {
    //console.log("entering")
    let list = document.getElementById("my-posts-go-here")

    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        let currID = "id_post_div_" + item.id

        if (document.getElementById(currID) == null) {
            let date = new Date(item.date_time)
            
            let formatDate = date.toLocaleDateString('en-US', { year: 'numeric', month: 'numeric', day: 'numeric' })
            let formatTime = date.toLocaleTimeString('en-US', { hour12: true, hour: 'numeric', minute: 'numeric' })


            let element = document.createElement('div')
            element.setAttribute("id", currID)
            /*
            let element_page = document.createElement('div')
            element_page.setAttribute("id", currID)
            element_page.innerHTML = '<div id = "id_page_name">Profile Page for' + item.first_name + " " + item.last_name + "</div>"
            list.prepend(element_page)
            */
            element.innerHTML = '<a href="/otherprofile/' + item.user_id + '"' + "id='id_post_profile_" + item.id + "'>" +
                                "Post by " + item.first_name + " " + item.last_name + item.id + "</a> <div id='id_post_text_" + item.id + "'>" +
                                sanitize(item.text) + "</div>" + "<b id='id_post_date_time_" + item.id + "'>" + 
                                formatDate + " " + formatTime + "</b>" + "<div id='comments_post_go_here_" + item.id + 
                                "'></div> <label>Comment:</label> <input type='text' id='id_comment_input_text_" + 
                                item.id + "' name = comment></input> <button id='id_comment_button_" + 
                                item.id + "' onClick = 'addComment(" + item.id + ")'> submit </button>" 
                                list.prepend(element)
        }

}
}

function updateComments(items){
    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        let currID = "id_comment_div_" + item.comment_id
        console.log("currID", currID)
        if (document.getElementById(currID) == null) {
            console.log("entering if")
            let date = new Date(item.comment_time)
            let formatDate = date.toLocaleDateString('en-US', { year: 'numeric', month: 'numeric', day: 'numeric' })
            let formatTime = date.toLocaleTimeString('en-US', { hour12: true, hour: 'numeric', minute: 'numeric' })
            let element = document.createElement('div')
            element.setAttribute("id", currID)
            element.className = "comment"
            element.innerHTML = '<a href="/otherprofile/' + item.creator_id + '"' + "id='id_comment_profile_" + item.comment_id + "'>" +
            "Comment by " + item.creator_first_name + " " + item.creator_last_name + "</a> <div id='id_comment_text_" + item.comment_id + "'>" +
            sanitize(item.comment_text) + "</div>" + "<b id='id_comment_date_time_" + item.comment_id + "'>" + 
            formatDate + " " + formatTime + "</b>"
            //element.innerHTML = item.comment_text
            let comLoc = document.getElementById("comments_post_go_here_" + item.post_id)
            console.log(comLoc)
            comLoc.append(element)
        }
    }

}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

function addItem() {
    let itemTextElement = document.getElementById("item")
    let itemTextValue   = itemTextElement.value

    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("POST", addItemURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("item="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());
}

function deleteItem(id) {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("POST", deleteItemURL(id), true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send("csrfmiddlewaretoken="+getCSRFToken())
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}