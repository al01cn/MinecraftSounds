from core.minecraft.main import *
from core.minecraft.projectPath import *
from core.project import *
from core.sounds import *

if __name__ == '__main__':
    mcpath = ProjectPath("test")
    test = Project("test")
    sound = Sounds("test")
    if not path.exists(mcpath.project_path):
        test.create()
    else:
        test.autoCreateSound()
        test.build()
