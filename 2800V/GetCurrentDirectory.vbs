' 현재 스크립트의 디렉토리를 얻는 함수
Function GetCurrentDirectory()
    Dim fso, currentScriptPath
    Set fso = CreateObject("Scripting.FileSystemObject")
    ' WScript.ScriptFullName은 현재 실행 중인 스크립트의 전체 경로를 반환합니다.
    currentScriptPath = fso.GetParentFolderName(WScript.ScriptFullName)
    GetCurrentDirectory = currentScriptPath
End Function

' 현재 디렉토리 경로를 변수에 저장
Dim currentDirectory
currentDirectory = GetCurrentDirectory()

' 결과를 메시지 박스로 표시
MsgBox "현재 폴더의 경로는 " & currentDirectory & " 입니다."