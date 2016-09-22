SetBatchLines,-1
#NoEnv
Coordmode,Mouse,Screen
MonitorMouseMovement := True
SetTimer,CheckMouseMovement,-1
Return

*~1::
	MonitorMouseMovement := True
	SetTimer,CheckMouseMovement,-1
Return

*~2::
	MonitorMouseMovement := False
	Sleep,-1
	ToolTip
Return

CheckMouseMovement()
{
	Global MonitorMouseMovement
	Static FirstRun = 1, OldX, OldY
	
	If (FirstRun){
		MouseGetPos,OldX,OldY
		FirstRun := False
		Return
	}
	
	If (!MonitorMouseMovement)
		Return 1
	
	MouseGetPos,CurrentX,CurrentY
	
	If (CurrentX != OldX Or CurrentY != OldY){
		ToolTip,Mouse Moved to: %CurrentX%`, %CurrentY%
		OldX := CurrentX, OldY := CurrentY
	} Else
		ToolTip
}

CheckMouseMovement:
	If (!CheckMouseMovement())
		SetTimer,CheckMouseMovement,-1
Return