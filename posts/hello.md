title: It Is Working
date: 2015-01-22

# Yeah!


### What is FlaSSGee?

Flassgee is a FLAsk bases Static Site Generator

### Template
	
	:::Python

	from flask import Flask
	app = Flask(__name__)

	@app.route("/")
	def hello():
	    return "Hello World!"

	if __name__ == "__main__":
	    app.run()