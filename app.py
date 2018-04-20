from flask import Flask, render_template
app = Flask(__name__)

import os
import psycopg2

try:
	DATABASE_URL = os.environ['DATABASE_URL']
except:
	print("defaulting to hardcoded URL")




@app.route("/")
def home():

		return render_template("welcome.html")


@app.route("/<string:fish>/<string:waterbody>/<string:length>/<string:sensitive>")
def db_query(fish,waterbody,length,sensitive):
		# number = pgselect * from fish_guide where waterbody_code=41508250 and specname=73 and length_category_id=40 and sensitive='Sensitive'
		number = 8

		'''
		fish = u'Northern Pike'
		waterbody = u'Hutchison Lake'
		length = u'70-75cm'
		sensitive = u'General'
		'''
		
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cur = conn.cursor()
		query_string = "SELECT * FROM fish_guide WHERE specname=\'" + fish + "\' AND guide_locname_eng=\'" + waterbody  +"\' AND population_type_desc=\'" + sensitive + "\' AND length_category_label=\'" + length + "\';"
		print(query_string)
		cur.execute(query_string)
		number = str(int(cur.fetchone()[10]))

		cur.close()
		conn.close()


		if sensitive == "Sensitive":
			text = "<br>You are in a sensitive population, so you can eat less fish than other people. <br>"
		else:
			text = ""

		text = text + "<br>You caught a <strong>" + fish + "</strong> in <strong>" + waterbody + "</strong>, and it was <strong>" + length +"</strong> long.<br><br>"
		text = text + "You can eat <strong>" + str(number) + "</strong> meals of this fish safely in one month. <br><br>"
		text = text + "Add the details for another fish above and search again!"
		#return "<p>" + " ".join([fish,waterbody,length,sensitive]) + "</p>"
		return text

application=app
if __name__ == '__main__':
	app.run(debug=True)
