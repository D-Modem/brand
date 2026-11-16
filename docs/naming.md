# Naming guide

This guide gives the names of the D-Modem repositories, programs and boards.
Use these names in READMEs, docs, wiki pages, UI text and commit messages.

## Repositories

| Name to write | Repository | Notes |
| --- | --- | --- |
| D-Modem | [D-Modem/D-Modem](https://github.com/D-Modem/D-Modem) | The softmodem: modem core, DSP, data link layer and its programs. Also the name of the full suite. For the suite, write "the D-Modem suite" |
| the D-Modem app | [D-Modem/app](https://github.com/D-Modem/app) | One app for Android and iOS/iPadOS |
| pico-serial | [D-Modem/hardware](https://github.com/D-Modem/hardware) | The board family. For the repository, write "the hardware repository" |
| modemmenu | [D-Modem/menu](https://github.com/D-Modem/menu) | The program. For the repository, write "the menu repository" |
| bbs | [D-Modem/bbs](https://github.com/D-Modem/bbs) | |
| go3270 | [D-Modem/go3270](https://github.com/D-Modem/go3270) | Our fork of [racingmars/go3270](https://github.com/racingmars/go3270). Go module `github.com/D-Modem/go3270` |
| brand | [D-Modem/brand](https://github.com/D-Modem/brand) | |

Link to a repository with its full URL, `https://github.com/D-Modem/<repo>`.
Then the link operates from all repositories, the wiki and the Pages sites.

## Programs and libraries (D-Modem)

| Name | What it is |
| --- | --- |
| dmodemd | The modem program: a SIP line, a softmodem codec or a USB modem, with a pty, COM port or socket for the DTE |
| libdmodem | The modem core and DSP as a library |
| libdmodem_sip | libdmodem with its SIP user agent: the modem on a SIP line as a library |
| dmodem-ari | D-Modem as an Asterisk ARI application |
| app_dmodem | The Asterisk dialplan application (built only for your own Asterisk) |
| codec_clearmode | The CLEARMODE codec of Asterisk for ISDN data calls |
| mod_dmodem | The FreeSWITCH module |

## Boards (hardware)

| Name | Spec |
| --- | --- |
| pico-serial | `SPEC.md`: USB-C to DB25 RS-232 adapter |
| pico-serial W | `SPEC-W.md`: the wireless variant (Bluetooth LE and classic) |
| pico-serial Line | `SPEC-L.md`: the phone-line USB stick |
| pico-serial WB | `SPEC-WB.md`: the wideband stick for a bare copper pair (V.wb) |

## Retired names

| Do not write | Write |
| --- | --- |
| D-Modem-RE | D-Modem |
| dmodem-android, D-Modem for Android | the D-Modem app |
| racingmars/go3270 (for our copy) | D-Modem/go3270 |

Some paths already have an old name (for example, the `external/d-modem-re`
submodule directory of the app). These paths can keep the old name until
someone renames them. The text around them uses the current name.
