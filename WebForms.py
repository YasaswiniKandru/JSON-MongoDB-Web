import json
import mysql.connector

from flask import Flask
from jsonschema import Draft3Validator

schema = {
    "type": "object",
    "properties": {
        "backendHost": {"type": "string"},
        "backendPort": {"type": "string"},
        "backendURL": {"type": "string"},
        "caption": {"type": "string"},
        "elements":
            {"type": "array",
             "items": {
                 "type": "object",
                 "properties": {
                     "caption": {"type": "string"},
                     "datatype": {"type": "string"},
                     "ename": {"type": "string"},
                     "etype": {"type": "string"},
                     "maxlength": {"type": "string"},
                     "required": {"type": "string"},
                     "size": {"type": "string"},
                     "group":
                         {"type": "array",
                          "items": {
                              "type": "object",
                              "properties": {
                                  "checked": {"type": "string"},
                                  "value": {"type": "string"},
                                  "caption": {"type": "string"}
                              }
                          }
                          }
                 }
             }
             },
        "id": {"type": "string"},
        "mysqlDB": {"type": "string"},
        "mysqlPWD": {"type": "string"},
        "mysqlUserID": {"type": "string"},
        "name": {"type": "string"}
    }
}

app = Flask('__name__')


def intiliazedbfile(data):
    mydb = mysql.connector.connect(
        host="localhost",
        user="raj",
        password="r123",
    )
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES LIKE " + "'" + data["mysqlDB"] + "';")
    if not mycursor:
        mycursor.execute("CREATE DATABASE " + data["mysqlDB"] + ";")
        mycursor.execute("SHOW DATABASES")
        for x in mycursor:
            print(x)
    else:
        f = open("interests.sql", "w")
        f.write('''SET FOREIGN_KEY_CHECKS = 0;''')
        f.close()


@app.route('/')
def hello_world():
    text = input("Json File Name:")  # form1.json form2.json
    inp = open(text, "r")
    data = json.loads(inp.read())
    instance = data
    v = Draft3Validator(schema)
    errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
    for error in errors:
        print(error.message)
    createjavascript(data)
    intiliazedbfile(data)
    createhtmlfile(data)
    return print()


def createsqlfile(main_table_element, main_table_datatype, new_table_element, new_table_datatype,
                  new_table_element_type, primary_col, primary_col_datatype, parent_table):
    db = open("interests.sql", "w")
    drp_st = ""
    create_main_table = "\n" + "CREATE TABLE main_table ("
    create_new_table = []
    if main_table_element is not []:
        drp_st = "\n" + "DROP TABLE if EXISTS main_table;"
        for i in range(len(main_table_element)):
            if i == 0:
                create_main_table = create_main_table + "\n" + main_table_element[i] + " " + main_table_datatype[i]
            else:
                create_main_table = create_main_table + "," + "\n" + main_table_element[i] + " " + main_table_datatype[
                    i]
        if primary_col in main_table_element:
            create_main_table = create_main_table + "," + "\n" + "primary key (" + primary_col + ")"
        else:
            create_main_table = create_main_table + "," + "\n" + primary_col + " " + primary_col_datatype
            create_main_table = create_main_table + "," + "\n" + "foreign key (" + primary_col + ")" + "references " + parent_table + "(" + primary_col + ")"

    if new_table_element is not []:
        for i in range(len(new_table_element)):
            drp_st = drp_st + "\n" + "DROP TABLE if EXISTS " + new_table_element_type[i] + ";"
            new_table = "\n" + "CREATE TABLE " + new_table_element_type[i] + " (" + "\n" + new_table_element[i] + " " + \
                        new_table_datatype[i]
            if primary_col == new_table_element[i]:
                new_table = new_table + "," + "\n" + "primary key (" + primary_col + ")"
            else:
                new_table = new_table + "," + "\n" + primary_col + " " + primary_col_datatype
                new_table = new_table + "," + "\n" + "primary key (" + primary_col + "," + new_table_element[i] + ")"
                new_table = new_table + "," + "\n" + "foreign key (" + primary_col + ")" + " references " + parent_table + "(" + primary_col + ")"
            new_table = new_table + "\n" + ");"
            create_new_table.append(new_table)

    drp_st = drp_st + "\n" + "SET FOREIGN_KEY_CHECKS = 1;"
    db.write(drp_st + "\n" + create_main_table + "\n" + ");" + "\n")
    for i in range(len(create_new_table)):
        db.write("\n" + create_new_table[i])
    db.close()


