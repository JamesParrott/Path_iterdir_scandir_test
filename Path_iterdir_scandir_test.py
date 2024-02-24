import os
import sys
from timeit import timeit
import tempfile
from pathlib import Path




def make_temp_path(PathClass):
    return PathClass(tempfile.gettempdir()) / PathClass(__file__).stem


class ScanDirPath(Path):
    def iterdir(self):
        return (self._make_child_direntry(entry) for entry in self._scandir())






def run_tests(N = 50_000, reps = 20):

    tmp_iterdir_path = make_temp_path(Path)
    tmp_scandir_path = make_temp_path(ScanDirPath)

    tmp_iterdir_path.mkdir(exist_ok=True, parents=True)

    paths = []

    # Create N files in tmp_iterdir_path, 0.txt, ..., N.txt
    for i in range(int(N)):
        path = tmp_iterdir_path / f'{i}.txt'
        paths.append(path)
        path.touch()

    print(f'Testing {reps=} of listing a directory of: {N} files')

    print(f'Time using Path.iterdir: {timeit(lambda: list(tmp_iterdir_path.iterdir()), number = reps)}')

    if sys.version_info >= (3, 13):
        print(f'Time using ScanDirPath.iterdir: {timeit(lambda: list(tmp_scandir_path.iterdir()), number = reps)}')
    else: 
        print("This test relies on implementation details of Python 3.13's pathlib, unavailable in earlier Pythons. ")

    print(f'Time using os.listdir: {timeit(lambda: os.listdir(), number = reps)}')
    print(f'Time using os.scandir: {timeit(lambda: [dir_entry.name for dir_entry in os.scandir()], number = reps)}')




    # Delete files (created earlier, used only for this test)
    for path in paths:
        path.unlink()


if __name__ == '__main__':
    int_args = [int(x) for x in sys.argv[1:3]]
    run_tests(*int_args)