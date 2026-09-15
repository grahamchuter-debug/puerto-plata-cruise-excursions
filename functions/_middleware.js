/**
 * Cloudflare Pages middleware (part of existing Pages project — not a Worker).
 * - www → apex 301
 * - Block internals even if a prior full-tree deploy left cached objects
 */
const BLOCKED = [
  /^\/content(\/|$)/i,
  /^\/partials(\/|$)/i,
  /^\/scripts(\/|$)/i,
  /^\/data(\/|$)/i,
  /^\/destination\.config\.json$/i,
  /^\/package(-lock)?\.json$/i,
  /^\/wrangler\.jsonc$/i,
];

export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === "www.puertoplatacruiseexcursion.com") {
    url.hostname = "puertoplatacruiseexcursion.com";
    return Response.redirect(url.toString(), 301);
  }

  if (BLOCKED.some((re) => re.test(url.pathname))) {
    let body =
      "<!DOCTYPE html><html lang=\"en-GB\"><head><meta charset=\"UTF-8\"/><meta name=\"robots\" content=\"noindex,follow\"/><title>Page not found | Puerto Plata Cruise Excursion</title></head><body><h1>Page not found</h1><p><a href=\"/\">Puerto Plata home</a></p></body></html>";
    let contentType = "text/html; charset=utf-8";
    try {
      if (context.env && context.env.ASSETS) {
        const asset = await context.env.ASSETS.fetch(
          new Request(new URL("/404.html", url.origin), context.request)
        );
        if (asset.ok) {
          body = await asset.text();
          contentType = asset.headers.get("content-type") || contentType;
        }
      }
    } catch (_) {
      /* use fallback body */
    }
    return new Response(body, {
      status: 404,
      headers: {
        "content-type": contentType,
        "cache-control": "private, no-store",
        "x-robots-tag": "noindex, follow",
      },
    });
  }

  return context.next();
}
