import { ConvexHttpClient } from "convex/browser";
import type { FunctionArgs } from "convex/server";
import { api } from "@/convex/_generated/api";
import { createPostHandler } from "@/lib/mission-control/task-create-only-post";

export const POST = createPostHandler(async (input) => {
  const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);
  return await convex.mutation(
    api.tasks.createOnlyByDedupeKey,
    input as FunctionArgs<typeof api.tasks.createOnlyByDedupeKey>,
  );
});
