#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp" //don't forget to add depend package in "package.xml" and CMakeList.txt

class NumberPublisherNode : public rclcpp::Node
{
public:
    NumberPublisherNode() : Node("number_publisher")
    {
        // Parameter
        // ----------------------------------------------------------------------------------------------------------------------
        // declare new parameter and set parameter
        this->declare_parameter("number_to_publish", 2); // (name_param, param default value) name of set and get parameter must be same
        this->declare_parameter("publish_frequency", 1000.0);

        // get parameter from the node
        number_ = this->get_parameter("number_to_publish").as_int(); // (name_param) ".as_..." for get value and "..." is type of value
        publisher_frequency_ = this->get_parameter("publish_frequency").as_double();
        // ----------------------------------------------------------------------------------------------------------------------

        publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number", 10);

        timer_ = this->create_wall_timer(std::chrono::milliseconds((int) (1000.0 / publisher_frequency_)),
                                         std::bind(&NumberPublisherNode::publishNumber, this));

        RCLCPP_INFO(this->get_logger(), "Number Publisher has been stared.");
    }

private:
    void publishNumber()
    {
        // create empty string object
        auto msg = example_interfaces::msg::Int64();
        // set data
        msg.data = number_;
        // publish message
        publisher_->publish(msg);
    }

    int number_;
    double publisher_frequency_;

    // declare the publisher
    rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;

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