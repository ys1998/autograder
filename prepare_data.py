import os
import shutil
import re

# Variables
ALL_SUBMISSIONS = 'lab3-submissions.zip'
ROLL_LIST       = 'Lab3/roll_list.txt'
EXTRACT_DIR     = 'Lab3/my_batch'

# Name of submission archive
# Keep as generic as possible unless strictly specified beforehand
# ?: is for not capturing that bracket as a group
SUBMISSION_NAME = re.compile('(?:la3|lab3)-([a-zA-Z0-9]+)\.(zip|tar\.gz|tgz)', re.IGNORECASE)

if __name__ == '__main__':
	# Read roll numbers to grade
	with open(ROLL_LIST, 'r') as f:
		temp = f.readlines()
		my_roll_numbers = [r.strip() for r in temp]
		carry_over = {r:1 for r in my_roll_numbers}
	
	# Unpack submissions in EXTRACT_DIR
	shutil.unpack_archive(filename=ALL_SUBMISSIONS, extract_dir=EXTRACT_DIR)
	
	# Convert folder names to roll-no
	for stud_dir in os.listdir(EXTRACT_DIR):
		for file in os.listdir(os.path.join(EXTRACT_DIR, stud_dir)):
			m = SUBMISSION_NAME.match(file)
			if m is not None:
				roll_no = m.group(1)
				if roll_no in my_roll_numbers:
					try:
						carry_over[roll_no] = 0
						shutil.unpack_archive(
							filename=os.path.join(EXTRACT_DIR, stud_dir, file),
							extract_dir=EXTRACT_DIR
						)
						shutil.move(
							src=os.path.join(EXTRACT_DIR, file.split('.')[0]),
							dst=os.path.join(EXTRACT_DIR, roll_no)
						)
					except:
						print('Name: %s, Roll no.: %s, error in unpacking/moving' % \
							(stud_dir.split('_')[0], roll_no))
				break
		shutil.rmtree(os.path.join(EXTRACT_DIR, stud_dir))

	# Write submission status to TSV
	# By default assumes wrong submission name as no submission
	# In such a case, manually change this TSV later
	with open('submission_status.tsv', 'w') as f:
		f.write('ID\tCarry Over\tWrong Submission\n')
		for r in my_roll_numbers:
			f.write('%s\t%d\t%d\n' % (r, carry_over[r], 0))
