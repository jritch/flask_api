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

		fish = u'Coho Salmon'
		waterbody = u'Lake Erie 1 - Western Basin'
		length = u'40-45cm'
		sensitive = u'General'

		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cur = conn.cursor()
		cur.execute("SELECT * FROM fish_guide_smol;")
		db_test = str(cur.fetchone())
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
		return text + db_test

application=app
if __name__ == '__main__':
	app.run(debug=True)
