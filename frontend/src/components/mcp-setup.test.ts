import { expect, it } from "vitest";

import { mcpSnippets } from "./mcp-setup";

it("keeps the key out of the URL in every snippet", () => {
  const url = "https://mcp.clipforge.ai/mcp";
  const snippets = mcpSnippets(url, "sk_test");
  expect(snippets.claudeCode).toBe(
    'claude mcp add --transport http clipforge https://mcp.clipforge.ai/mcp --header "Authorization: Bearer sk_test"',
  );
  expect(JSON.parse(snippets.json).mcpServers.clipforge).toEqual({
    url,
    headers: { Authorization: "Bearer sk_test" },
  });
  const desktop = JSON.parse(snippets.claudeDesktop).mcpServers.clipforge;
  expect(desktop.args).toContain(url);
  expect(desktop.env.CLIPFORGE_AUTH).toBe("Bearer sk_test");
  expect(snippets.stdio).toContain("CLIPFORGE_API_KEY=sk_test");
  expect(snippets.stdio).toContain("clipforge-mcp");
});
