// Minimal Cloudflare Worker: proxy aliasnet/aci via GitHub raw with jsDelivr fallback.
// Smart Placement is configured in wrangler.toml.

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", { status: 405 });
    }

    // Safe, normalized path; default to README.md at repo root.
    let path = decodeURIComponent(url.pathname || "/");
    if (!path || path === "/") path = "/README.md";
    path = "/" + path.split("/").filter(Boolean).join("/");

    const qs = url.search || "";

    const upstreamPrimary = `https://raw.githubusercontent.com/aliasnet/aci/main${path}${qs}`;
    const upstreamFallback = `https://cdn.jsdelivr.net/gh/aliasnet/aci@main${path}${qs}`;

    const CACHE_TTL = Number(env?.CACHE_TTL ?? 3600);

    const MIME = {
      ".json": "application/json; charset=utf-8",
      ".md":   "text/markdown; charset=utf-8",
      ".txt":  "text/plain; charset=utf-8",
      ".html": "text/html; charset=utf-8",
      ".css":  "text/css; charset=utf-8",
      ".js":   "text/javascript; charset=utf-8", // HTML standard pref
      ".svg":  "image/svg+xml",
      ".png":  "image/png",
      ".jpg":  "image/jpeg",
      ".jpeg": "image/jpeg",
      ".gif":  "image/gif",
      ".wasm": "application/wasm"
    };

    const ext = (path.match(/\.[^/.]+$/)?.[0] || "").toLowerCase();
    const contentType = MIME[ext] || "application/octet-stream";

    const withTimeout = async (u, ms = 12000) => {
      try {
        const c = new AbortController();
        const t = setTimeout(() => c.abort(), ms);
        const r = await fetch(u, { signal: c.signal });
        clearTimeout(t);
        return r;
      } catch {
        return null;
      }
    };

    let resp = await withTimeout(upstreamPrimary);
    if (!resp || resp.status === 404 || resp.status === 403) {
      resp = await withTimeout(upstreamFallback);
    }

    if (!resp) {
      return new Response(
        JSON.stringify({ error: "Upstream fetch failed" }),
        {
          status: 502,
          headers: {
            "Content-Type": "application/json; charset=utf-8",
            "Cache-Control": "public, max-age=60",
            "Access-Control-Allow-Origin": "*"
          }
        }
      );
    }

    if (resp.status === 404) {
      return new Response("Not found", {
        status: 404,
        headers: { "Access-Control-Allow-Origin": "*" }
      });
    }

    const headers = new Headers(resp.headers);
    headers.set("Content-Type", contentType);
    headers.delete("Set-Cookie");
    headers.set("Cache-Control", `public, max-age=${CACHE_TTL}`);
    headers.set("Access-Control-Allow-Origin", "*");
    headers.set("Referrer-Policy", "no-referrer");
    headers.set("X-Proxy-Source", resp.url);

    return new Response(resp.body, { status: resp.status, statusText: resp.statusText, headers });
  }
};
