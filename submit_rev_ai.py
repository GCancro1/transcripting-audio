from rev_ai import apiclient
import json
from pathlib import Path
# create your client
access = "02zL9HMFK5TQzyzJbuLDK19CmdBPbPwXYEYJYFDnJfsmBRkQE9YKVd3tsX5o3Bg1TQYC9dNmRxWZsOxV6qE-ArobXyy6o"
client = apiclient.RevAiAPIClient(access)

# send a local file
# filename = ""
# main_path = Path("BTC - Transcription - Diarization testing")

# files = ""
# for file_path in main_path.glob("*"):
#     print(file_path.stem)
#     files += str(file_path) + "\n"



with open("voicefiles.txt", "r") as f:
    files = f.readlines()

# print(files)
def submit_rev_ai_job(file_path, out_file_name):

    print("starting job at " + file_path)
    job = client.submit_job_local_file(file_path)

    # check job status

    job_details = client.get_job_details(job.id)

    print(job_details)

    return job.id

def out_rev(job_id, out_file_name):

    # retrieve transcript as text
    transcript_text = client.get_transcript_text(job_id)

        # retrieve transcript as JSON
    transcript_json = client.get_transcript_json(job_id)

    with open(out_file_name + ".txt", "w") as f:
        f.write(transcript_text)


    with open(out_file_name + ".json", "w") as f:
        json.dump(transcript_json, f)

    # retrieve transcript as a Python object
    # transcript_object = client.get_transcript_object(job.id)

# print(files[1])

with open(files[1][:-1], "r") as f:
    print("opened")
submit_rev_ai_job(files[1][:-1], "TEST-"+files[1][:-1])

# for i in range(2, 26):
# ...     submit_rev_ai_job(files[i][:-1], "TEST-"+files[i][:-1])

# for i in client.get_list_of_jobs():
#     out_rev(i.id, "out_rev/" + i.name[:-4])



def refactor_transcript(filename):

    with open(filename, "r") as f:
        contents = json.load(f)
        print(type(contents))
        print(contents["monologues"][0]["speaker"]) 

        out_data = ""
        for segment in contents["monologues"]:
            # print(segment["speaker"])
            print(segment["elements"][0])
            # segment = contents["monologues"][0]
            out = "\tSpeaker " + str(segment["speaker"]) + ": "

            for element in segment["elements"]:
                if str(element["value"]) == "?":
                    out += '__?__'
                else:
                    out += str(element["value"])
                if element["type"] == "text":
                    conf = element["confidence"] * 100
                    out += f" ({conf:2.2f}%)"
                
            out_data += out + "\n\n"

        out_file =  "confidence/" + filename[7:-5] + "__confidence.txt"
        
        with open(out_file, "w") as fo:
            fo.write(out_data)

path = Path("out_rev")
for f in path.glob("*.json"):
    refactor_transcript(str(f))