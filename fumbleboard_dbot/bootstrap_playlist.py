import sys
import tracklist
import os
import urllib.parse
import json

def process_input_url(url):
    filename = str(os.path.splitext(os.path.split(urllib.parse.urlparse(url).path)[1])[0])
    filename = filename.replace("%20", " ")
    separator_index = filename.find(" - ")
    if separator_index > 0 :
        tag = filename[:separator_index]
        title = filename[separator_index + 3:]
        return tracklist.Track(SourceURL=url.rstrip(), Title=title, Tags=[tag])
    else:
        return tracklist.Track(SourceURL=url.rstrip(), Title=filename)


def bootstrap_playlist(argv):
    input_path = argv[0]
    if len(argv) == 1:
        output_path = "./tracks.json"
    else:
        output_path = argv[1]
    
    print(f"Creating the initial track list from the file {input_path} in {output_path}")

    ImportedTracks=[]
    with open (input_path) as input_file:
        for line in input_file:
            ImportedTracks.append(process_input_url(line).asdict())
            print(ImportedTracks[-1])
    
    with open (output_path, "w") as output_file:
        json.dump(ImportedTracks,output_file, indent=2)


if __name__ == "__main__":
    bootstrap_playlist(sys.argv[1:])