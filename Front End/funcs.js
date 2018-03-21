function testEmail(email){
  var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email.toLowerCase());
}

function setErrorVisible(){
  document.getElementById("error").style.display = "inline";
}

function input(){
  email = document.getElementById("email").value;
  option = document.getElementById("option").value;
  if testEmail(email)==false{
    setErrorVisible();
  }
  else{
    console.log(email);
    console.log(option);
  }
}
