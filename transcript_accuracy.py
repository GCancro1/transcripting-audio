import json
from pathlib import Path
filename = "test_interview.json"

def refactor_transcript_rev(filename):

    with open(filename, "r") as f:
        contents = json.load(f)
        print(contents["monologues"][0]["speaker"]) 

        out_data = ""
        for segment in contents["monologues"]:
            # print(segment["speaker"])
            print(segment["elements"][0])
            # segment = contents["monologues"][0]
            out = "\tSpeaker " + str(segment["speaker"]) + ": "

            for element in segment["elements"]:
                out += str(element["value"])
                if element["type"] == "text":
                    conf = element["confidence"] * 100
                    out += f" ({conf:2.2f}%)"
            out_data += out + "\n\n"

        out_file =  "confidence/" + filename[7:-5] + "__confidence.txt"
        
        with open(out_file, "w") as fo:
            fo.write(out_data)


def refactor_transcript_deepgram(filename):
    with open(filename, "r") as f:
        contents = json.load(f)

        total_conf = contents["results"]["channels"][0]["alternatives"][0]["confidence"] * 100
        out = "Total Confidence: " + f" ({total_conf:2.2f}%)\n\n"
        for w in contents["results"]["channels"][0]["alternatives"][0]["words"]:
            if w["punctuated_word"][-1] == "?":
                out += w["punctuated_word"][:-1] + "__?__"
            else:
                out += w["punctuated_word"] 
            conf = w["confidence"] * 100
            out += f" ({conf:2.2f}%) "

        out_file =  "deepgram_confidence/" + filename[17:-5] + "__confidence.txt"
        
        with open(out_file, "w") as fo:
            fo.write(out)

# path = Path("out_rev")
path = Path("out_deepgram")
filename = ""
for f in path.glob("*.json"):
    refactor_transcript_deepgram(str(f))
    filename = str(f)