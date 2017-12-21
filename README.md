# ngc2laser

Tool to convert g-code files created by pcb2gcode to files to 3D printer compatible g-code

    Usage: ngc2laser.py [options] <filename>

    Options:
      -h, --help            show this help message and exit
      -f OUTPUT_FILE, --file=OUTPUT_FILE
                            Name of output file; if not specified stdout is used
      -u UNIT, --unit=UNIT  Output unit (mm or in); if not specified the unit used
                            in input file is preserved
      --header=GHEADER      Program header
      --footer=GFOOTER      Program footer
      --zero-cmd=ZERO_CMD   Virtual Zero Command
      --focus-height=FOCUS_HEIGHT
                            Focus Height (mm or in)
      --x-offset=X_OFFSET   Initial X offset (mm or in)
      --y-offset=Y_OFFSET   Initial Y offset (mm or in)
  
If *Program Header* of *Program Footer* are left empty reasonable and safe defaults are used.

Multiline commands are supported. Vertical bar (|) can be used as command separator` it will be replaced by newline in output file.

Predefined valuse can be stored in configuration files:
* file named `ngc2laser` in current directory
* file named `.ngc2laser` in user's home directory (`~/.ngc2laser` or `%USERPROFILE%\.ngc2laser`, depends on operating system)

First the file in user's home directory is processed, then file in current directory is processed and finally command line arguments are applied. Configuration file
format is straightforward - name of long command line option separated from value by colon, one option per line:

	header:M452|G28|G90|M201 X950 Y950|M202 X950 Y950
	focus-height:30

