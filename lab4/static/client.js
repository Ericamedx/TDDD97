var X = 5;
//lab3 change all calls to serverstub with htttp requests.
var server = "http://localhost:5000/";
var port = "5000";
var searchedemail = "";

function displayview(view){
  document.getElementById('containerdiv').innerHTML = document.getElementById(view).innerHTML;
}
window.onload = function(){
//code that is executed as the page is loaded.
//You shall put your own custom code here.

//window.alert() is not allowed to be used in your implementation.
connectwithsocket();
if(localStorage.token != null && localStorage.token != 0){ //&& localStorage.token != 0){
  document.getElementById('containerdiv').innerHTML = document.getElementById('profileview').innerHTML;
  showuserinfo();

  var formObject = new FormData();
  formObject.append('Authorization', localStorage.token);
  var reqheader = new Headers();
  reqheader.append('Authorization', localStorage.token);

  path = "Get_user_messages_by_token/";
    HTTPget(path, function(myhttphelper){
    result = JSON.parse(myhttphelper.responseText);
    userdata = result.posts;
    if(result.success){

    updatelist(userdata, 'submittedpostlist');
    }
  });


}
else{
document.getElementById('containerdiv').innerHTML = document.getElementById("welcomeview").innerHTML;
}
}
function connectwithsocket(){
    //var ws = new WebSocket("ws://" + document.domain + ':' + '5000' + "/api");
    var ws = new WebSocket("ws://" + "127.0.0.1:" + "5000/api")

    ws.onopen = function(){
      //window.alert("connection websocket");
      console.log("we've entered onopen");
    var data = {
      'token': localStorage.getItem('token'),
      //'email': localStorage.getItem('email')
    };
    //sends new session token
    if (data !== undefined) {
      console.log(JSON.stringify(data));
      ws.send(JSON.stringify(data));

    }
  }
  ws.onmessage = function(event) {
    //window.alert("onmessage");

    console.log(event.data);

    var msg = JSON.parse(event.data);
    console.log(msg.message)

    if (msg.success == false) {
      console.log("vi kom in i success = false")
      //window.alert("connection websocket: FALSE");
      localStorage.removeItem('token');
      localStorage.removeItem('email');
      //Forcelogoutclient();
      //signout();
      //window.onload();

      document.getElementById('containerdiv').innerHTML = document.getElementById('welcomeview').innerHTML;
      console.log(msg.message);
      //window.onload();
    }
  };


  ws.onclose = function() {
    //localStorage.removeItem('token');
    //localStorage.removeItem('email');
    //signout();
    //window.onload();
    console.log("Websocket closed");
	};

	ws.onerror = function() {
    console.log("Error in Websocket");
	};
}
function showforgotpassword(){
  div = document.getElementById('forgotpasswordform');
  div.style.display = "block";
  loginform = document.getElementById('loginform');
  loginform.style.display = "none";
  button1 = document.getElementById('returnloginbutton');
  button1.style.display = "block";
  button2 = document.getElementById('forgotpasswordbutton');
  button2.style.display = "none";
  errormessage = document.getElementById('errormessage');
  errormessage.innerHTML = "";
}

function showlogin(){
  div = document.getElementById('forgotpasswordform');
  div.style.display = "none";
  loginform = document.getElementById('loginform');
  loginform.style.display = "block";
  button1 = document.getElementById('returnloginbutton');
  button1.style.display = "none";
  button2 = document.getElementById('forgotpasswordbutton');
  button2.style.display = "block";
  errormessage = document.getElementById('errormessage');
  errormessage.innerHTML = "";
}

function HTTPget(path, fact){
    var myhttphelper = new XMLHttpRequest();
    myhttphelper.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      fact(this);
    }
  };
  var actualpath = server + path;
  myhttphelper.open("GET", actualpath);
  myhttphelper.setRequestHeader('Authorization', localStorage.token)
  myhttphelper.send();
}
function HTTP_post(path, form, fact){
  var myhttphelper = new XMLHttpRequest();
  myhttphelper.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      fact(this);
    }
  };
  var actualpath = server + path;
  myhttphelper.open("POST", actualpath);
  if(localStorage.token){
  myhttphelper.setRequestHeader('Authorization', localStorage.token)
  }
  myhttphelper.send(form);
}
function forgotpassword(){
    var email = document.getElementById('forgotemail');
    formobject = new FormData();
    formobject.append('email', email.value)
    errormessage = document.getElementById('errormessage');
    //create a server temporary code
    //send it to the user with email/
    //HTTP_post()

    path = "forgotpassword";
    HTTP_post(path, formobject, function(myhttphelper){

    result = JSON.parse(myhttphelper.responseText);
    if(result.success){
      console.log(result.message);

      errormessage.innerHTML = result.message;
    }
    else{
      errormessage.innerHTML = result.message;
    }
  });


    return false;

}
//todo, fix alert message to not be alert. maybe css and make the fields red
//klart
function showuserinfo(){
var personalinfotext = document.getElementById('personalinfotext');
HTTPget("get_user_data_by_token", function(myhttphelper){
  result = JSON.parse(myhttphelper.responseText);
  var userdata = result.userinfo;


  temp2string = "<pre>"+JSON.stringify(userdata, null, 2)+"</pre>";
  //temp2string.replace("{","").replace("", '');
  tempstring = "";
  if(userdata){
  tempstring += "email: " + userdata[0];
  tempstring += "<br/>"+ "First name: " + userdata[3];
  tempstring += "<br/>"+ "Family name: " + userdata[2];
  tempstring += "<br/>"+ "Gender: " + userdata[4];
  tempstring += "<br/>"+ "City: " + userdata[5];
  tempstring += "<br/>"+ "Country: " + userdata[6];
  }
  //tempstring = userdata[0];
  personalinfotext.innerHTML = tempstring;
});


}
function updatelist(userdata, list_id){
 var mylist = document.getElementById(list_id);

 if (mylist){


 while( mylist.firstChild ){
  mylist.removeChild( mylist.firstChild );
}
  for(var i = 0; i < userdata.length; i++){
    //var json = "user: "+ JSON.stringify(userdata.data[i].writer + userdata.data[i].content);
    var json = "user: " + userdata[i][1] + "       posted: " + userdata[i][2];
    //var json = userdata[i][1];
    //json.replace(/\\"/g,"\uFFFF");
    //json = json.replace(/\"([^(\")"]+)\":/g,"$1:");
    var entry = document.createElement('li');
    entry.appendChild(document.createTextNode(json));
    mylist.appendChild(entry);
    //document.getElementById('submittedpostlist').innerHTML = json;
  }
 }
}

