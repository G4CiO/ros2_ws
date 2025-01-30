// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_robot_interfaces:srv/SetNoise.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__SRV__DETAIL__SET_NOISE__BUILDER_HPP_
#define MY_ROBOT_INTERFACES__SRV__DETAIL__SET_NOISE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_robot_interfaces/srv/detail/set_noise__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetNoise_Request_variance
{
public:
  explicit Init_SetNoise_Request_variance(::my_robot_interfaces::srv::SetNoise_Request & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::srv::SetNoise_Request variance(::my_robot_interfaces::srv::SetNoise_Request::_variance_type arg)
  {
    msg_.variance = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::srv::SetNoise_Request msg_;
};

class Init_SetNoise_Request_mean
{
public:
  Init_SetNoise_Request_mean()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetNoise_Request_variance mean(::my_robot_interfaces::srv::SetNoise_Request::_mean_type arg)
  {
    msg_.mean = std::move(arg);
    return Init_SetNoise_Request_variance(msg_);
  }

private:
  ::my_robot_interfaces::srv::SetNoise_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::srv::SetNoise_Request>()
{
  return my_robot_interfaces::srv::builder::Init_SetNoise_Request_mean();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::srv::SetNoise_Response>()
{
  return ::my_robot_interfaces::srv::SetNoise_Response(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace my_robot_interfaces

#endif  // MY_ROBOT_INTERFACES__SRV__DETAIL__SET_NOISE__BUILDER_HPP_
