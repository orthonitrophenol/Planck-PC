
Outfile "Planck Installer.exe"

InstallDir $PROGRAMFILES

RequestExecutionLevel admin

Section

    SetOutPath $INSTDIR

    File /r D:\Farhan\Code\projects\planck-pc\downloads\PlanckWindows
    FileOpen $0 "$INSTDIR\PlanckWindows\cache.json" w
    FileWrite $0 "{}"
    FileClose $0
    CreateShortcut "$SMPROGRAMS\Planck.lnk" "$INSTDIR\PlanckWindows\Planck.exe"

    WriteUninstaller $INSTDIR\PlanckWindows\Uninstaller.exe
    CreateShortcut "$SMPROGRAMS\Planck Uninstaller.lnk" "$INSTDIR\Uninstaller.exe"

SectionEnd

Section "Uninstall"

    Delete "$SMPROGRAMS\Planck.lnk"
    Delete "$SMPROGRAMS\Planck Uninstaller.lnk"
    Delete $INSTDIR\PlanckWindows

SectionEnd
