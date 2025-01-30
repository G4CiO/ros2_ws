#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"
#include "example_interfaces/srv/set_bool.hpp"

using std::placeholders::_1;
using std::placeholders::_2;

class NumberCounter : public rclcpp::Node
{
public:
    NumberCounter() : Node("number_counter"), counter_(0)
    {
        subscriber_ = this->create_subscription<example_interfaces::msg::Int64>(
                                 "number", 10,
                                 std::bind(&NumberCounter::callbackNumber, this, std::placeholders::_1));

        publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number_count", 10);

        // create initialize service server
        server_ = this->create_service<example_interfaces::srv::SetBool>(
            "reset_counter",
            std::bind(&NumberCounter::call_back_set_bool, this, _1, _2));

        RCLCPP_INFO(this->get_logger(), "Number Counter has been stared.");
    }

private:
    void callbackNumber(const example_interfaces::msg::Int64::SharedPtr msg)
    {
        counter_ += msg->data;
        // RCLCPP_INFO(this->get_logger(), "Counter: %ld", counter_);

        // create empty string object
        auto new_msg = example_interfaces::msg::Int64();
        // set data
        new_msg.data = counter_;
        // publish message
        publisher_->publish(new_msg);
    }

    void call_back_set_bool(const example_interfaces::srv::SetBool::Request::SharedPtr request,
                            const example_interfaces::srv::SetBool::Response::SharedPtr response)
    {
        // set counter_ = 0
        if (request->data)
        {
            counter_ = 0;
            RCLCPP_INFO(this->get_logger(), "Set Counter to 0");
            response->success = true;
            response->message = "Set Counter to 0 complete";
        }
        else
        {
            RCLCPP_INFO(this->get_logger(), "Nothing change in Counter");
            response->success = false;
            response->message = "Set Counter to 0 not complete";
        }

    }

    // declare the subscriber
    rclcpp::Subscription<example_interfaces::msg::Int64>::SharedPtr subscriber_;
    // declare the publisher
    rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;

    int64_t counter_;

    // create timer
    rclcpp::TimerBase::SharedPtr timer_;
    // create server variable as server_
    rclcpp::Service<example_interfaces::srv::SetBool>::SharedPtr server_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NumberCounter>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}