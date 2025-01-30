#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

class SmartphoneNode : public rclcpp::Node
{
public:
    SmartphoneNode() : Node("smartphone")
    {
        //initialize sucscriber
        subscriber_ = this->create_subscription<example_interfaces::msg::String>(
                                 "robot_news", 10,
                                 std::bind(&SmartphoneNode::callbackRobotNews, this, std::placeholders::_1));
                                //(topic name, queue size, callback)
                                //std::placeholders is required for every parameter you have in a call back function
                                //if you have two parameters, it will be "std::placeholders::_2"

        RCLCPP_INFO(this->get_logger(), "Smartphone has been stared.");
    }

private:
    // This function callback when recevies a new message
    void callbackRobotNews(const example_interfaces::msg::String::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "%s", msg->data.c_str());
    }

    rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr subscriber_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SmartphoneNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}