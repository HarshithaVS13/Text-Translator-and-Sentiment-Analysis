from flask import Flask, request, render_template,url_for
from flask_cors import cross_origin
import boto3

app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/sound", methods = ["GET", "POST"])
@cross_origin()
def sound():
    if request.method == "POST":
        text = request.form['texttospeech']  
        sourcelanguage = request.form['sourcelanguage']
        targetlanguage = request.form['targetlanguage']
        translate = boto3.client(service_name='translate',region_name='us-east-1') 

        result = translate.translate_text(Text=text, SourceLanguageCode=sourcelanguage,TargetLanguageCode=targetlanguage) 

        translated = open("static/translated.txt","w+")
        translated.write(str(result["TranslatedText"]))
        translated.close()
        text = result["TranslatedText"]  
        gender = request.form['gender']
        polly = boto3.client(service_name='polly',region_name='us-east-1')
        if gender == "male":
             response = polly.synthesize_speech(OutputFormat='mp3', VoiceId='Brian',Text=text)
        else:
             response = polly.synthesize_speech(OutputFormat='mp3', VoiceId='Joanna',Text=text)
        file = open('static/speech.mp3', 'wb')
        file.write(response['AudioStream'].read())
        file.close()

        return render_template("index.html",conversion=result["TranslatedText"])
    else:
        return render_template("index.html")


@app.route("/sentiment", methods = ["GET", "POST"])
@cross_origin()
def sentiment():
    if request.method == "POST":
        text = request.form['texttospeech']  
        comprehend = boto3.client(service_name='comprehend',region_name='us-east-1') 

        result = comprehend.detect_sentiment(Text=text, LanguageCode='en')

        return render_template("index.html",result=result['Sentiment'])
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
