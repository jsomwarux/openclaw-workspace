# Autoresearch Checklist — google-drive

Score Drive upload workflows against these yes/no checks:

1. Does the workflow use the correct destination folder/path for the deliverable type?
2. Does it preserve or report the final Drive URL in the reply/log?
3. Does it avoid uploading secrets, API keys, or private operational logs?
4. Does it handle existing/duplicate files without creating confusing copies?
5. Does it verify upload success before claiming completion?
6. Does it keep external writes batched and rate-limit-safe?
