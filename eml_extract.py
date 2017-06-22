import glob, os, email


def caption(origin):
    """Extracts: To, From, Subject and Date from email.Message() or mailbox.Message()
    origin -- Message() object
    Returns tuple(From, To, Subject, Date)
    If message doesn't contain one/more of them, the empty strings will be returned.
    """
    Date = ""
    if "date" in origin: Date = origin["date"].strip()
    From = ""
    if "from" in origin: From = origin["from"].strip()
    To = ""
    if "to" in origin: To = origin["to"].strip()
    Subject = ""
    if "subject" in origin: Subject = origin["subject"].strip()
    return From, To, Subject, Date


def extract_email_addr(string):
    left = string.index('<')+1
    right = string.index('>')
    return string[left:right]

def extract_filename(filepath):
    rev = filepath[::-1]
    cut = rev[:rev.index('\\')]
    return cut[::-1]


def extract_attachments(src_dir, out_dir, extension="eml"):
    """
    try to extract the attachments from all files in cwd
    will process all files with the specified extension, or eml by default
    """
    # ensure that an output dir exists
    os.path.exists(out_dir) or os.makedirs(out_dir)
    output_count = 0
    ok = True
    a = 0

    err = open('error.txt', 'w')
    #err.write(f.name+'\n')
    err.close()

    for emlfile in glob.iglob(src_dir+"\\*.%s" % extension):
        try:
            with open(emlfile, "r") as f:
                msg = email.message_from_file(f)
                From, To, Subject, Date = caption(msg)

                #print(extract_email_addr(From))

                attachments = list(msg.get_payload()[1:])
                # If no attachments are found, skip this file
                if not attachments:
                    print("No attachment found for file %s!" % f.name)
                    ok = False
                    continue
                for attachment in attachments:
                    a += 1

                    output_filename = attachment.get_filename()

                    adr = extract_email_addr(From)

                    print('NOW '+str(a)+'>>> '+out_dir+'\\'+adr+'\\'+output_filename)

                    try:
                        os.makedirs(out_dir+'\\'+adr)
                    except OSError:
                        pass

                    '''mails = open(out_dir+'\\mails.txt', 'a+')
                    mails.write(adr+'\n')
                    mails.close()'''

                    '''with open(out_dir+'\\'+adr+'\\'+output_filename, 'wb') as of:
                        of.write(attachment.get_payload(decode=True))
                        output_count += 1'''
        # this should catch read and write errors
        except:
            #continue
            #print("There was a problem with %s or its attachment!" % f.name)
            err = open('error.txt', 'a+')
            err.write(f.name+'\n')
            err.close()

            ok = False
    if not ok:
        print("%s files were written, but there were some problems." % output_count)
    else:
        print("Done. %s CSVs written to the 'output' directory." % output_count)

def merge():
    thunder = 'G:\\emlout\\thunderbird\\'
    voyager = 'G:\\emlout\\voygaer\\'


if __name__ == "__main__":
    #  extract_attachments('G:\\eml', 'G:\\emlout') # najpierw
    extract_attachments('G:\\eml\\miksmaili-eml', 'G:\\emlout\\miksmaili')
