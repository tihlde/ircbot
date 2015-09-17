__author__ = 'haraldfw'

codeDeclerations = ""
codeSetupStart = "void setup() {"
codeSetup = ""
codeSetupEnd = "}"
codeLoopStart = "void loop() {"
codeLoop = ""
codeLoopEnd = ""

from subprocess import call

def compileAndUpload(beers):
    code = codeDeclerations + codeSetupStart + codeSetup + codeSetupEnd + codeLoopStart + codeLoop + codeLoopEnd;
    call("")