import sys
import json
from pathlib import Path
import traceback

sys.path.insert(0, str(Path(__file__).parent.parent))

from sipl.parser import parse_source
from sipl.interpreter.evaluator import SIPLInterpreter

LOG_FILE = Path(__file__).parent.parent.parent / "dap_debug.log"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

class DAPServer:
    def __init__(self):
        self.seq = 1
        self.trace = []
        self.current_step = 0
        self.breakpoints = []
        self.program_path = ""

    def send(self, msg):
        msg['seq'] = self.seq
        self.seq += 1
        body = json.dumps(msg).encode('utf-8')
        header = f"Content-Length: {len(body)}\r\n\r\n".encode('utf-8')
        sys.stdout.buffer.write(header + body)
        sys.stdout.buffer.flush()
        log(f"SENT: {msg}")

    def handle(self, req):
        log(f"RECV: {req}")
        cmd = req.get('command')
        args = req.get('arguments', {})
        req_seq = req['seq']

        if cmd == 'initialize':
            self.send({'type': 'response', 'request_seq': req_seq, 'success': True, 'command': cmd})
            self.send({'type': 'event', 'event': 'initialized'})
            
        elif cmd == 'launch':
            self.program_path = args['program']
            code = Path(self.program_path).read_text(encoding='utf-8')
            ast = parse_source(code)
            state = json.loads(args.get('state', '{}'))
            
            interpreter = SIPLInterpreter(state)
            interpreter.evaluate(ast)
            self.trace = interpreter.trace
            self.current_step = 0
            
            self.send({'type': 'response', 'request_seq': req_seq, 'success': True, 'command': cmd})
            self.send({'type': 'event', 'event': 'stopped', 'body': {'reason': 'entry', 'threadId': 1}})
            
        elif cmd == 'setBreakpoints':
            self.breakpoints = [b['line'] for b in args.get('breakpoints', [])]
            bps = [{'verified': True, 'line': l} for l in self.breakpoints]
            self.send({'type': 'response', 'request_seq': req_seq, 'success': True, 'command': cmd, 'body': {'breakpoints': bps}})
            
        elif cmd == 'threads':
            self.send({'type': 'response', 'request_seq': req_seq, 'success': True, 'command': cmd, 'body': {'threads': [{'id': 1, 'name': 'main'}]}})
            
        elif cmd == 'stackTrace':
            line = self.trace[self.current_step]['line'] if self.current_step < len(self.trace) else 1
            self.send({'type': 'response', 'request_seq': req_seq, 'success': True, 'command': cmd, 'body': {'stackFrames': [{'id': 1, 'name': 'main', 'line': line, 'column': 1, 'source': {'path': self.program_path}}]}})
            
        elif cmd == 'scopes':
            self.send({'type': 'response', 'request_seq': req_seq, 'success': True, 'command': cmd, 'body': {'scopes': [{'name': 'Local', 'variablesReference': 1, 'expensive': False}]}})
            
        elif cmd == 'variables':
            state = self.trace[self.current_step]['state'] if self.current_step < len(self.trace) else {}
            vars_list = [{'name': str(k), 'value': str(v), 'variablesReference': 0} for k, v in state.items()]
            self.send({'type': 'response', 'request_seq': req_seq, 'success': True, 'command': cmd, 'body': {'variables': vars_list}})
            
        elif cmd in ('continue', 'next'):
            self.current_step += 1
            if cmd == 'continue':
                while self.current_step < len(self.trace) and self.trace[self.current_step]['line'] not in self.breakpoints:
                    self.current_step += 1
                    
            if self.current_step < len(self.trace):
                self.send({'type': 'response', 'request_seq': req_seq, 'success': True, 'command': cmd})
                self.send({'type': 'event', 'event': 'stopped', 'body': {'reason': 'step', 'threadId': 1}})
            else:
                self.send({'type': 'response', 'request_seq': req_seq, 'success': True, 'command': cmd})
                self.send({'type': 'event', 'event': 'terminated'})
                
        elif cmd == 'disconnect':
            self.send({'type': 'response', 'request_seq': req_seq, 'success': True, 'command': cmd})
            sys.exit(0)

    def run(self):
        log("SERVER STARTED")
        while True:
            try:
                line = sys.stdin.buffer.readline()
                if not line:
                    break
                line = line.decode('utf-8')
                if line.startswith('Content-Length:'):
                    length = int(line.split(':')[1].strip())
                    sys.stdin.buffer.readline()
                    body = sys.stdin.buffer.read(length).decode('utf-8')
                    self.handle(json.loads(body))
            except Exception as e:
                log(f"ERROR: {traceback.format_exc()}")
                break

if __name__ == '__main__':
    DAPServer().run()