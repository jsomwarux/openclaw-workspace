import { redirect } from "next/navigation";
import { legacyRedirects } from "@/lib/mission-control/routes";

export default function AgentsRedirectPage() {
  redirect(legacyRedirects["/agents"]);
}
