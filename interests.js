function fetchdata(){
            $.ajax({
           type: 'GET',
    url:"http://localhost:5000/webforms/display",processData: true,
           data: {},
           dataType: "json",
           success: function (data) {
               processData(data);
           }
});


function processData(data){
    for (let i = 0; i < data["databases"].length; i++) {
         let db_name = data["databases"][i];
         document.write("<h2>database:" + db_name + "</h2>");
         document.write("<table style= \"width:100%; border: 1px solid black;\" >");
        for (let n = 0; n < data[db_name].length; n++){
                    document.write("</tr>");
                    for (let m = 0; m < data[db_name][n].length; m++){
                        if ( n === 0 ){
                            document.write("<th  style= \" border: 1px solid black;\">" + data[db_name][n][m] + "</th>");
                        }
                        else {
                            document.write("<td  style= \" border: 1px solid black;\">" + data[db_name][n][m] + "</td>");
                        }
                    }
                    document.write("</tr>");
         }
          document.write("</table>");
    }
}
}
