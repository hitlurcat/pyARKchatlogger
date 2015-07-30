import srcds as rcon
import os
import ConfigParser
import time
import platform
import errno

currDir = os.getcwd()
config = ConfigParser.SafeConfigParser()
conf = {}
getOs = platform.system()
defLogDir = "chatlogs"
rcon_return = None

# Write cfg if it doesnt exist.
if __name__ == '__main__':
    #write if doesnt exist
    if not os.path.isfile('settings.cfg'):
        print "Configuration file was either not found, blank, or doesnt exist, creating settings.cfg now..."
        # Sections
        config.add_section('connection_info')
        config.add_section('logging')
        config.add_section('debug')
        # connection_info
        config.set('connection_info', 'host', '127.0.0.1')
        config.set('connection_info', 'port', '27020')
        config.set('connection_info', 'pass', 'changeme321')
        config.set('connection_info', 'timeout', '15')
        config.set('connection_info', 'sleep', '3')
        # logging
        config.set('logging', 'logs_dir', defLogDir)
        # debug
        config.set('debug', 'debug', 'False')

        # Writing our configuration file to 'settings.cfg'
        with open('settings.cfg', 'wb') as configfile:
            config.write(configfile)
        print "Configuration file written and saved as 'settings.cfg' in " + currDir
        # write the logs folder based on logs_dir
    # cfg exists
    elif os.path.isfile('settings.cfg'):
        print getOs
        print "Configuration file found!" + "\n" + "Loading Config..."
        time.sleep(1)
        # read the file
        config.read('settings.cfg')

        # get and print config information
        # print host
        conf['host'] = config.get('connection_info', 'host')
        print "Host: " + conf['host']
        # print port
        conf['port'] = int(config.get('connection_info', 'port'))
        print "Port: " + str(conf['port'])
        # get pass
        conf['pass'] = config.get('connection_info', 'pass')
        #get timeout
        conf['timeout'] = int(config.get('connection_info', 'timeout'))
        # print debug information
        conf['debug'] = config.getboolean('debug', 'debug')
        if conf['debug']:
            print "Debug is Enabled"
        elif not conf['debug']:
            print "Debug is Disabled"
        # print log information
        time.sleep(1)
        conf['logs_dir'] = config.get('logging', 'logs_dir')
        currLogDir = conf['logs_dir']
        logsPath = os.path.join (currDir, config.get('logging', 'logs_dir'))
        # Check that the logs_dir in the .cfg is NOT empty
        if conf['logs_dir'] == "":
            config.set('logging', 'logs_dir', defLogDir)
            with open('settings.cfg', 'wb') as configfile:
                config.write(configfile)
            print "Error: logs_dir value is empty. Reverting to default directory of:" + defLogDir
            # if so attempt to create logs dir based off of default
            try:
                os.makedirs(defLogDir)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    print 'Unable to create logs folder'
        # otherwise make dir based of currently set dir in .cfg
        elif conf['logs_dir'] != "":
            try:
                os.makedirs(currLogDir)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    print 'unable to create logs folder'
            print "Logs will be saved to: " + logsPath + "\\"
        time.sleep(1)
        print "Configuration file loaded successfully!"
        # End of Config Loading, begin connection routine
        print "Attempting to connect to rcon..."
        time.sleep(1)
        # Attempt to connect to rcon
        try:
            con = rcon.SourceRcon(conf['host'], conf['port'], conf['pass'], conf['timeout'])
            con.rcon('listplayers')
            connTestPass = True
            print "Connected to RCON!"
        except:
            print "Unable to connect to RCON"
            exit()
        with open(currLogDir + '\Chat.log', 'a', 1) as clHist:
            print "Listening and collecting logs..."
            while connTestPass == True:
                time.sleep(1)
                # ARK by default, uses a 'buffer' system for this command
                # Running this command, prints chat stored in the buffer line by line
                # The command ONLY gets chat that is in the buffer since the LAST time
                # The buffer was cleared. IF the command was successfully run, but
                # there was nothing to return, the string "Server received, But no response!!" is returned.
                rcon_return = con.rcon('getchat')
                if conf['debug']:
                    print rcon_return
                # run the command to return the chat buffer
                for chatline in rcon_return.splitlines():
                    # for each line stored in result, make sure its an actual message and not the response
                    # from 'getchat'
                    if len(chatline) > 1 and not chatline.__contains__('Server received, But no response!!'):
                        # Write it
                        clHist.write(time.strftime("[%m/%d/%Y %H:%M:%S %p] ") + chatline + '\n')
                        # Flush it. Some have said this is unnecessary.
                        clHist.flush()