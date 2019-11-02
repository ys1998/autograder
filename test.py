import subprocess

def grade1():
	# d1
	m = 0
	r = subprocess.run('python dataClassifier.py -d d1 -c mira -i 5 -a', 
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)
	if r.returncode != 0:
		print(r.stderr.decode('utf-8'))
	else:
		try:
			x = r.stdout.decode('utf-8').split()
			best_c = float(x[0])
			acc = float(x[1])
			print('acc', acc)
			if best_c == 0.005:
				m += 0.5
				print('best C correct')
			if acc >= 75:
				m += 1
			elif acc >= 65:
				m += 0.75
			elif acc >= 55:
				m += 0.5
		except:
			pass
	return m

def grade2():
	# d2
	n = 0
	r = subprocess.run('python dataClassifier.py -d d2 -c mira -i 1 -a', 
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)
	if r.returncode != 0:
		print(r.stderr.decode('utf-8'))
	else:
		try:
			x = r.stdout.decode('utf-8').split()
			best_c = float(x[0])
			acc = float(x[1])
			print('acc', acc)
			if best_c == 0.003:
				n += 0.5
				print('best C correct')
			if acc >= 95:
				n += 1
			elif acc >= 85:
				n += 0.75
			elif acc >= 75:
				n += 0.5
		except:
			pass
	return n

if __name__ == '__main__':	
	# print(grade1()+grade2())
	# m = grade1()
	m = grade2()
	print(m)