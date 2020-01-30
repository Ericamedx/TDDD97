var X = 5;

displayView = function(){
// the code required to display a view
};
window.onload = function(){
//code that is executed as the page is loaded.
//You shall put your own custom code here.
//window.alert() is not allowed to be used in your implementation.
document.getElementById('containerdiv').innerHTML = document.getElementById("welcomeview").innerHTML;

}
//todo, fix alert message to not be alert. maybe css and make the fields red
function checkpassword(){
  var loginpassword = document.getElementById('loginpass');

  if(loginpassword.value.length < X){
    loginpassword.style.color = "red";
    //alert("för kort lösenord");
    return false;
  }
  else{
   return true;
  }
}
function checksamepass(){
  var pw1 = document.getElementById('pwd1');
  var pw2 = document.getElementById('pwd2');
  var temptext;
  if(pw1.value.length < X){
    //alert("ditt lösenord är för kort");
    temptext = "Lösenordet är för kort";
    pw1.style.color = "red";
    return false;
  }
  if(pw1.value != pw2.value){
    //alert("dem stämmer inte överrens")
    temptext = "Löseordet måste matcha!";
    pw2.style.color = "red";
    return false;
  }
  else{
    return true;
    //step 5
    //serverstub.signUp(document.getElementById('signupform'));
  }
  document.getElementById('text_pwd').innerHTML = temptext;
}
