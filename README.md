# Afterburn

Afterburn can automate some tasks after a uTorrent download is complete. Currently the scripts is only tested with uTorrent Server. Once a download is one the script gets called and can take the following actions:
 - Remove the download from the seeding queue
 - Send an email
 - Move the download to a share, mediaplayer or external storage

## Installation

The program runs to separate scripts. The **notifier** is used to send mails and remove torrents from the queue while the **transporter** moves downloads to another location.
First clone the repository
```
git clone https://github.com/yorickdewid/utserver-Afterburn.git
```
Change the settings in the `settings.conf`. See the list of options below.

### Notifier

To run the script after each download goto: *uTorrent* > *Settings* > *Advanced* > *Run Program*. Add the full path to the notifiction script (`notify.py`). Give the title of the torrent, status and info hash as parameters. For example:
```
/opt/utserver-Afterburn/notify.py -n '%N' -s '%M' -i '%I'
```
Now click one *Save settings* and you're good to go. The notification script doesn't require root privileges and can be run under any user.

### Transporter

Downloads cannot be written to an external location from uTorrent Server itself. Due to privileges and the limitations of some protocols a seperate process must handle this. In order make this work it's recommended to run this as root. Add the following to the cron config for root
```
0,30 * * * * /opt/utserver-Afterburn/transfer.py
```
This runs the transfer script every half hour. For directories and configuration see below.

## Config
The configuration file (`settings.conf`) must be present in the same directory as the program.
```
[Mail]
notice = true                    # Send email after download is compele? (true|false)
name = <user>                    # Name of the reveiver
from = <mail>                    # Sending email address
receiver = <mail>                # Receivers email address
SMTP = <server>                  # SMTP server, can include port number (smtp.gmail.com:465)
username = <SMTP username>       # Login user for email account (optional)
password = <SMTP password>       # Passwor for login user (optional)

[Directory]
destination = /mnt/media-share/  # Destination for downloads
source = /opt/utorrent/complete/ # Source directory (this is where complete downloads are moved from uTorrent)

[uTorrent]
remove = true                    # Remove torrent from queue after download is complete (true|false)
host = localhost                 # Host for the uTorrent Server API (default: localhost)
port = 8080                      # Port for the uTorrent Server API (default: 8080)
```

## License

GPL &copy; 2015
