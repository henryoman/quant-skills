import { describe, expect, test } from "bun:test";
import { conditionalProfileSpec } from "@quant/plotting";

describe("report studio", () => {
  test("consumes shared plotting contracts", () => {
    expect(conditionalProfileSpec({ feature: "x", target: "y", unit: "bps", scope: "test" }).plotId).toBe("conditional-x-y");
  });
});
