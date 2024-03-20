""" Imports. """
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool

def main():
    """ Main. """
    a = SleepLogTool()

    if a.suppress_qt_warnings():
        print("qt_warnings suppressed.")

    # Open the file explorer to select files and save those files data into a csv file
    file_list = a.file_explorer()
    file_name = a.save_file()
    saved_file = a.write_to_csv(file_name, file_list)

    df = a.csv_to_panda(saved_file)
    df = a.remove_time(df)
    a.calculating_statistics(df)
    a.plotting_graph(df)


if __name__ == '__main__':
    main()
