# generated from colcon_powershell/shell/template/prefix_chain.ps1.em

# This script extends the environment with the environment of other prefix
# paths which were sourced when this file was generated as well as all packages
# contained in this prefix path.

# function to source another script with conditional trace output
# first argument: the path of the script
function _colcon_prefix_chain_powershell_source_script {
  param (
    $_colcon_prefix_chain_powershell_source_script_param
  )
  # source script with conditional trace output
  if (Test-Path $_colcon_prefix_chain_powershell_source_script_param) {
    if ($env:COLCON_TRACE) {
      echo ". '$_colcon_prefix_chain_powershell_source_script_param'"
    }
    . "$_colcon_prefix_chain_powershell_source_script_param"
  } else {
    Write-Error "not found: '$_colcon_prefix_chain_powershell_source_script_param'"
  }
}

# source chained prefixes
_colcon_prefix_chain_powershell_source_script "/opt/ros/humble\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/carver_urdf/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/FUN4/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/microros_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/exam1/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/RoboticsDev2024/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/turtlebot3_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/MyRos2_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/FUN4_6509/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/dev_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/carver_imu_msg/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/solar_ws/install\local_setup.ps1"
_colcon_prefix_chain_powershell_source_script "/home/gun/CARVER_WS/install\local_setup.ps1"

# source this prefix
$env:COLCON_CURRENT_PREFIX=(Split-Path $PSCommandPath -Parent)
_colcon_prefix_chain_powershell_source_script "$env:COLCON_CURRENT_PREFIX\local_setup.ps1"
