from fltk.qries.base import QryRepo

from .utils import QryUtils


class QryGlobal(QryRepo):
    @property
    def utils(self) -> QryRepo:
        return QryUtils(self.conn, table_nm=self.table_nm)
