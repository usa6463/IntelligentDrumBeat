
import sys , scapy
from scapy.all import *

while 1:
	p = sniff(count=20)
	wrpcap("test.cap", p)

