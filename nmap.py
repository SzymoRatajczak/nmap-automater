#tools automating some of the nmapp funcionality especailly comparsion between scans 

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser,NmapParserException


def scanner(target,option,iteration):
    nmap=NmapProcess(target,option)
    return_code=nmap.run()
    #or nmap.run_background()
    #or nmap.sudo_ran_background(run_as=root)
    if return_code!=0:
        print('Scann cannot be completed:{0}',format(nmap.stderr))
    try:
        parsed=NmapParser(nmap.stdout)
        file=open('scan'+str(iteration+'.xml','w'))
        file.write(parsed)
        file.close()
    except NmapParserException as e:
        print('Parsing error: {0}'.format(e.msg))
   
def print_diffrences(new_rep,old_rep):
    #this contains all of the diffrences
    ndiff=new_rep.diff(old_rep)

    #to be more specifc
    what_changed(new_rep,old_rep,ndiff.changed())
    what_added(new_rep,ndiff.added())
    what_removed(old_rep,ndiff.removed())

def what_changed(new_rep,old_rep,changes):
    for key in changes:
        nested=splitting(key)
        if nested not in None:
            if nested[0]=='NmapHost':
                val1=new_rep.get_host_by_id(nested[1])
                val2=old_rep.get_host_by_id(nested[1])
            elif nested[0]=='NmapService':
                val1=new_rep.get_service_by_id(nested[1])
                val2=old_rep.get_service_by_id(nested[1])
            print("Values of the new repository:{0} \n values of the old repository {1}".format(val1,val2))



def what_added(new_rep,addings):
    for key in addings:
        nested=splitting(key)
        if nested not in None:
            if nested[0]=='NmapHost':
                val1=new_rep.get_host_by_id(nested[1])
            elif nested[0]=='NmapService':
                val1=new_rep.get_service_by_id(nested[1])
            print('Added {0}'.format(val1))

def what_removed(old_rep,removings):
    for key in removings:
        nested=splitting(key)
        if nested not in None:
            if nested[0]=='NmapHost':
                val2=old_rep.get_host_by_id(nested[1])
            elif nested[0]=='NmapService':
                val2=old_rep.get_service_by_id(nestedp[1])
            print('Removed:{0}'.format(val2))
        
        

def splitting(key):
    splitted=key.split('::')
    if splitted==2:
        return splitted
    #the value must be 2 coz everything is made of two parts
    # part 0 - NmapHost or NmapService
    # part 1 - actual value, we are into


def main():
    target='nmap.scan.org'
    option='-sT -A'

    for i in range(1,3):
        scanner(target,option,i)
        sleep(500)
    new_rep=NmapParser('scan1.xml')
    old_rep=NmapParser('scan2.xml')

    print_diffrences(new_rep,old_rep,)
    


if __init__=="__main__":
    main()