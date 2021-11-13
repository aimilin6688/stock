# This is a sample Python script.

# Press Alt+Shift+X to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+Shift+B to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from src.utils.log import init_log
    from src.stock.socket.socket_app import reopen
    init_log()
    t1 = reopen()
    t1.join()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
