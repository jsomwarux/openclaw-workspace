// Props shared by the desktop and mobile item screens.
import type { ReactNode } from "react";
import type { CockpitAction } from "@/lib/cockpit/actions";
import type { OpenItemChange } from "@/lib/cockpit/controller";
import type { ItemViewModel } from "@/lib/cockpit/view";

export type ButtonAction = Exclude<CockpitAction, "previous" | "next">;

export const ACTION_LABELS: Record<ButtonAction, string> = {
  start: "Start",
  complete: "Complete",
  saveAnswer: "Save answer",
  approve: "Approve",
  reject: "Reject",
  defer: "Defer",
  block: "Block",
};

export interface ActionModel {
  buttons: ButtonAction[];
  paused: string | null;
  readOnly: { text: string; title: string } | null;
  resolved: boolean;
  line: string | null;
  canUndo: boolean;
  failure: { title: string; body: string } | null;
  busy: boolean;
}

export interface Banner { tag: string; text: string; button: string; onClick: () => void }

export interface RailRow {
  id: string;
  position: number;
  title: string;
  status: string;
  group: string;
  current: boolean;
  handled: boolean;
  exception: string | null;
}

export interface ItemScreenProps {
  view: ItemViewModel;
  change: OpenItemChange | null;
  timeZone: string;
  positionText: string;
  handledText: string;
  freshText: string;
  freshShort: string;
  banner: Banner | null;
  rail: RailRow[];
  actions: ActionModel;
  panel: ReactNode;
  answerBox: ReactNode;
  evidenceEmphasis: boolean;
  evidenceMessage: string | null;
  notice: string | null;
  onPause: () => void;
  onQueue: () => void;
  onHelp: () => void;
  onPrevious: () => void;
  onNext: () => void;
  onAckChange: () => void;
  onRecheck: () => void;
  onAction: (action: ButtonAction) => void;
  onUndo: () => void;
  onRetry: () => void;
  onDismiss: () => void;
  onGoTo: (id: string) => void;
}
