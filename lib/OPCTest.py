import OpenOPC
#   http://openopc.sourceforge.net/api.html
#  DCOM mode is used to talk directly to OPC servers without the need for the OpenOPC Gateway Service. 
#   This mode is only available to Windows clients. 
#   opc = OpenOPC.client()
# In Open mode a connection is made to the OpenOPC Gateway Service running on the specified node. 
#   This mode is available to both Windows and non-Windows clients. 
#   opc = OpenOPC.open_client(host)
# Get a list of OPC servers
#   opc.servers()
# Connecting to an OPC Server
#   opc.connect('server_string', optionalHostParam)
# Reading an item
#   opc.read('Random.Int4')
#   (19169, 'Good', '06/24/07 15:56:11')
# Enumerating a tuple
#   value, quality, time = opc.read('Random.Int4')
# Reading Based on Tags
#   tags = ['Random.String', 'Random.Int4', 'Random.Real4']
#   opc.read(tags,group='test')
# Writing items
#   opc.write(('Random.Int4', 100.0))
# Short form...
#   opc['Random.Int4'] = 100.0
#
#
#