def createpythonfile(mysqluserid, mysqlpwd, mysqldb, main_table_element, main_table_datatype, new_table_element,
                     new_table_datatype,
                     new_table_element_type, primary_col, primary_col_datatype, backendHost, backendPort):
    f = open("interests.py", "w")
    f.write("from flask import Flask, json, request" + "\n" +
            "from flask_cors import CORS" + "\n" +
            "import mysql.connector" + "\n" + "\n" +
            "app = Flask(\'__name__\')" + "\n" +
            "CORS(app)" + "\n" + "\n" + "\n" +
            "@app.route('/webforms/insert', methods=['GET', 'POST'])" + "\n" +
            "def insertdata():" + "\n" + "\t" + "if request.method == 'POST':" + "\n" + "\t" + "\t" +
            "result = request.form.to_dict()" + "\n" + "\t" + "\t" +
            "intiliazedbfile(result)" + "\n" + "\n"
            )

    f.write("\n" + "def intiliazedbfile(data):" + "\n" +
            "\t" + "mydb = mysql.connector.connect(" + "\n" +
            "\t" + "\t" + "host=\"localhost\"," + "\n" +
            "\t" + "\t" + "user=\"" + mysqluserid + "\"," + "\n" +
            "\t" + "\t" + "password=\"" + mysqlpwd + "\"," + "\n" +
            "\t" + "\t" + "database=\"" + mysqldb + "\"" + ")" + "\n" +
            "\t" + "mycursor = mydb.cursor()" + "\n"
            )
    sql = "\t" + "sql = \"INSERT INTO main_table ("
    sql_val = ") VALUES ("
    val = "\t" + "val = ("
    for i in range(len(main_table_element)):
        if i == 0:
            sql = sql + main_table_element[i]
            sql_val = sql_val + "%s"
            val = val + "data[\"" + main_table_element[i] + "\"]"
        else:
            sql = sql + "," + main_table_element[i]
            sql_val = sql_val + "," + "%s"
            val = val + ", " + "data[\"" + main_table_element[i] + "\"]"
    if primary_col in main_table_element:
        print()
    else:
        sql = sql + "," + primary_col
        sql_val = sql_val + "," + "%s"
        val = val + ", " + "data[\"" + primary_col + "\"]"

    sql = sql + sql_val + ")\""
    val = val + ")"
    f.write(sql + "\n" + val + "\n")
    f.write("\t" + "mycursor.execute(sql, val)" + "\n" +
            "\t" + "mydb.commit()" + "\n" +
            "\t" + "print(mycursor.rowcount, " + "\"" + "record inserted" + "\"" + ")")

    for i in range(len(new_table_element)):
        sql = "\n" + "\t" + "sql = \"INSERT INTO " + new_table_element_type[i] + " ("
        sql_val = ") VALUES ("
        val = "\t" + "val = ("
        sql = sql + new_table_element[i]
        sql_val = sql_val + "%s"
        val = val + "data[\"" + new_table_element[i] + "\"]"
        if primary_col in new_table_element:
            print()
        else:
            sql = sql + "," + primary_col
            sql_val = sql_val + "," + "%s"
            val = val + ", " + "data[\"" + primary_col + "\"]"
        sql = sql + sql_val + ")\""
        val = val + ")"
        f.write(sql + "\n" + val + "\n")
        f.write("\t" + "mycursor.execute(sql, val)" + "\n" +
                "\t" + "mydb.commit()" + "\n" +
                "\t" + "print(mycursor.rowcount, " + "\"" + "record inserted" + "\"" + ")" + "\n" + "\n")

    f.write("@app.route('/webforms/display', methods=['GET', 'POST'])" + "\n" +
            "def displaydata():" + "\n" + "\t" +
            "if request.method == 'GET':" + "\n" + "\t" + "\t" +
            "mydb = mysql.connector.connect(" + "\n" + "\t" + "\t" + "\t" +
            "host=\"localhost\"," + "\n" + "\t" +
            "\t" + "\t" + "user=\"" + mysqluserid + "\"," + "\n" + "\t" +
            "\t" + "\t" + "password=\"" + mysqlpwd + "\"," + "\n" + "\t" +
            "\t" + "\t" + "database=\"" + mysqldb + "\"" + ")" + "\n" + "\t" +
            "\t" + "mycursor = mydb.cursor()" + "\n" + "\t" +
            "\t" + "main_dict = {}" + "\n" + "\t" +
            "\t" + "mycursor.execute(\"SHOW TABLES\")" + "\n" + "\t" +
            "\t" + "db_tables = mycursor.fetchall()" + "\n" + "\t" +
            "\t" + "db_tables = [i[0] for i in db_tables]" + "\n" + "\t" +
            "\t" + "main_dict[\"databases\"] = db_tables" + "\n" + "\t" +
            "\t" + "for db_table in db_tables:" + "\n" + "\t" +"\t" +
            "\t" + "mycursor.execute(\"DESCRIBE \" + db_table)" + "\n" + "\t" +"\t" +
            "\t" + "db_schema_data = mycursor.fetchall()" + "\n" + "\t" +"\t" +
            "\t" + "db_schema_data = [i[0] for i in db_schema_data]" + "\n" + "\t" +"\t" +
            "\t" + "main_dict[db_table] = [db_schema_data]" + "\n" + "\t" +"\t" +
            "\t" + "y = \"SELECT * from \" + db_table + \";\"" + "\n" + "\t" +"\t" +
            "\t" + "mycursor.execute(y)" + "\n" + "\t" +"\t" +
            "\t" + "db_data = mycursor.fetchall()" + "\n" + "\t" +"\t" +
            "\t" + "for data in db_data:" + "\n" + "\t" + "\t" +"\t" +
            "\t" + "main_dict[db_table].append(data)" + "\n" +"\t" +
            "\t" + "return json.dumps(main_dict)" + "\n"
            )

    f.write('''\n\n\nif __name__ == '__main__':\n''')
    f.write("\t" + "app.run(host=\"" + backendHost + "\"," + " port=" + backendPort + ")")
    f.close()


