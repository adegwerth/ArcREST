import arcrest

if __name__ == '__main__':
    """
    Creates a GPService from a ArcGIS Toolbox
    """

    username = ""
    password = ""
    url = "http://<server>:6080/arcgis"

    # create a security handler
    sh = arcrest.AGSTokenSecurityHandler(
        username=username,
        password=password,
        token_url=url + "/tokens/",
        org_url=url)

    # create the server object
    server = arcrest.ags.server.Server(
        url=url,
        securityHandler=sh)

    adminAGS = server.admin

    # get the server dirs
    srv_dirs = adminAGS.system.serverDirectories
    ags_jobs_dir = None
    ags_out_dir = None
    for srv_dir in srv_dirs:
        if srv_dir.name.lower() == "arcgisoutput":
            ags_out_dir = srv_dir
            continue
        if srv_dir.name.lower() == "arcgisjobs":
            ags_jobs_dir = srv_dir
            continue

    service_name = "myToolbox"
    service_description = "Description"
    service_folder = "Folder"
    # toolbox must be exists local on server or on file share
    toolbox_path = r"c:\myToolboxes\myToolbox.pyt"

    # service definition template
    service_def = {
        "serviceName": service_name,
        "type": "GPServer",
        "description": service_description,
        "capabilities": "null",
        "provider": "ArcObjects",
        "clusterName": "default",
        "minInstancesPerNode": 0,
        "maxInstancesPerNode": 3,
        "instancesPerContainer": 1,
        "maxWaitTime": 60,
        "maxStartupTime": 300,
        "maxIdleTime": 180,
        "maxUsageTime": 3000000,
        "loadBalancing": "ROUND_ROBIN",
        "isolationLevel": "HIGH",
        "configuredState": "STARTED",
        "recycleInterval": 24,
        "recycleStartTime": "00:00",
        "keepAliveInterval": -1,
        "private": False,
        "isDefault": False,  # True -> service can't be deleted
        "maxUploadFileSize": 0,
        "allowedUploadFileTypes": "",
        "properties": {
            "outputDir": ags_out_dir.physicalPath,
            "virtualOutputDir": ags_out_dir.virtualPath,
            "showMessages": "Info",
            "toolbox": toolbox_path,
            "jobsDirectory": ags_jobs_dir.physicalPath,
            "executionType": "Asynchronous",
            "jobsVirtualDirectory": ags_jobs_dir.virtualPath,
            "maximumRecords": "1000"
        },
        "extensions": [],
        "datasets": []
    }

    srv = adminAGS.services
    if service_folder != "":
        # set the current folder
        srv.folderName = service_folder

    res = srv.createService(service_def)
    if 'status' in res:
        if res['status'] != 'success':
            print "Error on create service."
            print res
