var X = 5;

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
}
else{
document.getElementById('containerdiv').innerHTML = document.getElementById("welcomeview").innerHTML;
}
}
//todo, fix alert message to not be alert. maybe css and make the fields red
//klart
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
   var token = loginresult.data;
   localStorage.token = token;
   window.onload();
  }
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
       window.alert(signupresult.message);

      success = signupresult.success;
      message = signupresult.message;
      window.onload();
      //window.alert("test" + message);
    //return true;
    //step 5
    //serverstub.signUp(document.getElementById('signupform'));
  }
}

function checkAll(){ //kolla igenom så alla är lika och sen returnera felmeddelande
  var uname = document.getElementById('uname');

  if(uname){

  }
}
function openPage(pageName) {
  var i;
  var pages = document.getElementsByClassName("profilepage");
  for (i = 0; i < pages.length; i++) {
    pages[i].style.display = "none";
  }
  document.getElementById(pageName).style.display = "block";

}
