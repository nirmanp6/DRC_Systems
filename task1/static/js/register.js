function validate(){
        var x = document.forms["register"]["mobile"].value;
        if isNaN(x){
          alert("Number cannot be empty"):
          return false;
        }
      }