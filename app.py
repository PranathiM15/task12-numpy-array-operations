from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import numpy as np

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8000"))
ROOT = os.path.dirname(os.path.abspath(__file__))

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ARRAY / LAB — NumPy Operations</title>
<style>
:root{--ink:#17212b;--paper:#f4f1e9;--card:#fffdf8;--orange:#ff6b35;--teal:#0d7774;--line:#d9d4c9;--muted:#68737d}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif}
header{background:var(--ink);color:#fff;padding:18px max(22px,calc((100% - 1120px)/2));display:flex;justify-content:space-between;align-items:center;gap:20px}
.brand{font-weight:900;letter-spacing:.14em;font-size:15px}.brand span{color:#ff9a70}.topnote{font-size:12px;color:#cbd4d8;letter-spacing:.08em}
main{max-width:1120px;margin:34px auto;padding:0 22px}.eyebrow{font-size:12px;letter-spacing:.16em;font-weight:800;color:var(--teal);text-transform:uppercase}
h1{font-size:clamp(34px,6vw,66px);line-height:.98;letter-spacing:-.055em;margin:12px 0 14px;max-width:780px}
.intro{color:var(--muted);max-width:650px;line-height:1.65;margin-bottom:28px}
.layout{display:grid;grid-template-columns: minmax(0,1.1fr) minmax(300px,.9fr);gap:18px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px;box-shadow:0 8px 24px #17212b08}
.panel h2{font-size:16px;margin:0 0 18px;letter-spacing:-.02em}.inputgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
label{display:block;font-size:12px;font-weight:800;color:var(--muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:.08em}
input,select{width:100%;border:1px solid var(--line);background:#fff;border-radius:10px;padding:13px 12px;font:inherit;color:var(--ink);outline-color:var(--teal)}
.full{grid-column:1/-1}.actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
button{border:0;border-radius:10px;padding:12px 16px;background:var(--ink);color:white;font-weight:800;cursor:pointer}
button.secondary{background:#e7e2d7;color:var(--ink)}button:hover{transform:translateY(-1px)}
.resulthead{display:flex;justify-content:space-between;align-items:center;gap:10px}.pill{background:#d9eeea;color:#0d625f;padding:6px 9px;border-radius:99px;font-size:11px;font-weight:900}
.arraybox{background:#17212b;color:#eaf3f2;border-radius:12px;padding:14px;margin:10px 0 14px;font:13px/1.8 ui-monospace,SFMono-Regular,Consolas,monospace;overflow-wrap:anywhere}
.opgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.op{border:1px solid var(--line);border-radius:12px;padding:12px;min-width:0}.opname{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);font-weight:900}.opvalue{font:13px/1.7 ui-monospace,monospace;margin-top:8px;overflow-wrap:anywhere}
.note{font-size:12px;color:var(--muted);line-height:1.6;margin-top:16px}.status{min-height:20px;font-size:13px;color:#b33a21;margin-top:12px}
.bottom{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px}.mini{padding:17px;border-top:3px solid var(--orange);background:#ebe6dc;border-radius:10px}.mini b{display:block;margin-bottom:6px}.mini p{font-size:12px;color:var(--muted);line-height:1.55;margin:0}
footer{max-width:1120px;margin:28px auto 36px;padding:0 22px;color:var(--muted);font-size:12px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
@media(max-width:760px){.layout{grid-template-columns:1fr}.bottom{grid-template-columns:1fr}.inputgrid{grid-template-columns:1fr}.full{grid-column:auto}header{padding:16px 22px}}
</style></head>
<body>
<header><div class="brand">ARRAY <span>/</span> LAB</div><div class="topnote">TASK 12 · PYTHON + NUMPY</div></header>
<main>
<div class="eyebrow">Interactive numerical workbench</div>
<h1>Two arrays.<br>Four operations.</h1>
<p class="intro">Explore NumPy vectorization by entering two numerical arrays. ARRAY / LAB calculates element-wise addition, subtraction, multiplication, and division, with shape validation built in.</p>
<div class="layout">
<section class="panel">
<h2>01 / Define your arrays</h2>
<div class="inputgrid">
<div class="full"><label for="a">Array A · comma-separated numbers</label><input id="a" value="12, 24, 36, 48" autocomplete="off"></div>
<div class="full"><label for="b">Array B · same number of values</label><input id="b" value="3, 6, 9, 12" autocomplete="off"></div>
<div><label for="precision">Decimal precision</label><select id="precision"><option value="2">2 decimal places</option><option value="0">Whole numbers</option><option value="4">4 decimal places</option><option value="6">6 decimal places</option></select></div>
<div><label for="preset">Try a sample</label><select id="preset"><option value="">Choose sample…</option><option value="basic">Basic integers</option><option value="decimal">Decimal values</option><option value="negative">Negative values</option><option value="zero">Division by zero</option></select></div>
</div>
<div class="actions"><button id="run">Run calculations ↗</button><button class="secondary" id="reset">Reset sample</button></div>
<div class="status" id="status" role="status"></div>
<p class="note">Arrays must be one-dimensional and have equal lengths. Division by zero is shown as “undefined” instead of crashing the calculation.</p>
</section>
<section class="panel">
<div class="resulthead"><h2>02 / Results console</h2><span class="pill" id="shape">SHAPE (4,)</span></div>
<div class="arraybox" id="arrays">A = [12, 24, 36, 48]<br>B = [3, 6, 9, 12]</div>
<div class="opgrid">
<div class="op"><div class="opname">A + B · Addition</div><div class="opvalue" id="add">[15, 30, 45, 60]</div></div>
<div class="op"><div class="opname">A − B · Subtraction</div><div class="opvalue" id="sub">[9, 18, 27, 36]</div></div>
<div class="op"><div class="opname">A × B · Multiplication</div><div class="opvalue" id="mul">[36, 144, 324, 576]</div></div>
<div class="op"><div class="opname">A ÷ B · Division</div><div class="opvalue" id="div">[4, 4, 4, 4]</div></div>
</div>
<p class="note" id="explain">NumPy performs each operation element by element. Matching shapes allow direct vectorized arithmetic without a Python loop.</p>
</section>
</div>
<div class="bottom">
<div class="mini"><b>Vectorization</b><p>One array expression applies an operation to every corresponding pair of elements.</p></div>
<div class="mini"><b>Shape matters</b><p>These operations require arrays with matching lengths for this exercise.</p></div>
<div class="mini"><b>NumPy engine</b><p>Calculations run in Python with NumPy on the server, not in a notebook.</p></div>
</div>
</main>
<footer><span>ARRAY / LAB · TASK 12</span><span>Built with Python standard library + NumPy</span></footer>
<script>
const $=id=>document.getElementById(id);
const defaults={a:"12, 24, 36, 48",b:"3, 6, 9, 12"};
$("preset").addEventListener("change",()=>{
 const p=$("preset").value;
 if(p==="basic"){ $("a").value="12, 24, 36, 48";$("b").value="3, 6, 9, 12";}
 if(p==="decimal"){ $("a").value="1.5, 2.75, 8.2";$("b").value="0.5, 1.25, 2";}
 if(p==="negative"){ $("a").value="-5, 10, -15";$("b").value="2, -4, 3";}
 if(p==="zero"){ $("a").value="10, 20, 30";$("b").value="2, 0, 5";}
});
$("reset").addEventListener("click",()=>{$("a").value=defaults.a;$("b").value=defaults.b;$("precision").value="2";$("preset").value="";calculate();});
function pretty(v){return "["+v.map(x=>x===null?"undefined":String(x)).join(", ")+"]";}
async function calculate(){
 $("status").textContent="";
 try{
  const r=await fetch("/api/calculate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({a:$("a").value,b:$("b").value,precision:Number($("precision").value)})});
  const d=await r.json(); if(!r.ok) throw new Error(d.error||"Calculation failed");
  $("arrays").innerHTML="A = "+pretty(d.a)+"<br>B = "+pretty(d.b);
  ["add","sub","mul","div"].forEach(k=>$(k).textContent=pretty(d.results[k]));
  $("shape").textContent="SHAPE ("+d.a.length+",)";
  $("explain").textContent="NumPy arrays with shape ("+d.a.length+",) were processed using vectorized operations. Each output element corresponds to the same index in A and B.";
 }catch(e){$("status").textContent=e.message;}
}
$("run").addEventListener("click",calculate);
calculate();
</script></body></html>"""

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, content, content_type="application/json; charset=utf-8"):
        body = content.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html; charset=utf-8")
        elif self.path == "/health":
            self._send(200, json.dumps({"status": "ok", "engine": "NumPy"}))
        else:
            self._send(404, json.dumps({"error": "Not found"}))

    def do_POST(self):
        if self.path != "/api/calculate":
            return self._send(404, json.dumps({"error": "Not found"}))
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 100_000:
                raise ValueError("Input is too large.")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            def parse(key):
                raw = payload.get(key, "")
                if isinstance(raw, list):
                    vals = raw
                elif isinstance(raw, str):
                    vals = [x.strip() for x in raw.split(",") if x.strip()]
                else:
                    raise ValueError(f"Array {key.upper()} must be comma-separated numbers.")
                if not vals:
                    raise ValueError(f"Array {key.upper()} cannot be empty.")
                try:
                    arr = np.array(vals, dtype=float)
                except (TypeError, ValueError):
                    raise ValueError(f"Array {key.upper()} contains a non-numeric value.")
                if arr.ndim != 1 or not np.all(np.isfinite(arr)):
                    raise ValueError(f"Array {key.upper()} must contain finite numbers.")
                return arr
            a, b = parse("a"), parse("b")
            if a.shape != b.shape:
                raise ValueError("Array A and Array B must have the same number of values.")
            precision = int(payload.get("precision", 2))
            if precision not in (0, 2, 4, 6):
                precision = 2
            with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
                operations = {"add": np.add(a,b), "sub": np.subtract(a,b), "mul": np.multiply(a,b), "div": np.divide(a,b)}
            def clean(arr):
                out=[]
                for value in arr:
                    if not np.isfinite(value):
                        out.append(None)
                    else:
                        n=round(float(value), precision)
                        out.append(int(n) if precision == 0 and n.is_integer() else n)
                return out
            result={"a":clean(a),"b":clean(b),"results":{k:clean(v) for k,v in operations.items()}}
            self._send(200, json.dumps(result, allow_nan=False))
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self._send(400, json.dumps({"error": str(exc)}))
        except Exception:
            self._send(500, json.dumps({"error": "Unexpected server error. Check the terminal for details."}))

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)
    print(f"ARRAY / LAB is running at http://127.0.0.1:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nServer stopped.")
    finally:
        server.server_close()
