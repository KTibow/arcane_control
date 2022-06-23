from flask import Flask, request
import requests
import json
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def home():
    page = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Arcane Control</title>
            <style>
                body {
                    background: black;
                    color: white;
                }
                button {
                    background: #181818;
                    color: white;
                    border: none;
                    padding: 8px;
                    margin: 8px;
                    font-size: 20px;
                }
                iframe {
                    background: white;
                    width: 100%;
                    border: none;
                }
                @media (min-width: 500px) {
                    button {
                        font-size: revert;
                    }
                }
            </style>
        </head>
        <body>
            <iframe name="status"></iframe>
    """
    # add stuff
    for button in json.load(open("options.json"))["buttons"]:
        page += f"""
            <form action="/call" method="POST" target="status">
                <input type="hidden" name="service" value='{button["service"]}'>
                <input type="hidden" name="serviceData" value='{button["service_data"]}'>
                <button type="submit">{button["text"]}</button>
            </form>
        """
    page += """
        </body>
    </html>
    """
    return page


@app.route("/call", methods=["POST"])
def call():
    return (
        request.form["service"]
        + " has been called<br>"
        + requests.post(
            "http://supervisor/core/api/services/"
            + request.form["service"].replace(".", "/"),
            json=json.loads(request.form["serviceData"]),
            headers={"Authorization": "Bearer " + os.environ["SUPERVISOR_TOKEN"]},
        ).text
    )


app.run(port=944, host="0.0.0.0")
