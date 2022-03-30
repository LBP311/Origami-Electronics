import o_elec as oe

oe.setup()
oe.ReadPad(0)
oe.ReadAll()
oe.WaitPad(0)
oe.WaitPadSequence([1])
oe.PlaySong(1)
oe.PlayNote(1, 2, 3)
oe.LED_ON()
oe.LED_OFF()
