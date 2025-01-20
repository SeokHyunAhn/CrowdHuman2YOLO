# CrowdHuman2YOLO
Convert CrowdHuman .odgt file from https://www.crowdhuman.org to YOLO label format.

# How to use
## 1. Download files 
**CrowdHuman_train01.zip, CrowdHuman_train02.zip, CrowdHuman_train03.zip, CrowdHuman_val.zip, annotation_train.odgt, annotation_val.odgt**

## 2. Run organize_dataset.py
Edit the file path (line[60])
<pre><code>python3 organize_dataset.py </code></pre>

## 3. Run odgt2yolo.py
If you don't need the head label(class 1), run odgt2yolo_without_head.py
<pre><code>python odgt2yolo.py annotation_train.odgt </code></pre>
<pre><code>python odgt2yolo.py --val annotation_val.odgt </code></pre>

# Result
<pre><code>
CrowdHuman/
├── train/
│   ├── images/
│   │   ├── 000001.jpg
│   │   ├── 000002.jpg
│   │   └── ...
│   ├── labels/
│       ├── 000001.txt
│       ├── 000002.txt
│       └── ...
├── val/
│   ├── images/
│   │   ├── 000001.jpg
│   │   ├── 000002.jpg
│   │   └── ...
│   ├── labels/
│       ├── 000001.txt
│       ├── 000002.txt
│       └── ...
</code></pre>
