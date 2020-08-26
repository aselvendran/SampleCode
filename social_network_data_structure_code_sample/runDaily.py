import sys
import importlib

if __name__ == "__main__":
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    methodToRun = argument_list[0]
    tweetsFileName, termFileName, nodeFile, fileToSave = argument_list[1:]

    module_to_run = importlib.import_module("TermNodeMatch")
    class_to_run = getattr(module_to_run, "TweetMessageNodeMapping")
    theclass = class_to_run(

        *[tweetsFileName, termFileName, nodeFile, fileToSave]

    )

    runFunc = getattr(theclass, methodToRun)
    runFunc()
