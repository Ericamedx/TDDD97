var X = 5;

var searchedemail = "";
//todo, eventually minor/major changes to code. needs to check that everything works properly and every condiition of the lab is correct.
// cont: css changes and general cleanup pls älskling <3
// also take away every window.alert if its still left.
//updatepost needs fix i think
  //<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
displayView = function(){
// the code required to display a view
};
window.onload = function(){
//code that is executed as the page is loaded.
//You shall put your own custom code here.
//window.alert() is not allowed to be used in your implementation.
if(localStorage.token != null){
  document.getElementById('containerdiv').innerHTML = document.getElementById('profileview').innerHTML;

  var userdata = serverstub.getUserMessagesByEmail(localStorage.token, localStorage.email);
  showuserinfo();
  updatelist(userdata, 'submittedpostlist');
}
else{
document.getElementById('containerdiv').innerHTML = document.getElementById("welcomeview").innerHTML;
}
}
//todo, fix alert message to not be alert. maybe css and make the fields red
//klart
function showuserinfo(){
var personalinfotext = document.getElementById('personalinfotext');
var userdata = serverstub.getUserDataByToken(localStorage.token);
temp2string = "<pre>"+JSON.stringify(userdata.data, null, 2)+"</pre>";
//temp2string.replace("{","").replace("", '');
tempstring = "";

tempstring += "email: " + userdata.data.email;
tempstring += "<br/>"+ "First name: " + userdata.data.firstname;
tempstring += "<br/>"+ "Family name: " + userdata.data.familyname;
tempstring += "<br/>"+ "Gender: " + userdata.data.gender;
tempstring += "<br/>"+ "City: " + userdata.data.city;
tempstring += "<br/>"+ "Country: " + userdata.data.country;
personalinfotext.innerHTML = tempstring;
}
function updatelist(userdata, list_id){
 var mylist = document.getElementById(list_id);

 while( mylist.firstChild ){
  mylist.removeChild( mylist.firstChild );
}
  for(var i = 0; i < userdata.data.length; i++){
    //var json = "user: "+ JSON.stringify(userdata.data[i].writer + userdata.data[i].content);
    var json = "user: " + userdata.data[i].writer + "       posted: " + userdata.data[i].content;

    //json.replace(/\\"/g,"\uFFFF");
    //json = json.replace(/\"([^(\")"]+)\":/g,"$1:");

    var entry = document.createElement('li');
    entry.appendChild(document.createTextNode(json));
    mylist.appendChild(entry);
    //document.getElementById('submittedpostlist').innerHTML = json;
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
  var result = serverstub.postMessage(localStorage.token, postmessage.value, searchedemail);
  updatebrowseposts();
//}
}
return false;
}
function updatebrowseposts(){
var userdata = serverstub.getUserMessagesByEmail(localStorage.token, searchedemail);
updatelist(userdata, 'founduserlist')
return false;

}
function browseuser(){
var searchemail = document.getElementById('searchinput');
searchedemail = searchemail.value;
var errormessage = document.getElementById('error_search');
var userinfo = document.getElementById('founduserinfo');

var userdata = serverstub.getUserDataByEmail(localStorage.token, searchemail.value);
//window.alert(userdata.message);
if(userdata.success){
  //temp2string = "<pre>"+JSON.stringify(userdata.data, null, 2)+"</pre>";
  //temp2string.replace("{","").replace("", '');
  //window.alert(userdata.message);
  var browsediv = document.getElementById('browsepostdiv');
  browsediv.style.display = "block";
  tempstring = "";

  tempstring += "email: " + userdata.data.email;
  tempstring += "<br/>"+ "First name: " + userdata.data.firstname;
  tempstring += "<br/>"+ "Family name: " + userdata.data.familyname;
  tempstring += "<br/>"+ "Gender: " + userdata.data.gender;
  tempstring += "<br/>"+ "City: " + userdata.data.city;
  tempstring += "<br/>"+ "Country: " + userdata.data.country;
  userinfo.innerHTML = tempstring;
  errormessage.innerHTML = "";
  //userinfo.innerHTML = JSON.stringify(result.data.value);
//window.alert(userdata.message);
}
else{
  //window.alert(userdata.message);
  errormessage.innerHTML = userdata.message;

}
var userposts = serverstub.getUserMessagesByEmail(localStorage.token, searchemail.value);
if(userposts.success){
updatelist(userposts, 'founduserlist');
errormessage.innerHTML = "";
//window.alert(userdata.message);

}
else{
  errormessage.innerHTML = userdata.message;
  userinfo.innerHTML = "";
  var mylist = document.getElementById('founduserlist');
  while( mylist.firstChild ){
   mylist.removeChild( mylist.firstChild );
 }
}
return false;

}

function checkpassword(){
  var loginpassword = document.getElementById('loginpass');
  var loguname = document.getElementById('uname');
  var errormessage = document.getElementById('errormessage');


  if(loginpassword.value.length < X){
    loginpassword.style.backgroundColor = "red";
    errormessage.innerHTML = "Lösenordet är för kort!";
    //alert("för kort lösenord");

    return false;
  }
  else{
   loginpassword.style.backgroundColor = "white";
   var loginresult = serverstub.signIn(loguname.value, loginpassword.value);
   var success = loginresult.success;
   var message = loginresult.message;
   if(success){
     var token = loginresult.data;
     localStorage.token = token;
     window.onload();

   }
   else{
     errormessage.innerHTML = message;
     return false;
     //window.onload();
   }

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
      var result = serverstub.changePassword(localStorage.token, oldpass.value, newpass.value);
      //changed oldpass and newpass to oldpass.value and newpass.value
      //window.alert(result.message);
      temptext.innerHTML = result.message;
      return false;
      }
      return false;
}
function signout(){
  var temptext = document.getElementById('text_newpass');
  var result = serverstub.signOut(localStorage.token);
  //window.alert(result.message);
  temptext.innerHTML = result.message;
  localStorage.removeItem("token");
  window.onload();



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

      // window.alert(serverstub.signUp(formObject));
       var signupresult = serverstub.signUp(formObject);
       //window.alert(signupresult.message);

      success = signupresult.success;
      message = signupresult.message;
      if(success){
        localStorage.email = formObject.email;
        localStorage.firstname = formObject.firstname;
        localStorage.familyname = formObject.famalyname;
        localStorage.gender = formObject.gender;
        localStorage.city = formObject.city;
        localStorage.country = formObject.country;
        serverstub.signIn(formObject.email, formObject.password);
        temptext.innerHTML = message;
        //window.onload();
      }
      else{
        temptext.innerHTML = message;
      }
      //window.alert("test" + message);
    //return true;
    //step 5
    //serverstub.signUp(document.getElementById('signupform'));
  }
  return false;
}

function userpost(){
var postmessage = document.getElementById("posttextarea");
if(postmessage.value.length < 1){
  return false;
}
else{
var result = serverstub.postMessage(localStorage.token, postmessage.value, localStorage.email);
//window.alert("test" + postmessage.value);
window.onload();
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
