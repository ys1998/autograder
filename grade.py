"""
Autograding script. 
- Should be run from the evaluation directory. 
- All statistics will be dumped there.
"""

import os
import shutil
import subprocess
import glob

ROLL_LIST = 'roll_list.txt'          # List of students to grade
SRC_DIR   = 'my_batch'                   # Locations of student submissions

###############################################################################
#                          Question specific details                          #
###############################################################################

# Name of the question(s) to be evaluated
QUESTIONS = ['Q6a', 'Q6b']

# Name of file(s) to be copied from the students directory to ours for 
# evaluation. Should be a list of strings for each question. Wildcard (*)
# entries supported. Eg. '*.pdf', '*.txt', etc.
#
# CAUTION: Don't use wildcard for the extensions of files important for testing
#          Example, *.py. This is because an intermediate _remove_files step 
#          will delete all files matching the wildcard, that might include some
#          important files too.
#
FILES = [['*.pdf'], ['*.pdf']]

# Commmand to be executed, one for each question. The command should terminate 
# after printing just the marks obtained, if AUTOGRADE = True for that question.
COMMANDS = ['xdg-open *.pdf', 'xdg-open *.pdf']

# Whether to automatically grade the question, or prompt the examiner to enter 
# marks manually.
AUTOGRADE = [False, False]

# Allowed imports for the files. Should be a list of the same length as FILES, 
# with elements as list of list of allowed imports for those questions' files.
ALLOWED_IMPORTS = [
	[
		# ['import numpy as np', 'from utils import *']
		[]
	],
	[
		[]
	]
]

# Whether to do question-wise (useful for automatic evaluation) or student-wise
# (useful for manual evaluation)
ORDER = 'student'

###############################################################################
############################ DO NOT EDIT BELOW ################################
###############################################################################

# Check that arguments above are filled correctly.
assert len(QUESTIONS) == len(FILES)
assert len(QUESTIONS) == len(COMMANDS)
assert len(QUESTIONS) == len(AUTOGRADE)
assert len(QUESTIONS) == len(ALLOWED_IMPORTS)
assert all([len(f) == len(i) for f,i in zip(FILES, ALLOWED_IMPORTS)])
assert ORDER in ['question', 'student']

###############################################################################
#                             Helper functions                                #
###############################################################################

def _check_imports(filename, imports):
	if not imports:
		return True
	with open(filename, 'r') as f:
		lines = f.readlines()
		lines = [l.strip() for l in lines]
		for l in lines:
			toks = l.split()
			if len(toks) > 0 and toks[0] != '#' and toks[0] != '"""':
				if 'import' in toks and l not in imports:
					return False
		return True

def _execute(command, autograde=True):
	try:
		result = subprocess.run(
			command,
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)
		if result.returncode == 0 and autograde:
			return float(result.stdout.decode('utf-8')), 'NA'
		elif result.returncode == 0 and not autograde:
			return 0., 'NA'
		else:
			return 0., result.stderr.decode('utf-8').strip().split('\n')[-1]
	except:
		return 0., 'execution error'

def _copy_files(src_dir, dest_dir, files):
	try:
		for f in files:
			for f_ in glob.glob(os.path.join(src_dir, f)):
				shutil.copy(f_, dest_dir)
		return True
	except:
		return False

def _remove_files(files):
	try:
		for f in files:
			for f_ in glob.glob(f):
				os.remove(f_)
		return True
	except:
		return False

###############################################################################
#                                Start grading                                #
###############################################################################

if __name__ == '__main__':
	# Read roll numbers to grade
	with open(ROLL_LIST, 'r') as f:
		my_roll_numbers = f.read().split()

	# Placeholder for question statistics
	qstats = {}
	for r in my_roll_numbers:
		qstats[r] = {}
		for q in QUESTIONS:
			qstats[r][q] = {'marks': 0, 'comments': 'NA'}

	# Evaluate
	if ORDER == 'question':
		for i, q in enumerate(QUESTIONS):
			for r in os.listdir(SRC_DIR):
				if r not in my_roll_numbers:
					continue
				evaluate = True
				if not _copy_files(os.path.join(SRC_DIR, r), '.', FILES[i]):
					qstats[r][q]['comments'] = 'file(s) missing'
					evaluate = False
					continue

				for j, f in enumerate(FILES[i]):
					if AUTOGRADE[i] and not _check_imports(FILES[i][j], ALLOWED_IMPORTS[i][j]):
						qstats[r][q]['comments'] = 'invalid import(s)'
						evaluate = False
						break

				if evaluate:
					m, c = _execute(COMMANDS[i], AUTOGRADE[i])
					if AUTOGRADE[i]:
						qstats[r][q]['marks'] = m
						qstats[r][q]['comments'] = c
					else:
						if c != 'NA':
							print('Error: %s' % c)
						print('Enter marks for [%s][%s]: ' % (r, q), end='')
						qstats[r][q]['marks'] = float(input())
						print('Enter comments for [%s][%s]: ' % (r, q), end='')
						qstats[r][q]['comments'] = input()
					_remove_files(FILES[i])
	else:
		for r in os.listdir(SRC_DIR):
			if r not in my_roll_numbers:
				continue
			for i, q in enumerate(QUESTIONS):
				evaluate = True
				if not _copy_files(os.path.join(SRC_DIR, r), '.', FILES[i]):
					qstats[r][q]['comments'] = 'file(s) missing'
					evaluate = False
					break

				for j, f in enumerate(FILES[i]):
					if AUTOGRADE[i] and not _check_imports(FILES[i][j], ALLOWED_IMPORTS[i][j]):
						qstats[r][q]['comments'] = 'invalid import(s)'
						evaluate = False
						break

				if evaluate:
					m, c = _execute(COMMANDS[i], AUTOGRADE[i])
					if AUTOGRADE[i]:
						qstats[r][q]['marks'] = m
						qstats[r][q]['comments'] = c
					else:
						if c != 'NA':
							print('Error: %s' % c)
						print('Enter marks for [%s][%s]: ' % (r, q), end='')
						qstats[r][q]['marks'] = float(input())
						print('Enter comments for [%s][%s]: ' % (r, q), end='')
						qstats[r][q]['comments'] = input()
					_remove_files(FILES[i])


	# Dump results to a tsv file
	with open('marks.tsv', 'w') as f:
		header = ['ID']
		header += QUESTIONS
		header += ['Comments']
		f.write('\t'.join(header) + '\n')
		
		for r in my_roll_numbers:
			line = [r]
			line += [str(qstats[r][q]['marks']) for q in QUESTIONS]
			line += [', '.join([qstats[r][q]['comments'] for q in QUESTIONS])]
			f.write('\t'.join(line) + '\n')