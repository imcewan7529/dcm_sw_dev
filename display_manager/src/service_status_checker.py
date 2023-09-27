from time import sleep

def service_status_checker_main(queue_tx):
    # FIXME REMOVE: This is a temporary status manager,
    # must be replaced with actual status checking service.
    while 1:
        queue_tx.put("LOGGING")
        sleep(60)