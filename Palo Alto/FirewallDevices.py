from panos.panorama import Panorama
from panos.devices import SystemSettings
from panos.policies import PreRulebase, SecurityRule
import getpass

#input username and password

username = input("enter your username")
password = getpass.getpass("Enter your password: ")

# Panorama Details

Pano = panorama("PanoramaIP", username, password)

# Searches for the devices on the panorama
devices = pano.refresh_devices(expand_vsys=False, include_device_group=False)
# Search for the rules on the pre-rulebase
pre_rulebase = pano.add(PreRulebase())
rules = SecurityRule.refreshall(pre_rulebase)

#Print each firewall Serial number and management IPs and version
for device in devices
  system_setting = device.find("", SystemSettings)
  print(f"{device.serial}{system_setting.hostname}{system_settings.ip_address}{device.version}")

# Print the firewall rules
for rule in rules:
  print(rule.name)
