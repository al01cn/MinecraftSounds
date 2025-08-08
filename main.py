from core.minecraft.main import *
from core.minecraft.projectPath import *
from core.project import *
from core.sounds import *

if __name__ == '__main__':
    test = Project("test")
    if not path.exists(test.path):
        test.create()
    else:
        test.autoCreateSound()
        test.build()
