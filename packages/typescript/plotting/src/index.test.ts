import { describe, expect, test } from "bun:test";
import { validatePlotSpec } from "@quant/contracts";
import { costDelaySpec } from "./index";

describe("diagnostic specs", () => {
  test("cost-delay spec is contract-valid", () => {
    expect(validatePlotSpec(costDelaySpec("BTCUSDT · locked test"))).toEqual([]);
  });
});
