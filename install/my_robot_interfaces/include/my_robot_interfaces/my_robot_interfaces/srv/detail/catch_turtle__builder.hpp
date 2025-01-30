// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_robot_interfaces:srv/CatchTurtle.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__SRV__DETAIL__CATCH_TURTLE__BUILDER_HPP_
#define MY_ROBOT_INTERFACES__SRV__DETAIL__CATCH_TURTLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_robot_interfaces/srv/detail/catch_turtle__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_CatchTurtle_Request_name_turtle_caught
{
public:
  Init_CatchTurtle_Request_name_turtle_caught()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::my_robot_interfaces::srv::CatchTurtle_Request name_turtle_caught(::my_robot_interfaces::srv::CatchTurtle_Request::_name_turtle_caught_type arg)
  {
    msg_.name_turtle_caught = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::srv::CatchTurtle_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::srv::CatchTurtle_Request>()
{
  return my_robot_interfaces::srv::builder::Init_CatchTurtle_Request_name_turtle_caught();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_CatchTurtle_Response_name_res
{
public:
  Init_CatchTurtle_Response_name_res()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::my_robot_interfaces::srv::CatchTurtle_Response name_res(::my_robot_interfaces::srv::CatchTurtle_Response::_name_res_type arg)
  {
    msg_.name_res = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::srv::CatchTurtle_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::srv::CatchTurtle_Response>()
{
  return my_robot_interfaces::srv::builder::Init_CatchTurtle_Response_name_res();
}

}  // namespace my_robot_interfaces

#endif  // MY_ROBOT_INTERFACES__SRV__DETAIL__CATCH_TURTLE__BUILDER_HPP_
