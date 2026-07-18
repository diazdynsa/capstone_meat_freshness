import os
import shutil
import pandas as pd

def organize_dir(directory):
    csv_path = os.path.join(directory, '_classes.csv')
    if not os.path.exists(csv_path):
        print(f"File _classes.csv tidak ditemukan di {directory}.")
        return

    print(f"Merapikan folder {directory} berdasarkan _classes.csv...")
    try:
        df = pd.read_csv(csv_path)
        # Bersihkan nama kolom 
        df.columns = [col.strip() for col in df.columns]
        
        classes = ['Fresh', 'Half-Fresh', 'Spoiled']
        for cls in classes:
            os.makedirs(os.path.join(directory, cls), exist_ok=True)
            
        moved_count = 0
        for _, row in df.iterrows():
            filename = str(row['filename']).strip()
            
            # Menentukan kelas
            if row.get('Fresh', 0) == 1:
                cls = 'Fresh'
            elif row.get('Half-Fresh', 0) == 1:
                cls = 'Half-Fresh'
            elif row.get('Spoiled', 0) == 1:
                cls = 'Spoiled'
            else:
                continue
                
            src = os.path.join(directory, filename)
            dst = os.path.join(directory, cls, filename)
            
            if os.path.exists(src):
                shutil.move(src, dst)
                moved_count += 1
                
        print(f"Selesai! {moved_count} gambar dipindahkan ke sub-folder di {directory}.")
    except Exception as e:
        print(f"Error saat merapikan {directory}: {e}")

if __name__ == '__main__':
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
    organize_dir(os.path.join(base_dir, 'train'))
    organize_dir(os.path.join(base_dir, 'val'))
    organize_dir(os.path.join(base_dir, 'test'))
