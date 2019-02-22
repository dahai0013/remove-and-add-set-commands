import re,os
import itertools
import shutil

def check(mystring,myfile,myinterface):
    '''
    This function will look thru a file to match a first string like " ... interface ... DATA ",
    then match an second string: interface like: "ge-0/0/"
    :param mystring:   first string like "unit 0 family ethernet-switching vlan members DATA"
    :param myfile:   config file name
    :param myinterface: second string like: "ge-0/0/"
    :return:
        numberofline, Total number of line matching the string
        lmymatch: after second filtering the interface number. Example the list xx in ge-0/0/xx
        mylines:
        lmachingif: list of interfaces : example ge-0/0/xx
    '''
    numberofline = 0
    lmymatch = []
    mylines = []
    lmachingif = []
    #print("all variables, string:", mystring," file name",myfile,"interface",myinterface)
    #open the original configuraton file
    sfile = open(myfile, 'r')
    sdatafile = sfile.readlines()

    # go thru line by line to try to match the first string example: "..... DATA"
    for line in sdatafile:
        # match action
        if mystring in line:
            line = line.strip("\n")
            #print only the line that have the interface
            if myinterface in line:
                mylines.append(line)
                #print("list of matching full lines:",line)

            #this regular expression will match ge-d/d/dd or xe-d/d/dd ( second string)
            lmatch = re.findall(myinterface+r'\d+',line)
            #match = re.search(r'[xg]e-\d/\d/\d+',line)
            #print(len(lmatch))
            #
            for match in lmatch:
                lmachingif.append(match)
                #print(match)
                match = str(match).strip('ge-')
                #print(match)
                lintfnumber = re.findall(r'\d+$', match)
                #print(lintfnumber[0])
                lmymatch.append(int(lintfnumber[0]))
            numberofline = numberofline +1
    sfile.close
    return (numberofline,lmymatch,mylines,lmachingif)

def add_2_file(list_range,myif,second_file):
    myif_mod = myif.replace("/","-")
    # convert range list into an strings
    #for i in range(len(list(to_ranges(lmymatch)))):
    for i in range(len(list_range)):
        #startif = str(list(to_ranges(lmymatch))[i][0])
        startif = str(list_range[i][0])
        #endif = str(list(to_ranges(lmymatch))[i][1])
        endif = str(list_range[i][1])
        myrange = (myif + "[" + startif + "-" + endif + "]")
        # print(myrange)
        #
        #myif_mod = myif_mod1 + startif
        string2add = [ 'set interfaces interface-range "if_ge_data" member "' + myrange + '"']

            # 'set interfaces interface-range "if_' + myif_mod + '" member "' + myrange + '"', \
            # 'set protocols dot1x authenticator interface "if_' + myif_mod + '" supplicant multiple', \
            # 'set protocols dot1x authenticator interface "if_' + myif_mod + '" retries 2', \
            # 'set protocols dot1x authenticator interface "if_' + myif_mod + '" transmit-period 3', \
            # 'set protocols dot1x authenticator interface "if_' + myif_mod + '" mac-radius', \
            # 'set protocols dot1x authenticator interface "if_' + myif_mod + '" no-reauthentication', \
            # 'set protocols dot1x authenticator interface "if_' + myif_mod + '" server-reject-vlan QUARANTINE', \
            # 'set protocols dot1x authenticator interface "if_' + myif_mod + '" eapol-block server-fail 300', \
            # 'set protocols dot1x authenticator interface "if_' + myif_mod + '" server-fail vlan-name DATA', \
            # 'set protocols dot1x authenticator interface "if_' + myif_mod + '" server-fail-voip vlan-name VOICE', \
            # 'set protocols vstp interface "if_' + myif_mod + '" edge', \
            # 'set protocols vstp interface "if_' + myif_mod + '" no-root-port', \
            # 'set switch-options voip interface "if_' + myif_mod + '" vlan VOICE', \
            # 'set switch-options voip interface "if_' + myif_mod + '" forwarding-class voice' \
            # ]
        #print(string2add)

        #create/or append and write into the file
        addedf = open(second_file, "a+")
        for line in string2add:
                line = line+"\n"
                addedf.write(line)
        addedf.close()

def add_2_file_static (second_file):
    #open the file and write
    addedf = open(second_file, "a+")

    # Add at the end of the file
    string2add = [ \
    'set protocols dot1x authenticator interface "if_ge_data" supplicant multiple', \
    'set protocols dot1x authenticator interface "if_ge_data" retries 2', \
    'set protocols dot1x authenticator interface "if_ge_data" transmit-period 3', \
    'set protocols dot1x authenticator interface "if_ge_data" mac-radius', \
    'set protocols dot1x authenticator interface "if_ge_data" no-reauthentication', \
    'set protocols dot1x authenticator interface "if_ge_data" server-reject-vlan QUARANTINE', \
    'set protocols dot1x authenticator interface "if_ge_data" eapol-block server-fail 300', \
    'set protocols dot1x authenticator interface "if_ge_data" server-fail vlan-name DATA', \
    'set protocols dot1x authenticator interface "if_ge_data" server-fail-voip vlan-name VOICE', \
    'set protocols vstp interface "if_ge_data" edge', \
    'set protocols vstp interface "if_ge_data" no-root-port', \
    'set switch-options voip interface "if_ge_data" vlan VOICE', \
    'set switch-options voip interface "if_ge_data" forwarding-class voice']

    for line in string2add:
            line = line+"\n"
            addedf.write(line)
    addedf.close()

