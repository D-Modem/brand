<!-- Made by tools/brand_ref.py from tools/gen.py and tools/art.py: change the code (or the script), not this page. -->

# Reference

This page gives the colours of the suite and the art of each repository, as `tools/gen.py` draws them. It also gives the command line of `tools/art.py`. [Palette, type and the app icon](palette.md) tells why they are so. [Assets](assets.md) tells how to make the images.

## Repositories

The Rainbow Book of each repository is its accent: on its banner, its social preview and its site.

| repository | Book | colour | icon | tagline | second line | tags |
|---|---|---|---|---|---|---|
| `D-Modem` | Red (CD-DA) | <span class="suite-swatch" style="background:#ff4d5e"></span> `#ff4d5e` | `wave` | V.92 softmodem over SIP | Cross-platform engine. V.92 / V.90 / V.34 / fax. | C++, SIP, Asterisk, FreeSWITCH |
| `app` | Yellow (CD-ROM) | <span class="suite-swatch" style="background:#ffd23d"></span> `#ffd23d` | `phone` | A dial-up modem in your pocket | Android app: V.92 over a SIP call. | Android, Kotlin, NDK, V.92 |
| `hardware` | Orange (CD-R/RW) | <span class="suite-swatch" style="background:#ff8a3d"></span> `#ff8a3d` | `chip` | Open source hardware modem designs | pico-serial: RP2040 serial and phone-line USB sticks. | RP2040, DB25, USB-C, CERN-OHL-S |
| `bbs` | Blue (CD Extra) | <span class="suite-swatch" style="background:#3d8bff"></span> `#3d8bff` | `bbs` | A bulletin board for every caller | Telnet, TN3270 and modem callers, in Go. | Go, ANSI, TN3270, Doors |
| `go3270` | Purple (DDCD) | <span class="suite-swatch" style="background:#a66bff"></span> `#a66bff` | `3270` | Go servers for 3270 terminals | Build TN3270 data streams from fields. | Go, TN3270, EBCDIC |
| `menu` | Green (CD-i) | <span class="suite-swatch" style="background:#3ddc84"></span> `#3ddc84` | `menu` | User login and management for dial-up callers | modemmenu: a login, then the BBS, PPP or a shell. | Go, PAM, LDAP, SQL, PPP |
| `gui` | Scarlet | <span class="suite-swatch" style="background:#c8102e"></span> `#c8102e` | `gui` | D-Modem on the desktop | Native GUIs for the modem, its terminal and fax. | Windows, macOS, Linux, Desktop |
| `brand` | White | <span class="suite-swatch" style="background:#f2f4fa"></span> `#f2f4fa` | `books` | Logos, colours and type | The mark, the Rainbow Books, Sauce Code Pro. | SVG, PNG, Rainbow Books, Sauce Code Pro |
| `suite` | Rainbow | <span class="suite-swatch" style="background:#9fb0d8"></span> `#9fb0d8` | `mark` | The open source dial-up suite | V.92 softmodem, app, boards, BBS and login. | V.92, SIP, Android, RP2040, BBS |

`suite` is the banner and social preview of the organization (for its profile and website), with the mark in all six Books.

## Palette

### Rainbow Books

| Book | format | colour |
|---|---|---|
| Red | CD-DA | <span class="suite-swatch" style="background:#ff4d5e"></span> `#ff4d5e` |
| Orange | CD-R/RW | <span class="suite-swatch" style="background:#ff8a3d"></span> `#ff8a3d` |
| Yellow | CD-ROM | <span class="suite-swatch" style="background:#ffd23d"></span> `#ffd23d` |
| Green | CD-i | <span class="suite-swatch" style="background:#3ddc84"></span> `#3ddc84` |
| Blue | CD Extra | <span class="suite-swatch" style="background:#3d8bff"></span> `#3d8bff` |
| Purple | DDCD | <span class="suite-swatch" style="background:#a66bff"></span> `#a66bff` |

The free Books, for a repository that does not have a Book yet (`tools/art.py --book`):

| Book | colour |
|---|---|
| Beige | <span class="suite-swatch" style="background:#d9c7a0"></span> `#d9c7a0` |
| White | <span class="suite-swatch" style="background:#f2f4fa"></span> `#f2f4fa` |

### The other colours

| name | colour | use |
|---|---|---|
| `BG` | <span class="suite-swatch" style="background:#0a0f1c"></span> `#0a0f1c` | background |
| `BG2` | <span class="suite-swatch" style="background:#121a2e"></span> `#121a2e` | the second shade of the background |
| `INK` | <span class="suite-swatch" style="background:#e8f0ff"></span> `#e8f0ff` | text |
| `DIM` | <span class="suite-swatch" style="background:#7f8bab"></span> `#7f8bab` | muted text |
| `GREEN` | <span class="suite-swatch" style="background:#3dff9a"></span> `#3dff9a` | the carrier, and the accent of the suite |

Type: SauceCodePro Nerd Font Mono, Source Code Pro, monospace.

## tools/art.py

Makes the banner and social preview of a repository, and puts the banner in its checkout.

    python3 tools/art.py [names...] [options]

| argument | value | what it does |
|---|---|---|
| `names` | ... | Repositories (default: all, and suite) |
| `--install` | REPO_DIR | Copy the banner into this checkout and its README (one name) |
| `--book` | BOOK | Rainbow Book for a new repository: Red, Orange, Yellow, Green, Blue, Purple, Beige, White |
| `--color` | COLOR | Accent colour instead of a Book's, e.g. #d9c7a0 |
| `--tag` | TAG | The coloured tagline |
| `--sub` | SUB | The muted line under it |
| `--icon` | ICON | The repository's icon (default: wave) (`wave`, `mark`, `phone`, `chip`, `bbs`, `3270`, `menu`, `gui`, `books`) |
| `--chips` | CHIPS | Comma-separated tags on the social preview, e.g. Go,PAM |
| `--only` | ONLY | Make only one of the two (`banner`, `social`) |
