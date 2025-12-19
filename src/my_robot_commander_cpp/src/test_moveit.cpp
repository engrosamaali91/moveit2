#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <thread>


int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("test_moveit_node");
    rclcpp::executors::SingleThreadedExecutor executor;
    executor.add_node(node);
    auto spinner = std::thread([&executor]() { executor.spin(); });


    // moveit
    auto arm = moveit::planning_interface::MoveGroupInterface(node, "arm");
    arm.setMaxVelocityScalingFactor(1.0);
    arm.setMaxAccelerationScalingFactor(1.0);

    // Named goal

    arm.setStartStateToCurrentState();
    arm.setNamedTarget("pose_1");

    moveit::planning_interface::MoveGroupInterface::Plan plan_1;
    bool success_1 = arm.plan(plan_1) == moveit::core::MoveItErrorCode::SUCCESS;
    if (success_1)
    {
        arm.execute(plan_1);
    }


    arm.setStartStateToCurrentState();
    arm.setNamedTarget("home");

    moveit::planning_interface::MoveGroupInterface::Plan plan_2;
    bool success_2 = arm.plan(plan_2) == moveit::core::MoveItErrorCode::SUCCESS;
    if (success_2)
    {
        arm.execute(plan_2);
    }

    rclcpp::shutdown();
    spinner.join();
    return 0;
}