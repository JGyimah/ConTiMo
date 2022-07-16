#include <pluginlib/class_list_macros.h>
#include "../../include/motivml_ros/plugin_base.h"
#include "../../include/motivml_ros/motivml_plugins.h"

//Static Late and Dynamic binding of plugins to plugin interface through pluginlib export

PLUGINLIB_EXPORT_CLASS(motivml_plugins::Slam, plugin_base::PluginInterface)

PLUGINLIB_EXPORT_CLASS(motivml_plugins::Hands, plugin_base::PluginInterface)

PLUGINLIB_EXPORT_CLASS(motivml_plugins::Pointscloud, plugin_base::PluginInterface)

PLUGINLIB_EXPORT_CLASS(static_integration::Amclros, static_base::StaticInterface)



