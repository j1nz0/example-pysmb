from smb.SMBConnection import SMBConnection
import io
import sys

SMB_USER = "testUser"
SMB_DOMAIN = "workGroup"  # optional
SMB_PASSWORD = "test123"
SMB_SERVER_IP = "xxx.xx.xxx.xx"
SMB_SERVER = "test-hostname"
SMB_SHARE = "shared-test-folder"
SMB_PORT = 445
LOCAL = "your-local-machine-hostname"


def main():
    connection = SMBConnection(SMB_USER, SMB_PASSWORD, LOCAL, SMB_SERVER, domain=SMB_DOMAIN,
                               use_ntlm_v2=True,
                               is_direct_tcp=True)

    try:
        connection.connect(SMB_SERVER_IP, SMB_PORT)
        print('[+] Successfully connected to %s' % SMB_SERVER)
    except Exception as e:
        sys.exit('[-]Could not connect to %s: %s' % (SMB_SERVER, e))

    try:
        # Check if the files we want are there
        result = get_files_array(connection)
        # "load" to your local machine
        load_file_bytes(connection, result)
    except Exception as e:
        sys.exit(e)


def close_connection(connection):
    # Close connection
    connection.close()


def get_files_array(connection):
    files = connection.listPath(SMB_SHARE, "/")

    counter = 0
    file_arr = []
    for item in files:
        counter += 1
        file_arr.append(item.filename)
    if not counter == 0:
        print('[+] %s files returned' % counter)
    else:
        close_connection(connection)
        sys.exit('[-] %s files returned' % counter)
    return file_arr


def load_file_bytes(connection, file_array):
    counter = 1
    for file_object in file_array:
        try:
            buffer = io.BytesIO()
            connection.retrieveFile(SMB_SHARE, file_object, buffer)
            f = open(file_object, "wb")
            f.write(buffer.getvalue())
            f.flush()
            f.close()
            counter += 1
        except Exception as e:
            close_connection(connection)
            sys.exit('[-] An error has occurred: %s' % e)
    print('[+] Finished! %s files loaded' % counter)


if __name__ == '__main__':
    main()
