# VMware ESXi Host Backups Python Script
<br>
This script by default will backup VMware ESXI host configurations to a file and if desired copy to TFTP server<br>
<br>
Author - Nick Moody - netassured.co.uk
<br>
Last Updated 19th May 2018<br>
<br>
<b>Requirements:</b>
<br>
1) VMware VCli installed - https://code.vmware.com/tool/vsphere-cli/6.5<br>
2) Intially connect to the host to retrieve the thumbprint<br>
3) TFTP server to send the running configs too<br>
<br>
Known limitations:<br>
TFTP is not encrypted so only execute this script on a dedicated management network or over a VPN.
<br>
This script backs up the host configuration only it does not backup the VM's running on the host. You will
need another backup solution for the VM's https://netassured.co.uk/implementing-vm-backup-solution-home-lab
