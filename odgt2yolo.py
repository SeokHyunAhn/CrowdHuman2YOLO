import os
import json
from PIL import Image
from pathlib import Path
import argparse

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

def create_output_dir(output_dir):
    """
    Ensure that the output directory exists.
    """
    os.makedirs(output_dir, exist_ok=True)

def convert_to_yolo_format(opt):
    """
    Convert the data to YOLO format, including class 1 (head).
    """
    with open(opt.path, 'r') as rf:
        for x in rf:
            aitem = json.loads(x)

            # Determine output directory
            output_dir = os.path.join(ROOT, "train" if not opt.val else "val", "labels")
            create_output_dir(output_dir)
            output_file = os.path.join(output_dir, f"{aitem['ID']}.txt")

            # Determine image path
            image_folder = "train/images" if not opt.val else "val/images"
            image_path = os.path.join(ROOT, image_folder, f"{aitem['ID']}.jpg")

            if not os.path.exists(image_path):
                print(f"Warning: Image not found: {image_path}")
                continue

            img = Image.open(image_path)

            with open(output_file, 'w') as wf:
                for af in aitem["gtboxes"]:
                    if af["tag"] == 'mask':
                        continue

                    if af.get('extra', {}).get("ignore", 0) == 1:
                        continue

                    # Get bounding box details for person (class 0)
                    vbox = af["vbox"]
                    center_x = vbox[0] + vbox[2] / 2
                    center_y = vbox[1] + vbox[3] / 2
                    width = vbox[2]
                    height = vbox[3]

                    wf.write(f'0 {(center_x/img.width):.6f} {(center_y/img.height):.6f} '
                             f'{(width/img.width):.6f} {(height/img.height):.6f}\n')

                    # Get bounding box details for head (class 1)
                    if "hbox" in af:
                        hbox = af["hbox"]
                        center_x = hbox[0] + hbox[2] / 2
                        center_y = hbox[1] + hbox[3] / 2
                        width = hbox[2]
                        height = hbox[3]

                        wf.write(f'1 {(center_x/img.width):.6f} {(center_y/img.height):.6f} '
                                 f'{(width/img.width):.6f} {(height/img.height):.6f}\n')

            img.close()

def convert(opt):
    """
    Main function to handle conversion.
    """
    convert_to_yolo_format(opt)

def usage():
    """
    Print usage information.
    """
    print(f'Usage: python {__file__} filename')

def parse_opt(known=False):
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--val', action='store_true', help='Process validation set (val).')
    parser.add_argument('path', help='Path to the .odgt file.')
    return parser.parse_known_args()[0] if known else parser.parse_args()

if __name__ == "__main__":
    opt = parse_opt()
    convert(opt)

