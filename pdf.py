import sys
from pathlib import Path
from subprocess import call

# pdf2txt.py のパス
py_path = Path(sys.exec_prefix) / "Scripts" / "pdf2txt.py"

# pdf2txt.py の呼び出し
call(["py", str(py_path), "-o extract-sample.txt", "-p 1", "sample.pdf"])
