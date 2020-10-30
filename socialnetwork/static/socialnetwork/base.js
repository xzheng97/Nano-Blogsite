
/**** DROP DOWN ****/
/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function showNav() {
    document.getElementById("my_dropdown").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }


/**** PAGE UPDATE ****/

// Sends a new request to update the to-do list
function refreshGlobal() {
    let request = new XMLHttpRequest()
    request.onreadystatechange = function() {
        if (request.readyState != 4) return
        updatePage(request)
    }

    request.open("GET", "/socialnetwork/refresh-global", true)
    request.send()
}

function refreshFollower() {
  let request = new XMLHttpRequest()
  request.onreadystatechange = function() {
      if (request.readyState != 4) return
      updatePage(request)
  }

  request.open("GET", "/socialnetwork/refresh-follower", true)
  request.send()
}




function updatePage(request) {
    if (request.status != 200) {
        displayError("Received status code = " + request.status)
        return
    }
    
    let response = JSON.parse(request.responseText)

    console.log("update page in base.js: ", response)
    if (Array.isArray(response.post)) {
      updatePost(response.post)
    }
    if (Array.isArray(response.comment)) {
      updateComment(response.comment)
    } 
    else if (response.hasOwnProperty('error')) {
        displayError(response.error)
    } 
    else {
        displayError(reponse)
    }
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updatePost(items) {
    // Removes the old post list items
    let list = document.getElementById("post-list")

    // Adds each new post item to the list
    for (let i = 0; i < items.length; i++) {
      let item = items[i]
      if (document.getElementById("id_post_" + item.id) == null) {
        // Builds a new HTML list item for the todo-list
        let post_i = document.createElement("div")
        let post_header = document.createElement("div")
        let post_user_info = document.createElement("div")
        let post_profile_pic = document.createElement("div")
        let postAuthor = document.createElement("p")
        let postText = document.createElement("p")
        let postDate = document.createElement("p")
        if (item.profile_pic == "true") {
          post_profile_pic.innerHTML =  "<a href='/socialnetwork/profile/" + item.user_id + 
          "'><img src='/socialnetwork/photo/" + item.user_id + "' width='70px' height='70px'></a>"
        }
        else {
          post_profile_pic.innerHTML =  "<a href='/socialnetwork/profile/" + item.user_id + 
          "'><img src='../../static/socialnetwork/profile.jpg' width='70px' height='70px'></a>"
        }
        post_profile_pic.setAttribute("class","postProfilePic")
        
        postAuthor.innerHTML = "<a id='id_post_profile_" + item.id + "' " + "href='/socialnetwork/profile/" + 
          item.user_id + "'>" + item.first_name + " " + item.last_name + "</a>"

        postText.innerHTML = sanitize(item.post_text)
        postText.setAttribute("id", "id_post_text_" + item.id)
        postText.setAttribute("class", "postText")

        var date = new Date(item.post_time)
        postDate.innerHTML = date.toLocaleDateString() + " " + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}).replace(" ","")
        postDate.setAttribute("id", "id_post_date_time_" + item.id) 
        postDate.setAttribute("class", "postDate")

        post_user_info.appendChild(postAuthor)
        post_user_info.appendChild(postDate)
        post_user_info.setAttribute("class", "postUserInfo")

        post_header.setAttribute("class", "postHeader")
        post_header.appendChild(post_profile_pic)
        post_header.appendChild(post_user_info)

        post_i.appendChild(post_header)
        post_i.appendChild(postText)
        post_i.setAttribute("class", "post")



        let comments_i = document.createElement("ul")
        comments_i.setAttribute("id","comment-list-" + item.id)
        
        let add_comment = document.createElement("div")
        let newCommentInput = document.createElement("textarea")
        let newCommentButton = document.createElement("button")
        newCommentInput.setAttribute("id", "id_comment_input_text_" + item.id)
        newCommentInput.setAttribute("rows", "2")
        newCommentInput.setAttribute("placeholder", "comment..")
        newCommentInput.setAttribute("class", "commentInput")
        newCommentButton.innerHTML = "Submit"
        newCommentButton.setAttribute("onclick", "addComment("+ item.id + ")")
        newCommentButton.setAttribute("id", "id_comment_button_" + item.id)
        newCommentButton.setAttribute("class", "commentButton")
        add_comment.appendChild(newCommentInput)
        add_comment.appendChild(newCommentButton)


        let element = document.createElement("div")
        let post_wrapper = document.createElement("div")
        post_wrapper.setAttribute("class", "card")
        element.appendChild(post_i)
        element.appendChild(comments_i)
        element.appendChild(add_comment)
        element.setAttribute("id", "id_post_" + item.id)
        element.setAttribute("class", "card-body")
        post_wrapper.appendChild(element)
        // Adds the todo-list item to the HTML list
        list.prepend(post_wrapper)
      }
    }
}

