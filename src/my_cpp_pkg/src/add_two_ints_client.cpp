#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

class AddTwoIntsClientNode : public rclcpp::Node //MODIFY NAME
{
public:
    AddTwoIntsClientNode() : Node("add_two_ints_client") //MODIFY NAME
    {
        // call function "callAddTwoIntsService" and initialize a and b
        
        // thread1_ = std::thread(std::bind(&AddTwoIntsClientNode::callAddTwoIntsService, this, 1, 4)); //for call one time
        threads_.push_back(std::thread(std::bind(&AddTwoIntsClientNode::callAddTwoIntsService, this, 1, 4))); //for call multiple time
        threads_.push_back(std::thread(std::bind(&AddTwoIntsClientNode::callAddTwoIntsService, this, 5, 2))); //for call multiple time
        threads_.push_back(std::thread(std::bind(&AddTwoIntsClientNode::callAddTwoIntsService, this, 6, 9))); //for call multiple time

    }
    
// This part below can use for any of another service client.(like template of service client)
//------------------------------------------------------------------------------------------------------------------------------
    // create function to call service
    void callAddTwoIntsService(int a, int b)
    {
        // create client
        auto client = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints"); //(service name)

        // wait server on
        while(!client->wait_for_service(std::chrono::seconds(1))) //if server not on after one second it will return false.
        {
            RCLCPP_WARN(this->get_logger(), "Waiting for the server to be up...");
        }

        // create request
        auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
        request->a = a;
        request->b = b;

        // send request and get responce in "future" (call server).
        auto future = client->async_send_request(request);

        // wait for the response
        try
        {
            auto response = future.get(); // "future.get()" will pause program here and wait until future get a response
            RCLCPP_INFO(this->get_logger(), "%d +%d = %d", (int)a, (int)b, (int)response->sum);
        }
        catch(const std::exception &e) // if try fails, it willthrow the exception in catch here.
        {
            RCLCPP_ERROR(this->get_logger(), "Service call failed");
        }
    }
//------------------------------------------------------------------------------------------------------------------------------
private:
    // create new thread for potect blocking from "future.get()" and it will can"t "spin(node)" in main function
    
    // std::thread thread1_;   // This can initialize a and b one time
    std::vector<std::thread> threads_; // This can initialize a and b multiple time

};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<AddTwoIntsClientNode>(); //MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}