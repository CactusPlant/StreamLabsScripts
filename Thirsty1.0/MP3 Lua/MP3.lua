--Intro stuff
local read_lines = {}
filename = "C:\\Users\\Cactus\\AppData\\Roaming\\Streamlabs\\Streamlabs Chatbot\\Services\\Scripts\\MarioParty3\\commands.txt"
local file = io.open(filename, "r")
io.input(file)

---Tables and Tables of data
local read_commands = {}
local execution_table = {}
local command_list = {}-- Table of Command references
command_list["coinsup"] = CoinsUp
command_list["coinsdown"]=CoinsDown
command_list["starsup"]=StarsUp
command_list["starsdown"]=StarsDown
command_list["giveitem"]=GiveItem
command_list["takeitem"]=TakeItem
command_list["reverse"]=Reverse
command_list["adjustroll"]=AdjustRoll
--------------------------
--END COMMAND ASSIGNMENT
--------------------------

polyline = {color="blue", thickness=2, npoints=4,
{x=0,   y=0},
{x=-10, y=0},
{x=-10, y=1},
{x=0,   y=1}
}
local address_data = {} --Player address table
address_data["1"] = {}
address_data["1"].roll=0x0CDB95 
address_data["1"].item1=0x0D1120
address_data["1"].item2=0x0D1121
address_data["1"].item3=0x0D1122
address_data["1"].reverse=0x0D111F
address_data["1"].coins1=0x0D1112
address_data["1"].coins2=0x0D1113
address_data["1"].stars=0x0D1116
        
address_data["2"]={}
address_data["2"].roll=0x0CDC21
address_data["2"].item1=0x0D1158
address_data["2"].item2=0x0D1159
address_data["2"].item3=0x0D115A
address_data["2"].reverse=0x0D1157
address_data["2"].coins1=0x0D114A
address_data["2"].coins2=0x0D114B
address_data["2"].stars=0x0D114E
        
address_data["3"]={}
address_data["3"].roll=0x0CDC6D
address_data["3"].item1=0x0D1190
address_data["3"].item2=0x0D1191
address_data["3"].item3=0x0D1192
address_data["3"].reverse=0x0D118F
address_data["3"].coins1=0x0D1182
address_data["3"].coins2=0x0D1183
address_data["3"].stars=0x0D1186
        
address_data["4"]={}
address_data["4"].roll=0x0CDCB9
address_data["4"].item1=0x0D11C8
address_data["4"].item2=0x0D11C9
address_data["4"].item3=0x0D11CA
address_data["4"].reverse=0x0D11C7
address_data["4"].coins1=0x0D11BA
address_data["4"].coins2=0x0D11BB
address_data["4"].stars=0x0D11BE

--Create Command
function CreateCommand(ordernum, u,cmd,tgt,val)
    newCommand = {}
    newCommand.order_number = ordernum
    newCommand.command = cmd
    newCommand.user = u
    newCommand.target = tgt
    newCommand.value = val
    return newCommand
end

---Main Functions
--Set Roll
function set_roll(command)
    currentroll = mainmemory.readbyte(address_data[command.target].roll)
    if currentroll ~= 0 then
        memory.writebye(player.roll, value)
        return true
    end
    return false
end

--Edit Item 
function GiveItem(cmd)
    if mainmemory.readbyte(address_data[cmd.target].item1) == 255 then
        print(cmd.value)
        mainmemory.writebyte(address_data[cmd.target].item1, tonumber(cmd.value))
    elseif mainmemory.readbyte(address_data[cmd.target].item2) == 255 then
        mainmemory.writebyte(address_data[cmd.target].item2, tonumber(cmd.value))
    else 
        mainmemory.writebyte(address_data[cmd.target].item3, tonumber(cmd.value))
    end
    return true
end

