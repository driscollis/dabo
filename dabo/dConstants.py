""" dConstants.py """

# Return values for most operations
# FILE_OK = 0
# FILE_CANCEL = -1
# FILE_NORECORDS = -2
# FILE_BOF = -3
# FILE_EOF = -4

# Return values for updates to the database
# UPDATE_OK = 0
# UPDATE_NORECORDS = -2

# Return values from Requery
# REQUERY_SUCCESS = 0
# REQUERY_ERROR = -1

# Referential Integrity constants
REFINTEG_IGNORE = 1
REFINTEG_RESTRICT = 2
REFINTEG_CASCADE = 3

# Constants specific to cursors
CURSOR_MEMENTO = "dabo-memento"
CURSOR_NEWFLAG = "dabo-newrec"
CURSOR_TMPKEY_FIELD = "dabo-tmpKeyField"

DLG_OK = 0
DLG_CANCEL = -1

FIND_DIALOG_FINDTEXT = -210
FIND_DIALOG_REPLACETEXT = -212
