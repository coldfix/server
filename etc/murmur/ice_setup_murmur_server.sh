#! /bin/bash

port=64738

CTL() { ./murmurcl.py "$@" }
CFG() { CTL cfgserver "$@" on $port }

CTL addchannel $port Kätzchen 0
CTL addchannel $port Krümelchen 0
CTL addchannel $port Flauschetierchen 0
CTL addchannel $port Fette Torten 0
CFG rememberchannel false
CFG defaultchannel 1
CFG serverpassword nichtlieb
