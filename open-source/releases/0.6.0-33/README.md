# Ensceno 0.6.0 (33) — SMB replacement materials, revision 2

Prepared 2026-10-31. The developer has confirmed the supplemental permissions and public delivery of these materials. Modified-library execution on Vision Pro remains pending; publication alone does not close that verification.

## Contents and version matching

- `Unencrypted/ImmersiFin.app`: the unencrypted build 33 application executable and resources, with no provisioning profile or developer private key. Do not use a FairPlay-encrypted App Store download as input.
- `SMBDependencySources.zip`: exact bundled AMSMB2/libsmb2 sources, original notices, Package.swift and build instructions.
- `ThirdPartyNotices.txt`: the build 33 notices, unchanged.
- `replace_smb_framework.py`: checks the device platform, install name, exported interfaces and non-overwriting output path before replacing the framework in a new app copy.
- `ADDITIONAL-PERMISSIONS.md`: confirmed English/Chinese permissions for personal modifications and reverse engineering to debug them. It does not open-source the proprietary application.
- `SHA256.json`: hashes for every supplied file other than the manifest itself.

These materials apply only to build 33. A later external candidate needs its own executable, resources, source archive and hashes. No perpetual offer or three-year written offer is made by this package.

## Build and replace

Unzip the source archive. In its `AMSMB2` package directory, modify the library while preserving the public Swift/C interfaces. With Xcode and the visionOS SDK:

```sh
xcodebuild -scheme AMSMB2 -destination 'generic/platform=visionOS' -configuration Release -derivedDataPath /tmp/EnscenoLibraryBuild CODE_SIGNING_ALLOWED=NO build
python3 replace_smb_framework.py --app Unencrypted/ImmersiFin.app --framework /tmp/EnscenoLibraryBuild/Build/Products/Release-xros/PackageFrameworks/AMSMB2.framework --output /tmp/EnscenoModified.app --bundle-id your.own.ensceno-modified
```

The output path must not exist. The tool preserves the inputs and does not install or sign with a developer identity.

## Sign for your own Vision Pro

Use Xcode to create a visionOS development provisioning profile for the exact independent bundle ID above, your own team and your device. Use your own Apple Development identity. Keep the profile and signing key outside this distribution kit.

1. Embed that development profile as `EnscenoModified.app/embedded.mobileprovision`.
2. Create signing entitlements matching your own profile and bundle ID (application identifier, team identifier, development debugging and keychain groups if applicable); never reuse Ensceno's team/keychain identifiers. The app has no separately required private server credentials or proprietary licensing server.
3. Sign `Frameworks/AMSMB2.framework` first, then the outer app with those entitlements. `codesign --verify --deep --strict` checks the resulting signature; it cannot prove device installation or playback.
4. Install this independent development app through Xcode/Device Hub. Keep the original TestFlight app and its data. Sign in to your media source again in the independent copy.
5. Confirm the modified library actually runs, then browse one SMB folder and play one compatible short video. Do not infer success from exported symbols alone.

## Evidence and remaining boundary

A source copy containing a harmless verification marker was built for a physical visionOS device on 2026-10-31. It retained all 833 original exports, was substituted into an independent app copy and passed strict ad-hoc signature checks. The application's `__TEXT,__text` machine code matched the original. This validation copy is not the unmodified binary distributed in this kit.

The physical Vision Pro was unavailable. Modified-library execution, SMB browse/play and development signing for the independent identity remain pending. The original build 33 archive and the previous kit's 20 hashed files were unchanged. No private signing material or media-source account is included.

Support: ensceno.app@outlook.com
