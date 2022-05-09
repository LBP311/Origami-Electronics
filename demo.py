import o_elec1 as oe

oe.setup()

oe.ReadPad(0)
oe.ReadAll()
oe.WaitPad(0)
oe.WaitPadSequence(0)
oe.PlaySong(0)
oe.PlayNote(0,0,0)
oe.LED_ON()
oe.LED_OFF()
oe.MotorVibLevel(4)
oe.MotorOFF()
oe.MotorON()

