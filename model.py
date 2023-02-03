import json
from pyresparser import ResumeParser
from flask import Flask, request

app = Flask(__name__)


@app.route('/parse-cv', methods=['GET'])
def parse():
    for item in input(f"upload your CVs here please: "):
        filename = request.args.get(item)

        if filename is None:
            text = "please upload at least one file to be parsed"

        else:
            cv_data = ResumeParser(filename)\
                .get_extracted_data()
            text = json.dumps(cv_data)

        return text


parse()


if __name__ == '__model__':
    app.run(debug=True, threaded=True, port=8000)