import os, shutil
import pandas as pd

def copy_files(source_dir, destination_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_dir, os.path.relpath(source_path, source_dir))
            try:
                shutil.copy(source_path, destination_path)
            except shutil.SameFileError:
                print(f'File {file} already exists')

def copy_file(source_file, destination_dir):
    file_name = os.path.basename(source_file)
    destination_path = os.path.join(destination_dir, file_name)
    try:
        shutil.copy(source_file, destination_path)
    except shutil.SameFileError:
        print(f'File {file_name} already exists')


def organize_data(csv_file):
    df = pd.read_csv(csv_file)
    columns = df.columns.tolist()
    print(columns)
    check1 = str(input(f'Choose the column name to groupby (FROM 0 TO N, LEFT TO RIGHT):\n'))
    grouped = df.groupby(check1)
    check2 = str(input(f'Choose the column name to be groupbyed (FROM 0 TO N, LEFT TO RIGHT):\n'))
    filtered = grouped[check2].max()
    new_df = pd.DataFrame(filtered)
    return new_df

path = os.getcwd()
files = os.listdir(path)

folders = [file for file in files if os.path.isdir(file)]
print(folders)

check = int(input(f'Choose the folder name that has your files (FROM 0 TO N, LEFT TO RIGHT):\n'))
new_path = os.path.join(path, folders[check])
os.chdir(new_path)

try:
    os.mkdir('all_data')
except FileExistsError:
    pass

final_path = os.path.join(new_path, 'all_data')

for folder in os.listdir(new_path):
    copy_files(os.path.join(new_path, folder), final_path)

os.chdir(final_path)

l = list()
for file in os.listdir(final_path):
    if os.path.isfile(os.path.join(final_path, file)):
        l.append(organize_data(file))

index = [i for i in range(len(l))]

with pd.ExcelWriter('final_data.xlsx', engine='openpyxl') as writer:
    for i, df in enumerate(l):
        df.to_excel(writer, sheet_name=f'sheet{index[i]}')

for file in os.listdir(final_path):
    if file.endswith('.xlsx'):
        copy_file(os.path.join(final_path, file), path)
