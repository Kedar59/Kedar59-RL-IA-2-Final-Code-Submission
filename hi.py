import logging as log
# # Configure logging to show all logs including DEBUG and above
log.basicConfig(filename="logs.log", filemode="w",
                format='%(levelname)s:%(message)s', level=log.INFO)


def main():


    log.debug("This is a debug message")  # This will be shown
    log.info("This is an info message")   # This will be shown
    log.warning("This is a warning message")  # This will be shown
    # Your application logic here



main()
