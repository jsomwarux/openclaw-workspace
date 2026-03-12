import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Every night at 3:00 AM UTC — archive done tasks older than 7 days
crons.cron(
  "nightly-auto-archive",
  "0 3 * * *",
  internal.tasks.autoArchive,
);

export default crons;
