#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"


int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("add_two_ints_client_no_oop"); //MODIFY NAME

    // create client
    auto client = node->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints"); //(service name)

    // wait server on
    while(!client->wait_for_service(std::chrono::seconds(1))) //if server not on after one second it will return false.
    {
        RCLCPP_WARN(node->get_logger(), "Waiting for the server to be up...");
    }
    // This line server on
    // create request
    auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
    request->a = 3;
    request->b = 8;

    // send request and get responce in "future" (call server).
    auto future = client->async_send_request(request);

    // this function wait for the response(future) and node, it will spin until future get response complete.
    if (rclcpp::spin_until_future_complete(node, future) == rclcpp::FutureReturnCode::SUCCESS)
    {
        // This line future get response complete
        RCLCPP_INFO(node->get_logger(), "%d + %d = %d", (int)request->a, (int)request->b, (int)future.get()->sum);
    }
    else
    {
        RCLCPP_ERROR(node->get_logger(), "Error whilr calling service");
    }

    rclcpp::shutdown();
    return 0;
}