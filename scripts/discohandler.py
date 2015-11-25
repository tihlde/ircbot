# coding: utf-8
__author__ = 'Harald'

import confighandler as ch
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

discoActive = True
maxDiscoTime = 3000
standardDiscoTime = 20


def parsediscowish(ircmsg, sender):
    if sender not in ch.groups["drift"].members:  # if sender is not in group "drift" do nothing
        return ''
    global discoActive
    if ircmsg.find('.discodeactivate') != -1:
        discoActive = False
        return 'Discotime deactivated'
    elif ircmsg.find('.discoreactivate') != -1:
        discoActive = True
        return 'Discotime reactivated'
    try:
        if discoActive and ircmsg.find('.discotime') != -1:
            try:
                discoTime = int(
                    ircmsg[ircmsg.find('(') + 1: ircmsg.find(')')])
            except ValueError:
                discoTime = standardDiscoTime
            if discoTime > maxDiscoTime:
                discoTime = maxDiscoTime
            print('Discotime for ' + str(discoTime) + '!')
            ser.write(str.encode(str(discoTime)))
            print(ser.read())
        else:
            ser.write(b'0')
    except serial.serialutil.SerialException:
        print('Device unplugged or wrong device used')
    return ''
