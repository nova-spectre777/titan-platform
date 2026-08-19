from pathlib import Path
import compileall,sys,subprocess
root=Path(__file__).resolve().parents[1]
print("TITAN repository check")
print("python files:",len(list(root.rglob("*.py"))))
print("total files:",len([p for p in root.rglob("*") if p.is_file()]))
ok=compileall.compile_dir(root/"titan",quiet=1) and compileall.compile_dir(root/"tests",quiet=1)
print("compile:","ok" if ok else "failed")
if not ok: sys.exit(1)
res=subprocess.run([sys.executable,"-m","unittest","discover","-s",str(root/"tests"),"-p","test_*.py"],cwd=root)
sys.exit(res.returncode)
