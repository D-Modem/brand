# Naming guide

How the D-Modem repositories, programs and boards are named in READMEs,
docs, wiki pages, UI text and commit messages.

## Repositories

| Name to write | Repository | Notes |
| --- | --- | --- |
| D-Modem | [D-Modem/D-Modem](https://github.com/D-Modem/D-Modem) | The softmodem: modem core, DSP, data link layer and its programs. Also the name of the whole suite; say "the D-Modem suite" when that is meant |
| the D-Modem app | [D-Modem/app](https://github.com/D-Modem/app) | One app for Android and iOS/iPadOS |
| pico-serial | [D-Modem/hardware](https://github.com/D-Modem/hardware) | The board family; "the hardware repository" for the repository itself |
| modemmenu | [D-Modem/menu](https://github.com/D-Modem/menu) | The program; "the menu repository" for the repository |
| bbs | [D-Modem/bbs](https://github.com/D-Modem/bbs) | |
| go3270 | [D-Modem/go3270](https://github.com/D-Modem/go3270) | Our fork of [racingmars/go3270](https://github.com/racingmars/go3270); Go module `github.com/D-Modem/go3270` |
| brand | [D-Modem/brand](https://github.com/D-Modem/brand) | |

Link a repository by its full URL, `https://github.com/D-Modem/<repo>`, so
the link works from any repository, the wiki and the Pages sites.

## Programs and libraries (D-Modem)

| Name | What it is |
| --- | --- |
| dmodemd | The modem program: a SIP line, a softmodem codec or a USB modem, with a pty, COM port or socket for the DTE |
| libdmodem | The modem core and DSP as a library |
| libdmodem_sip | libdmodem with its SIP user agent, the modem on a SIP line as a library |
| dmodem-ari | D-Modem as an Asterisk ARI application |
| app_dmodem | The Asterisk dialplan application (built only for your own Asterisk) |
| codec_clearmode | Asterisk's CLEARMODE codec for ISDN data calls |
| mod_dmodem | The FreeSWITCH module |

## Boards (hardware)

| Name | Spec |
| --- | --- |
| pico-serial | `SPEC.md`: USB-C to DB25 RS-232 adapter |
| pico-serial W | `SPEC-W.md`: the wireless variant (Bluetooth LE and classic) |
| pico-serial Line | `SPEC-L.md`: the phone-line USB stick |
| pico-serial WB | `SPEC-WB.md`: the wideband stick for a bare copper pair (V.wb) |

## Retired names

| Don't write | Write |
| --- | --- |
| D-Modem-RE | D-Modem |
| dmodem-android, D-Modem for Android | the D-Modem app |
| racingmars/go3270 (for our copy) | D-Modem/go3270 |

Paths that already carry an old name (such as the app's
`external/d-modem-re` submodule directory) can keep it until they are
renamed; the text around them uses the current name.
