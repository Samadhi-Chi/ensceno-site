# Ensceno 1.0 (34) · SMB replacement materials

This download matches the visionOS 1.0 (34) candidate. Check the version and build in Ensceno before choosing a kit. The outer ZIP digest is in the public version manifest. SHA256.json lists the digest of each payload file.

- Unencrypted/ImmersiFin.app contains the unsigned release executable and its resources from the build 34 archive.
- SMBDependencySources.zip contains the exact bundled AMSMB2/libsmb2 source, notices and package build instructions.
- ThirdPartyNotices.txt and ADDITIONAL-PERMISSIONS.md contain the complete notices and the developer's supplemental permission for users to modify their own copy and debug those modifications.
- replace_smb_framework.py checks the replacement's platform and exported symbols and writes a separate application copy.

## Build the library

Extract SMBDependencySources.zip. In the extracted AMSMB2 package directory, make your changes while preserving the public interfaces, then build for a physical Vision Pro using Xcode and the visionOS SDK.

```sh
xcodebuild -scheme AMSMB2 -destination 'generic/platform=visionOS' -configuration Release -derivedDataPath /tmp/EnscenoLibraryBuild CODE_SIGNING_ALLOWED=NO build
```

From the directory containing this README, use a new output path and your own independent bundle identifier.

```sh
python3 replace_smb_framework.py --app Unencrypted/ImmersiFin.app --framework /tmp/EnscenoLibraryBuild/Build/Products/Release-xros/PackageFrameworks/AMSMB2.framework --output /tmp/EnscenoModified.app --bundle-id your.own.ensceno-modified
```

## Sign and run on your device

1. Obtain an Apple Development identity and a visionOS development profile for your team, bundle ID and Vision Pro. Copy that profile to EnscenoModified.app/embedded.mobileprovision.
2. Use signing entitlements matching that profile and independent bundle ID, including its application identifier, team identifier, development debugging and own keychain group as applicable.
3. Sign Frameworks/AMSMB2.framework with your identity, then sign the outer app with the matching entitlements. Verify the result with codesign --verify --deep --strict.
4. Install the copy through Xcode on your Vision Pro, open it and sign in to your test share. Confirm your library change executes and browse and play a compatible short movie.

## 中文

本材料对应入境 1.0（34）。解压 SMBDependencySources.zip，在 AMSMB2 包目录中修改库并使用上面的命令针对 visionOS 实机构建。在本说明所在目录运行替换工具，输出到一个新的路径，指定自己的独立应用标识。用自己的开发证书、设备描述文件和相符的权限先签内部框架，再签外层应用。可在 Xcode 安装独立副本，连接自己的测试共享并验证实际运行效果。原版与独立副本可同时安装。

工程支持和反馈请联系 ensceno.app@outlook.com。Supplemental permissions are included in English and Chinese.
