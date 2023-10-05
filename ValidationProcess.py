
# The list of items that are not permitted in the username and password. This is a preliminary form of data cleansing
# used to prevent SQL injection.
forbidden_items = ["*", "(", ")", "$", "&", "£", "=", '"', "%"]

# This file is to validate the entry from the main screen
def ValidateInput(Input):
    for chars in Input:
        print("Testing " + chars)
        for items in forbidden_items:
            print(items)
            if chars == items:
                return 1
            elif len(Input) < 6:
                return 2
    return 0


if __name__ == "__main__":
    print(ValidateInput(Input='''apple"dkdk@!"£$$%^^^^&**'''))
    # Blackbox testing