def createbuttonhtmlfile():
    f = open("interests_display.html", "w")
    f.write('''<html><body><head>
    <style>
    table, th, td {
  border: 1px solid black;
}
</style>
    <title>Button</title>
</head>
<script src="./interests.js"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
<button type="button" onclick= fetchdata()>Click Me!</button>
<p id="demo"></p>
</body>
    </html>''')
    f.close()


def appendjavascriptfile(url):
    f = open("interests.js", "w")
    f.write('''function fetchdata(){
            $.ajax({
           type: 'GET',
    ''')
    f.write("url:\"" + url + "display\",")
    f.write('''processData: true,
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
         document.write("<table style= \\"width:100%; border: 1px solid black;\\" >");
        for (let n = 0; n < data[db_name].length; n++){
                    document.write("</tr>");
                    for (let m = 0; m < data[db_name][n].length; m++){
                        if ( n === 0 ){
                            document.write("<th  style= \\" border: 1px solid black;\\">" + data[db_name][n][m] + "</th>");
                        }
                        else {
                            document.write("<td  style= \\" border: 1px solid black;\\">" + data[db_name][n][m] + "</td>");
                        }
                    }
                    document.write("</tr>");
         }
          document.write("</table>");
    }
}
}
''')
    f.close()


def createhtmlfile(data):
    f = open("interests.html", "w")
    f.write('''<html>
                <body>
                <script src="./interests.js"></script>
            ''')
    backendURL = data["backendURL"]
    backendHost = data["backendHost"]
    backendPort = data["backendPort"]
    mysqluserid = data["mysqlUserID"]
    mysqlpwd = data["mysqlPWD"]
    mysqldb = data["mysqlDB"]
    f.write("<form name=" + "\"myForm\"" + " action =\"" + backendURL + "insert" + "\" onsubmit= \" return validation() \" method =" + "\"POST\">")
    for x, y in data.items():
        if x == "elements":
            i = 0
            main_table_element = []
            main_table_datatype = []
            new_table_element = []
            new_table_datatype = []
            primary_col = ""
            primary_col_datatype = ""
            new_table_element_type = []
            checkbox_count = 0
            multiselect_count = 0
            parent_table = ""
            for j in y:

                if j["etype"] == "textbox":
                    l = "<label for=" + j["ename"] + ">" + j["caption"] + "</label>" \
                                                                          "<input type=text  id=" + j[
                            "ename"] + "  name=" + j["ename"] + "  maxlength=" + j["maxlength"] + "  size=" + j[
                            "size"]
                    if j["required"] == "true":
                        l = l + "  required><br>"
                    else:
                        l = l + "><br>"
                    f.write(l)


                    main_table_element.append(j["ename"])
                    main_table_datatype.append(dbdatatype(j["datatype"]))
                    if "key" in j.keys():
                        primary_col = j["ename"]
                        primary_col_datatype = dbdatatype(j["datatype"])
                        parent_table = "main_table"

                elif j["etype"] == "checkbox" or j["etype"] == "radiobutton":
                    caption = "<p>" + j["caption"] + "</p>"
                    f.write(caption)
                    if j["etype"] == "radiobutton":
                        j["etype"] = "radio"
                        main_table_element.append(j["ename"])
                        main_table_datatype.append(dbdatatype(j["datatype"]))
                    else:
                        new_table_element.append(j["ename"])
                        new_table_datatype.append(dbdatatype(j["datatype"]))
                        if checkbox_count == 0:
                            element_type = "checkbox"
                        else:
                            element_type = "checkbox_" + checkbox_count
                        new_table_element_type.append(element_type)
                        checkbox_count = checkbox_count + 1
                    if "key" in j.keys():
                        primary_col = j["ename"]
                        primary_col_datatype = dbdatatype(j["datatype"])
                        parent_table = "main_table"
                    for g in j["group"]:
                        l = "<label for=" + j["ename"] + ">" + g["caption"] + "</label>" \
                                                                              "<input type=" + j["etype"] + "  id=" + j[
                                "ename"] + "  name=" + j["ename"] + " value=" + g["value"]

                        if "checked" in g.keys() and j["etype"] == "checkbox":
                            l = l + "  checked" + "><br>"
                        else:
                            l = l + "><br>"
                        f.write(l)

                elif j["etype"] == "selectlist" or j["etype"] == "multiselectlist":
                    element_type = ""
                    if j["etype"] == "selectlist":
                        main_table_element.append(j["ename"])
                        main_table_datatype.append(dbdatatype(j["datatype"]))
                    else:
                        new_table_element.append(j["ename"])
                        new_table_datatype.append(dbdatatype(j["datatype"]))
                        if multiselect_count == 0:
                            element_type = "multiselect"
                        else:
                            element_type = "multiselect_" + multiselect_count
                        new_table_element_type.append(element_type)
                        multiselect_count = multiselect_count + 1
                    if "key" in j.keys():
                        primary_col = j["ename"]
                        primary_col_datatype = dbdatatype(j["datatype"])
                        parent_table = element_type
                    label = "<br><label for=" + j["ename"] + ">" + j["caption"] + "</label>" + "<select name=" + j[
                        "ename"] + " id=" + j["ename"] + ">"
                    f.write(label)
                    for g in j["group"]:
                        inp = "<option value=" + g["value"] + ">" + g["caption"] + "</option>"
                        f.write(inp)
                    f.write('''</select>''')

                elif j["etype"] == "submit" or j["etype"] == "reset":
                    sr = "<br><input type=" + j["etype"] + "  value=" + j["ename"] + ">   "
                    f.write(sr)
                createsqlfile(main_table_element, main_table_datatype, new_table_element, new_table_datatype,
                              new_table_element_type, primary_col, primary_col_datatype, parent_table)
                createpythonfile(mysqluserid, mysqlpwd, mysqldb, main_table_element, main_table_datatype,
                                 new_table_element,new_table_datatype,new_table_element_type, primary_col, primary_col_datatype, backendHost, backendPort)
                createbuttonhtmlfile()
                appendjavascriptfile(backendURL)
    js = '<script>'
    error = ''

    js += 'function validation() {\n'
    for element in data['elements']:
                ename = element['ename']
                etype = element['etype']

                if etype == 'textbox':
                    js += 'var ' + ename + ' = document.getElementById("' + ename + '").value.trim();\n'

                elif etype == 'selectlist':
                    js += 'var ' + ename + ' = document.querySelector("#' + ename + '").value;\n'

                elif etype == 'radiobutton':
                    js += 'var ' + ename + ' = document.querySelector(input[name=' + ename + ']:checked);\n'

                elif etype == 'checkbox':
                    js += 'var ' + ename + ' = [];\n'
                    js += 'var ' + etype + ' = document.querySelectorAll(\'input[name="' + ename + '"]:checked\');checkbox.forEach((checkbox) => { ' + ename + '.push(checkbox.value); });\n'

                elif etype == 'multiselectlist':
                    js += 'var ' + ename + ' = [];\n'
                    js += 'document.querySelectorAll(\'#' + ename + ' option:checked\').forEach((msl) => { ' + ename + '.push(msl.value);})\n'

    js += 'error = \" \";\n'
    for element in data['elements']:
                ename = element['ename']
                if ('required' in element.keys()):
                    if (element['required'] == "true"):
                        js += 'if (' + ename + ' == "" ) {\n'
                        js += 'alert( "Please fill  ' + element['caption'] + ' ") \n   }\n'
                if ('datatype' in element.keys()):
                    if (element['datatype']=="integer"):
                        js += "var numbers = /^[0-9]+$/;\n"
                        js += ' if (!'+ element['ename'] + '.match(numbers)){\n'
                        js += 'alert( "' + element['caption'] + ' must be Integer");}\n'
                    if (element['datatype']=="string"):
                        js += "var numbers = /^[a-z]+$/;\n"
                        js += ' if (!'+ element['ename'] + '.match(numbers)){\n'
                        js += 'alert("' + element['caption'] + ' must be String");}\n'

    js += "\n} </script>"
    f.write(js)

    f.write('''
    </form>
    </body>
    </html>''')
    f.close()


def createjavascript(data):
    k = open("interests.js", "w")
    k.close()


def dbdatatype(dt):
    if dt == "integer":
        return "INT"
    elif dt == "string":
        return "VARCHAR(100)"


if __name__ == '__main__':
    app.run()