
execName = "program"
buildDir = "build"

env = Environment()
env.VariantDir(buildDir, 'src')

sourceNodes = Glob('src/*.cpy')

cpypec = Builder(action = '"C:\Program Files\Python36\python" buildtools\cpype.py $SOURCE $TARGET')
env.Append(BUILDERS = {'CPype' : cpypec})

lzzc = Builder(action = 'buildtools\lzz -c $SOURCE')
env.Append(BUILDERS = {'Lzz' : lzzc})

cppList = []

Command(buildDir + "/cpype.h", "buildtools/cpype.h", Copy("$TARGET", "$SOURCE"))

for node in sourceNodes:
	fname = str(node).replace("src", buildDir, 1)[:-4] # src/fname.lzz -> build/fname
	env.CPype(fname + '.lzz', fname + '.cpy')
	env.Lzz([fname + '.h', fname + '.cpp'], fname + '.lzz')
	cppList.append(fname + '.cpp')

env.Program(execName, cppList)