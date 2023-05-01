

// //Get the button
// let mybutton = document.getElementById("btn-back-to-top");

// // When the user scrolls down 10px from the top of the document, show the button
// window.onscroll = function() {
//   scrollFunction();
// };

// function scrollFunction() {
//   if (
//     document.body.scrollTop > 10 ||
//     document.documentElement.scrollTop > 10
//   ) {
//     mybutton.style.display = "block";
//   } else {
//     mybutton.style.display = "none";
//   }
// }
// // When the user clicks on the button, scroll to the top of the document
// mybutton.addEventListener("click", backToTop);

// function backToTop() {
//   document.body.scrollTop = 0;
//   document.documentElement.scrollTop = 0;
// }

// -------------------------------------------------------------------

// fetch('./data/db.json')
//   .then((response) => response.json())
//   .then((db) => add_names(db))
//   .then((db) => save_data(db))
//   // .then(add_event());
//   // .then((db) =>console.log(db));

// var myData;

// function save_data(data){
//   myData= data;
// }


// function add_names(input_names){

//   var ul = document.getElementById("namesList");
  
//   // Loop through list
//     for (var i = 0; i < input_names.length; i++) {
//     var name = input_names[i]["name"];
//     var a = document.createElement('a');
//     a.appendChild(document.createTextNode(name));
//     a.className ="list-group-item list-group-item-action";
//     a.id="attender"
//     a.href="#";
//     a.addEventListener("click", add_attendance)
//     // a.name=name;
//     ul.appendChild(a);
// }//End Loop


//   return input_names;
// }




                  
// function add_event()
// {
//     // var links = document.getElementById("attender");
//   var ul = document.getElementById("namesList");
//   var links = ul.getElementsByTagName("a");

  
//     // console.log("before");
//   // console.log(links["0"]);

//    for (i = 0; i < links.length; i++) {
//      console.log(links[i])
//      // links[i].addEventListener("click", add_attendance)
//    }//end adding onclick loop
  
//   // console.log("after");
//   console.log(links);

  
// }




function filterNames()
{
  var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("namesList");
    li = ul.getElementsByTagName("button");
    for (i = 0; i < li.length; i++) {
        // a = li[i].getElementsByTagName("a")[0];
        txtValue = li[i].value || li[i].innerText; //textContent
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function add_attendance(clickedElement)
{  
  console.log(clickedElement.srcElement.innerText)
  console.log(myData)
  // save_json()
  
}

function save_json()
{

   var textToSave = JSON.stringify(myData),
      filename = 'file.txt',
      blob = new Blob([textToSave], {type: "text/plain;charset=utf-8"});

  // saveAs(blob, filename);

  var link=window.URL.createObjectURL(blob);
// window.location=link;
  var file = new File([blob], "test.txt");

  
}

function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}

// download(myData, 'json.txt', 'text/plain');

// document.addEventListener("DOMContentLoaded", add_event());

// window.addEventListener("load", function(event) {
//     console.log(document.getElementsByTagName('a').length);
//   add_event();
// });
        

