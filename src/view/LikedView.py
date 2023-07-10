# coding:utf-8
from src.view.ImportView import ImportView

class LikedView(ImportView):

    def __init__(self, controller):
        super().__init__(controller)

    def remove_track(self, file_path):
        for track_widget in self.trackWidgets:
            if track_widget.path == file_path:
                self.vlayout.removeWidget(track_widget)
                track_widget.hide()
                self.trackWidgets.remove(track_widget)
                track_widget.deleteLater()