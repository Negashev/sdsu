# Schedule docker service upgrade

Service for upgrade docker service to image (the newest) with load from regitsry


`SERVICE_IMAGE` - image for update

`SERVICE_ID` - ID or name of the service

`SERVICE_INTERVAL_UPGRADE` - time in seconds for scheduler

## using

Update service test-service every 1 hour to latest `nginx:alpine `

```bash
docker run -it
 -e SERVICE_ID=test-service
 -e SERVICE_IMAGE=nginx:alpine  
 -e SERVICE_INTERVAL_UPGRADE=3600
 -v /var/run/docker.sock:/var/run/docker.sock
 negash/sdsu
```