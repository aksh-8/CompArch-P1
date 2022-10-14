#######################################################################
# Authors
# Akash Biswal (axb200166)
# Mayank Kumar Singhal (mks200001)
#######################################################################

import os
import subprocess
import itertools

#add folder name to this and save those stats.txt etc int that folder
rootoutput = '/home/011/a/ax/axb200166/Desktop/Akash/CompArch/Outputs_458'
testoutput = '/home/011/a/ax/axb200166/Desktop/Akash/CompArch/Test'

#BranchPredictor.py file path var
BPtype = '/home/011/a/ax/axb200166/Desktop/Akash/CompArch/gem5/src/cpu/pred/BranchPredictor.py'
BPtemplate = '/home/011/a/ax/axb200166/Desktop/Akash/CompArch/Auto1/BPpytemplate.py'

#BaseSimpleCPU.py file path var
CPUtype = '/home/011/a/ax/axb200166/Desktop/Akash/CompArch/gem5/src/cpu/simple/BaseSimpleCPU.py'
CPUtemplate = '/home/011/a/ax/axb200166/Desktop/Akash/CompArch/Auto1/CPUtypetemplate.py'

#shell script paths
runG52 = '/home/011/a/ax/axb200166/m5out/benchmarks/458.sjeng/runGem5.sh'
runG5template2 = '/home/011/a/ax/axb200166/Desktop/Akash/CompArch/Auto1/runGem5temp2.sh'

#the scons command to rebuild
sconspath = 'build/X86/gem5.opt'


# lists of all diffrent configurations
BTBentries = [2048, 4096]
LBPlpsize = TBPlpsize = [1024, 2048]
BMBPgpsize = BMBPcpsize = [2048, 8192]
TBPgpsize = TBPcpsize = [4096, 8192]


# scons is already built for localBP, need to rebuild only for bimode and tourney...
# stored files as templates, edit templates and then write to og location

#function to rewrite the shell script
def rewriteshell(loc2):
	
	#edit the shell script of 458.sjeng before running subprocess
	f2 = open(runG5template2, "r")
	lines = f2.readlines()
	f2.close()
	f2 = open(runG52, "w")
	for line in lines:
		if('~/m5out' in line):
			line = line.replace('~/m5out', loc2)
		f2.write(line)
	f2.close()


