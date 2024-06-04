from PyQt6.QtCore import QObject


class LogProcessor(QObject):
    def __init__(self):
        super().__init__()
        self.funccalls = set()
        self.flags = set()
        self.tooltip_errors = []

    def rough_cut(self, line: str):
        if not line:
            return
        if line.startswith('\x00'):
            i = 0
            while line[i:].startswith('\x00'):
                i += 4
            line = line[i:]
            return line
        # D 10:00:01.5326437 ...
        flag, timestamp, *message = line.split()
        if message[0].startswith('GameState'):
            with open('gamestate.txt', 'a') as f:
                f.write(f"{flag} {' '.join(message)}")
            funccall, trash, *content = message
            funccall = funccall.split('.')[1]
            self.flags.add(flag)
            self.funccalls.add(funccall)
            with open('content.txt', 'a') as f:
                f.write(f"{flag} {funccall} {content}")
        elif message[0:3] == 'Unable to display':
            # tooltip error
            return
        elif (message[0].startswith('Card.TransitionToZone()') or message[0].startswith('PowerProcessor')
              or message[0].startswith('PowerTaskList')):
            # errors, errors
            # skins, emotes, etc eye candy loaded as an entity
            return
        else:
            with open('others.txt', 'a') as f:
                f.write(' '.join(line))
        return line

    def match_case_version(self, line: str):
        # print(line)
        if not line:
            return ''


        match line.split(' '):
            # [NUL]D 15:51:03.8648217 GameState.DebugPrintPowerList() - Count=286
            # \x00\x00D 21:31:55.5569134 PowerProcessor.EndCurrentTaskList() - m_currentTaskList=706
            case [nulls, most_of_next_line] if nulls.startswith('\x00'):

                return self.handle_null_line(nulls, most_of_next_line)



            case ["D", timestamp, command, "-", data] if command.startswith('PowerProcessor.'):
            # a powerprocessor hit
                # pass
                return line
            # D 12:04:43.2471597 GameState.DebugPrintPower ....
            case _:
                # pass
                return line
# D 21:31:55.5569134 PowerProcessor.EndCurrentTaskList() - m_currentTaskList=706

    def get_data(self):
        return self.funccalls, self.flags

    def handle_null_line(self, nulls, most_of_next_line):
        number_of_nulls = nulls.count('\x00')
        flag = nulls[-1]
        null_report = f"{flag} {number_of_nulls}xNUL"
        return f'<html><p style:"color:red;">{null_report}</p></html>\n{nulls[-1]} {most_of_next_line}'


class Gamestateline:
    """
    not used anywhere, just a schematic
    """
    def __init__(self, flag, time, funccall, content):
        self.flag = flag
        self.time = time
        self.funccall = funccall.split('.')[1]
        self.content = content


if __name__=='__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    service = LogProcessor()
    with open('raw_input.txt', 'r') as fi:
        data = fi.read()
    data_lines = data.split("\n")
    print(f"{data_lines[1]=}")
    null_filtered = [service.match_case_version(line) for line in data_lines if line]
    print(f"{null_filtered[1]=}")
    with open('null_filtered.txt', 'a') as fi:
        for line in null_filtered:
            fi.write(f"{line}\n")
