from io import StringIO
import re
import datetime
from luigi.contrib.dropbox import DropboxTarget
from pipeline.config import DROPBOX_TOKEN
import dropbox


def dropbox_target(path):
    return DropboxTarget(path, DROPBOX_TOKEN)


def textio2stringio(text_io_wrapper):
    """Converts the contents of a text io wrapper to a StringIO instance

    Pandas doesn't accept a TextIOWrapper because it expect that it will have the name kwarg set,
    we can't do that since we're using dropbox to store files and the client download content as bytes
    (https://luigi.readthedocs.io/en/stable/_modules/luigi/contrib/dropbox.html#DropboxTarget.temporary_path),
    however pandas accepts an StringIO instances.
    """
    return StringIO(text_io_wrapper.read())


def textio2binary(text_io_wrapper):
    return text_io_wrapper.buffer.read()


# ? ==============================
# ? dropbox_clear_space
# ? Additions re: Dropbox clear space
def ensure_available_space(min_space):

    dbx = dropbox.Dropbox(DROPBOX_TOKEN)

    # test if usage threshhold exceeded (below min space)
    # if below, delete last two days of data (subject to change)
    usage = dbx.users_get_space_usage()
    print(usage)
    used = usage.used
    allocated = usage.allocation.get_individual().allocated
    remaining_space = allocated - used
    print("remaining space: {}".format(str(remaining_space)))

    if remaining_space >= min_space:
        print("space is sufficient")
        return None
    else:
        print("space is insufficient!")

        # patterns
        p1 = "^\d{4}-\d{2}-\d{2}-mcgm\.stopcoronavirus\.pdf$"
        p2 = "^\d{4}-\d{2}-\d{2}\.json$"
        p3 = "\d{4}-\d{2}-\d{2}"

        # list files
        project_files = dbx.files_list_folder("", recursive=True).entries
        print(project_files)
        stopcovid_pdf = [
            entry.name
            for entry in project_files
            if re.search(p1, entry.name) is not None
        ]
        proj_json = [
            entry.name
            for entry in project_files
            if re.search(p2, entry.name) is not None
        ]

        # filter files for oldest 10 files (arbitrary)
        date_sort = lambda val: datetime.datetime.strptime(
            val[re.search(p3, val).start() : re.search(p3, val).end()], "%Y-%m-%d"
        )
        stopcovid_pdf = sorted(stopcovid_pdf, key=date_sort)[0]
        proj_json = sorted(proj_json, key=date_sort)[0]

        print(stopcovid_pdf)
        print(proj_json)

        # for entry in dbx.files_list_folder("", recursive=True).entries:
        #     if (re.search(p1, entry.name) is not None) | (
        #         re.search(p2, entry.name) is not None
        #     ):
        #         print(entry.name)
        # print(dbx.files_get_metadata(entry.name))

        # delete file
        # path = proj_json
        # dbx.files_delete(path)

        return None


if __name__ == "__main__":

    ensure_available_space(1000)
