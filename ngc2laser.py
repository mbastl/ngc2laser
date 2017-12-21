#!/usr/bin/env python
"""
Created by Milan B. (C) 2017 www.bastl.sk

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import sys
import os
import re
from optparse import OptionParser


defaults = {
'unit' : "mm",
#'maxsize' : "5.0",
#'spindle-on' : "M03 S255",
#'spindle-off' : "M05",
#'tool-cmd' : "",
#'init-cmd' : "",
'zero-cmd' : "G92 X0 Y0",
'focus-height' : "0",
'x-offset':"0.0",
'y-offset' : "0.0",
#'drill-speed' : "50",
#'retract-speed' : "700",
#'move-speed' : "5000",
#'header' : "M452|G28|G90|M201 X100 Y100|M202 X100 Y100",
'header' : "M452|G28|G90|M201 X950 Y950|M202 X950 Y950",
'footer' : "G28 X|M84|M201 X950 Y950|M202 X950 Y950"
}

    
def parse_config(file):
  with open(file) as c: 
    for cn in c:
      c=cn.strip('\r\n ')
      k = c.split(":")
      if len(k) == 2:
	defaults[k[0]]=k[1]
  


# read configuration files in home directory and current directory

home=os.path.expanduser("~")
if os.path.isfile(home+os.sep+'.ngc2laser'):
  parse_config(home+os.sep+'.ngc2laser')
if os.path.isfile('ngc2laser'):
  parse_config('ngc2laser')

# Parse command line arguments

usage = "Usage: %prog [options] <filename>"
cmdline = OptionParser(usage=usage)

cmdline.add_option("-f", "--file",   action="store", type="string", dest="output_file",   default="",   help="Name of output file; if not specified stdout is used")
cmdline.add_option("-u", "--unit",   action="store", type="string", dest="unit",   default=defaults['unit'],   help="Output unit (mm or in); if not specified the unit used in input file is preserved")
#cmdline.add_option("-x", "--maxsize",   action="store", type="float", dest="maxsize",   default=float(defaults['maxsize']),   help="Maximum drill diameter (mm or in)")
cmdline.add_option("", "--header",   action="store", type="string", dest="gheader",   default=defaults['header'],   help="Program header")
cmdline.add_option("", "--footer",   action="store", type="string", dest="gfooter",   default=defaults['footer'],   help="Program footer")
#cmdline.add_option("", "--spindle-on",   action="store", type="string", dest="spindle_on",   default=defaults['spindle-on'],   help="Spindle ON Command")
#cmdline.add_option("", "--spindle-off",   action="store", type="string", dest="spindle_off",   default=defaults['spindle-off'],   help="Spindle OFF Command")
#cmdline.add_option("", "--init-cmd",   action="store", type="string", dest="init_cmd",   default=defaults['init-cmd'],   help="Additional initializatiom")
#cmdline.add_option("", "--tool-cmd",   action="store", type="string", dest="tool_cmd",   default=defaults['tool-cmd'],   help="Tool Change Command")
cmdline.add_option("", "--zero-cmd",   action="store", type="string", dest="zero_cmd",   default=defaults['zero-cmd'],   help="Virtual Zero Command")
cmdline.add_option("", "--focus-height",   action="store", type="float", dest="focus_height",   default=float(defaults['focus-height']),   help="Focus Height (mm or in)")
cmdline.add_option("", "--x-offset",   action="store", type="float", dest="x_offset",   default=float(defaults['x-offset']),   help="Initial X offset (mm or in)")
cmdline.add_option("", "--y-offset",   action="store", type="float", dest="y_offset",   default=float(defaults['y-offset']),   help="Initial Y offset (mm or in)")
#cmdline.add_option("", "--drill-speed",   action="store", type="int", dest="drill_speed",   default=int(defaults['drill-speed']),   help="Drill speed (mm/min)")
#cmdline.add_option("", "--retract-speed",   action="store", type="int", dest="retract_speed",   default=int(defaults['retract-speed']),   help="Retract speed (mm/min)")
#cmdline.add_option("", "--move-speed",   action="store", type="int", dest="move_speed",   default=int(defaults['move-speed']),   help="Move speed (mm/min)")

(options, filenames) = cmdline.parse_args()

# Some sanity checks

if len(filenames) != 1 or options.unit not in ["", "mm", "in"]:
  cmdline.print_help()
  sys.exit(2)

# Let's go

#tools = {}     # list of all used tools
#zero="lz"      # zero padding mode
#inunit="mm"    # internal file unit (comes from METRIC or INCH commands)
#unit="mm"      # output unit

of = open(options.output_file, "w") if options.output_file != "" else sys.stdout

mode="none"
with open(filenames[0]) as f: 

  of.write(options.gheader.replace("|","\n")+"\n");
  if options.unit == "mm":
    of.write("G21\n")
  else:
    of.write("G20\n")
  
  xs=" X%.3f" %  options.x_offset if options.x_offset != 0. else ""
  ys=" Y%.3f" %  options.y_offset if options.y_offset != 0. else ""
  
  of.write("G00"+xs+ys+" Z%.3f" % options.focus_height)

  of.write("\n")
  
  if (options.x_offset != 0.) or (options.y_offset != 0.):
    of.write(options.zero_cmd.replace("|","\n")+"\n");

  for ln in f:
    l=ln.strip('\r\n ').replace("(", ";").replace(")", "")
    
    if (len(l) == 0):
      of.write("\n")
    elif (l[0] == "X") or (l[0] == "Y") or (l[0] == "F"):
      of.write("G01 "+l+"\n")
    elif (l[0] == "S"):
      of.write("M03 " + l + "\n")
    elif (l[0:5] == "G00 Z") or (l[0:5] == "G01 Z") or (l[0:2] == "M9") or (l[0:2] == "M2") or (l[0:2] == "M3") or (l[0:3] == "G94") or (l[0:3] == "G6	4"):
      pass
    else:
      of.write(l+"\n")

  of.write(options.gfooter.replace("|","\n")+"\n");

of.close()

sys.exit(0)

