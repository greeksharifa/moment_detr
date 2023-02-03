import jsonlines
import re
import os, glob

url_format = 'https://www.youtube.com/embed/{}?start={}&end={}&version=3'
reObj = re.compile(r'(.*)_(\d+\.0)_(\d+\.0)')

with open('download.sh', mode="w", encoding="utf-8") as f_sh:
    f_sh.write("#!/usr/bin/env bash\n\n")  # write bash file header

    for filename in glob.glob('highlight_*_release.jsonl'):
        save_dir = '/home/ywjang/Downloads/QVHighlights/' + filename.split('_')[1] + '/'
        with jsonlines.open(filename) as f:
            for line in f.iter():
                vid = line['vid']
                matchObj = reObj.match(vid)
                youtube_id = matchObj.group(1)
                start_time = matchObj.group(2)
                end_time = matchObj.group(3)
                
                url = url_format.format(youtube_id, start_time, end_time)
    
                cmd = 'yt_dlp -f best -f mp4 "{}" -o "{}"'.format(url, save_dir + 'v_' + youtube_id + '.mp4')
                
                f_sh.write(cmd + '\n')
                
                # print(cmd)
                # print(os.system(cmd))