function updateposts(){

  window.onload();
}

function browsepost(){
  var postmessage = document.getElementById("posttextareabrowse");
  if(postmessage.value.length < 1){
    return false;
  }
  else{
  //if(searchedemail.length < 1){
  var formobject = new FormData();
  //formobject.append('Authorization', localStorage.token);
  formobject.append('message', postmessage.value);
  formobject.append('email', searchedemail);
  HTTP_post("post_message", formobject, function(myhttphelper){
    result = JSON.parse(myhttphelper.responseText);
    //localStorage.removeItem("token");
    //window.onload();
    updatebrowseposts();
    return false;
  });
}
return false;
}
function updatebrowseposts(){
    path = "get_user_messages_by_email/" + searchedemail;
    HTTPget(path, function(myhttphelper){

    result = JSON.parse(myhttphelper.responseText);
    userdata = result.posts;
    if(result.success){

    updatelist(userdata, 'founduserlist');
    }
  });
//HTTPget("get_user_messages_by_email", function(myhttphelper){
//  result = JSON.parse(myhttphelper.responseText);
//  userdata = result.userinfo;
//});
//updatelist(userdata, 'founduserlist')
return false;

}
function browseuser(){
var searchemail = document.getElementById('searchinput');
searchedemail = searchemail.value;
var errormessage = document.getElementById('error_search');
var userinfo = document.getElementById('founduserinfo');

path = "get_user_data_by_email/" + searchemail.value;
  HTTPget(path, function(myhttphelper){

  result = JSON.parse(myhttphelper.responseText);
  userdata = result;

  if(userdata.success){
    //temp2string = "<pre>"+JSON.stringify(userdata.data, null, 2)+"</pre>";
    //temp2string.replace("{","").replace("", '');
    var browsediv = document.getElementById('browsepostdiv');
    browsediv.style.display = "block";
    tempstring = "";
    userdata = userdata.userinfo;

    tempstring += "email: " + userdata[0];
    tempstring += "<br/>"+ "First name: " + userdata[3];
    tempstring += "<br/>"+ "Family name: " + userdata[2];
    tempstring += "<br/>"+ "Gender: " + userdata[4];
    tempstring += "<br/>"+ "City: " + userdata[5];
    tempstring += "<br/>"+ "Country: " + userdata[6];
    userinfo.innerHTML = tempstring;
    errormessage.innerHTML = "";
    //userinfo.innerHTML = JSON.stringify(result.data.value);
  }
  else{

    errormessage.innerHTML = userdata.message;
}
});


path = "get_user_messages_by_email/" + searchemail.value;
HTTPget(path, function(myhttphelper){
result = JSON.parse(myhttphelper.responseText);
userposts = result;
if(userposts.success){
updatelist(userposts.posts, 'founduserlist');
errormessage.innerHTML = "";


}
else{
  errormessage.innerHTML = userdata.message;
  userinfo.innerHTML = "";
  var mylist = document.getElementById('founduserlist');
  while( mylist.firstChild ){
   mylist.removeChild( mylist.firstChild );
 }
}
});
return false;

}

function checkpassword(){

  var loginpassword = document.getElementById('loginpass');
  var loguname = document.getElementById('loguname');
  var errormessage = document.getElementById('errormessage');


  if(loginpassword.value.length < X){
    loginpassword.style.backgroundColor = "red";
    errormessage.innerHTML = "Lösenordet är för kort!";
    //alert("för kort lösenord");

    return false;
  }
  else{
   loginpassword.style.backgroundColor = "white";


   formObject = new FormData();
   formObject.append('email', loguname.value);
   formObject.append('password', loginpassword.value);
   path = "";
   //var loginresult = HTTP_post("sign_in", formObject, )
   HTTP_post("sign_in", formObject, function(myhttphelper){
     result = JSON.parse(myhttphelper.responseText);
     errormessage.innerHTML = result.message;
     if(result.success){
       localStorage.token = result.token;
       localStorage.email = loguname.value;
       //connectwithsocket();
       window.onload();
     }
     return false;
   });

}
  return false;
}

