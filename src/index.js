export default {
  async fetch(request) {
    const url = new URL(request.url);
    const originUrl = "https://raw.githubusercontent.com/aliasnet/aci/main" + url.pathname;
    const resp = await fetch(originUrl);

    let contentType = "text/plain";
    if (originUrl.endsWith(".json")) {
      contentType = "application/json; charset=utf-8";
    } else if (originUrl.endsWith(".md")) {
      contentType = "text/markdown; charset=utf-8";
    }

    return new Response(resp.body, {
      headers: {
        "Content-Type": contentType,
        "Cache-Control": "public, max-age=3600"
      }
    });
  }
}
