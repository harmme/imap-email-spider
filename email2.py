#This is a script created thanks to
#https://gist.github.com/robulouski/7441883
#
import sys
import getopt
import imaplib
import getpass
import email
import email.header
import datetime
import re


# Use 'INBOX' to read inbox.  Note that whatever folder is specified, 
# after successfully running this script all emails in that folder 
# will be marked as read.
EMAIL_FOLDER = "INBOX"


def process_mailbox(M):
    """
    Do something with emails messages in the folder.  
    For the sake of this example, print some headers.
    """

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_string(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(msg['FROM']))
        from_mail = str(hdr)
        print('Message %s: %s' % (num, from_mail))
        print('CC:', msg['CC'])
        print('BCC:', msg['BCC'])


def login_mailbox(account):
    M = imaplib.IMAP4_SSL(account[0])

    try:
        rv, data = M.login(account[2], account[3])
    except imaplib.IMAP4.error:
        print ("LOGIN FAILED!!! ")
        sys.exit(1)

    print(rv, data)

    rv, mailboxes = M.list()
    if rv == 'OK':
        print("Mailboxes:")
        print(mailboxes)

    rv, data = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        print("Processing mailbox...\n")
        process_mailbox(M)
        M.close()
    else:
        print("ERROR: Unable to open mailbox ", rv)

    M.logout()

def main(argv):
    inputfile = ''
    outputfile = ''
    excludefile = ''
    aaccounts = list()

    try:
      opts, args = getopt.getopt(argv,"hi:o:e:",["ifile=","ofile=","efile="])
    except getopt.GetoptError:
      print sys.argv[0]," -i <inputfile> [-o <outputfile> [-e <excludefile>]]"
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0]," -i <inputfile> [-o <outputfile> [-e <excludefile>]]"
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-e", "--efile"):
            excludefile = arg
    if inputfile == "":
        print sys.argv[0]," -i <inputfile> [-o <outputfile> [-e <excludefile>]]"
        sys.exit();
    print "Input file is:", inputfile
    print "Output file is:", outputfile
    print "Exclude file is:", excludefile
    with open(inputfile) as f:
        accounts = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    accounts = [x.strip() for x in accounts] 
    for account in accounts:
        aaccount = account.split("|")
        login_mailbox(aaccount)
        print aaccount[2]

if __name__ == "__main__":
   main(sys.argv[1:])