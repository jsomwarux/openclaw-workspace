import Foundation
import Security

let account = "jtsomwaru"
let protocolVersion = "outreach-capabilities-v5"
let capabilitySetService = "com.openclaw.mission-control.outreach-capability-set-v3"

struct ExistingSet: Codable {
    let version: Int
    let review: String
    let decision: String
    let reviewAuthorityWrite: String?
    let reviewAuthorityRead: String?
}

struct CapabilitySet: Codable {
    let version: Int
    let review: String
    let decision: String
    let reviewAuthorityWrite: String?
    let reviewAuthorityRead: String?
    let laneProducer: String
    let laneDecision: String
}

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data((message + "\n").utf8))
    exit(2)
}

func randomCapability() -> String {
    var bytes = [UInt8](repeating: 0, count: 48)
    guard SecRandomCopyBytes(kSecRandomDefault, bytes.count, &bytes) == errSecSuccess else {
        fail("capability generation failed")
    }
    return Data(bytes).base64EncodedString()
}

func query(_ service: String) -> [String: Any] {
    [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecAttrService as String: service,
    ]
}

func helperAccess() -> SecAccess {
    var trusted: SecTrustedApplication?
    let path = URL(fileURLWithPath: CommandLine.arguments[0]).standardizedFileURL.path
    guard SecTrustedApplicationCreateFromPath(path, &trusted) == errSecSuccess,
          let trusted else { fail("keychain trust creation failed") }
    var access: SecAccess?
    guard SecAccessCreate(
        "Mission Control outreach and lane capabilities" as CFString,
        [trusted] as CFArray,
        &access
    ) == errSecSuccess, let access else { fail("keychain access creation failed") }
    return access
}

func store(_ value: Data) {
    let key = query(capabilitySetService)
    let update = SecItemUpdate(key as CFDictionary, [kSecValueData as String: value] as CFDictionary)
    if update == errSecItemNotFound {
        var item = key
        item[kSecValueData as String] = value
        item[kSecAttrAccess as String] = helperAccess()
        guard SecItemAdd(item as CFDictionary, nil) == errSecSuccess else {
            fail("capability storage failed")
        }
    } else if update != errSecSuccess {
        fail("capability update failed")
    }
}

func read(allowMissing: Bool = false) -> Data? {
    var key = query(capabilitySetService)
    key[kSecReturnData as String] = true
    key[kSecMatchLimit as String] = kSecMatchLimitOne
    var item: CFTypeRef?
    let status = SecItemCopyMatching(key as CFDictionary, &item)
    if allowMissing && status == errSecItemNotFound { return nil }
    guard status == errSecSuccess, let value = item as? Data, !value.isEmpty else {
        fail("stored capability is unavailable")
    }
    return value
}

func validatedExistingSet() -> ExistingSet {
    let input = FileHandle.standardInput.readDataToEndOfFile()
    guard !input.isEmpty,
          let value = try? JSONDecoder().decode(ExistingSet.self, from: input),
          value.version == 1 else { fail("capability migration failed") }
    let authorityValues = [value.reviewAuthorityWrite, value.reviewAuthorityRead]
    guard authorityValues.allSatisfy({ $0 == nil }) || authorityValues.allSatisfy({ $0 != nil }) else {
        fail("capability migration failed")
    }
    let values = [value.review, value.decision] + authorityValues.compactMap { $0 }
    let normalized = values.map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }
    guard normalized.allSatisfy({ !$0.isEmpty }), Set(normalized).count == normalized.count else {
        fail("capability migration failed")
    }
    return value
}

func newDistinctCapability(excluding: inout Set<String>) -> String {
    while true {
        let value = randomCapability()
        if !excluding.contains(value) {
            excluding.insert(value)
            return value
        }
    }
}

let args = Array(CommandLine.arguments.dropFirst())
if args == ["probe", protocolVersion] {
    exit(0)
} else if args == ["install-set"] {
    let existing = validatedExistingSet()
    var used = Set([existing.review, existing.decision] + [
        existing.reviewAuthorityWrite,
        existing.reviewAuthorityRead,
    ].compactMap { $0 })
    let value = CapabilitySet(
        version: 3,
        review: existing.review,
        decision: existing.decision,
        reviewAuthorityWrite: existing.reviewAuthorityWrite,
        reviewAuthorityRead: existing.reviewAuthorityRead,
        laneProducer: newDistinctCapability(excluding: &used),
        laneDecision: newDistinctCapability(excluding: &used)
    )
    let encoder = JSONEncoder()
    encoder.outputFormatting = [.sortedKeys]
    guard let encoded = try? encoder.encode(value) else { fail("capability migration failed") }
    store(encoded)
} else if args == ["read-set"] {
    if let value = read(allowMissing: true) {
        FileHandle.standardOutput.write(value)
        FileHandle.standardOutput.write(Data("\n".utf8))
    } else {
        exit(3)
    }
} else {
    fail("unsupported keychain operation")
}
