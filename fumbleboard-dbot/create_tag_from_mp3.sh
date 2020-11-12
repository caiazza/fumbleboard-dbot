jq '.[] | {SourceFile, Title,Artist,Album}' <(exiftool -j music/*tags.mp3) | sed 's/"Album":\(.*\)/"Tags" : [\1]/' > playlist.json 
