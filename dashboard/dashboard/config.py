from PyQt6.QtCore import QSettings


class ConfigReader:
    def __init__(self, path):
        self.settings = QSettings(path, QSettings.Format.IniFormat)

    def _groups(self):
        return self.settings.childGroups()

    def _values(self, group):
        self.settings.beginGroup(group)
        vals = {k: self.settings.value(k) for k in self.settings.allKeys()}
        self.settings.endGroup()
        return vals

    def load(self):
        return {group: self._values(group) for group in self._groups()}

    def tabs(self):
        return {group: self._values(group) for group in self._groups() if group.startswith('tab_')}
