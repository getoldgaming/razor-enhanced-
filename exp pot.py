#Explode pot tosser
msgcolor = 53
serial = Target.GetLast()
boomtarget = Mobiles.FindBySerial(serial)
self = Player.Serial

Target.Cancel()
Target.ClearQueue()
Journal.Clear()

def potThrow():
    if Items.BackpackCount(0x0F0D, -1) == 0:
        Player.HeadMessage(msgcolor, 'Out of Exp pots')
        return False
    else:
        Items.UseItemByID(0x0F0D, -1)
        Target.WaitForTarget(1500, False)
        Target.Cancel()

    Player.HeadMessage(msgcolor, 'Charging')
    Journal.WaitJournal('2', 4000)
    Player.HeadMessage(msgcolor, 'Boom!')

    Items.UseItemByID(0x0F0D, -1)
    Target.WaitForTarget(1500, False)
    #Target.TargetExecuteRelative(self, -5)
    #Target.Last()

    if Player.DistanceTo(boomtarget) >= 12:
        Player.HeadMessage(msgcolor, 'Out of range, dumping!')
        Target.TargetExecuteRelative(self, -5)
    else:
        Misc.Pause(100)
        Target.Last()
        if Journal.Search('cannot be seen.'):
            Player.HeadMessage(msgcolor, 'Target not seen, dumping!')
            Target.TargetExecuteRelative(self, -5)
            
potThrow()