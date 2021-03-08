import sys, os
import multiprocessing
import inotify.adapters
from colorama import Fore as textcol

def get_input_paths(args):
    if len(sys.argv) < 2:
        raise Exception("You must set folder path(s) as input argument(s).")
    else:
        folderpaths = []
        for i in range(1, len(args)):
            folder = args[i]
            if not os.path.exists(folder):
                raise Exception("'{}' not found".format(folder))
            elif not os.path.isdir(folder):
                raise Exception("'{}' is not a folder.".format(folder))
            else:
                folderpaths.append(folder)
        return folderpaths


def monitor_path(folderpath):
    i = inotify.adapters.InotifyTree(folderpath)

    while True:  # loop for rerunning try block on exceptions
        try:
            for event in i.event_gen(yield_nones=False):
                (_, type_names, path, filename) = event


                # FOLDER

                if len(type_names) == 2:

                    # created folder
                    if type_names[0] == 'IN_CREATE' and type_names[1] == 'IN_ISDIR':
                        print(f"{path}/{filename}", textcol.LIGHTBLACK_EX, "d", textcol.GREEN, "c", textcol.RESET)

                    # deleted folder
                    elif type_names[0] == 'IN_DELETE_SELF':
                        print(f"{path}", textcol.LIGHTBLACK_EX, "d", textcol.RED, "d", textcol.RESET)
                    elif type_names[0] == 'IN_DELETE' and type_names[1] == 'IN_ISDIR':
                        print(f"{path}/{filename}", textcol.LIGHTBLACK_EX, "d", textcol.RED, "d", textcol.RESET)



                # FILE

                elif len(type_names) == 1:

                    # created file
                    if type_names[0] == 'IN_CREATE':
                        print(f"{path}/{filename}", textcol.LIGHTBLACK_EX, "f", textcol.GREEN, "c", textcol.RESET)

                    # deleted file
                    elif type_names[0] == 'IN_DELETE':
                        print(f"{path}/{filename}", textcol.LIGHTBLACK_EX, "f", textcol.RED, "d", textcol.RESET)

                #  verbose info, uncomment to see all changes
                #print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
                #    path, filename, type_names))

        except inotify.calls.InotifyError as ne:
            print(f"err: {ne}")
            continue


def _main():

    folderpaths = get_input_paths(sys.argv)

    # start processes
    pool = multiprocessing.Pool(processes=len(folderpaths))
    pool.map(monitor_path,folderpaths)


if __name__ == '__main__':
    _main()
