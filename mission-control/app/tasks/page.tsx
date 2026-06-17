import { redirect } from "next/navigation";
import { legacyRedirects } from "@/lib/mission-control/routes";

export default function TasksRedirectPage() {
  redirect(legacyRedirects["/tasks"]);
}
