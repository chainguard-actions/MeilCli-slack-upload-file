// Minimal local mock of the Slack Web API endpoints used by filesUploadV2.
// Usage: node mock-slack-server.js <port> [ok|error]
const http = require("http");
const fs = require("fs");

const port = parseInt(process.argv[2] || "8765", 10);
const mode = process.argv[3] || "ok";
const logFile = process.env.MOCK_LOG || "/tmp/mock-slack-requests.log";
let counter = 0;

function log(line) {
    fs.appendFileSync(logFile, line + "\n");
}

function sendJson(res, obj) {
    const body = JSON.stringify(obj);
    res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
    res.end(body);
}

const server = http.createServer((req, res) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
        const raw = Buffer.concat(chunks);
        const url = req.url || "";
        log(`${req.method} ${url} ${raw.length}`);

        if (url.startsWith("/health")) {
            res.writeHead(200);
            res.end("ok");
            return;
        }

        if (url.startsWith("/upload/")) {
            log(`UPLOAD_BODY ${url} ${raw.toString("utf8").replace(/\s+/g, " ").slice(0, 2000)}`);
            res.writeHead(200, { "Content-Type": "text/plain" });
            res.end("OK - " + raw.length);
            return;
        }

        if (mode === "error") {
            sendJson(res, { ok: false, error: "invalid_auth" });
            return;
        }

        let params = new URLSearchParams();
        const ct = req.headers["content-type"] || "";
        const text = raw.toString("utf8");
        if (ct.includes("application/json")) {
            try {
                const obj = JSON.parse(text);
                for (const k of Object.keys(obj)) {
                    params.set(k, typeof obj[k] === "string" ? obj[k] : JSON.stringify(obj[k]));
                }
            } catch (e) {}
        } else {
            params = new URLSearchParams(text);
        }
        const qIndex = url.indexOf("?");
        if (qIndex >= 0) {
            for (const [k, v] of new URLSearchParams(url.slice(qIndex + 1))) {
                params.set(k, v);
            }
        }
        log(`PARAMS ${url} ${JSON.stringify(Object.fromEntries(params))}`);

        if (url.includes("files.getUploadURLExternal")) {
            counter += 1;
            const id = `F00MOCK${counter}`;
            sendJson(res, {
                ok: true,
                upload_url: `http://127.0.0.1:${port}/upload/${id}`,
                file_id: id,
            });
            return;
        }

        if (url.includes("files.completeUploadExternal")) {
            let files = [];
            try {
                files = JSON.parse(params.get("files") || "[]");
            } catch (e) {}
            sendJson(res, {
                ok: true,
                files: files.map((f) => ({ id: f.id, title: f.title || "" })),
            });
            return;
        }

        if (url.includes("files.delete")) {
            sendJson(res, { ok: true });
            return;
        }

        sendJson(res, { ok: true });
    });
});

server.listen(port, "127.0.0.1", () => {
    log(`listening ${port} mode=${mode}`);
});
