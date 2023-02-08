import os, glob, json, jsonlines
import re

reObj = re.compile(r'(.*)_(\d+\.0)_(\d+\.0)')

s_list = ['train', 'val', 'test']

video_dir = '/data/video_datasets/QVHighlights/'
dataset_dir = './'

ids = {
    'train': set(),
    'val': set(),
    'test': set()
}

for filename in glob.glob('highlight_*_release.jsonl'):
    with jsonlines.open(filename) as f:
        s = filename.split('_')[1]
        for line in f.iter():
            vid = line['vid']
            matchObj = reObj.match(vid)
            youtube_id = matchObj.group(1)
            ids[s].add(youtube_id)


for s in s_list:
    print('{}_video_ids', s, len(ids[s]))

# print(ids['train'][0])

all_video_ids = set(ids['train'].union(ids['val']).union(ids['test']))
print("all_video_ids", len(all_video_ids))


video_ids = []

for i, path in enumerate(glob.glob(video_dir + '*')):
    video_ids.append(path.split('/')[-1][2:-4])


video_ids = set(video_ids)

result = {
    'train': {
        'exists' : list(ids['train'].intersection(video_ids)),
        'missing': list(ids['train'].difference(video_ids))
    },
    'val': {
        'exists' : list(ids['val'].intersection(video_ids)),
        'missing': list(ids['val'].difference(video_ids))
    },
    'test': {
        'exists' : list(ids['test'].intersection(video_ids)),
        'missing': list(ids['test'].difference(video_ids))
    },
}

for s in s_list:
    print('{}\t: exists={}\t, missing={}'.format(s, len(result[s]['exists']), len(result[s]['missing'])))

with open(dataset_dir + 'downloaded_vids.json', 'w', encoding='utf8') as f:
    json.dump(result, f)