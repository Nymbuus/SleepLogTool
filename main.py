""" Imports. """
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool
from sleep_log_tool_repo.menu import Menu

def main():
    """ Main. """
    _slt = SleepLogTool()
    _menu = Menu()

    _menu.selection_window()

    # Open the file explorer to select files and save those files data into a csv file
    file_list = _slt.file_explorer()
    file_name = _slt.save_file()
    saved_file = _slt.write_to_csv(file_name, file_list)

    df = _slt.csv_to_panda(saved_file)
    df = _slt.remove_time(df)
    _slt.calculating_statistics(df)
    _slt.plotting_graph(df)


if __name__ == '__main__':
    main()
