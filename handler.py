from src.main import main

USER_LIST_FILE = "userlist.txt"


def handle(event, context):
    main(USER_LIST_FILE)