function TakeItem(cmd)
    if mainmemory.readbyte(address_data[cmd.target].item3) < 255 then 
        mainmemory.writebyte(address_data[cmd.target].item3, 255)
    elseif mainmemory.readbyte(address_data[cmd.target].item2) < 255 then
        mainmemory.writebyte(address_data[cmd.target].item2, 255)
    elseif mainmemory.readbyte(address_data[cmd.target].item1) < 255 then
        mainmemory.writebyte(address_data[cmd.target].item1, 255)
    else 
        return false
    end
    return true
end

--Edit Coins
function CoinsUp(cmd) 
    current = ((mainmemory.readbyte(address_data[cmd.target].coins1))*256) + (mainmemory.readbyte(address_data[cmd.target].coins2))
    new = current + cmd.value
    if new > 999 then new = 999 end
    c1 = math.floor(new/256)
    c2 = new%256
    mainmemory.writebyte(address_data[cmd.target].coins1, c1)
    mainmemory.writebyte(address_data[cmd.target].coins2, c2)
    return true
end
function CoinsDown(cmd)
    current = ((mainmemory.readbyte(address_data[cmd.target].coins1))*256) + (mainmemory.readbyte(address_data[cmd.target].coins2))
    new = current - cmd.value
    if new < 0 then new = 0 end

    c1 = math.floor(new/256)
    c2 = new%256

    mainmemory.writebyte(address_data[cmd.target].coins1, c1)
    mainmemory.writebyte(address_data[cmd.target].coins2, c2)
    return true
end

--Edit Stars
function StarsUp(cmd)
    current = mainmemory.readbyte((address_data[cmd.target].stars))
    new = current + cmd.value
    if new > 99 then new = 99 end
    mainmemory.writebyte((address_data[cmd.target].stars),new)
    return true 
end
function StarsDown(cmd)
    current = mainmemory.readbyte((address_data[cmd.target].stars))
    new = current - cmd.value
    if new < 0 then new = 0 end
    mainmemory.writebyte((address_data[cmd.target].stars),new)
    return true
end

--Reverse Player
function Reverse(cmd)
    if mainmemory.readbyte(address_data[1].reverse) ~= 128 and mainmemory.readbyte(address_data[2].reverse) ~= 128 and mainmemory.readbyte(address_data[3].reverse) ~= 128 and mainmemory.readbyte(address_data[4].reverse) ~= 128 then
        mainmemory.writebyte(address_data[1].reverse, 128)
        mainmemory.writebyte(address_data[2].reverse, 128)
        mainmemory.writebyte(address_data[3].reverse, 128)
        mainmemory.writebyte(address_data[4].reverse, 128)
        return true
    end
    return false
end

--Adjust Roll
function AdjustRoll(cmd)
    if mainmemory.readbyte(address_data[cmd.target].roll) ~= 0 then
        current = mainmemory.readbyte(address_data[cmd.target].roll)
        new = current + cmd.value
        if new < 1 then new = 1 end
        if new > 35 then new = 35 end
        mainmemory.writebyte(address_data[cmd.target].roll, new)
        return true
    end
    return false
end

--Execute Commands(from table commands)
function Command_Handler()
    for line in io.lines(filename) do
        rawdata = split(line,";")
        new = false
        if read_commands[rawdata[1]] == nil then new = true end
        if new then
            newcmd = CreateCommand(rawdata[1],rawdata[2],rawdata[3],rawdata[4],rawdata[5])
            execution_table[newcmd.order_number] = newcmd
            read_commands[newcmd.order_number] = newcmd
        end
    end    
end

function ExecuteCMD()
    for k,cmd in pairs(execution_table) do 
        if command_list[cmd.command](cmd) then
            execution_table[cmd.order_number] = nil
        end
    end
end

function split(str,sep)
    local array = {}
    local reg = string.format("([^%s]+)",sep)
    for mem in string.gmatch(str,reg) do
        table.insert(array, mem)
    end
    return array
end




--Main Loop
while true do
    Command_Handler()
    ExecuteCMD()
    emu.frameadvance()
end