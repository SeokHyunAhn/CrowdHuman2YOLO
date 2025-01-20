import os
import zipfile
from pathlib import Path
import shutil

def extract_and_organize_files(base_path):
    # 압축파일 경로
    base_path = Path(base_path).expanduser()
    
    # 이미지 및 라벨 폴더 생성
    train_image_dir = base_path / 'train' / 'images'
    train_label_dir = base_path / 'train' / 'labels'
    val_image_dir = base_path / 'val' / 'images'
    val_label_dir = base_path / 'val' / 'labels'

    # 필요한 디렉토리 생성
    train_image_dir.mkdir(parents=True, exist_ok=True)
    train_label_dir.mkdir(parents=True, exist_ok=True)
    val_image_dir.mkdir(parents=True, exist_ok=True)
    val_label_dir.mkdir(parents=True, exist_ok=True)

    # 압축 파일 찾기
    zip_files = list(base_path.glob('*.zip'))

    for zip_file in zip_files:
        print(f"Processing {zip_file}...")
        
        # 압축 해제용 임시 디렉토리 생성
        temp_extract_dir = base_path / 'temp_extract'
        temp_extract_dir.mkdir(exist_ok=True)

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # 압축 해제
            zip_ref.extractall(temp_extract_dir)
        
        # 압축 파일의 목적지 폴더 결정
        if 'train' in zip_file.name.lower():
            destination = train_image_dir
        elif 'val' in zip_file.name.lower():
            destination = val_image_dir
        else:
            print(f"Skipping unknown file: {zip_file}")
            shutil.rmtree(temp_extract_dir)
            continue
        
        # temp_extract_dir에서 Images 폴더의 내용물만 이동
        images_folder = temp_extract_dir / 'Images'
        if images_folder.exists():
            for file in images_folder.iterdir():
                if file.is_file():  # 파일만 이동
                    shutil.move(str(file), destination)
        else:
            print(f"Warning: 'Images' folder not found in {zip_file}")
        
        # 임시 폴더 삭제
        shutil.rmtree(temp_extract_dir)
        print(f"Extracted and organized {zip_file} to {destination}")
    
    print(f"All files are organized in train/images and val/images")

if __name__ == "__main__":
    # 압축파일이 위치한 기본 경로 설정
    dataset_path = "~/Downloads/Custom-Yolo-Dataset/CrowdHuman"
    extract_and_organize_files(dataset_path)

