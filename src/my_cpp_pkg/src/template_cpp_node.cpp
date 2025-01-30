#include "rclcpp/rclcpp.hpp"

class MyNodeName : public rclcpp::Node //MODIFY NAME
{
public:
    MyNodeName() : Node("node name") //MODIFY NAME
    {
    }

private:
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyNodeName>(); //MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}