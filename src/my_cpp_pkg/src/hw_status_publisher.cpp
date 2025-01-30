#include "rclcpp/rclcpp.hpp"
#include "my_robot_interfaces/msg/hardware_status.hpp"

class HardWareStatusPublisherNode : public rclcpp::Node
{
public:
    HardWareStatusPublisherNode() : Node("hardware_status_publisher")
    {

        publisher_ = this->create_publisher<my_robot_interfaces::msg::HardwareStatus>("hardware_status", 10);

        timer_ = this->create_wall_timer(std::chrono::milliseconds(500),
                                         std::bind(&HardWareStatusPublisherNode::publishHardWareStatus, this));

        RCLCPP_INFO(this->get_logger(), "Hardware status publisher has been stared.");
    }

private:
    void publishHardWareStatus()
    {
        // create empty string object
        auto msg = my_robot_interfaces::msg::HardwareStatus();
        // set data
        msg.temperature = 100;
        msg.are_motor_ready = false;
        msg.debug_message = "Motors are too hot!";
        // publish message
        publisher_->publish(msg);
    }

    // declare the publisher
    rclcpp::Publisher<my_robot_interfaces::msg::HardwareStatus>::SharedPtr publisher_;
    // create timer
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<HardWareStatusPublisherNode>(); //MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}