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
      "canonicalManifestSha256": "f0722d1b868c89bf497aa85bb9e21cef25ed8f2b2c8a018b55f84e6bd9ae1eaf",
      "command": "audit-history",
      "expectedManifestSha256": "f0722d1b868c89bf497aa85bb9e21cef25ed8f2b2c8a018b55f84e6bd9ae1eaf",
      "generatedAt": "2026-09-30T13:46:48.234145+00:00",
      "inputs": [
        {
          "path": "memory/content/linkedin-content-os/corpus-authority-manifest.supplement-1.v1.json",
          "role": "authority_manifest",
          "sha256": "624429279edc32bd9e48c458e6d858a922843280998e90b92201fbeab3456d6b"
        },
        {
          "path": "memory/content/linkedin-content-os/outcomes.v1.jsonl",
          "role": "outcomes",
          "sha256": "10a7b5bf4b45573b2df5ffcdef6c34df646c14ec752e6e79d0ef61ba787ca732"
        },
        {
          "path": "memory/content/posted-log.jsonl",
          "role": "posted_log",
          "sha256": "fcbd176927ec299c3a3c56d98c49619ba1b6d1873f64f681f885900d0179aedf"
        },
        {
          "path": "memory/content/linkedin-content-os/run-context.supplement-1-authority.v1.json",
          "role": "run_context",
          "sha256": "3b9fb55bea45c1b6c2ce7b3151750809788ab1136c3d62dd212d710bfa230abb"
        }
      ],
      "outputs": [
        {
          "path": "memory/content/linkedin-content-os/historical-audit.v1.json",
          "role": "historical_audit",
          "sha256": "c9f6b666b90681319658d7d3abbf881fdf3928fb7ecce6160c773aba1b6b4e2d"
        },
        {
          "path": "memory/content/linkedin-content-os/historical-recovery-request.v1.json",
          "role": "recovery_request",
          "sha256": "2086eab6a4acbfa75743049ddd61d21c2c12e2633c617d863fab8d55bdfefa56"
        }
      ],
      "receiptSha256": "76eddac0176e321d82c07a1adf848f04d78f611a889a089dad8aa07aff014a97",
      "runContextSha256": "3b9fb55bea45c1b6c2ce7b3151750809788ab1136c3d62dd212d710bfa230abb",
      "schemaVersion": "linkedin-authority-consumption-receipt.v1"
    },
    "phase2Corpus": {
      "canonicalManifestSha256": "f0722d1b868c89bf497aa85bb9e21cef25ed8f2b2c8a018b55f84e6bd9ae1eaf",
      "command": "build-corpus",
      "expectedManifestSha256": "f0722d1b868c89bf497aa85bb9e21cef25ed8f2b2c8a018b55f84e6bd9ae1eaf",
      "generatedAt": "2026-09-30T13:46:48.234145+00:00",
      "inputs": [
        {
          "path": "memory/content/linkedin-content-os/historical-audit.v1.json",
          "role": "audit",
          "sha256": "c9f6b666b90681319658d7d3abbf881fdf3928fb7ecce6160c773aba1b6b4e2d"
        },
        {
          "path": "memory/content/linkedin-content-os/outcomes.v1.jsonl",
          "role": "outcomes",
          "sha256": "10a7b5bf4b45573b2df5ffcdef6c34df646c14ec752e6e79d0ef61ba787ca732"
        },
        {
          "path": "memory/content/linkedin-content-os/run-context.supplement-1-authority.v1.json",
          "role": "run_context",
          "sha256": "3b9fb55bea45c1b6c2ce7b3151750809788ab1136c3d62dd212d710bfa230abb"
        }
      ],
      "outputs": [
        {
          "path": "memory/content/linkedin-content-os/contrastive-pairs.v0.jsonl",
          "role": "contrastive_pairs",
          "sha256": "6262b750eaa9ed281e092448dd69ad06e747240ba58b95fa603894328b5e7e63"
        },
        {
          "path": "memory/content/linkedin-content-os/voice-gold.v0.jsonl",
          "role": "voice_gold",
          "sha256": "69f80dd463c0a3966fc0c6f493ef290246691c50d80c2c0d9b44b5e02035da71"
        }
      ],
      "receiptSha256": "ac20eaedfb581dd2c8341abdfd1b9155ddb229e825b1f0f49371eb544d87ce94",
      "runContextSha256": "3b9fb55bea45c1b6c2ce7b3151750809788ab1136c3d62dd212d710bfa230abb",
      "schemaVersion": "linkedin-authority-consumption-receipt.v1"
    }
  },
  "authorityContextDigest": "3b9fb55bea45c1b6c2ce7b3151750809788ab1136c3d62dd212d710bfa230abb",
  "baseAuthority": {
    "authorityContextDigest": "3eaa9a32e88e5616679762a1d2285db5801dfa6d75cd05cb66fb6300b77653d5",
    "ledgerPosition": 25,
    "manifestSha256": "891536743e6c26ab213934603d79ef69acc20a6d9b95bad83eb6219a940e2c2e"
  },
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
    },
    {
      "afterFileSha256": "e838c3f7fb9ab93f0472f3fd7240f35a0ba27cd0ced828479694c5b717a65834",
      "afterPath": "memory/content/linkedin-content-os/boundaries.supplement-1.after.v1.json",
      "afterSha256": "f7bf7faa1d63e837e3fa01e4f7b4cb0e3128c582f1d04b2ad67bb949806fdced",
      "beforeFileSha256": "227319012527e46a23cbe9f5e3c054b23e1d9f727d9917357544029b7d0e206d",
      "beforePath": "memory/content/linkedin-content-os/boundaries.supplement-1.before.v1.json",
      "beforeSha256": "979aae13b487ffa5cdca24c5255036e3e29b40cc1f62f4b3bb2629d5ac2750c3",
      "generatedAt": "2026-09-30T13:46:48.234145+00:00",
      "governedKeys": [
        "missionControl",
        "cronDefinitionSha256",
        "launchAgents",
        "protectedInputs",
        "primaryCheckoutFingerprint"
      ],
      "governedValuesEqual": true,
      "runId": "sha256:bedfa9f8366176463cbf8c4562c979dd983f6eb01d45ae700613c5e994a88766"
    }
  ],
  "canonicalManifestSha256": "f0722d1b868c89bf497aa85bb9e21cef25ed8f2b2c8a018b55f84e6bd9ae1eaf",
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
      "sha256": "76caa21bd222183291ba18d007d78bd817e3a1dd7c04fd67bd2adc6cac68421a"
    },
    {
      "path": "memory/content/linkedin-content-os/authority-consumption.phase-2-corpus.v1.json",
      "sha256": "c01fb3e1309da967183d7722b1613995bd2322c255f44dea18a92d5b9bf47286"
    }
  ],
  "schemaVersion": "linkedin-program-0-verification.v1",
  "statusCounts": {
    "not_posted_confirmed": 0,
    "posted_confirmed": 1,
    "status_unknown": 100
  },
  "supplementalAuthority": {
    "authorityContextDigest": "3b9fb55bea45c1b6c2ce7b3151750809788ab1136c3d62dd212d710bfa230abb",
    "blockEventCount": 4,
    "corrections": [
      {
        "authorityEventSha256": "0fddd8d77da1af2f938b941f70e8c0b4236a2e32ff26befe5fa70b155c041cc9",
        "authorityOutcomeEventId": "authority-supplement-1:fabf927a2f54fa40a8d4cc48948f32393259c842d7ada3bbd5bfae84f2f69ccf",
        "correctionEventSha256": "22356a769973587033f7cafd1817f3235f976cb3bebbd9855b736508ef74d2f1",
        "correctionOutcomeEventId": "correction-supplement-1:fabf927a2f54fa40a8d4cc48948f32393259c842d7ada3bbd5bfae84f2f69ccf",
        "legacyRowSha256": "fabf927a2f54fa40a8d4cc48948f32393259c842d7ada3bbd5bfae84f2f69ccf",
        "publicationEventSha256": "22c5512b6f76f46c676131a9ef7b45f2916fe644e1e50f46d1614f3bfcc35976",
        "publicationOutcomeEventId": "publication-supplement-1:fabf927a2f54fa40a8d4cc48948f32393259c842d7ada3bbd5bfae84f2f69ccf",
        "replacementEventSha256": "0f829647ddda7a6ba3cd27b78d4c584c009c94833737f1ffb181d22393b70057",
        "replacementOutcomeEventId": "history-supplement-1:fabf927a2f54fa40a8d4cc48948f32393259c842d7ada3bbd5bfae84f2f69ccf",
        "targetEventSha256": "efdce6b62d51133b261f4b6b1426bb4aa529459273f68174caa2e27f1b6f8e86",
        "targetOutcomeEventId": "history:fabf927a2f54fa40a8d4cc48948f32393259c842d7ada3bbd5bfae84f2f69ccf"
      }
    ],
    "manifestPath": "memory/content/linkedin-content-os/corpus-authority-manifest.supplement-1.v1.json",
    "manifestSha256": "f0722d1b868c89bf497aa85bb9e21cef25ed8f2b2c8a018b55f84e6bd9ae1eaf",
    "priorEventCount": 25,
    "runContextSha256": "e461a1c566655f8d23a0101e015050b111bf2c0a7a2daac55ed742a2bc06add5",
    "runId": "22f32fd051f10c96d2816610bba444263eda5f45ace7a512498c22e89f3c68fb",
    "supplementId": "supplement-1",
    "supplementPath": "memory/content/linkedin-content-os/human-gate-supplement-1.v1.json",
    "supplementSha256": "40a368e64b7675f37bbec3410fce8851a8d3562ebd33b006d01605108d007229"
  },
  "verdict": "program-0-local-proof-ready-for-independent-verification",
  "voiceGoldCount": 1
}
```
