// Cloudflare Worker: proxy aliasnet/aci via GitHub raw (canonical) with Cloudflare fallback.
// Only GET/HEAD, safe path, predictable MIME, simple caching.

export default {
  async fetch(request) {
    const url = new URL(request.url);

    // Allow only safe methods
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", { status: 405 });
    }

    // Normalize and sanitize path; default to README.md
    let path = decodeURIComponent(url.pathname || "/");
    if (!path || path === "/") path = "/README.md";
    path = "/" + path.split("/").filter(Boolean).join("/");

    const qs = url.search || "";

    // Upstreams
    const primary = `https://raw.githubusercontent.com/aliasnet/aci/main${path}${qs}`;
    const fallback = `https://aci.aliasmail.cc${path}${qs}`;

    // MIME map
    const MIME = {
      ".json": "application/json; charset=utf-8",
      ".md":   "text/markdown; charset=utf-8",
      ".txt":  "text/plain; charset=utf-8",
      ".html": "text/html; charset=utf-8",
      ".css":  "text/css; charset=utf-8",
      ".js":   "text/javascript; charset=utf-8",
      ".svg":  "image/svg+xml",
      ".png":  "image/png",
      ".jpg":  "image/jpeg",
      ".jpeg": "image/jpeg",
      ".gif":  "image/gif",
      ".wasm": "application/wasm"
    };
    const ext = (path.match(/\.[^/.]+$/)?.[0] || "").toLowerCase();
    const contentType = MIME[ext] || "application/octet-stream";

    // Helper: fetch with timeout
    const fetchWithTimeout = async (u, ms = 12000) => {
      try {
        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), ms);
        const res = await fetch(u, { signal: ctrl.signal });
        clearTimeout(tid);
        return res;
      } catch {
        return null;
      }
    };

    // Try canonical first, then fallback
    let upstream = await fetchWithTimeout(primary);
    if (!upstream || upstream.status === 404 || upstream.status === 403) {
      upstream = await fetchWithTimeout(fallback);
    }

    if (!upstream) {
      return new Response(JSON.stringify({ error: "Upstream fetch failed" }), {
        status: 502,
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Cache-Control": "public, max-age=60",
          "Access-Control-Allow-Origin": "*"
        }
      });
    }

    if (upstream.status === 404) {
      return new Response("Not found", {
        status: 404,
        headers: { "Access-Control-Allow-Origin": "*" }
      });
    }

    // Build outgoing headers
    const headers = new Headers(upstream.headers);
    headers.set("Content-Type", contentType);
    headers.delete("Set-Cookie");
    headers.set("Cache-Control", "public, max-age=3600, stale-while-revalidate=60");
    headers.set("Access-Control-Allow-Origin", "*");
    headers.set("Referrer-Policy", "no-referrer");
    headers.set("X-Proxy-Source", upstream.url);

    return new Response(upstream.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers
    });
  }
};
