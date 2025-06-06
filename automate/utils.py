from colorama import init, Fore, Back, Style

def print_banner():
    lines = [
        "\n"
        "                           nþ   ‚                      ",
        "                   ¸Æð    ä Ã¶    ÆÆ                   ",
        "                 ÖÆÄ     `ð yÆ      ÆÆ£                ",
        "                ÆË¯      ÙT íÆš      éÆÆ               ",
        "              ƒEÚD       šÓ 4Æ        ÆWÆ              ",
        "              Ä2ð    y    ®lÆƒ    Æ   ?ëýÆ             ",
        "             ŽhíÐ    Gû         ÏÆÆ    €ÏWù            ",
        "             #1ïp    ÌÝÎäu    ÆHÚÅ<   «ÚnšÆ            ",
        "             œ1>O     4®fx9  ÆÒ¥þá    èf¢¥Õ            ",
        "             ¾Y{ÏÝ      ©Fq*üÆÆx      Å@òG             ",
        "              Aó×®‰ ƒÆ            Æ  Ýµ½yÆ             ",
        "               ¶ürUJ  ÆÆF      ŠÆq  ŽZaûW              ",
        "                f$5eø   dÆ    Æ'  JÐZÇÕp               ",
        "                  ùœãRMS        ÆÆÆÃ#â                 ",
        "                      '¼ÝVl˜ !b8¾7                     ",
        "                                                       ",
        "    ÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆÆÆÆÆ       xÆÆÆÆÆÆÆÆ     ÆÆÆÆÆÆÆÆÆ ",
        "  ÆÆ           ÆÆ      ÆÆ     ÆÆ       Æ    ÆÆ         ",
        "  ÆÆ          ÆÆ        ÆÆ   ÆÆ             ÆÆ         ",
        "    ÆÆÆÆÆ     ÆÆ        ÆÆ   Æî      Æ6Æ6    ÆÆÆÆÆÆÆ   ",
        "         ÆÆY  ÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆ        ÆÆ  ÞÆÆ         ",
        "          ÆÆ  ÆÆ        ÆÆ   ÆÆÆ       ÆÆ  ÆÆ          ",
        "  ÆÆÆÆÆÆÆÆÆ   ÆÆO       ÆÆ     ÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆ "
        "\n\n"
    ]
    
    green_shades = [
        '\033[38;2;0;100;0m',      # Dark green
        '\033[38;2;0;150;0m',      # Medium green  
        '\033[38;2;0;200;0m',      # Bright green
        '\033[38;2;50;255;50m',    # Light green
        '\033[38;2;100;255;100m',  # Very light green
        '\033[38;2;34;139;34m'     # Forest green
    ]
    
    colored_lines = []
    for i, line in enumerate(lines):
        if i < 15:
            shade = green_shades[i % len(green_shades)]
            colored_lines.append(f"{shade}{line}\033[0m")
        else:
            colored_lines.append(f"\033[38;2;0;255;0m\033[1m{line}\033[0m")
    
    print('\n'.join(colored_lines))