def to_ranges(iterable):
    iterable = sorted(set(iterable))
    for key, group in itertools.groupby(enumerate(iterable),
                                        lambda t: t[1] - t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]

def remove_from_file(mystring,src_file, dst_file):
    srcf = open(src_file,"r")
    dstf = open(dst_file,"w")

    d = srcf.readlines()
    srcf.seek(0)
    dstf.seek(0)
    for i in d:
        #if i == mystring :
            #print(i)
        if i != mystring :
            #print(i)
            dstf.write(i)
    #srcf.truncate()
    srcf.close()
    dstf.close()
    return(dst_file)

def main():
    # will check is a string is in the file
    myfile = "EX4300-TEMPLATE.txt"
    #create the working and destination files
    working_file = myfile + "modif"
    dst_file = myfile + ".modif.txt"
    shutil.copyfile(myfile, working_file)
    second_file = myfile + "add_if_range.txt"
    try:
        os.remove(second_file)
    except:
        pass

    origmystring = "unit 0 family ethernet-switching vlan members DATA"
    interfaces = ["ge-0/0/","ge-1/0/","ge-2/0/","ge-3/0/","ge-4/0/","ge-5/0/","ge-6/0/","ge-7/0/","ge-8/0/"]
    #interfaces = ["ge-1/0/"]

    #
    for myif in interfaces:
        print("the interface:", myif)
        numberofline, lmymatch , mylines , lmachingif = check(origmystring, myfile,myif)
        #print("mylines:",mylines)
        print("Interface list:",lmachingif)
        #print("Total number of machine line:",numberofline)
        print("List of interfaces (lmymatch):",lmymatch)
        # will convert the list of integer into ranges
        print("ranges :", list(to_ranges(lmymatch)))

        # call he function to add new lines
        add_2_file(list(to_ranges(lmymatch)),myif,second_file)

        # create file
        for i in range(len(lmachingif)):
            #print("the interface:",lmachingif[i])
            mystrings = [\
                         "set interfaces "+lmachingif[i]+" unit 0 family ethernet-switching vlan members DATA",\
                         "set interfaces "+lmachingif[i]+" ether-options auto-negotiation",\
                         "set interfaces "+lmachingif[i]+" ether-options flow-control",\
                         "set interfaces "+lmachingif[i]+" unit 0 family ethernet-switching interface-mode access",\
                         "set protocols dot1x authenticator interface " + lmachingif[i] + ".0 supplicant multiple",\
                         "set protocols dot1x authenticator interface " + lmachingif[i] + ".0 retries 2",\
                         "set protocols dot1x authenticator interface " + lmachingif[i] + ".0 transmit-period 3",\
                         "set protocols dot1x authenticator interface " + lmachingif[i] + ".0 mac-radius",\
                         "set protocols dot1x authenticator interface " + lmachingif[i] + ".0 no-reauthentication",\
                         "set protocols dot1x authenticator interface " + lmachingif[i] + ".0 server-reject-vlan QUARANTINE",\
                         "set protocols dot1x authenticator interface " + lmachingif[i] + ".0 eapol-block server-fail 300",\
                         "set protocols dot1x authenticator interface " + lmachingif[i] + ".0 server-fail vlan-name DATA",\
                         "set protocols dot1x authenticator interface " + lmachingif[i] + ".0 server-fail-voip vlan-name VOICE",\
                         "set protocols vstp interface "+lmachingif[i]+" edge",\
                         "set protocols vstp interface "+lmachingif[i]+" no-root-port",\
                         "set switch-options voip interface " + lmachingif[i] + ".0 vlan VOICE",\
                         "set switch-options voip interface " + lmachingif[i] + ".0 forwarding-class voice"]


            # will remove one line at the time and copy the file
            for mystring in mystrings:
                #print(mystring.strip())
                remove_from_file(mystring+"\n", working_file, dst_file)
                shutil.copyfile(dst_file, working_file)
        #print("interface ",i," done.")
        shutil.copyfile(dst_file, working_file)


    # add the static config to the dile
    add_2_file_static(second_file)

    # clean and remove the file
    os.remove(working_file)
    print("La Fin")

if __name__ == "__main__":
    # 1: will strip the first argument, the script.py itself
    main()