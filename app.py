from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
		return render_template("welcome.html")

@app.route("/<string:fish>/<string:waterbody>/<string:length>/<string:sensitive>")
def db_query(fish,waterbody,length,sensitive):
		# number = pgselect * from fish_guide where waterbody_code=41508250 and specname=73 and length_category_id=40 and sensitive='Sensitive'
		number = 8

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
