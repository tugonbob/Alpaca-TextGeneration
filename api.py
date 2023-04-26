from flask import Flask, request
from Tiffany import Tiffany

# init api
app = Flask(__name__)
API_KEY = "svs@TX77079"
bot = Tiffany()


@app.route("/Tiffany/", methods=["GET", "POST"])
def tiffany():
    # return {"response": "hi"}
    given_key = str(request.args.get("key"))
    invalid_api_key = given_key != API_KEY

    if invalid_api_key:
        return {"error": "Please provide a valid api key"}

    elif request.method == "GET":
        query = str(request.args.get("query"))
        response = bot.chat(query)
        print(response)
        return {"response": response}


# an example of how to do a get request to this api
def get_request():
    import requests

    key = "svs@TX77079"
    query = "Do you have any kids that you hate"
    url = f"https://idcirco.serveo.net/Tiffany/?key={key}&query={query}"
    response = requests.get(url)
    print(response.json())


# an example of how to do a post request to this api
def post_request():
    import requests
    import base64

    # IMPORTANT: convert your audio file to a base64 string
    enc = base64.b64encode(open("./test.wav", "rb").read())
    key = "svs@TX77079"
    url = f"https://bc35-2603-300c-114-9800-4545-1bdc-3d03-4182.ngrok.io/Tiffany/?key={key}"
    payload = {"audio": enc}
    response = requests.post(url, data=payload)
    print(response.json())


if __name__ == "__main__":
    app.run(host="localhost", port=8888)
