import { NextResponse } from "next/server";
import { exec } from "child_process";

export async function POST() {
  try {
    await new Promise<string>((resolve, reject) => {
      exec(
        'bash /Users/jtsomwaru/.openclaw/workspace/scripts/restart-gateway.sh "manual restart from MC"',
        { timeout: 30000 },
        (error, stdout, stderr) => {
          if (error) {
            reject(new Error(stderr || error.message));
          } else {
            resolve(stdout);
          }
        }
      );
    });

    return NextResponse.json({ success: true, message: "Gateway restart initiated" });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ success: false, error: message }, { status: 500 });
  }
}
