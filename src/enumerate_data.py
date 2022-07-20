import os
import pandas as pd
import heapq

# get the subdirectories that contain the attack folders
dir = '/Users/manasg/Downloads/Final_project_ML/AWID/AWID3_Dataset_CSV/CSV/'
folders = [x[0] for x in os.walk(dir)]

attack_traffic_files = {}
no_attack_traffic_files = []

for ind, i in enumerate(folders):
	if ind == 0: 
		continue
	else:
		path = f'{i}/'
		files = os.listdir(path)
		print(f'File Path: {path}')

		file_names = []
		for f in files:
			file_names.append(f)

		cnt = 0
		cnt_attck = 0

		for file in file_names:
			#print(f'{file}')
			df = pd.read_csv(str(path)+file, low_memory=True, usecols = ['Label'])
			attack_count= (~df["Label"].str.contains("Normal", na=False)).sum()

			if attack_count>0:
				print(f"There are {attack_count} attack rows in {file}")
				attack_data_ratio = attack_count/df.shape[0]
				attack_traffic_files[file]= attack_data_ratio
				cnt_attck += 1
			else:
				no_attack_traffic_files.append(file)
				cnt += 1
			
		print(f"\nTotal files with attack data: {cnt_attck} ; Files without attack data: {cnt}")
		print("\n")


print("\nFile names with Attack data and ratio of attack to normal rows: \n", attack_traffic_files)
print("\nFile names with no attack data: ", no_attack_traffic_files)

# export the list of files with NO attack traffic to a txt file
f = open('/Users/manasg/Downloads/Final_project_ML/AWID/AWID3_Dataset_CSV/no_Attack_data.txt', 'w')
with open('/Users/manasg/Downloads/Final_project_ML/AWID/AWID3_Dataset_CSV/no_Attack_data.txt', 'w') as filehandle:
    for listitem in no_attack_traffic_files:
        filehandle.write('%s\n' % listitem)

# find the files with the largest and smallest attack to normal traffic ratio
lowest = heapq.nsmallest(5, attack_traffic_files, key=attack_traffic_files.get)
print(f'\nFiles with the lowest attack data {lowest}')
highest = heapq.nlargest(5, attack_traffic_files, key=attack_traffic_files.get)
print(f'Files with the highest attack data {highest}')
