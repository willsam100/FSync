# FSync
Sync files between two Synology NAS reading over FTPe

Simple script to sync (recusivly copy) files from one NAS to another. This is only useful if you have cheap NASs and a lot of data. More expensice NASs have FTP Clients.
Files that already exist, filename and size matches, will be skipped. 

Usage:

  enalbe FTP on source NAS
  
  enalbe ssh on target NAS
  
  Copy script to target NAS (update the target ip address in the source code)
  
  ssh into target NAS 
  
  python fsync.py source target
  
