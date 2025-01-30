#include "rclcpp/rclcpp.hpp"

class MyNode : public rclcpp::Node
{
public:
    MyNode() : Node("cpp_test"), counter_(0) // write constructor and initialize the node with the node name "cpp_test"
    {
        RCLCPP_INFO(this->get_logger(), "Hello Cpp Node");

        //create timer
        timer_ = this->create_wall_timer(std::chrono::seconds(1),
                                         std::bind(&MyNode::timercallback, this));
    }

private:
    void timercallback()
    {
        counter_ ++;
        RCLCPP_INFO(this->get_logger(), "Hello %d", counter_); //print "Hello" on cmd
    }

    rclcpp::TimerBase::SharedPtr timer_;
    int counter_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv); // initialize ROS2 communication
    //------------------------------------------------------
    // auto node = std::make_shared<rclcpp::Node>("cpp_test"); //create node name (shared pointer)
    // RCLCPP_INFO(node->get_logger(), "Hello Cpp Node"); //print "Hello world" in Ros2
    //------------------------------------------------------
    auto node = std::make_shared<MyNode>(); // use oop instead
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}