function checknewpass(){
  var oldpass = document.getElementById('oldpass');
  var pw1 = document.getElementById('newpass');
  var pw2 = document.getElementById('newpass2');
  var temptext = document.getElementById('text_newpass');
  //var email = tokenToEmail(localStorage.token));

  if(pw1.value.length < X){
    //alert("ditt lösenord är för kort");
    temptext.innerHTML = "Nya lösenordet är för kort!";
    pw1.style.backgroundColor = "red";
  //  pw1.style.border-color ="red";
    return false;
  }
  else if(pw1.value != pw2.value){
    //alert("dem stämmer inte överrens")
    pw1.style.backgroundColor = "white";
    temptext.innerHTML = "Nya löseordet måste matcha!";
    pw2.style.backgroundColor = "red";
    return false;

  }
    else{
    pw2.style.backgroundColor = "white";
    var formobject = new FormData();
    formobject.append('oldPassword', oldpass.value)
    formobject.append('newPassword', pw1.value)
    HTTP_post("Change_password", formobject, function(myhttphelper){
      result = JSON.parse(myhttphelper.responseText);
      temptext.innerHTML = result.message;

      return false;
    });
      //changed oldpass and newpass to oldpass.value and newpass.value
      //temptext.innerHTML = result.message;
      }
      return false;
}
function signout(){
  var temptext = document.getElementById('text_newpass');
  //localStorage.token = 0;
  var formobject = new FormData();
  formobject.append('token', localStorage.token)
  HTTP_post("sign_out", formobject, function(myhttphelper){
    result = JSON.parse(myhttphelper.responseText);
    //temptext.innerHTML = result.message;

    localStorage.token = 0;
    localStorage.removeItem("token");
    window.onload();
    return false;
  });

  //temptext.innerHTML = result.message;
  //localStorage.removeItem("token");
  //window.onload();



}
function checksamepass(){
  var pw1 = document.getElementById('pwd1');
  var pw2 = document.getElementById('pwd2');
  var temptext = document.getElementById('text_pwd');
  if(pw1.value.length < X){
    //alert("ditt lösenord är för kort");
    temptext.innerHTML = "Lösenordet är för kort!";
    pw1.style.backgroundColor = "red";
  //  pw1.style.border-color ="red";
    return false;
  }
  else{
    pw1.style.backgroundColor = "white";
  }
  if(pw1.value != pw2.value){
    //alert("dem stämmer inte överrens")
    temptext.innerHTML = "Löseordet måste matcha!";
    pw2.style.backgroundColor = "red";
    return false;
  }
  else{
    pw2.style.backgroundColor = "white";

     var success;
     var message;
     var formObject = {
     email : document.getElementById('email').value,
     password : document.getElementById('pwd1').value,
     firstname : document.getElementById('uname').value,
     familyname : document.getElementById('fname').value,
     gender : document.getElementById('gender').value,
     city : document.getElementById('city').value,
     country : document.getElementById('country').value
     };

     var formData = new FormData();

     formData.append('email', formObject.email);
     formData.append('password', formObject.password);
     formData.append('firstname', formObject.firstname);
     formData.append('familyname', formObject.familyname);
     formData.append('gender', formObject.gender);
     formData.append('city', formObject.city);
     formData.append('country', formObject.country);

       var path = "sign_up";

       HTTP_post(path, formData, function(myhttphelper){
         result = JSON.parse(myhttphelper.responseText);
         temptext.innerHTML = result.message;
         return false;
         //if (result.success){
           //
         //}
       });

  }
  return false;
}

function userpost(){
var postmessage = document.getElementById("posttextarea");
if(postmessage.value.length < 1){
  return false;
}
else{
  var formobject = new FormData();
  //formobject.append('Authorization', localStorage.token);
  formobject.append('message', postmessage.value);
  formobject.append('email', localStorage.email);
  HTTP_post("post_message", formobject, function(myhttphelper){
    result = JSON.parse(myhttphelper.responseText);
    //localStorage.removeItem("token");
    window.onload();
    return false;
  });
}
//var submittext = document.getElementById("submittedposttext");
//submittext.innerHTML = result.message;

return false;
}

function checkAll(){ //kolla igenom så alla är lika och sen returnera felmeddelande
  var uname = document.getElementById('uname');

  if(uname){

  }
}
function openPage(evt, pageName) {
  var i, pages, tablinks;
  pages = document.getElementsByClassName("profilepage");
  for (i = 0; i < pages.length; i++) {
    pages[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tabbuttons")
  for(i = 0; i< pages.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" activetab", "");
  }
  document.getElementById(pageName).style.display = "block";
  evt.currentTarget.className += " activetab";

}
