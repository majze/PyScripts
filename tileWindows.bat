<# :
:: Based on https://gist.github.com/coldnebo/1148334
:: Converted to a batch/powershell hybrid via http://www.dostips.com/forum/viewtopic.php?p=37780#p37780
:: Array comparison from http://stackoverflow.com/a/6368667/4158862
@echo off
setlocal
set "POWERSHELL_BAT_ARGS=%*"
if defined POWERSHELL_BAT_ARGS set "POWERSHELL_BAT_ARGS=%POWERSHELL_BAT_ARGS:"=\"%"
endlocal & powershell -NoLogo -NoProfile -Command "$_ = $input; Invoke-Expression $( '$input = $_; $_ = \"\"; $args = @( &{ $args } %POWERSHELL_BAT_ARGS% );' + [String]::Join( [char]10, $( Get-Content \"%~f0\" ) ) )"
goto :EOF
#>

# Create an instance of the Win32 API object to handle and manipulate windows
Add-Type @"
  using System;
  using System.Runtime.InteropServices;

  public class Win32 {
    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
  }
"@

# Get a list of existing Explorer Windows
$previous_array = @()
$shell_object = New-Object -COM 'Shell.Application'

foreach($old_window in $shell_object.Windows())
{
    $previous_array += $old_window.HWND
}

# Open four more Explorer Windows in the current directory
explorer "\\location1"
sleep 1
explorer "\\location2"
sleep 1
explorer "\\location3"
sleep 1
explorer "\\location4"

# Pause for 1 second so that the windows have time to finish opening
sleep 1

# Get the list of new Explorer Windows
$new_array = @()
foreach($new_window in $shell_object.Windows())
{
    $new_array += $new_window.HWND
}

# Compare the two arrays and only process the new windows
$only_new = Compare-Object -ReferenceObject $previous_array -DifferenceObject $new_array -PassThru

# MoveWindow takes HWND value, X-position on screen, Y-position on screen, window width, and window height
# I've just hard-coded the values, adjust them to suit your needs
# You may need an offset such as x-10
[Win32]::MoveWindow($only_new[0],0-10,0,1100,600,$true) 
[Win32]::MoveWindow($only_new[1],1470,0,1100,600,$true)
[Win32]::MoveWindow($only_new[2],0-10,820-10,1100,600,$true)
[Win32]::MoveWindow($only_new[3],1470,820-10,1100,600,$true)