"""Cliente da automação do FigCraft (2ª instância com --control). Uso: python3 fcctl.py <cmd> [json]"""
import json, socket, subprocess, sys, time, os
PORT = int(os.environ.get("FC_PORT", "47611"))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # pdv/design/figcraft: gerador + arquivo final
_id = 0
def launch(path=None):
    args = ["open", "-n", "-a", "FigCraft", "--args", "--control", str(PORT),
            "--automation-read-root", ROOT, "--automation-write-root", ROOT]
    if path: args.append(path)
    subprocess.run(args, check=True)
    for _ in range(60):
        try:
            socket.create_connection(("127.0.0.1", PORT), timeout=1).close(); return True
        except OSError: time.sleep(0.5)
    raise SystemExit("FigCraft não abriu a porta de controle")
class Conn:
    def __init__(self):
        self.s = socket.create_connection(("127.0.0.1", PORT), timeout=120); self.f = self.s.makefile("rwb"); self.i = 0
    def call(self, method, params=None):
        self.i += 1
        self.f.write((json.dumps({"id": self.i, "method": method, "params": params or {}}) + "\n").encode()); self.f.flush()
        while True:
            line = self.f.readline()
            if not line: raise SystemExit("conexão fechada")
            r = json.loads(line)
            if r.get("id") == self.i: return r
    def ex(self, command, params=None):
        return self.call("engine.execute", {"command": command, "params": params or {}})
if __name__ == "__main__":
    c = Conn()
    if sys.argv[1] in ("engine", "ex"):
        print(json.dumps(c.ex(sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}), ensure_ascii=False)[:4000])
    else:
        print(json.dumps(c.call(sys.argv[1], json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}), ensure_ascii=False)[:4000])
