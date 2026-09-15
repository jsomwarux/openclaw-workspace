import Foundation
import Security

let account = "jtsomwaru"
let services = [
    "review": "com.openclaw.mission-control.outreach-review",
    "decision": "com.openclaw.mission-control.outreach-decision",
]

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data((message + "\n").utf8))
    exit(2)
}

func randomCapability() -> Data {
    var bytes = [UInt8](repeating: 0, count: 48)
    guard SecRandomCopyBytes(kSecRandomDefault, bytes.count, &bytes) == errSecSuccess else {
        fail("capability generation failed")
    }
    return Data(bytes).base64EncodedData()
}

func query(_ service: String) -> [String: Any] {
    return [
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
        "Mission Control outreach capabilities" as CFString,
        [trusted] as CFArray,
        &access
    ) == errSecSuccess, let access else { fail("keychain access creation failed") }
    return access
}

func store(_ service: String, _ value: Data) {
    let key = query(service)
    let update = SecItemUpdate(key as CFDictionary, [kSecValueData as String: value] as CFDictionary)
    if update == errSecItemNotFound {
        var item = key
        item[kSecValueData as String] = value
        item[kSecAttrAccess as String] = helperAccess()
        let added = SecItemAdd(item as CFDictionary, nil)
        guard added == errSecSuccess else { fail("capability storage failed") }
    } else if update != errSecSuccess {
        fail("capability update failed")
    }
}

func read(_ service: String) -> Data {
    var key = query(service)
    key[kSecReturnData as String] = true
    key[kSecMatchLimit as String] = kSecMatchLimitOne
    var item: CFTypeRef?
    let status = SecItemCopyMatching(key as CFDictionary, &item)
    guard status == errSecSuccess, let value = item as? Data, !value.isEmpty else {
        fail("stored capability is unavailable")
    }
    return value
}

let args = Array(CommandLine.arguments.dropFirst())
if args == ["install"] {
    let review = randomCapability()
    let decision = randomCapability()
    guard review != decision else { fail("capability generation collision") }
    store(services["review"]!, review)
    store(services["decision"]!, decision)
} else if args.count == 2, args[0] == "read", let service = services[args[1]] {
    FileHandle.standardOutput.write(read(service))
    FileHandle.standardOutput.write(Data("\n".utf8))
} else {
    fail("unsupported keychain operation")
}
