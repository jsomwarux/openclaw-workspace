# LinkedIn Content OS Program 0

```json
{
  "authorityConsumptionBindings": {
    "phase1Corpus": {
      "canonicalManifestSha256": "a868bcdf6baac9e162188b5e7226f9897f5531cafbee69a2297c4dd23db4fa4b",
      "command": "build-corpus",
      "expectedManifestSha256": null,
      "generatedAt": "2026-09-28T20:21:23.790936+00:00",
      "inputs": [
        {
          "path": "memory/content/linkedin-content-os/historical-audit.phase-1.v1.json",
          "role": "audit",
          "sha256": "def6fb69128925f607d96d58731108aa8ad309e087a7f0e314ad833cd2626177"
        },
        {
          "path": "memory/content/linkedin-content-os/outcomes.phase-1.v1.jsonl",
          "role": "outcomes",
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        },
        {
          "path": "memory/content/linkedin-content-os/run-context.phase-1.v1.json",
          "role": "run_context",
          "sha256": "3f1886c61f9afc70244bef4b0612582e0bada16e28919069d8504542d3b06756"
        }
      ],
      "outputs": [
        {
          "path": "memory/content/linkedin-content-os/contrastive-pairs.phase-1.v0.jsonl",
          "role": "contrastive_pairs",
          "sha256": "6a489405bf58f0f0f4aaddbb2af527a239e5a5d7f8eea4f057f133284c638572"
        },
        {
          "path": "memory/content/linkedin-content-os/voice-gold.phase-1.v0.jsonl",
          "role": "voice_gold",
          "sha256": "6a489405bf58f0f0f4aaddbb2af527a239e5a5d7f8eea4f057f133284c638572"
        }
      ],
      "receiptSha256": "8a521676162a37e820fb1f50a5bcdfbb0091410884ea084c254e05ceaad67f06",
      "runContextSha256": "3f1886c61f9afc70244bef4b0612582e0bada16e28919069d8504542d3b06756",
      "schemaVersion": "linkedin-authority-consumption-receipt.v1"
    },
    "phase2Audit": {
      "canonicalManifestSha256": "891536743e6c26ab213934603d79ef69acc20a6d9b95bad83eb6219a940e2c2e",
      "command": "audit-history",
      "expectedManifestSha256": "891536743e6c26ab213934603d79ef69acc20a6d9b95bad83eb6219a940e2c2e",
      "generatedAt": "2026-09-28T23:06:57.547749+00:00",
      "inputs": [
        {
          "path": "memory/content/linkedin-content-os/corpus-authority-manifest.v1.json",
          "role": "authority_manifest",
          "sha256": "e7559f317c4a73d9dec65fc502075bf8aeceef3726cfd942a1f373a343c5773a"
        },
        {
          "path": "memory/content/linkedin-content-os/outcomes.v1.jsonl",
          "role": "outcomes",
          "sha256": "e27dc5bbef8eae4baf2e5788f076aac09d94147faba96dce30e37b554660e953"
        },
        {
          "path": "memory/content/posted-log.jsonl",
          "role": "posted_log",
          "sha256": "fcbd176927ec299c3a3c56d98c49619ba1b6d1873f64f681f885900d0179aedf"
        },
        {
          "path": "memory/content/linkedin-content-os/run-context.phase-2-authority.v1.json",
          "role": "run_context",
          "sha256": "3eaa9a32e88e5616679762a1d2285db5801dfa6d75cd05cb66fb6300b77653d5"
        }
      ],
      "outputs": [
        {
          "path": "memory/content/linkedin-content-os/historical-audit.v1.json",
          "role": "historical_audit",
          "sha256": "a0b66794f739caba5f5095c0ee9fbd7b5c5fbb5d6ba913e9ee1926ebda0fe6fe"
        },
        {
          "path": "memory/content/linkedin-content-os/historical-recovery-request.v1.json",
          "role": "recovery_request",
          "sha256": "62deff6d0e48091527b14a6335237e774c9f7df61ba5b22fe1b9f8ee094b61ec"
        }
      ],
      "receiptSha256": "5e6ff041e3c26a454d132e9cafa329fda4bbe4fe6b359789ac30aaa80adf2d68",
      "runContextSha256": "3eaa9a32e88e5616679762a1d2285db5801dfa6d75cd05cb66fb6300b77653d5",
      "schemaVersion": "linkedin-authority-consumption-receipt.v1"
    },
    "phase2Corpus": {
      "canonicalManifestSha256": "891536743e6c26ab213934603d79ef69acc20a6d9b95bad83eb6219a940e2c2e",
      "command": "build-corpus",
      "expectedManifestSha256": "891536743e6c26ab213934603d79ef69acc20a6d9b95bad83eb6219a940e2c2e",
      "generatedAt": "2026-09-28T23:06:57.547749+00:00",
      "inputs": [
        {
          "path": "memory/content/linkedin-content-os/historical-audit.v1.json",
          "role": "audit",
          "sha256": "a0b66794f739caba5f5095c0ee9fbd7b5c5fbb5d6ba913e9ee1926ebda0fe6fe"
        },
        {
          "path": "memory/content/linkedin-content-os/outcomes.v1.jsonl",
          "role": "outcomes",
          "sha256": "e27dc5bbef8eae4baf2e5788f076aac09d94147faba96dce30e37b554660e953"
        },
        {
          "path": "memory/content/linkedin-content-os/run-context.phase-2-authority.v1.json",
          "role": "run_context",
          "sha256": "3eaa9a32e88e5616679762a1d2285db5801dfa6d75cd05cb66fb6300b77653d5"
        }
      ],
      "outputs": [
        {
          "path": "memory/content/linkedin-content-os/contrastive-pairs.v0.jsonl",
          "role": "contrastive_pairs",
          "sha256": "6a489405bf58f0f0f4aaddbb2af527a239e5a5d7f8eea4f057f133284c638572"
        },
        {
          "path": "memory/content/linkedin-content-os/voice-gold.v0.jsonl",
          "role": "voice_gold",
          "sha256": "6a489405bf58f0f0f4aaddbb2af527a239e5a5d7f8eea4f057f133284c638572"
        }
      ],
      "receiptSha256": "2ab9f5219512dcdb2015383ee41c67f6a662adaf7ff5fefaba27bccf4c71802d",
      "runContextSha256": "3eaa9a32e88e5616679762a1d2285db5801dfa6d75cd05cb66fb6300b77653d5",
      "schemaVersion": "linkedin-authority-consumption-receipt.v1"
    }
  },
  "authorityContextDigest": "3eaa9a32e88e5616679762a1d2285db5801dfa6d75cd05cb66fb6300b77653d5",
  "boundaryPairsEqual": true,
  "boundaryProof": [
    {
      "afterFileSha256": "2835506284a4db32191ab54248a22aa406cc959a7ef47158fdaaae074704148a",
      "afterPath": "memory/content/linkedin-content-os/boundaries.phase-1-fresh.after.v1.json",
      "afterSha256": "59f36b246fe19e774199988da899cc3282587b19f56f6403a510bb45733a28ca",
      "beforeFileSha256": "356ca91ddd3da9505664fa92efeda68a052b1f9f0c94cc398ff71a7cfb2632d2",
      "beforePath": "memory/content/linkedin-content-os/boundaries.phase-1-fresh.before.v1.json",
      "beforeSha256": "b4d89a427d3b7ab47cc661b8992f0011214f0f5f14f391a4bedc915cb2c12304",
      "generatedAt": "2026-09-28T20:21:23.790936+00:00",
      "governedKeys": [
        "missionControl",
        "cronDefinitionSha256",
        "launchAgents",
        "protectedInputs",
        "primaryCheckoutFingerprint"
      ],
      "governedValuesEqual": true,
      "runId": "sha256:3f5726390bf8c5377c1b8461a86b85d92082cd963c887d62ea555650a378f9d6"
    },
    {
      "afterFileSha256": "497eabebd28b3b9de04c91c11c17582658a06da695244d9a6e6b3698c5f0c2cf",
      "afterPath": "memory/content/linkedin-content-os/boundaries.phase-2-replacement.after.v1.json",
      "afterSha256": "2572e17447b9b74fbafadedcbe6421a2bc8418e9f8e1158f1e1f3d4991342ec0",
      "beforeFileSha256": "97431fc4e0438e6e3f9c0bf49ae7723ba34e69527e18ea0508d70242a041806c",
      "beforePath": "memory/content/linkedin-content-os/boundaries.phase-2-replacement.before.v1.json",
      "beforeSha256": "63b4981aa9c2fa91142f47d972033a84e2b09a8ce764b9e43eab752b3b20fc62",
      "generatedAt": "2026-09-28T23:06:57.547749+00:00",
      "governedKeys": [
        "missionControl",
        "cronDefinitionSha256",
        "launchAgents",
        "protectedInputs",
        "primaryCheckoutFingerprint"
      ],
      "governedValuesEqual": true,
      "runId": "sha256:c9632b20d279a333f1d800a89cfd914f27486941cf2c7ec174777ae072640e82"
    }
  ],
  "canonicalManifestSha256": "891536743e6c26ab213934603d79ef69acc20a6d9b95bad83eb6219a940e2c2e",
  "checkinPreviewCount": 0,
  "contrastivePairCount": 0,
  "fixtureClassifications": {
    "gap": 2,
    "negative": 1,
    "positive": 1
  },
  "focusTargets": [
    {
      "desiredOutcome": "Publish only proof-led consulting content that clears evidence and permission gates",
      "kind": "consulting",
      "label": "Permissioned consulting proof",
      "sourceRefs": [
        {
          "path": "memory/content/current-efforts.md",
          "sha256": "99b419e7a2a66e792e759d011e3a32ec0a1e3947549d8ecbd216ee2980421628"
        }
      ],
      "targetId": "consulting-proof"
    },
    {
      "desiredOutcome": "Show evidence-backed enterprise AI execution without exposing internal machinery",
      "kind": "career",
      "label": "Enterprise AI operator authority",
      "sourceRefs": [
        {
          "path": "memory/job-state/job-market-daily-research.md",
          "sha256": "c2efdc048cc4c448b5b503f3ad156b33d39418c69135f5ba5efb30eca451a4b2"
        }
      ],
      "targetId": "career-authority"
    },
    {
      "desiredOutcome": "Turn verified shipped outcomes into commercially relevant public lessons",
      "kind": "product",
      "label": "Shipped product distribution",
      "sourceRefs": [
        {
          "path": "memory/north-star/active-this-week.md",
          "sha256": "10bd4c4b050ed353a88d5356646652808d3171ad3b56da2e4aca7ecbc044cd18"
        }
      ],
      "targetId": "product-distribution"
    }
  ],
  "humanGateAnswerCount": 23,
  "humanGateResolved": true,
  "liveOrExternalActionOccurred": false,
  "missingFinalTextCount": 0,
  "missingUrlCount": 0,
  "receipts": [
    {
      "path": "memory/content/linkedin-content-os/authority-consumption.phase-1-corpus.v1.json",
      "sha256": "aa8990bf01b9056f704930730c6d89af30e5d87f362d9ac9bc51e1d7d94f444b"
    },
    {
      "path": "memory/content/linkedin-content-os/authority-consumption.phase-2-audit.v1.json",
      "sha256": "7bcbaa2af794939e85d79f2daf958d335a0d48114f0f29e50573d32aba0ee1dc"
    },
    {
      "path": "memory/content/linkedin-content-os/authority-consumption.phase-2-corpus.v1.json",
      "sha256": "a6b617375527c6b4f6111e8542737c4e4c7c9534943c90aa1f90e6f3508a0bb9"
    }
  ],
  "schemaVersion": "linkedin-program-0-verification.v1",
  "statusCounts": {
    "not_posted_confirmed": 0,
    "posted_confirmed": 0,
    "status_unknown": 101
  },
  "verdict": "program-0-local-proof-ready-for-independent-verification",
  "voiceGoldCount": 0
}
```
