import json, os, random
from collections import defaultdict

# Load train dataset
with open(r'c:\Users\Pedro\estudos\puc\VLM_Benchmark_Vestments\original_dataset\instances_attributes_train2020.json') as f:
    data = json.load(f)

# Build lookups
images_by_id = {img['id']: img for img in data['images']}
attrs_by_id = {a['id']: a['name'] for a in data['attributes']}
cats_by_id = {c['id']: c['name'] for c in data['categories']}

# 5 chosen categories
chosen_cats = {
    10: 'dress',
    1: 'top, t-shirt, sweatshirt',
    6: 'pants',
    23: 'shoe',
    4: 'jacket'
}

# Group annotations by image
annots_by_image = defaultdict(list)
for ann in data['annotations']:
    annots_by_image[ann['image_id']].append(ann)

# Find images where ALL annotations belong to the 5 chosen categories
valid_images = []
for img_id, anns in annots_by_image.items():
    cat_ids = set(a['category_id'] for a in anns)
    if cat_ids.issubset(set(chosen_cats.keys())):
        valid_images.append(img_id)

print(f'Images with only 5 chosen categories: {len(valid_images)}')

# Sample 10 that exist on disk
img_path = r'C:\Users\Pedro\Downloads\train2020\train'
found = []
random.seed(42)
random.shuffle(valid_images)
for img_id in valid_images:
    fname = images_by_id[img_id]['file_name']
    fpath = os.path.join(img_path, fname)
    if os.path.exists(fpath):
        found.append(img_id)
    if len(found) >= 10:
        break

print(f'Found {len(found)} images on disk')
print()

for i, img_id in enumerate(found, 1):
    img = images_by_id[img_id]
    anns = annots_by_image[img_id]
    print(f'=== Image {i}: {img["file_name"]} ===')
    for ann in anns:
        cat = cats_by_id[ann['category_id']]
        attrs = [attrs_by_id[aid] for aid in ann.get('attribute_ids', [])]
        print(f'  Category: {cat}')
        print(f'  Attributes: {", ".join(attrs) if attrs else "(none)"}')
    print()
