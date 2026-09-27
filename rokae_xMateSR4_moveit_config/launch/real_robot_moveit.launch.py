"""
xMateSR4 真机 MoveIt + RViz（第二步；不启动 ros2_control / robot_state_publisher）

前置：
  1) RobotAssist 已退出；本机可 ping 控制器。
  2) 已先启动硬件栈，例如：
       ros2 launch rokae_hardware real_moveit.launch.py \\
         robot_type:=SR4 robot_ip:=192.168.2.160 local_ip:=192.168.2.161 use_sim_time:=false
     此时应仅有 /controller_manager 与 /robot_state_publisher。

本 launch 只启动 move_group + rviz2，Plan & Execute 使用已激活的 arm_controller。

示例:
  ros2 launch rokae_xMateSR4_moveit_config real_robot_moveit.launch.py \\
    robot_ip:=192.168.2.160 local_ip:=192.168.2.161
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    hardware_share = get_package_share_directory("rokae_hardware")

    robot_ip = LaunchConfiguration("robot_ip")
    local_ip = LaunchConfiguration("local_ip")
    use_sim_time = LaunchConfiguration("use_sim_time")
    velocity_scaling = LaunchConfiguration("velocity_scaling")
    acceleration_scaling = LaunchConfiguration("acceleration_scaling")

    moveit_rviz_only = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(hardware_share, "launch", "xMate_moveit_config.launch.py")
        ),
        launch_arguments={
            "robot_type": "SR4",
            "robot_ip": robot_ip,
            "local_ip": local_ip,
            "use_fake_hardware": "false",
            "use_sim_time": use_sim_time,
            "velocity_scaling": velocity_scaling,
            "acceleration_scaling": acceleration_scaling,
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "robot_ip",
                default_value="192.168.2.160",
                description="Rokae controller IP（与 xacro / MoveIt 模型一致，不重复连 SDK）",
            ),
            DeclareLaunchArgument(
                "local_ip",
                default_value="192.168.2.161",
                description="本机在机器人网段的 IP",
            ),
            DeclareLaunchArgument("use_sim_time", default_value="false"),
            DeclareLaunchArgument("velocity_scaling", default_value="0.15"),
            DeclareLaunchArgument("acceleration_scaling", default_value="0.15"),
            moveit_rviz_only,
        ]
    )
