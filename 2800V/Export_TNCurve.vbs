'---------------------------------------------------------------------
'Name: Export_TNCurve.vbs
'Menu-en: 
'Type: VBScript
'Create: February 10, 2024 JSOL Corporation
'Comment-en: 
'---------------------------------------------------------------------
' JMAG-Designer Script
' Set designer = CreateObject("designer.Application") 
' designer.Show()

' ���� ��ũ��Ʈ�� ���丮�� ��� �Լ�
Function GetCurrentDirectory()
    Dim fso, currentScriptPath
    Set fso = CreateObject("Scripting.FileSystemObject")
    ' WScript.ScriptFullName�� ���� ���� ���� ��ũ��Ʈ�� ��ü ��θ� ��ȯ�մϴ�.
    currentScriptPath = fso.GetParentFolderName(WScript.ScriptFullName)
    GetCurrentDirectory = currentScriptPath
End Function

' ���� ���丮 ��θ� ������ ����
Dim currentDirectory
currentDirectory = GetCurrentDirectory()

' ����� �޽��� �ڽ��� ǥ��
MsgBox "���� ������ ��δ� " & currentDirectory & " �Դϴ�."

Set app = designer
Call app.SetCurrentStudy(5)
Call app.GetModel(0).GetStudy(5).GetEfficiencyMapPlot(0).ExportDataFromRange(2, "G:/01. project/01. rotem_EMU/01_LastVersion/01_projectfile/231130~/01_EfficiencyMap.csv", 0, 4400, 201, 0, 3400, 201)
Call app.GetModel(0).GetStudy(5).GetEfficiencyMapPlot(0).ExportDataFromRange(14, "G:/01. project/01. rotem_EMU/01_LastVersion/01_projectfile/231130~/02_Lamda_d.csv", 0, 4400, 201, 0, 3400, 201)
Call app.GetModel(0).GetStudy(5).GetEfficiencyMapPlot(0).ExportDataFromRange(15, "G:/01. project/01. rotem_EMU/01_LastVersion/01_projectfile/231130~/03_Lamda_q.csv", 0, 4400, 201, 0, 3400, 201)
Call app.GetModel(0).GetStudy(5).GetEfficiencyMapPlot(0).ExportDataFromRange(4, "G:/01. project/01. rotem_EMU/01_LastVersion/01_projectfile/231130~/04_Current_d.csv", 0, 4400, 201, 0, 3400, 201)
Call app.GetModel(0).GetStudy(5).GetEfficiencyMapPlot(0).ExportDataFromRange(5, "G:/01. project/01. rotem_EMU/01_LastVersion/01_projectfile/231130~/05_Current_q.csv", 0, 4400, 201, 0, 3400, 201)
Call app.GetModel(0).GetStudy(5).GetEfficiencyMapPlot(0).ExportDataFromRange(26, "G:/01. project/01. rotem_EMU/01_LastVersion/01_projectfile/231130~/06_PowerFactor.csv", 0, 4400, 201, 0, 3400, 201)
Call app.GetModel(0).GetStudy(5).GetEfficiencyMapPlot(0).ExportDataFromRange(17, "G:/01. project/01. rotem_EMU/01_LastVersion/01_projectfile/231130~/07_LoadAngle.csv", 0, 4400, 201, 0, 3400, 201)
Call app.GetModel(0).GetStudy(5).GetEfficiencyMapPlot(0).ExportDataFromRange(23, "G:/01. project/01. rotem_EMU/01_LastVersion/01_projectfile/231130~/08_TorqueRipple.csv", 0, 4400, 201, 0, 3400, 201)
Call app.GetModel(0).GetStudy(5).GetEfficiencyMapPlot(0).ExportDataFromRange(16, "G:/01. project/01. rotem_EMU/01_LastVersion/01_projectfile/231130~/09_Voltage.csv", 0, 4400, 201, 0, 3400, 201)
