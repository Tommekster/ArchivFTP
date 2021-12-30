from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.filesystems import AbstractedFS
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
import gzip


# The port the FTP server will listen on.
# This must be greater than 1023 unless you run this script as root.
FTP_PORT = 2121

# The name of the FTP user that can log in.
FTP_USER = "myuser"

# The FTP user's password.
FTP_PASSWORD = "change_this_password"

# The directory the FTP user will have full read/write access to.
FTP_DIRECTORY = "./data"
#FTP_DIRECTORY = "/srv/users/SYSUSER/apps/APPNAME/public/"


class ArchiveAbstractedFS(AbstractedFS):
    def open(self, filename, mode):
        """Open a file returning its handler."""
        assert isinstance(filename, str), filename
        gz_name = self._gz(filename)
        return gzip.open(gz_name, mode)

    def listdir(self, path):
        listing = super().listdir(path)
        listing = set(self._ungz(x) for x in listing)
        return list(listing)

    def listdirinfo(self, path):
        return self.listdir(path)

    def remove(self, path):
        gz_path = self._gz(path)
        return super().remove(gz_path)

    def rename(self, src, dst):
        gz_src = self._gz(src)
        if os.path.isfile(gz_src):
            gz_dst = self._gz(dst)
            return super().rename(gz_src, gz_dst)
        else:
            return super().rename(src, dst)

    def isfile(self, path):
        gz_path = self._gz(path)
        return super().isfile(gz_path)

    def lexists(self, path):
        return self._gzify(super().lexists, path)

    def stat(self, path):
        return self._gzify(super().stat, path)

    def lstat(self, path):
        return self._gzify(super().lstat, path)

    def _gz(self, path):
        return path + ".gz"

    def _gzify(self, func, path):
        gz_path = self._gz(path)
        return (
            func(gz_path)
            if os.path.isfile(gz_path)
            else func(path)
        )

    def _ungz(self, path: str):
        return path[:-3] if path.endswith(".gz") else path


class ArchiveFTPHandler(FTPHandler):
    abstracted_fs = ArchiveAbstractedFS


def main():
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions.
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')

    handler = ArchiveFTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Optionally specify range of ports to use for passive connections.
    #handler.passive_ports = range(60000, 65535)

    address = ('', FTP_PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()


if __name__ == '__main__':
    main()
