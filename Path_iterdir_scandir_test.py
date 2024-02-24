from timeit import timeit
import tempfile
from pathlib import Path


def make_temp_path(PathClass):
    return PathClass(tempfile.gettempdir()) / PathClass(__file__).stem


class ScanDirPath(Path):
    def iterdir(self):
        return (self._make_child_direntry(entry) for entry in self._scandir())


tmp_iterdir_path = make_temp_path(Path)
tmp_scandir_path = make_temp_path(ScanDirPath)

tmp_iterdir_path.mkdir(exist_ok=True, parents=True)

N = 15_000

paths = []

# Create N files in TEST_DIR, 0.txt, ..., N.txt
for i in range(N):
    path = tmp_iterdir_path / f'{i}.txt'
    paths.append(path)
    path.touch()


print(f'Time using Path.iterdir: {timeit(lambda: list(tmp_iterdir_path.iterdir()), number = 4)}')
print(f'Time using Path.iterdir: {timeit(lambda: list(tmp_scandir_path.iterdir()), number = 10)}')





for path in paths:
    path.unlink()