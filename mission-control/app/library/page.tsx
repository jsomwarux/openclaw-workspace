import { redirect } from "next/navigation";
import { legacyRedirects } from "@/lib/mission-control/routes";

// Library aliases the existing /skills surface for now. The dedicated
// skills + agents lane lands in a later phase.
export default function LibraryAliasPage() {
  redirect(legacyRedirects["/library"]);
}
