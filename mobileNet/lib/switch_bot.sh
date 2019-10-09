#!/bin/sh

gatttool -b E6:22:94:C3:BC:C2 -t random --char-write-req --handle=0x0016 --value=570102