function updateComment(items) {
  // Adds each new post item to the list
  console.log("in base.js received:", items)
  for (let i = 0; i < items.length; i++) {
    let item = items[i]
    if (document.getElementById("id_comment_" + item.id) == null){  
      // Builds a new HTML list item for the comment-list
      let comment_i = document.createElement("div")
      let comment_profile_pic = document.createElement("div")
      let commentInfo = document.createElement("div")
      let commentTextWrap = document.createElement("p")
      let commentAuthor = document.createElement("span")
      let commentText = document.createElement("span")
      let commentDate = document.createElement("p")
      if (item.profile_pic == "true") {
        comment_profile_pic.innerHTML = "<a href='/socialnetwork/profile/" + item.user_id + 
          "'><img src='/socialnetwork/photo/" + item.user_id + "' width='50px' height='50px'></a>"
      }
      else {
        comment_profile_pic.innerHTML = "<a href='/socialnetwork/profile/" + item.user_id + 
          "'><img src='../../static/socialnetwork/profile.jpg' width='50px' height='50px'></a>"
      }
      comment_profile_pic.setAttribute("class","commentProfilePic mr-3")

      
      commentAuthor.innerHTML = "<a id='id_comment_profile_" + item.id + "' " + "href='/socialnetwork/profile/" + 
        item.user_id + "'>" + item.first_name + " " + item.last_name + "</a>: "
      commentText.innerHTML = sanitize(item.comment_text)
      commentText.setAttribute("id", "id_comment_text_" + item.id) 
      var date = new Date(item.comment_time)
      commentDate.innerHTML = date.toLocaleDateString() + " " + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}).replace(" ","")
      commentDate.setAttribute("id", "id_comment_date_time_" + item.id) 
      commentDate.setAttribute("class", "commentDate")

      commentTextWrap.appendChild(commentAuthor)
      commentTextWrap.appendChild(commentText)
      commentTextWrap.setAttribute("class", "commentTextWrap")

      commentInfo.appendChild(commentTextWrap)
      commentInfo.appendChild(commentDate)

      comment_i.appendChild(comment_profile_pic)
      comment_i.appendChild(commentInfo)
      comment_i.setAttribute("id", "id_comment_" + item.id)
      comment_i.setAttribute("class", "comment")

      let list = document.getElementById("comment-list-" + item.post_id)
      list.appendChild(comment_i)
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

function addComment(postId) {
    var itemTextElement = document.getElementById("id_comment_input_text_" + postId)
    var itemTextValue   = itemTextElement.value

    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    displayError('')

    var req = new XMLHttpRequest()
    req.onreadystatechange = function() {
        if (req.readyState != 4) return
        if (req.status != 200) return
        var response = JSON.parse(req.responseText);
        if (response.hasOwnProperty('error')) {
          displayError(response.error);
        } else {
          if (Array.isArray(response.post)) {
            updatePost(response.post)
          }
          if (Array.isArray(response.comment)) {
            updateComment(response.comment)
          } 
        }
    }

    req.open("POST", "/socialnetwork/add-comment", true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("comment_text="+itemTextValue+"&post_id="+postId+"&csrfmiddlewaretoken="+getCSRFToken());

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