# function to run the LocalBP for all possible BTB entries and LBPlpsize values
def runlocalBP():

	#change the Branch Predictor type
	f3 = open(CPUtemplate, "r")
	lines = f3.readlines()
	f3.close()
	f3 = open(CPUtype, "w")
	for line in lines:
		if('BPtype' in line):
			line = line.replace('BPtype', 'LocalBP()')
		f3.write(line)
	f3.close()

	#dont have to run scons here because the CPU is already built with localBP()
	l = [BTBentries, LBPlpsize]
	combos = list(itertools.product(*l))
	for c in combos:

		tempfolder2 = '/458LocalBP' + str(c[0]) + '_' + str(c[1]) + '/'
		outloc2 = rootoutput + tempfolder2
		

		#changing the BP sizes and parameters here
		#open the template
		f1 = open(BPtemplate, "r")
		lines = f1.readlines()
		f1.close()
		f1 = open(BPtype,'w')
		for line in lines:
			if('PH1' in line):
				line = line.replace('PH1', str(c[0]))
			if('PH2' in line):
				line = line.replace('PH2', str(c[1]))
			if('PH3' in line):
				line = line.replace('PH3', str(BMBPgpsize[0]))
			if('PH4' in line):
				line = line.replace('PH4', str(BMBPcpsize[0]))
			if('PH5' in line):
				line = line.replace('PH5', str(TBPlpsize[0]))
			if('PH6' in line):
				line = line.replace('PH6', str(TBPgpsize[0]))
			if('PH7' in line):
				line = line.replace('PH7', str(TBPcpsize[0]))
			f1.write(line)
		f1.close()

		#call to rewrite the shell script o/p path
		rewriteshell(outloc2)
		
		#call scons for every change
		subprocess.call(['scons', sconspath], cwd="/home/011/a/ax/axb200166/Desktop/Akash/CompArch/gem5")

		#subprocess call to run shell script
		subprocess.call(['sh', runG52], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		print("Completed iteration of " + tempfolder2)

		
						
def runbimodeBP():

	#change the Branch Predictor type
	f3 = open(CPUtemplate, "r")
	lines = f3.readlines()
	f3.close()
	f3 = open(CPUtype, "w")
	for line in lines:
		if('BPtype' in line):
			line = line.replace('BPtype', 'BiModeBP()')
		f3.write(line)
	f3.close()

	

	#once scons is rebuilt start the iterations
	l = [BTBentries, BMBPgpsize, BMBPcpsize]
	combos = list(itertools.product(*l))
	for c in combos:

		#creating specific output folders for each iteration
		tempfolder2 = '/458BiModeBP' + str(c[0]) + '_' + str(c[1]) + '_' + str(c[2]) + '/'
		outloc2 = rootoutput + tempfolder2


		#changing the BP sizes and parameters here
		#open the template
		f1 = open(BPtemplate, "r")
		lines = f1.readlines()
		f1.close()
		f1 = open(BPtype,'w')
		for line in lines:
			if('PH1' in line):
				line = line.replace('PH1', str(c[0]))
			if('PH2' in line):
				line = line.replace('PH2', str(LBPlpsize[0]))
			if('PH3' in line):
				line = line.replace('PH3', str(c[1]))
			if('PH4' in line):
				line = line.replace('PH4', str(c[2]))
			if('PH5' in line):
				line = line.replace('PH5', str(TBPlpsize[0]))
			if('PH6' in line):
				line = line.replace('PH6', str(TBPgpsize[0]))
			if('PH7' in line):
				line = line.replace('PH7', str(TBPcpsize[0]))
			f1.write(line)
		f1.close()

		#call scons for every change
		subprocess.call(['scons', sconspath], cwd="/home/011/a/ax/axb200166/Desktop/Akash/CompArch/gem5")

		#call to rewrite the shell script o/p path
		rewriteshell(outloc2)

		#subprocess call to run shell script
		subprocess.call(['sh', runG52], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		print("Completed iteration of " + tempfolder2)



def runtourneyBP():

	#change the Branch Predictor type
	f3 = open(CPUtemplate, "r")
	lines = f3.readlines()
	f3.close()
	f3 = open(CPUtype, "w")
	for line in lines:
		if('BPtype' in line):
			line = line.replace('BPtype', 'TournamentBP()')
		f3.write(line)
	f3.close()


	#once scons is rebuilt start the iterations
	l = [BTBentries, TBPlpsize, TBPgpsize, TBPcpsize]
	combos = list(itertools.product(*l))
	for c in combos:

		tempfolder2 = '/458TourneyBP' + str(c[0]) + '_' + str(c[1]) + '_' + str(c[2]) + '_' + str(c[3]) + '/'
		outloc2 = rootoutput + tempfolder2

		#changing the BP sizes and parameters here
		#open the template
		f1 = open(BPtemplate, "r")
		lines = f1.readlines()
		f1.close()
		f1 = open(BPtype,'w')
		for line in lines:
			if('PH1' in line):
				line = line.replace('PH1', str(c[0]))
			if('PH2' in line):
				line = line.replace('PH2', str(LBPlpsize[0]))
			if('PH3' in line):
				line = line.replace('PH3', str(BMBPgpsize[0]))
			if('PH4' in line):
				line = line.replace('PH4', str(BMBPcpsize[0]))
			if('PH5' in line):
				line = line.replace('PH5', str(c[1]))
			if('PH6' in line):
				line = line.replace('PH6', str(c[2]))
			if('PH7' in line):
				line = line.replace('PH7', str(c[3]))
			f1.write(line)
		f1.close()

		#call function to rewrite the shell scripts
		rewriteshell(outloc2)

		#call scons for every change
		subprocess.call(['scons', sconspath], cwd="/home/011/a/ax/axb200166/Desktop/Akash/CompArch/gem5")

		#subprocess call to run shell script
		subprocess.call(['sh', runG52], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		print("Completed iteration of " + tempfolder2)



if __name__ == '__main__':
	print("##############################Starting the Automation#########################")
	print("------------------------------------------------------------------------------")

	print("Running the LocalBP for all configurations on both the benchmarks")
	print("------------------------------------------------------------------------------")
	runlocalBP()

	print("Running the BiModeBP for all configurations on both the benchmarks")
	print("------------------------------------------------------------------------------")
	runbimodeBP()

	print("Running the TournamentBP for all configurations on both the benchmarks")
	print("------------------------------------------------------------------------------")
	runtourneyBP()

	print("###########################All Simulations completed##########################")

