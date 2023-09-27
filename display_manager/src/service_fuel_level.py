from time import sleep

def service_fuel_level_main(queue_tx, queue_rx):
    ## FIXME REMOVE: the following is just for demo
    # Actual implementation should read from rabbitmq & integrate to get fuel level,
    # As well as save this info to a file periodically to avoid loss of power induced data loss
    fuel_level = 85
    while 1:
        sleep(1) # sleep for 1s
        # If fuel level reset was requested
        if not queue_rx.empty():
            fuel_level = queue_rx.get()
        # Put the new fuel level out
        queue_tx.put(fuel_level)
        # Iterate to show usage
        if fuel_level > 0:
            fuel_level = fuel_level - 1
        else:
            fuel_level = 100
