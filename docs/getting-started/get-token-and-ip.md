# Get the token and the IP address

[Home](../../README.md) / [Getting started](index.md) / Token and IP

Local control uses two values per robot: the **IP address** on your network and the **device token** (32 hex characters, the key from which the packet encryption is derived, see [miIO protocol](../concepts/miio-protocol.md#encryption)). Everything on this page is external, unverified knowledge: the plugin bundles do not contain tokens or the discovery procedure.

## IP address

- Look the robot up in your router's DHCP client list (hostname usually starts with `rockrobo` or `roborock`) and give it a fixed lease.
- The robot must be reachable from the machine that sends the commands over UDP port `54321` (the miIO port, ⚪ Legacy [miIO protocol](../concepts/miio-protocol.md)). Guest networks, VLANs and "client isolation" on the access point block this.

## Token

Options that existed at the time of writing (external, check each project's own instructions):

- Query your Xiaomi account through the Mi Home cloud and read the token of the device: the python-miio project and the community tool "Xiaomi-cloud-tokens-extractor" do this.
- Read the token from an Android Mi Home backup or from the app's local database (works only with older app versions).
- A robot that was just reset and not yet bound to an account answers the "hello" packet with its token (⚪ Legacy [miIO protocol](../concepts/miio-protocol.md#initial-handshake-smartconnect); newer firmware reveals it only in this state). Resetting binds you to the pairing process again, so use it only if you accept that.

Treat the token like a password: with it anyone on your network can control the robot. Never publish it (this repository's documentation uses placeholders).

## Check that the values work

Send a status request ([first command](first-command.md)). A wrong token produces no reply at all (the robot ignores packets it cannot decrypt).

## See also

- [Send your first command](first-command.md)
- [Troubleshooting](troubleshooting.md)
