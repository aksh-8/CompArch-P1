import os
import subprocess
import itertools

#add folder name to this and save those stats.txt etc int that folder
rootoutput = '/home/eng/m/mks200001/CAproj/Outputs_470'


#BranchPredictor.py file path var
BPtype = '/home/eng/m/mks200001/CAproj/gem5/src/cpu/pred/BranchPredictor.py'
BPtemplate = '/home/eng/m/mks200001/CAproj/Auto/BPpytemplate.py'

#BaseSimpleCPU.py file path var
CPUtype = '/home/eng/m/mks200001/CAproj/gem5/src/cpu/simple/BaseSimpleCPU.py'
CPUtemplate = '/home/eng/m/mks200001/CAproj/Auto/CPUtypetemplate.py'

#runGem5.sh script path var for both the benchmarks
runG51 = '/home/eng/m/mks200001/CAproj/benchmarks/470.lbm/runGem5.sh'
runG5template1 = '/home/eng/m/mks200001/CAproj/Auto/runGem5temp1.sh'


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
def rewriteshell(loc1):
	#edit the shell script of 470.lbm before running subprocess
	f2 = open(runG5template1, "r")
	lines = f2.readlines()
	f2.close()
	f2 = open(runG51, "w")
	for line in lines:
		if('~/m5out' in line):
			line = line.replace('~/m5out', loc1)
		f2.write(line)
	f2.close()

#function to fix the bug before running scons
def fixbug():
	f1 = open(BPtemplate, "r")
	lines = f1.readlines()
	f1.close()
	f1 = open(BPtype,'w')
	for line in lines:
		if('PH1' in line):
			line = line.replace('PH1', str(BTBentries[0]))
		if('PH2' in line):
			line = line.replace('PH2', str(LBPlpsize[0]))
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

# function to run the LocalBP for all possible BTB entries and LBPlpsize values
def runlocalBP():

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
		#for j in LBPlpsize:
		tempfolder1 = '/470LocalBP' + str(c[0]) + '_' + str(c[1]) + '/'
		outloc1 = rootoutput + tempfolder1
		
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
		rewriteshell(outloc1)

		#rebuild opt file using scons
		subprocess.call(['scons', sconspath], cwd="/home/eng/m/mks200001/CAproj/gem5")
	
		#subprocess call to run shell script
		subprocess.call(['sh', runG51], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		print("Completed iteration of " + tempfolder1)

					
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

		tempfolder1 = '/470BiModeBP' + str(c[0]) + '_' + str(c[1]) + '_' + str(c[2]) + '/'
		outloc1 = rootoutput + tempfolder1

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

		#call to rewrite the shell script o/p path
		rewriteshell(outloc1)

		#rebuild opt file using scons
		subprocess.call(['scons', sconspath], cwd="/home/eng/m/mks200001/CAproj/gem5")
		
		#subprocess call to run shell script
		subprocess.call(['sh', runG51], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		print("Completed iteration of " + tempfolder1)




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

	combos = [(4096, 1024, 4096, 4096), (2048, 2048, 4096, 4096)]

	for c in combos:

		tempfolder1 = '/470TourneyBP' + str(c[0]) + '_' + str(c[1]) + '_' + str(c[2]) + '_' + str(c[3]) + '/'
		outloc1 = rootoutput + tempfolder1

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
		rewriteshell(outloc1)

		#rebuild opt file using scons
		subprocess.call(['scons', sconspath], cwd="/home/eng/m/mks200001/CAproj/gem5")

		#subprocess call to run shell script
		subprocess.call(['sh', runG51], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		print("Completed iteration of " + tempfolder1)



if __name__ == '__main__':
	print("##############################Starting the Automation#########################")
	print("------------------------------------------------------------------------------")

	#print("Running the LocalBP for all configurations on both the benchmarks")
	#print("------------------------------------------------------------------------------")
	#runlocalBP()

	#print("Running the BiModeBP for all configurations on both the benchmarks")
	#print("------------------------------------------------------------------------------")
	#runbimodeBP()

	print("Running the TournamentBP for all configurations on both the benchmarks")
	print("------------------------------------------------------------------------------")
	runtourneyBP()

	print("###########################All Simulations completed##########################")

