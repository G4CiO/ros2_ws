#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp" //don't forget to add depend package in "package.xml" and CMakeList.txt

class NumberPublisherNode : public rclcpp::Node
{
public:
    NumberPublisherNode() : Node("robot_news_station"), robot_name_("ZEUS")
    {
        publisher_ = this->create_publisher<example_interfaces::msg::String>("robot_news", 10);

        timer_ = this->create_wall_timer(std::chrono::milliseconds(500),
                                         std::bind(&NumberPublisherNode::publishNumber, this));

        RCLCPP_INFO(this->get_logger(), "Robot News Station has been stared.");
    }

private:
    void publishNumber()
    {
        // create empty string object
        auto msg = example_interfaces::msg::String();
        // set data
        msg.data = ("Hi my name is ") + robot_name_ + std::string(" from Real steel");
        // publish message
        publisher_->publish(msg);
    }

    std::string robot_name_;

    // declare the publisher
    rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;

    // create timer
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NumberPublisherNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}