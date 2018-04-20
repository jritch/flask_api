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
		row = cur.fetchone()


		if row:
			number = str(int(row[9]))

			if sensitive == "Sensitive":
				text = "<br>You are in a sensitive population, so you can eat less fish than other people. <br>"
			else:
				text = ""

			text = text + "<br>You caught a <strong>" + fish + "</strong> in <strong>" + waterbody + "</strong>, and it was <strong>" + length +"</strong> long.<br><br>"
			text = text + "You can eat <strong>" + str(number) + "</strong> meals of this fish safely in one month. <br><br>"
			text = text + "Add the details for another fish above and search again!"
		#return "<p>" + " ".join([fish,waterbody,length,sensitive]) + "</p>"
		else:
			text = "<br>Unfortunately, this combination of fish, location, and length is missing from our data. <br><br>"
			query_string = "SELECT specname FROM fish_guide WHERE guide_locname_eng=\'" + waterbody  +"\';"
			cur.execute(query_string)
			row = cur.fetchall()
			spec_set = set()
			if row:
				for item in row:
					spec_set.add(item[0])
				text = text + "The location you have selected has entries for the following species of fish: " +  ", ".join(spec_set) + ".<br><br>"

			text = text + "Add the details for another fish, size or location above and try again."

		cur.close()
		conn.close()
		return text

application=app
if __name__ == '__main__':
	app.run(debug=True)
