
import sys, os
sys.path.append("buildtools")
import cpype

execName = "program"
buildDir = "build"

env = Environment(CXXFLAGS="-std=c++14")
env.VariantDir(buildDir, 'src')

sourceNodes = Glob(os.path.join('src', '*.cpy'))

cpypec = Builder(action = cpype.translate, suffix=".lzz", src_suffix=".pyc")

env.Append(BUILDERS = {'CPype' : cpypec})

lzzc = Builder(action = os.path.join('buildtools', 'lzz') + ' -c $SOURCE')
env.Append(BUILDERS = {'Lzz' : lzzc})

cppList = []

Command(os.path.join(buildDir, "cpype.h"), os.path.join("buildtools", "cpype.h"), Copy("$TARGET", "$SOURCE"))

for node in sourceNodes:
	fname = str(node).replace("src", buildDir, 1)[:-4] # src/fname.lzz -> build/fname
	env.CPype(fname + '.lzz', fname + '.cpy')
	env.Lzz([fname + '.h', fname + '.cpp'], fname + '.lzz')
	cppList.append(fname + '.cpp')

env.Program(execName, cppList)
