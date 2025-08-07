#ifndef MIDASINTERFACE_REAL_ROBOT_H
#define MIDASINTERFACE_REAL_ROBOT_H

#include <iostream>
#include <boost/asio.hpp>
#include <nlohmann/json.hpp>

#include "rclcpp/time.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_lifecycle/state.hpp"
#include "std_msgs/msg/float64.hpp"

#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "hardware_interface/types/hardware_interface_type_values.hpp"

using hardware_interface::CallbackReturn;
using hardware_interface::return_type;
using nlohmann::json;

using namespace boost::asio;
using namespace std;

class MidasInterface : public hardware_interface::SystemInterface
{
	public:
        RCLCPP_SHARED_PTR_DEFINITIONS(MidasInterface)

    	CallbackReturn on_init(const hardware_interface::HardwareInfo &info) override;

        CallbackReturn on_activate(const rclcpp_lifecycle::State& /*previous_state*/) override;

        CallbackReturn on_deactivate(const rclcpp_lifecycle::State& /*previous_state*/) override;

		vector<hardware_interface::StateInterface> export_state_interfaces() override;

		vector<hardware_interface::CommandInterface> export_command_interfaces() override;

        return_type read(const rclcpp::Time& /*time*/, const rclcpp::Duration& /*period*/) override;

        return_type write(const rclcpp::Time& /*time*/, const rclcpp::Duration& /*period*/) override;

	private:
        rclcpp::Logger logger_{rclcpp::get_logger("MidasInterface")};

	    std::chrono::time_point<std::chrono::system_clock> time_;

	    hardware_interface::HardwareInfo info_;

	    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr sub_pos_msg;

	    double latest_value_ = 0.0;

		io_service io_;

		unique_ptr<serial_port> serial_;

		string port_ = "/dev/ttyUSB0";

		int baud_rate_ = 9600;

		vector<string> motor_name_;

		vector<double> motor_pos_;

		vector<double> motor_vel_;

		vector<double> motor_cmd_;
};

#endif