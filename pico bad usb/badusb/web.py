import os
import ipaddress
import wifi
import socketpool


def _html_list(payloads, ip):
    rows = []
    for name in payloads:
        safe = name.replace("<", "").replace(">", "")
        rows.append(f'<li><a href="/run?name={safe}">Run {safe}</a></li>')
    items = "\n".join(rows) if rows else "<li>No payloads found</li>"
    return f"""<!DOCTYPE html>
<html>
<head><title>Pico W Payloads</title></head>
<body>
<h3>Pico W Payloads</h3>
<p>IP: {ip}</p>
<ul>{items}</ul>
</body>
</html>"""


def _list_payloads(directory):
    try:
        return [f for f in os.listdir(directory) if f.lower().endswith(".txt")]
    except Exception:
        return []


def start_ap(ssid, password):
    wifi.radio.start_ap(ssid=ssid, password=password)
    return str(ipaddress.IPv4Address(wifi.radio.ipv4_address_ap))


def serve(command, payload_dir="/payloads"):
    pool = socketpool.SocketPool(wifi.radio)
    server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    server.setsockopt(pool.SOL_SOCKET, pool.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 80))
    server.listen(1)

    while True:
        conn, _ = server.accept()
        request = conn.recv(1024).decode("utf-8", errors="ignore")
        if not request:
            conn.close()
            continue

        line = request.split("\r\n")[0]
        parts = line.split(" ")
        path = parts[1] if len(parts) > 1 else "/"

        if path.startswith("/run?name="):
            name = path.split("=", 1)[1].replace("+", " ")
            payload_path = f"{payload_dir}/{name}"
            try:
                command.execute(payload_path)
                body = f"Running {name}"
            except Exception as exc:
                body = f"Failed: {exc}"
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + body
        else:
            payloads = _list_payloads(payload_dir)
            ip = str(ipaddress.IPv4Address(wifi.radio.ipv4_address_ap))
            body = _html_list(payloads, ip)
            response = (
                "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + body
            )

        conn.send(response.encode("utf-8"))
        conn.close()
