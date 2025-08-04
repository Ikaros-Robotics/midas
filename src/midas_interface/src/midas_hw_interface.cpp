#include "midas_interface/midas_hw_interface.h"

/* Called once during initialization. */
CallbackReturn MidasInterface::on_init(const hardware_interface::HardwareInfo &info)
{

  if (hardware_interface::SystemInterface::on_init(info) != CallbackReturn::SUCCESS)
  {
      return CallbackReturn::ERROR;
  }

  RCLCPP_INFO(logger_, "Configuring...");

  time_ = std::chrono::system_clock::now();
  info_ = info;

  //Gets motor name from URDF info published by robot_state_publisher, if it exists
  //Everything gets initialized to 0
  for(const auto &joint : info_.joints)
  {
    motor_name_.emplace_back(joint.name);
    motor_pos_.emplace_back(0.0);
    motor_cmd_.emplace_back(0.0);
  }

  //Set up the serial connection
	try
  {
	  serial_ = make_unique<serial_port>(io_, port_);
	  serial_->set_option(serial_port_base::baud_rate(baud_rate_));
	  RCLCPP_INFO(logger_, "Serial Port Opened");
	} catch (std::exception& e) {
	  RCLCPP_ERROR(logger_, "Serial Port Error: %s", e.what());
	  return CallbackReturn::ERROR;
	}

  RCLCPP_INFO(logger_, "Finished Configuration");
  return CallbackReturn::SUCCESS;
}


vector<hardware_interface::StateInterface> MidasInterface::export_state_interfaces()
{
  //set up state interfaces to monitor motor velocity and position
  vector<hardware_interface::StateInterface> state_interfaces;

  //hardware_interface::StateInterface(name, interface type, &value)
  for(size_t i = 0; i < motor_name_.size(); ++i)
  {
    state_interfaces.emplace_back(hardware_interface::StateInterface(motor_name_[i], hardware_interface::HW_IF_POSITION, &motor_pos_[i]));
  }

  return state_interfaces;
}


vector<hardware_interface::CommandInterface> MidasInterface::export_command_interfaces()
{
  //set up a command interface to set desired position for each motor
  vector<hardware_interface::CommandInterface> command_interfaces;

  //hardware_interface::CommandInterface(name, interface type, &value)
  for(size_t i = 0; i < motor_name_.size(); ++i)
  {
    command_interfaces.emplace_back(hardware_interface::CommandInterface(motor_name_[i], hardware_interface::HW_IF_POSITION, &motor_cmd_[i]));
  }

  return command_interfaces;
}


CallbackReturn MidasInterface::on_activate(const rclcpp_lifecycle::State & /*&previous_state*/)
{
  RCLCPP_INFO(logger_, "Starting Controller...");
  return CallbackReturn::SUCCESS;
}


CallbackReturn MidasInterface::on_deactivate(const rclcpp_lifecycle::State & /*previous_state*/)
{
  RCLCPP_INFO(logger_, "Stopping Controller...");
  if (serial_ && serial_->is_open()){
    serial_->cancel();
    serial_.reset();
    RCLCPP_INFO(logger_, "Serial Port Closed");
  }
  return CallbackReturn::SUCCESS;
}


return_type MidasInterface::read(const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
{
  try {
    boost::asio::streambuf buf;
    boost::asio::read_until(*serial_, buf, '\n');
    std::istream is(&buf);
    std::string line;
    std::getline(is, line);

    json feedback = json::parse(line);

    for (size_t i = 0; i < motor_name_.size(); ++i) {
      std::string key = "J" + std::to_string(i + 1) + "POS";
      if (feedback.contains(key)) {
        float revolutions = feedback[key];
        float radians = revolutions * 2.0 * M_PI;
        motor_pos_[i] = radians;
        // Velocity is constant for now
      }
    }
  } catch (std::exception& e) {
    RCLCPP_ERROR(logger_, "Serial Read Error: %s", e.what());
    return return_type::ERROR;
  }

  return return_type::OK;
}


return_type MidasInterface::write(const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
{

  if (1==0)  //check connection
  {
    return return_type::ERROR;
  }
  
  //Building a JSON array to hold motor data
  json motor_data;
  motor_data["Motor Data"] = json::array();

  //Filling in the array
  for(size_t i = 0; i < motor_name_.size(); ++i){
    motor_data["Motor Data"].push_back({
      { "name", motor_name_[i] },
      { "pos", motor_pos_[i] },
    });
  };

  //Converts JSON into a plain text message
  string message = motor_data.dump() + "\n";

  //Write the message over serial
  try {
    boost::asio::write(*serial_, boost::asio::buffer(message));
  } catch (exception& e) {
    RCLCPP_ERROR(logger_, "Serial Write Error: %s", e.what());
    return return_type::ERROR;
  }

  return return_type::OK;
}


#include "pluginlib/class_list_macros.hpp"

PLUGINLIB_EXPORT_CLASS(
  MidasInterface,
  hardware_interface::SystemInterface
) 