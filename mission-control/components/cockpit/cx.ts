// Class merging for the cockpit. The shared cn() does not know the bundle's token classes, so it
// reads text-mc-11 as a color and drops it next to text-mc-ink-muted. This merger is taught the
// token font sizes, density spacing, radii and font families.
import { clsx } from "clsx";
import type { ClassValue } from "clsx";
import { extendTailwindMerge } from "tailwind-merge";
import cockpitTokens from "@/docs/design/mission-control-redesign/tokens/tailwind.config";
import { densitySpacing } from "@/lib/cockpit/density";

const tokens = cockpitTokens.theme.extend;
const radii = Object.keys(tokens.borderRadius);

const merge = extendTailwindMerge({
  extend: {
    theme: { spacing: Object.keys(densitySpacing) },
    classGroups: {
      "font-size": [{ text: Object.keys(tokens.fontSize) }],
      "font-family": [{ font: ["mc-sans", "mc-mono"] }],
      rounded: [{ rounded: radii }],
      "rounded-t": [{ "rounded-t": radii }],
    },
  },
});

export function cx(...inputs: ClassValue[]): string {
  return merge(clsx(inputs));
}
