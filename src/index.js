// ACI GitHub Raw Proxy 

// Defaults (can be overridden via Worker Variables)
const DEFAULT_TTL = 300;   // 5 min
const RELAXED_TTL = 1800;  // 30 min

export default {
  async fetch(request, env, ctx) {
    const url     = new URL(request.url);
    const method  = request.method.toUpperCase();
    const ua      = request.headers.get("user-agent") || "";
    const cf      = request.cf || {};
    const asn     = (cf.asn ?? cf.clientAsn ?? cf.clientASNumber ?? "").toString();

    if (method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: buildCorsHeaders(request)
      });
    }

    const wantsHead = method === "HEAD";

    if (method !== "GET" && !wantsHead) {
      return new Response("Method Not Allowed", {
        status: 405,
        headers: buildCorsHeaders(request)
      });
    }

    // Normalize root to something helpful (optional)
    if (url.pathname === "/" || url.pathname === "") {
      return Response.redirect(new URL("/prime_directive.md?aci", url).toString(), 302);
    }

    // ---- config from variables (with sane fallbacks)
    const ORG     = env.ORG     ?? "aliasnet";
    const REPO    = env.REPO    ?? "aci";
    const BRANCH  = env.BRANCH  ?? "main";
    const TTL     = parseInt(env.TTL ?? `${DEFAULT_TTL}`, 10) || DEFAULT_TTL;
    const RTL     = parseInt(env.RELAXED_TTL ?? `${RELAXED_TTL}`, 10) || RELAXED_TTL;
    const UA_ALLOW  = (env.UA_ALLOW  ?? "").split(",").map(s => s.trim()).filter(Boolean);
    const ASN_ALLOW = (env.ASN_ALLOW ?? "").split(",").map(s => s.trim()).filter(Boolean);

    // ---- relaxed mode gate
    const signedOK   = await isSignedOkay(url, env.SECRET); // strong gate
    const aciFlag    = url.searchParams.has("aci");
    const uaAllowed  = UA_ALLOW.length ? UA_ALLOW.some(tok => new RegExp(tok, "i").test(ua)) : false;
    const asnAllowed = ASN_ALLOW.length ? ASN_ALLOW.includes(asn) : false;

    // "Relaxed" gives extra knobs; otherwise we still allow normal pass-through
    const relaxed = signedOK || (aciFlag && uaAllowed) || asnAllowed;

    // ---- compute upstream URL (mirror GitHub raw)
    const path   = url.pathname.replace(/^\/+/, "");
    const origin = new URL(`https://raw.githubusercontent.com/${ORG}/${REPO}/${BRANCH}/${path}`);

    // ---- cache policy
    const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
    let ttl = relaxed ? RTL : TTL;
    const ttlOverride = url.searchParams.get("ttl");
    if (relaxed && ttlOverride && /^\d+$/.test(ttlOverride)) {
      ttl = clamp(parseInt(ttlOverride, 10), 60, 86400);
    }
    const wantNoCache = relaxed && url.searchParams.has("nocache");

    // ---- fetch with edge cache (caches.default respects Cache-Control)
    const cache = caches.default;
    const cacheKey = new Request(url.toString(), { method: "GET" }); // include qs in key (fmt/ttl matter)
    let resp = null;

    if (!wantNoCache) {
      resp = await cache.match(cacheKey);
      if (resp) {
        const prepared = withHeaders(resp, ttl, url, request);
        return wantsHead ? toHeadResponse(prepared) : prepared;
      }
    }

    // Origin fetch
    const upstream = await fetch(origin, {
      method: "GET",
      headers: { "user-agent": "ACI-Proxy/1.3 (+cf-worker)" },
      cf: { cacheEverything: false }
    });

    // Pass through body; adjust headers below
    resp = new Response(upstream.body, upstream);

    // ---- content-type tweaks (relaxed only)
    const fmt = (relaxed ? (url.searchParams.get("fmt") || "") : "").toLowerCase();
    if (fmt === "md")   resp.headers.set("content-type", "text/markdown; charset=utf-8");
    if (fmt === "json") resp.headers.set("content-type", "application/json; charset=utf-8");
    if (fmt === "raw")  resp.headers.set("content-type", "text/plain; charset=utf-8");
    if (fmt === "html") resp.headers.set("content-type", "text/html; charset=utf-8"); // still sends raw content

    // ---- CORS + caching
    applyCorsHeaders(resp.headers, request);
    resp.headers.set("cache-control", `public, max-age=${ttl}, stale-while-revalidate=60, stale-if-error=86400`);

    if (!wantNoCache && upstream.ok) {
      ctx.waitUntil(cache.put(cacheKey, resp.clone()));
    }
    return wantsHead ? toHeadResponse(resp) : resp;
  }
};

// ---------- helpers ----------
async function isSignedOkay(url, secret) {
  if (!secret) return false;
  const sig = url.searchParams.get("sig");
  const exp = url.searchParams.get("exp");
  if (!sig || !exp) return false;
  const now = Math.floor(Date.now()/1000);
  if (now > parseInt(exp, 10)) return false;

  const data = `${url.pathname}|${exp}`;
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = await crypto.subtle.sign("HMAC", key, enc.encode(data));
  const hex = [...new Uint8Array(mac)].map(b => b.toString(16).padStart(2,"0")).join("");
  return timingSafeEqual(hex, sig);
}
function timingSafeEqual(a, b) {
  if (!a || !b || a.length !== b.length) return false;
  let out = 0;
  for (let i = 0; i < a.length; i++) out |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return out === 0;
}
function withHeaders(resp, ttl, url, request) {
  const r = new Response(resp.body, resp);
  applyCorsHeaders(r.headers, request);
  r.headers.set("cache-control", `public, max-age=${ttl}, stale-while-revalidate=60, stale-if-error=86400`);
  return r;
}

function toHeadResponse(resp) {
  return new Response(null, {
    status: resp.status,
    statusText: resp.statusText,
    headers: resp.headers
  });
}

function applyCorsHeaders(headers, request) {
  const cors = buildCorsHeaders(request);
  cors.forEach((value, key) => {
    headers.set(key, value);
  });
}

function buildCorsHeaders(request) {
  const headers = new Headers({
    "access-control-allow-origin": "*",
    "access-control-allow-methods": "GET,HEAD,OPTIONS"
  });
  const reqHeaders = request?.headers?.get("access-control-request-headers");
  headers.set("access-control-allow-headers", reqHeaders || "*");
  return headers;
}
